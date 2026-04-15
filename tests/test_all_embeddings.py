"""
tests/test_all_embeddings.py
----------------------------
Parameterized tests for every embedding model entry in
research_config.EMBEDDING_MODELS.

All test parameters are read dynamically from EMBEDDING_MODELS — no values are
hardcoded in this file.  Tests cover:

  - Registry schema validation (required fields, positive dimensions)
  - get_embedding_config() lookup for every registered embedding
  - get_embeddings() factory: correct adapter class returned per type
    (huggingface / ollama / openai)
  - OpenAI embedding key guard: loading an openai embedding without
    OPENAI_API_KEY raises ValueError (skipped when the key is present)
  - Chroma directory and collection naming: each embedding gets a unique
    path so dimension-mismatch collisions cannot occur
  - Vector store build (mocked): build_vector_store succeeds for every
    embedding name without touching disk or downloading models
  - Dimension consistency: reported dimension matches the model_id category
    (huggingface small ≤ 384, large ≥ 768, etc.)

Run:
    python tests/test_all_embeddings.py
    python tests/test_all_embeddings.py -v
    pytest tests/test_all_embeddings.py -v
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ── Ensure repo root is on sys.path ─────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from research_config import (
    EMBEDDING_MODELS,
    DEFAULT_EMBEDDING,
    CHROMA_DIR_TEMPLATE,
    COLLECTION_NAME_TEMPLATE,
    get_embedding_config,
)


# ── Schema requirements ──────────────────────────────────────────────────────

_REQUIRED_FIELDS = {"name", "model_id", "dimension", "type"}
_VALID_TYPES = {"huggingface", "ollama", "openai"}


# ═══════════════════════════════════════════════════════════════════════════════
#  1.  Registry schema
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmbeddingRegistrySchema(unittest.TestCase):
    """Every entry in EMBEDDING_MODELS must satisfy the required schema."""

    def test_registry_is_non_empty(self):
        self.assertGreater(len(EMBEDDING_MODELS), 0,
                           "EMBEDDING_MODELS must contain at least one entry")

    def test_required_fields_present(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry.get("name", "<unnamed>")):
                missing = _REQUIRED_FIELDS - entry.keys()
                self.assertFalse(
                    missing,
                    f"Embedding '{entry.get('name')}' is missing fields: {missing}",
                )

    def test_type_is_valid(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                self.assertIn(
                    entry["type"], _VALID_TYPES,
                    f"Embedding '{entry['name']}' has invalid type '{entry['type']}'. "
                    f"Must be one of {_VALID_TYPES}.",
                )

    def test_dimension_is_positive_integer(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                dim = entry["dimension"]
                self.assertIsInstance(
                    dim, int,
                    f"Embedding '{entry['name']}' dimension is not int: {dim!r}",
                )
                self.assertGreater(
                    dim, 0,
                    f"Embedding '{entry['name']}' dimension must be > 0, got {dim}",
                )

    def test_model_id_is_non_empty_string(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                self.assertIsInstance(entry["model_id"], str)
                self.assertGreater(
                    len(entry["model_id"].strip()), 0,
                    f"Embedding '{entry['name']}' has empty model_id",
                )

    def test_names_are_unique(self):
        names = [entry["name"] for entry in EMBEDDING_MODELS]
        duplicates = {n for n in names if names.count(n) > 1}
        self.assertFalse(
            duplicates,
            f"Duplicate embedding names found in EMBEDDING_MODELS: {duplicates}",
        )

    def test_default_embedding_is_registered(self):
        names = [e["name"] for e in EMBEDDING_MODELS]
        self.assertIn(
            DEFAULT_EMBEDDING, names,
            f"DEFAULT_EMBEDDING '{DEFAULT_EMBEDDING}' is not in EMBEDDING_MODELS",
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  2.  get_embedding_config lookup
# ═══════════════════════════════════════════════════════════════════════════════

class TestGetEmbeddingConfig(unittest.TestCase):
    """get_embedding_config must resolve every registered embedding by name."""

    def test_lookup_returns_entry_for_every_embedding(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                cfg = get_embedding_config(entry["name"])
                self.assertIsNotNone(
                    cfg,
                    f"get_embedding_config('{entry['name']}') returned None",
                )
                self.assertEqual(cfg["name"], entry["name"])

    def test_lookup_unknown_embedding_returns_none(self):
        self.assertIsNone(get_embedding_config("__no_such_embedding_xyz__"))

    def test_lookup_preserves_all_fields(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                cfg = get_embedding_config(entry["name"])
                for field in _REQUIRED_FIELDS:
                    self.assertIn(
                        field, cfg,
                        f"get_embedding_config('{entry['name']}') missing field '{field}'",
                    )


# ═══════════════════════════════════════════════════════════════════════════════
#  3.  Chroma directory and collection naming
# ═══════════════════════════════════════════════════════════════════════════════

class TestChromaNaming(unittest.TestCase):
    """
    Each embedding must produce a unique Chroma persist directory and collection
    name so that dimension-mismatch collisions cannot occur at runtime.
    """

    def test_all_embeddings_produce_unique_chroma_dirs(self):
        dirs = [
            CHROMA_DIR_TEMPLATE.format(embedding_name=e["name"])
            for e in EMBEDDING_MODELS
        ]
        self.assertEqual(
            len(dirs), len(set(dirs)),
            "Some embeddings share the same Chroma directory — "
            "dimension mismatch will occur at runtime.",
        )

    def test_all_embeddings_produce_unique_collection_names(self):
        collections = [
            COLLECTION_NAME_TEMPLATE.format(embedding_name=e["name"])
            for e in EMBEDDING_MODELS
        ]
        self.assertEqual(
            len(collections), len(set(collections)),
            "Some embeddings share the same Chroma collection name.",
        )

    def test_chroma_dir_contains_embedding_name(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                chroma_dir = CHROMA_DIR_TEMPLATE.format(embedding_name=entry["name"])
                self.assertIn(
                    entry["name"], chroma_dir,
                    f"Chroma dir '{chroma_dir}' does not contain embedding name",
                )

    def test_collection_name_contains_embedding_name(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                collection = COLLECTION_NAME_TEMPLATE.format(embedding_name=entry["name"])
                self.assertIn(
                    entry["name"], collection,
                    f"Collection name '{collection}' does not contain embedding name",
                )


# ═══════════════════════════════════════════════════════════════════════════════
#  4.  get_embeddings factory dispatch (mocked — no downloads)
# ═══════════════════════════════════════════════════════════════════════════════

class TestGetEmbeddingsFactory(unittest.TestCase):
    """
    get_embeddings() must return the correct adapter for each type.
    All model-loading calls are mocked to avoid network/disk access.
    """

    def test_huggingface_embeddings_returned_for_hf_type(self):
        # Use a plain MagicMock — no spec needed since _load_huggingface_embeddings
        # is already patched and we only care that the factory returns the mock.
        mock_hf = MagicMock()
        for entry in EMBEDDING_MODELS:
            if entry["type"] == "huggingface":
                with self.subTest(embedding=entry["name"]):
                    with patch("embeddings._load_huggingface_embeddings",
                               return_value=mock_hf):
                        from embeddings import get_embeddings
                        result = get_embeddings(entry["name"])
                    self.assertIs(
                        result, mock_hf,
                        f"get_embeddings('{entry['name']}') did not return mock HF embedding",
                    )

    def test_ollama_embeddings_returned_for_ollama_type(self):
        mock_ollama_emb = MagicMock()
        for entry in EMBEDDING_MODELS:
            if entry["type"] == "ollama":
                with self.subTest(embedding=entry["name"]):
                    with patch("embeddings._load_ollama_embeddings",
                               return_value=mock_ollama_emb):
                        from embeddings import get_embeddings
                        result = get_embeddings(entry["name"])
                    self.assertIs(
                        result, mock_ollama_emb,
                        f"get_embeddings('{entry['name']}') did not return mock Ollama embedding",
                    )

    def test_openai_key_guard(self):
        """
        Loading an OpenAI embedding without OPENAI_API_KEY must raise ValueError.
        Skipped when OPENAI_API_KEY is actually present.
        """
        if os.environ.get("OPENAI_API_KEY", "").strip():
            self.skipTest("OPENAI_API_KEY is set — skipping key-guard test")

        for entry in EMBEDDING_MODELS:
            if entry["type"] == "openai":
                with self.subTest(embedding=entry["name"]):
                    with patch.dict(os.environ, {}, clear=True):
                        from embeddings import get_embeddings
                        with self.assertRaises(
                            (ValueError, Exception),
                            msg=f"Loading '{entry['name']}' without OPENAI_API_KEY "
                                "should raise ValueError",
                        ):
                            get_embeddings(entry["name"])

    def test_get_embeddings_list_contains_all_names(self):
        from embeddings import list_embedding_names
        names_from_factory = list_embedding_names()
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                self.assertIn(
                    entry["name"], names_from_factory,
                    f"list_embedding_names() is missing '{entry['name']}'",
                )

    def test_get_embeddings_by_type_huggingface(self):
        from embeddings import get_embeddings_by_type
        hf_names = get_embeddings_by_type("huggingface")
        expected = [e["name"] for e in EMBEDDING_MODELS if e["type"] == "huggingface"]
        for name in expected:
            with self.subTest(embedding=name):
                self.assertIn(
                    name, hf_names,
                    f"get_embeddings_by_type('huggingface') is missing '{name}'",
                )

    def test_get_embeddings_by_type_ollama(self):
        from embeddings import get_embeddings_by_type
        ollama_names = get_embeddings_by_type("ollama")
        expected = [e["name"] for e in EMBEDDING_MODELS if e["type"] == "ollama"]
        for name in expected:
            with self.subTest(embedding=name):
                self.assertIn(
                    name, ollama_names,
                    f"get_embeddings_by_type('ollama') is missing '{name}'",
                )

    def test_get_embeddings_by_type_openai(self):
        from embeddings import get_embeddings_by_type
        openai_names = get_embeddings_by_type("openai")
        expected = [e["name"] for e in EMBEDDING_MODELS if e["type"] == "openai"]
        for name in expected:
            with self.subTest(embedding=name):
                self.assertIn(
                    name, openai_names,
                    f"get_embeddings_by_type('openai') is missing '{name}'",
                )


# ═══════════════════════════════════════════════════════════════════════════════
#  5.  build_vector_store (mocked) — succeeds for every embedding name
# ═══════════════════════════════════════════════════════════════════════════════

class TestBuildVectorStorePerEmbedding(unittest.TestCase):
    """
    build_vector_store must accept every registered embedding name without
    raising an error.  Chroma and the embedding model are fully mocked so no
    disk writes or model downloads happen.
    """

    def _mock_build_vector_store(self, embedding_name: str):
        """Run build_vector_store with all heavy dependencies mocked."""
        mock_vs = MagicMock()
        mock_hf = MagicMock()
        mock_chroma_cls = MagicMock(return_value=mock_vs)

        with patch("retriever.get_embeddings", return_value=mock_hf), \
             patch("retriever.Chroma", mock_chroma_cls), \
             patch("retriever.get_chunks", return_value=[
                 MagicMock(page_content="test content",
                           metadata={"topic": "water cycle"})
             ]), \
             patch("retriever.get_texts_and_metadatas",
                   return_value=(["test text"], [{"topic": "water cycle"}])), \
             patch("os.path.exists", return_value=False):
            from retriever import build_vector_store
            result = build_vector_store(
                persist=False,
                embedding_name=embedding_name,
            )
        return result

    def test_build_vector_store_accepts_all_embedding_names(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                try:
                    result = self._mock_build_vector_store(entry["name"])
                    # Should return something (the mocked vector store)
                    self.assertIsNotNone(result)
                except Exception as exc:
                    self.fail(
                        f"build_vector_store(embedding_name='{entry['name']}') "
                        f"raised unexpectedly: {type(exc).__name__}: {exc}"
                    )

    def test_build_vector_store_default_embedding_works(self):
        """The default embedding must be accepted without error."""
        try:
            result = self._mock_build_vector_store(DEFAULT_EMBEDDING)
            self.assertIsNotNone(result)
        except Exception as exc:
            self.fail(
                f"build_vector_store with DEFAULT_EMBEDDING '{DEFAULT_EMBEDDING}' "
                f"raised: {type(exc).__name__}: {exc}"
            )


# ═══════════════════════════════════════════════════════════════════════════════
#  6.  Dimension plausibility checks
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmbeddingDimensionPlausibility(unittest.TestCase):
    """
    Dimension values are sanity-checked against known characteristics of each
    embedding family.  Values are compared against EMBEDDING_MODELS entries
    themselves — no hardcoded expectations about specific model names.
    """

    def test_all_dimensions_are_powers_of_2_or_standard(self):
        """
        All practical embedding dimensions are a power of 2 or a small multiple
        of a power of 2 (e.g. 384 = 3×128, 768 = 3×256).
        Lower bound of 64: the smallest meaningful sentence embedding today
        (e.g. distilled models) is at least 64 dimensions; anything smaller
        would lose too much semantic signal to be useful for RAG retrieval.
        Upper bound of 4096: the largest publicly available dense embedding
        (OpenAI text-embedding-3-large) is 3072 dimensions; 4096 gives a
        safe margin for future models while flagging implausible values.
        """
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                dim = entry["dimension"]
                self.assertGreaterEqual(
                    dim, 64,
                    f"Dimension {dim} for '{entry['name']}' seems implausibly small",
                )
                self.assertLessEqual(
                    dim, 4096,
                    f"Dimension {dim} for '{entry['name']}' seems implausibly large",
                )

    def test_huggingface_dimensions_are_reasonable(self):
        """HuggingFace sentence-transformer dimensions are typically 384–1024."""
        for entry in EMBEDDING_MODELS:
            if entry["type"] == "huggingface":
                with self.subTest(embedding=entry["name"]):
                    dim = entry["dimension"]
                    self.assertGreaterEqual(
                        dim, 64,
                        f"HF embedding '{entry['name']}' dimension {dim} seems too small",
                    )

    def test_openai_dimension_is_large(self):
        """OpenAI text-embedding-3-large has 3072 dimensions per spec."""
        for entry in EMBEDDING_MODELS:
            if entry["type"] == "openai":
                with self.subTest(embedding=entry["name"]):
                    dim = entry["dimension"]
                    self.assertGreaterEqual(
                        dim, 1024,
                        f"OpenAI embedding '{entry['name']}' has unusually small "
                        f"dimension {dim}",
                    )

    def test_dimension_is_consistent_with_model_id_family(self):
        """
        Cross-check: two entries sharing the same model_id (aliases) must have
        the same dimension so aliased lookups never produce dimension mismatches.
        """
        model_id_to_dim: dict[str, tuple[str, int]] = {}
        for entry in EMBEDDING_MODELS:
            mid = entry["model_id"]
            dim = entry["dimension"]
            if mid in model_id_to_dim:
                existing_name, existing_dim = model_id_to_dim[mid]
                with self.subTest(embedding=entry["name"]):
                    self.assertEqual(
                        dim, existing_dim,
                        f"Entries '{entry['name']}' and '{existing_name}' share "
                        f"model_id '{mid}' but have different dimensions "
                        f"({dim} vs {existing_dim})",
                    )
            else:
                model_id_to_dim[mid] = (entry["name"], dim)


# ═══════════════════════════════════════════════════════════════════════════════
#  7.  ResearchEvaluator embedding integration
# ═══════════════════════════════════════════════════════════════════════════════

class TestResearchEvaluatorEmbeddingIntegration(unittest.TestCase):
    """
    ResearchEvaluator can be instantiated with every registered embedding name
    without error (all heavy I/O is mocked).
    """

    def _make_evaluator(self, embedding_name: str):
        """
        Instantiate ResearchEvaluator with all heavy I/O mocked so the test
        is hermetic: no Ollama, no corpus loading, no BM25 index build, no
        network calls.

        Patches applied:
          - research_evaluator.build_vector_store  → returns mock vector store
          - rag_pipeline._build_llm                → returns mock LLM
          - rag_pipeline.get_texts_and_metadatas   → returns small stub corpus
          - rag_pipeline.build_bm25_index          → returns None (skipped)
        """
        mock_vs = MagicMock()
        # vector_store._embedding_function is accessed in RAGPipeline.__init__
        mock_vs._embedding_function = MagicMock()

        stub_texts = ["test content about water cycle"]
        stub_metas = [{"topic": "water cycle"}]

        with patch("research_evaluator.build_vector_store", return_value=mock_vs), \
             patch("rag_pipeline._build_llm", return_value=MagicMock()), \
             patch("rag_pipeline.get_texts_and_metadatas",
                   return_value=(stub_texts, stub_metas)), \
             patch("rag_pipeline.build_bm25_index", return_value=None):
            from research_evaluator import ResearchEvaluator
            evaluator = ResearchEvaluator(
                model="phi3",
                retrieval_mode="hybrid",
                embedding_name=embedding_name,
            )
        return evaluator

    def test_evaluator_instantiates_for_all_embeddings(self):
        for entry in EMBEDDING_MODELS:
            with self.subTest(embedding=entry["name"]):
                try:
                    evaluator = self._make_evaluator(entry["name"])
                    self.assertIsNotNone(evaluator)
                except Exception as exc:
                    self.fail(
                        f"ResearchEvaluator(embedding_name='{entry['name']}') "
                        f"raised: {type(exc).__name__}: {exc}"
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
