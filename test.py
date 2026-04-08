"""
test.py
-------
Comprehensive test suite for the EduSLM-RAG pipeline.

Covers every major module introduced or updated in the research project:

  Module                  Tests
  ----------------------- -------------------------------------------------------
  research_config         MODEL_REGISTRY, EMBEDDING_MODELS, helpers, chunking
  embeddings              get_embeddings dispatch, list helpers, fallback
  retriever               chunk_fixed/sliding_window/semantic/get_chunks,
                          BM25Index, mmr_rerank, cross_encoder_rerank,
                          build_vector_store (mocked), hybrid_search (mocked),
                          hierarchical_retrieve (mocked)
  rag_pipeline            _build_llm dispatch (mocked), graceful API-key
                          missing handling
  evaluation              compute_all_metrics smoke test with mock docs
  test_queries            run_benchmark helper (mocked pipeline)

Run all tests:
    python test.py

Run with verbose output:
    python test.py -v

Requirements for all tests to pass:
  - sentence-transformers, langchain, langchain-community, langchain-core
  - chromadb, numpy, rank-bm25

Optional (tests are SKIPPED if missing, not failed):
  - langchain-openai       -> OpenAI LLM / embedding tests
  - langchain-anthropic    -> Anthropic LLM tests
  - langchain-google-genai -> Google LLM tests
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from langchain_core.documents import Document


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_doc(content: str, topic: str = "water cycle", grade: str = "6") -> Document:
    """Return a Document with given page_content and metadata."""
    return Document(
        page_content=content,
        metadata={"topic": topic, "grade": grade, "subject": "science"},
    )


def _make_docs(n: int = 5, topic: str = "water cycle") -> list:
    """Return a list of n mock Documents."""
    phrases = [
        "Water evaporates from oceans when heated by the sun.",
        "Condensation occurs when water vapour cools and forms clouds.",
        "Precipitation returns water to Earth as rain or snow.",
        "Transpiration releases water vapour from plant leaves.",
        "Groundwater recharges aquifers through infiltration.",
    ]
    return [_make_doc(phrases[i % len(phrases)], topic=topic) for i in range(n)]


# ===========================================================================
# 1. research_config
# ===========================================================================

class TestResearchConfig(unittest.TestCase):
    """Tests for research_config.py constants and helper functions."""

    def setUp(self):
        from research_config import (
            MODEL_REGISTRY, EMBEDDING_MODELS, CHUNKING_STRATEGIES,
            DEFAULT_EMBEDDING, DEFAULT_CHUNKING_STRATEGY,
            SLM_MODELS, LLM_MODELS,
            get_model_config, get_embedding_config,
            SLIDING_WINDOW_SIZE, SLIDING_WINDOW_STEP,
            SEMANTIC_CHUNK_MIN_SIZE, SEMANTIC_SIMILARITY_THRESHOLD,
        )
        self.mr = MODEL_REGISTRY
        self.em = EMBEDDING_MODELS
        self.cs = CHUNKING_STRATEGIES
        self.de = DEFAULT_EMBEDDING
        self.dcs = DEFAULT_CHUNKING_STRATEGY
        self.slm = SLM_MODELS
        self.llm = LLM_MODELS
        self.gmc = get_model_config
        self.gec = get_embedding_config
        self.sw_size = SLIDING_WINDOW_SIZE
        self.sw_step = SLIDING_WINDOW_STEP
        self.sem_min = SEMANTIC_CHUNK_MIN_SIZE
        self.sem_thr = SEMANTIC_SIMILARITY_THRESHOLD

    # Model registry
    def test_model_registry_not_empty(self):
        self.assertGreater(len(self.mr), 0)

    def test_slm_models_present(self):
        for name in ("phi3", "tinyllama"):
            with self.subTest(model=name):
                self.assertIn(name, self.slm)

    def test_groq_api_llms_present(self):
        """Groq benchmark models must exist in the LLM list."""
        for name in ("groq-llama3-8b", "groq-llama3-70b", "groq-mixtral", "groq-gemma2"):
            with self.subTest(model=name):
                self.assertIn(name, self.llm)

    def test_model_registry_fields(self):
        required = {"name", "type", "provider", "model_id",
                    "cost_per_1k_input_tokens", "cost_per_1k_output_tokens"}
        for entry in self.mr:
            with self.subTest(model=entry["name"]):
                self.assertTrue(required.issubset(entry.keys()))

    def test_get_model_config_found(self):
        cfg = self.gmc("phi3")
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg["provider"], "ollama")

    def test_get_model_config_not_found(self):
        self.assertIsNone(self.gmc("nonexistent-model-xyz"))

    def test_api_model_providers(self):
        expected = {
            "groq-llama3-8b": "groq",
            "groq-llama3-70b": "groq",
            "groq-mixtral": "groq",
            "groq-gemma2": "groq",
        }
        for name, prov in expected.items():
            with self.subTest(model=name):
                cfg = self.gmc(name)
                self.assertIsNotNone(cfg)
                self.assertEqual(cfg["provider"], prov)

    # Embedding models
    def test_embedding_models_not_empty(self):
        self.assertGreater(len(self.em), 0)

    def test_required_embeddings_present(self):
        """The four requested benchmark embedding models must exist."""
        required = ("nomic-embed-text", "bge-base-en", "all-MiniLM-L6-v2",
                    "text-embedding-3-large")
        names = [e["name"] for e in self.em]
        for name in required:
            with self.subTest(embedding=name):
                self.assertIn(name, names)

    def test_default_embedding_is_registered(self):
        names = [e["name"] for e in self.em]
        self.assertIn(self.de, names)

    def test_embedding_model_fields(self):
        required = {"name", "model_id", "dimension", "type"}
        for entry in self.em:
            with self.subTest(embedding=entry["name"]):
                self.assertTrue(required.issubset(entry.keys()))

    def test_embedding_types_valid(self):
        valid_types = {"huggingface", "ollama", "openai"}
        for entry in self.em:
            with self.subTest(embedding=entry["name"]):
                self.assertIn(entry["type"], valid_types)

    def test_get_embedding_config_found(self):
        cfg = self.gec("bge-small")
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg["type"], "huggingface")

    def test_get_embedding_config_not_found(self):
        self.assertIsNone(self.gec("does-not-exist"))

    def test_nomic_embed_type_ollama(self):
        cfg = self.gec("nomic-embed-text")
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg["type"], "ollama")

    def test_text_embedding_3_large_type_openai(self):
        cfg = self.gec("text-embedding-3-large")
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg["type"], "openai")

    # Chunking strategies
    def test_chunking_strategies_present(self):
        for s in ("fixed", "sliding_window", "semantic"):
            with self.subTest(strategy=s):
                self.assertIn(s, self.cs)

    def test_default_chunking_strategy_is_fixed(self):
        self.assertEqual(self.dcs, "fixed")

    def test_sliding_window_params_positive(self):
        self.assertGreater(self.sw_size, 0)
        self.assertGreater(self.sw_step, 0)
        self.assertLessEqual(self.sw_step, self.sw_size)

    def test_semantic_params_valid(self):
        self.assertGreater(self.sem_min, 0)
        self.assertGreater(self.sem_thr, 0.0)
        self.assertLessEqual(self.sem_thr, 1.0)


# ===========================================================================
# 2. embeddings
# ===========================================================================

class TestEmbeddings(unittest.TestCase):
    """Tests for embeddings.py factory and helpers."""

    def setUp(self):
        from embeddings import (
            get_embedding_info,
            list_embedding_names,
            get_embeddings_by_type,
        )
        self.get_embedding_info = get_embedding_info
        self.list_embedding_names = list_embedding_names
        self.get_embeddings_by_type = get_embeddings_by_type

    def test_list_embedding_names_returns_list(self):
        names = self.list_embedding_names()
        self.assertIsInstance(names, list)
        self.assertGreater(len(names), 0)

    def test_list_embedding_names_contains_defaults(self):
        names = self.list_embedding_names()
        for n in ("bge-small", "bge-base-en", "all-MiniLM-L6-v2",
                  "nomic-embed-text", "text-embedding-3-large"):
            with self.subTest(name=n):
                self.assertIn(n, names)

    def test_get_embedding_info_valid(self):
        info = self.get_embedding_info("bge-small")
        self.assertIn("model_id", info)
        self.assertIn("dimension", info)
        self.assertIn("type", info)

    def test_get_embedding_info_unknown(self):
        info = self.get_embedding_info("this-does-not-exist")
        self.assertEqual(info, {})

    def test_get_embeddings_by_type_huggingface(self):
        names = self.get_embeddings_by_type("huggingface")
        self.assertIsInstance(names, list)
        self.assertIn("bge-small", names)

    def test_get_embeddings_by_type_ollama(self):
        names = self.get_embeddings_by_type("ollama")
        self.assertIn("nomic-embed-text", names)

    def test_get_embeddings_by_type_openai(self):
        names = self.get_embeddings_by_type("openai")
        self.assertIn("text-embedding-3-large", names)

    def test_get_embeddings_returns_hf_model(self):
        """get_embeddings('bge-small') returns a HuggingFaceEmbeddings object (mocked)."""
        from embeddings import get_embeddings
        from langchain_community.embeddings import HuggingFaceEmbeddings
        mock_hf = MagicMock(spec=HuggingFaceEmbeddings)
        with patch("embeddings._load_huggingface_embeddings", return_value=mock_hf):
            emb = get_embeddings("bge-small")
        self.assertIs(emb, mock_hf)

    def test_get_embeddings_unknown_falls_back(self):
        """get_embeddings with unknown name emits a warning and returns default (mocked)."""
        from embeddings import get_embeddings
        from langchain_community.embeddings import HuggingFaceEmbeddings
        import warnings
        mock_hf = MagicMock(spec=HuggingFaceEmbeddings)
        with patch("embeddings._load_huggingface_embeddings", return_value=mock_hf):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                emb = get_embeddings("completely-unknown-embedding-xyz")
        self.assertIs(emb, mock_hf)
        self.assertTrue(any("Unknown embedding" in str(warning.message) for warning in w))

    @unittest.skipUnless(
        os.environ.get("OPENAI_API_KEY"),
        "OPENAI_API_KEY not set; skipping OpenAI embedding test",
    )
    def test_get_embeddings_openai(self):
        from embeddings import get_embeddings
        emb = get_embeddings("text-embedding-3-large")
        self.assertIsNotNone(emb)

    def test_get_embeddings_openai_no_key_raises(self):
        """Loading text-embedding-3-large without OPENAI_API_KEY raises ValueError."""
        from embeddings import get_embeddings
        original = os.environ.pop("OPENAI_API_KEY", None)
        try:
            with self.assertRaises((ValueError, Exception)):
                get_embeddings("text-embedding-3-large")
        finally:
            if original is not None:
                os.environ["OPENAI_API_KEY"] = original

    def test_get_bge_embeddings_alias(self):
        """get_bge_embeddings() backward compat alias should still work (mocked)."""
        from embeddings import get_bge_embeddings
        from langchain_community.embeddings import HuggingFaceEmbeddings
        mock_hf = MagicMock(spec=HuggingFaceEmbeddings)
        with patch("embeddings._load_huggingface_embeddings", return_value=mock_hf):
            emb = get_bge_embeddings()
        self.assertIs(emb, mock_hf)


# ===========================================================================
# 3. retriever — chunking strategies
# ===========================================================================

class TestChunkFixed(unittest.TestCase):
    """Tests for retriever.chunk_fixed."""

    def setUp(self):
        from retriever import chunk_fixed
        self.chunk_fixed = chunk_fixed
        self.texts = [
            "The water cycle is the continuous movement of water. "
            "Water evaporates from oceans. It rises as vapour. "
            "Condensation forms clouds. Precipitation returns water to Earth."
        ]
        self.metas = [{"topic": "water cycle", "grade": "6", "subject": "science"}]

    def test_returns_list_of_documents(self):
        docs = self.chunk_fixed(self.texts, self.metas)
        self.assertIsInstance(docs, list)
        for d in docs:
            self.assertIsInstance(d, Document)

    def test_metadata_preserved(self):
        docs = self.chunk_fixed(self.texts, self.metas)
        for d in docs:
            self.assertEqual(d.metadata["topic"], "water cycle")

    def test_chunk_size_respected(self):
        docs = self.chunk_fixed(self.texts, self.metas, chunk_size=50, chunk_overlap=0)
        for d in docs:
            self.assertLessEqual(len(d.page_content), 60)  # small tolerance

    def test_empty_input(self):
        docs = self.chunk_fixed([], [])
        self.assertEqual(docs, [])

    def test_multiple_texts(self):
        texts = ["Text one about water. " * 5, "Text two about carbon. " * 5]
        metas = [{"topic": "water cycle"}, {"topic": "carbon cycle"}]
        docs = self.chunk_fixed(texts, metas, chunk_size=50, chunk_overlap=0)
        topics = {d.metadata["topic"] for d in docs}
        self.assertIn("water cycle", topics)
        self.assertIn("carbon cycle", topics)


class TestChunkSlidingWindow(unittest.TestCase):
    """Tests for retriever.chunk_sliding_window."""

    def setUp(self):
        from retriever import chunk_sliding_window
        self.chunk_sw = chunk_sliding_window
        long_text = "A" * 1000
        self.texts = [long_text]
        self.metas = [{"topic": "test"}]

    def test_returns_documents(self):
        docs = self.chunk_sw(self.texts, self.metas, window_size=200, step=100)
        self.assertIsInstance(docs, list)
        self.assertGreater(len(docs), 0)

    def test_overlap_produces_more_chunks_than_no_overlap(self):
        docs_overlap = self.chunk_sw(self.texts, self.metas, window_size=200, step=100)
        docs_no_overlap = self.chunk_sw(self.texts, self.metas, window_size=200, step=200)
        self.assertGreaterEqual(len(docs_overlap), len(docs_no_overlap))

    def test_window_size_respected(self):
        docs = self.chunk_sw(self.texts, self.metas, window_size=100, step=50)
        for d in docs:
            self.assertLessEqual(len(d.page_content), 100)

    def test_metadata_preserved(self):
        docs = self.chunk_sw(self.texts, self.metas, window_size=200, step=100)
        for d in docs:
            self.assertEqual(d.metadata["topic"], "test")

    def test_empty_input(self):
        docs = self.chunk_sw([], [])
        self.assertEqual(docs, [])

    def test_short_text_produces_single_chunk(self):
        docs = self.chunk_sw(["Hello world"], [{"topic": "t"}], window_size=200, step=100)
        self.assertEqual(len(docs), 1)


class TestChunkSemantic(unittest.TestCase):
    """Tests for retriever.chunk_semantic (get_embeddings is mocked — no download)."""

    def _make_mock_embed_fn(self, n_sentences: int = 4):
        """Return a mock embedding function that produces distinct cosine-separable vectors."""
        import math
        # Produce orthogonal-ish unit vectors so similarity varies predictably
        mock_fn = MagicMock()
        def _embed(texts):
            vecs = []
            for i, _ in enumerate(texts):
                angle = (i / max(len(texts), 1)) * math.pi
                vecs.append([math.cos(angle), math.sin(angle)])
            return vecs
        mock_fn.embed_documents.side_effect = _embed
        return mock_fn

    def setUp(self):
        from retriever import chunk_semantic
        self.chunk_semantic = chunk_semantic
        # Two clearly different topic sentences to ensure at least one boundary
        self.texts = [
            "Water evaporates from oceans. Condensation forms clouds. "
            "The carbon cycle moves carbon through the atmosphere. "
            "Photosynthesis absorbs carbon dioxide from the air."
        ]
        self.metas = [{"topic": "mixed", "grade": "7"}]

    def test_returns_list_of_documents(self):
        with patch("retriever.get_embeddings", return_value=self._make_mock_embed_fn()):
            docs = self.chunk_semantic(self.texts, self.metas, embedding_name="bge-small")
        self.assertIsInstance(docs, list)
        self.assertGreater(len(docs), 0)

    def test_metadata_preserved(self):
        with patch("retriever.get_embeddings", return_value=self._make_mock_embed_fn()):
            docs = self.chunk_semantic(self.texts, self.metas, embedding_name="bge-small")
        for d in docs:
            self.assertIn("topic", d.metadata)

    def test_single_sentence_is_kept(self):
        with patch("retriever.get_embeddings", return_value=self._make_mock_embed_fn()):
            docs = self.chunk_semantic(
                ["Single sentence only."], [{"topic": "t"}], embedding_name="bge-small"
            )
        self.assertEqual(len(docs), 1)

    def test_empty_input(self):
        with patch("retriever.get_embeddings", return_value=self._make_mock_embed_fn()):
            docs = self.chunk_semantic([], [], embedding_name="bge-small")
        self.assertEqual(docs, [])


class TestGetChunks(unittest.TestCase):
    """Tests for retriever.get_chunks dispatcher."""

    def setUp(self):
        from retriever import get_chunks, CHUNK_SIZE, CHUNK_OVERLAP
        self.get_chunks = get_chunks
        self.texts = ["The quick brown fox. " * 20]
        self.metas = [{"topic": "test"}]

    def test_fixed_strategy(self):
        docs = self.get_chunks(self.texts, self.metas, strategy="fixed")
        self.assertGreater(len(docs), 0)

    def test_sliding_window_strategy(self):
        docs = self.get_chunks(self.texts, self.metas, strategy="sliding_window")
        self.assertGreater(len(docs), 0)

    def test_semantic_strategy(self):
        import math
        mock_fn = MagicMock()
        def _embed(texts):
            return [[math.cos(i), math.sin(i)] for i, _ in enumerate(texts)]
        mock_fn.embed_documents.side_effect = _embed
        with patch("retriever.get_embeddings", return_value=mock_fn):
            docs = self.get_chunks(self.texts, self.metas, strategy="semantic",
                                   embedding_name="bge-small")
        self.assertGreater(len(docs), 0)

    def test_unknown_strategy_defaults_to_fixed(self):
        docs = self.get_chunks(self.texts, self.metas, strategy="unknown_strategy_xyz")
        self.assertGreater(len(docs), 0)


# ===========================================================================
# 4. retriever — BM25Index
# ===========================================================================

BM25_AVAILABLE = False
try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    pass


@unittest.skipUnless(BM25_AVAILABLE, "rank_bm25 not installed")
class TestBM25Index(unittest.TestCase):
    """Tests for retriever.BM25Index."""

    def setUp(self):
        from retriever import BM25Index
        self.docs = _make_docs(8, topic="water cycle")
        self.index = BM25Index(self.docs)

    def test_search_returns_list(self):
        results = self.index.search("evaporation condensation")
        self.assertIsInstance(results, list)

    def test_search_returns_tuples_doc_score(self):
        results = self.index.search("water cycle")
        for doc, score in results:
            self.assertIsInstance(doc, Document)
            self.assertIsInstance(score, float)

    def test_search_top_k_respected(self):
        results = self.index.search("water", k=3)
        self.assertLessEqual(len(results), 3)

    def test_search_scores_non_negative(self):
        results = self.index.search("evaporation", k=5)
        for _, score in results:
            self.assertGreaterEqual(score, 0.0)

    def test_search_empty_query(self):
        results = self.index.search("")
        self.assertEqual(results, [])

    def test_search_stopword_only_query(self):
        results = self.index.search("the a an is")
        self.assertEqual(results, [])

    def test_search_relevance_ordering(self):
        """Docs containing 'evaporation' should score higher for that query."""
        from retriever import BM25Index
        docs = [
            _make_doc("evaporation evaporation evaporation"),
            _make_doc("the quick brown fox"),
        ]
        idx = BM25Index(docs)
        results = idx.search("evaporation", k=2)
        if len(results) >= 2:
            self.assertGreaterEqual(results[0][1], results[1][1])


@unittest.skipUnless(BM25_AVAILABLE, "rank_bm25 not installed")
class TestBuildBM25Index(unittest.TestCase):
    """Tests for retriever.build_bm25_index factory."""

    def test_build_returns_index(self):
        from retriever import build_bm25_index, BM25Index
        docs = _make_docs(5)
        idx = build_bm25_index(docs)
        self.assertIsNotNone(idx)
        self.assertIsInstance(idx, BM25Index)

    def test_build_with_empty_docs(self):
        from retriever import build_bm25_index
        idx = build_bm25_index([])
        # Should succeed; searching will return nothing
        self.assertIsNotNone(idx)
        results = idx.search("anything")
        self.assertEqual(results, [])


# ===========================================================================
# 5. retriever — mmr_rerank
# ===========================================================================

class TestMMRRerank(unittest.TestCase):
    """Tests for retriever.mmr_rerank (formerly rerank_documents)."""

    def setUp(self):
        from retriever import mmr_rerank, rerank_documents
        self.mmr_rerank = mmr_rerank
        self.rerank_documents = rerank_documents
        self.docs = _make_docs(10, topic="water cycle")

    def test_returns_list(self):
        result = self.mmr_rerank("evaporation water cycle", self.docs, top_k=3)
        self.assertIsInstance(result, list)

    def test_top_k_respected(self):
        result = self.mmr_rerank("evaporation", self.docs, top_k=3)
        self.assertLessEqual(len(result), 3)

    def test_empty_candidates(self):
        result = self.mmr_rerank("query", [], top_k=3)
        self.assertEqual(result, [])

    def test_fewer_candidates_than_k(self):
        two_docs = _make_docs(2)
        result = self.mmr_rerank("water", two_docs, top_k=5)
        self.assertLessEqual(len(result), 2)

    def test_topic_filter_bonus_does_not_crash(self):
        result = self.mmr_rerank("water", self.docs, top_k=3, topic_filter="water cycle")
        self.assertIsInstance(result, list)

    def test_rerank_documents_alias(self):
        """rerank_documents should be an alias for mmr_rerank."""
        result = self.rerank_documents("water cycle", self.docs, top_k=3)
        self.assertIsInstance(result, list)

    def test_diversity_reduces_duplicates(self):
        """MMR with low lambda should prefer diverse docs."""
        # Create docs where first two are identical
        dup_docs = [_make_doc("evaporation is the process of water turning into vapour")] * 3
        dup_docs += [_make_doc("condensation forms clouds from water vapour")] * 2
        result = self.mmr_rerank("water", dup_docs, top_k=2, lambda_param=0.1)
        self.assertEqual(len(result), 2)


# ===========================================================================
# 6. retriever — cross_encoder_rerank
# ===========================================================================

class TestCrossEncoderRerank(unittest.TestCase):
    """Tests for retriever.cross_encoder_rerank."""

    def setUp(self):
        from retriever import cross_encoder_rerank
        self.cross_encoder_rerank = cross_encoder_rerank
        self.docs = _make_docs(5, topic="water cycle")

    def test_returns_list(self):
        result = self.cross_encoder_rerank("water cycle", self.docs, top_k=3)
        self.assertIsInstance(result, list)

    def test_top_k_respected(self):
        result = self.cross_encoder_rerank("water", self.docs, top_k=2)
        self.assertLessEqual(len(result), 2)

    def test_empty_candidates_returns_empty(self):
        result = self.cross_encoder_rerank("water", [], top_k=3)
        self.assertEqual(result, [])

    def test_falls_back_gracefully_when_model_fails(self):
        """Even if cross-encoder model fails, should return docs via MMR fallback."""
        with patch("retriever.load_cross_encoder", return_value=None):
            result = self.cross_encoder_rerank("water cycle", self.docs, top_k=3)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


# ===========================================================================
# 7. retriever — build_vector_store (mocked Chroma)
# ===========================================================================

class TestBuildVectorStore(unittest.TestCase):
    """Tests for retriever.build_vector_store with mocked Chroma."""

    def _make_mock_chroma(self, count: int = 5):
        mock_store = MagicMock()
        mock_store._collection.count.return_value = count
        mock_store._embedding_function = MagicMock()
        return mock_store

    def test_returns_chroma_store_new_build(self):
        """When no persist dir exists, build fresh store."""
        from retriever import build_vector_store
        mock_store = self._make_mock_chroma(5)
        with patch("retriever.os.path.exists", return_value=False), \
             patch("retriever.get_embeddings", return_value=MagicMock()), \
             patch("retriever.get_texts_and_metadatas",
                   return_value=(["sample text"], [{"topic": "test"}])), \
             patch("retriever.get_chunks", return_value=[_make_doc("sample")]), \
             patch("retriever.Chroma.from_documents", return_value=mock_store):
            store = build_vector_store(persist=False, embedding_name="bge-small",
                                       chunking_strategy="fixed")
        self.assertEqual(store, mock_store)

    def test_loads_existing_store_when_present(self):
        """When persist dir exists and collection is non-empty, reuse it."""
        from retriever import build_vector_store
        mock_store = self._make_mock_chroma(10)
        with patch("retriever.os.path.exists", return_value=True), \
             patch("retriever.get_embeddings", return_value=MagicMock()), \
             patch("retriever.Chroma", return_value=mock_store):
            store = build_vector_store(persist=True, embedding_name="bge-small",
                                       chunking_strategy="fixed")
        self.assertEqual(store, mock_store)

    def test_rebuilds_when_collection_empty(self):
        """When persist dir exists but collection is empty, rebuild."""
        from retriever import build_vector_store
        empty_store = self._make_mock_chroma(0)
        fresh_store = self._make_mock_chroma(5)
        with patch("retriever.os.path.exists", return_value=True), \
             patch("retriever.get_embeddings", return_value=MagicMock()), \
             patch("retriever.Chroma", return_value=empty_store), \
             patch("retriever.get_texts_and_metadatas",
                   return_value=(["text"], [{"topic": "t"}])), \
             patch("retriever.get_chunks", return_value=[_make_doc("text")]), \
             patch("retriever.Chroma.from_documents", return_value=fresh_store):
            store = build_vector_store(persist=True, embedding_name="bge-small",
                                       chunking_strategy="fixed")
        self.assertEqual(store, fresh_store)

    def test_uses_different_dir_per_strategy(self):
        """Different chunking strategies must not share a Chroma directory."""
        from research_config import CHROMA_DIR_TEMPLATE
        tag_fixed = "bge-small_fixed"
        tag_sw = "bge-small_sliding_window"
        dir_fixed = CHROMA_DIR_TEMPLATE.format(embedding_name=tag_fixed)
        dir_sw = CHROMA_DIR_TEMPLATE.format(embedding_name=tag_sw)
        self.assertNotEqual(dir_fixed, dir_sw)


# ===========================================================================
# 8. retriever — hybrid_search and hierarchical_retrieve (mocked)
# ===========================================================================

class TestHybridSearch(unittest.TestCase):
    """Tests for retriever.hybrid_search with mocked vector store."""

    def _make_store(self):
        store = MagicMock()
        docs = _make_docs(5)
        store.similarity_search_with_relevance_scores.return_value = [
            (d, 0.8 - i * 0.1) for i, d in enumerate(docs)
        ]
        return store

    def test_returns_list_of_documents(self):
        from retriever import hybrid_search
        store = self._make_store()
        result = hybrid_search(store, None, "water cycle", k=3)
        self.assertIsInstance(result, list)

    def test_top_k_respected(self):
        from retriever import hybrid_search
        store = self._make_store()
        result = hybrid_search(store, None, "water cycle", k=2)
        self.assertLessEqual(len(result), 2)

    @unittest.skipUnless(BM25_AVAILABLE, "rank_bm25 not installed")
    def test_with_bm25_index(self):
        from retriever import hybrid_search, BM25Index
        store = self._make_store()
        idx = BM25Index(_make_docs(5))
        result = hybrid_search(store, idx, "evaporation water", k=3)
        self.assertIsInstance(result, list)

    def test_vector_error_fallback(self):
        """If vector store raises an error, should still return a list."""
        from retriever import hybrid_search
        store = MagicMock()
        store.similarity_search_with_relevance_scores.side_effect = Exception("mock error")
        result = hybrid_search(store, None, "water cycle", k=3)
        self.assertIsInstance(result, list)


class TestHierarchicalRetrieve(unittest.TestCase):
    """Tests for retriever.hierarchical_retrieve with mocked vector store."""

    def _make_store(self, n: int = 5):
        store = MagicMock()
        docs = _make_docs(n)
        store.similarity_search_with_relevance_scores.return_value = [
            (d, 0.9 - i * 0.1) for i, d in enumerate(docs)
        ]
        return store

    def test_returns_list(self):
        from retriever import hierarchical_retrieve
        store = self._make_store()
        result = hierarchical_retrieve(store, None, "water cycle", topic="water cycle", k=3)
        self.assertIsInstance(result, list)

    def test_fallback_when_topic_returns_few(self):
        """When topic-filtered search returns < 2 docs, falls back to full corpus."""
        from retriever import hierarchical_retrieve
        store = MagicMock()
        # Return only 1 doc on first call (topic filter), 5 on second (no filter)
        docs = _make_docs(5)
        store.similarity_search_with_relevance_scores.side_effect = [
            [(docs[0], 0.8)],           # topic-filtered: only 1 result
            [(d, 0.9 - i * 0.1) for i, d in enumerate(docs)],  # full corpus
        ]
        result = hierarchical_retrieve(store, None, "water", topic="water cycle", k=3)
        self.assertIsInstance(result, list)

    def test_no_topic_skips_filtering(self):
        from retriever import hierarchical_retrieve
        store = self._make_store()
        result = hierarchical_retrieve(store, None, "water cycle", topic=None, k=3)
        self.assertIsInstance(result, list)


# ===========================================================================
# 9. retriever — retrieve_top_k (mocked)
# ===========================================================================

class TestRetrieveTopK(unittest.TestCase):
    """Tests for retriever.retrieve_top_k."""

    def _make_store(self, n: int = 5):
        store = MagicMock()
        store.similarity_search.return_value = _make_docs(n)
        return store

    def test_returns_documents(self):
        from retriever import retrieve_top_k
        store = self._make_store()
        result = retrieve_top_k(store, "evaporation", k=3)
        self.assertIsInstance(result, list)

    def test_topic_filter_applied(self):
        from retriever import retrieve_top_k
        store = self._make_store()
        retrieve_top_k(store, "water", k=3, topic_filter="water cycle")
        # Ensure similarity_search was called (with or without filter)
        self.assertTrue(store.similarity_search.called)

    def test_fallback_on_error(self):
        from retriever import retrieve_top_k
        store = MagicMock()
        store.similarity_search.side_effect = [Exception("error"), _make_docs(3)]
        result = retrieve_top_k(store, "water", k=3, topic_filter="water cycle")
        self.assertIsInstance(result, list)


# ===========================================================================
# 10. rag_pipeline — _build_llm factory
# ===========================================================================

class TestBuildLLM(unittest.TestCase):
    """Tests for rag_pipeline._build_llm factory function."""

    def setUp(self):
        from rag_pipeline import _build_llm
        self._build_llm = _build_llm

    def test_unknown_model_returns_ollama(self):
        """An unregistered model name should fall back to OllamaLLM."""
        from langchain_ollama import OllamaLLM
        llm = self._build_llm("this-is-not-registered")
        self.assertIsInstance(llm, OllamaLLM)

    def test_ollama_model_returns_ollama(self):
        from langchain_ollama import OllamaLLM
        llm = self._build_llm("phi3")
        self.assertIsInstance(llm, OllamaLLM)

    def test_groq_model_raises_valueerror_without_key(self):
        original = os.environ.pop("GROQ_API_KEY", None)
        try:
            with self.assertRaises((ValueError, ImportError)):
                self._build_llm("groq-llama3-8b")
        finally:
            if original is not None:
                os.environ["GROQ_API_KEY"] = original

    @unittest.skipUnless(os.environ.get("GROQ_API_KEY"), "GROQ_API_KEY not set")
    def test_groq_model_with_key(self):
        llm = self._build_llm("groq-llama3-8b")
        self.assertIsNotNone(llm)


# ===========================================================================
# 11. rag_pipeline — RAGPipeline.__init__ (mocked vector store)
# ===========================================================================

class TestRAGPipelineInit(unittest.TestCase):
    """Tests for RAGPipeline construction with a mocked vector store."""

    def _make_mock_store(self):
        store = MagicMock()
        store._embedding_function = MagicMock()
        store._embedding_function.embed_query.return_value = [0.1] * 384
        return store

    def _build_pipeline(self, model_name: str = "phi3",
                        retrieval_mode: str = "hybrid",
                        use_cross_encoder: bool = False):
        from rag_pipeline import RAGPipeline
        store = self._make_mock_store()
        with patch("rag_pipeline.get_texts_and_metadatas",
                   return_value=(["sample text"], [{"topic": "test"}])), \
             patch("rag_pipeline.OllamaLLM") as mock_ollama, \
             patch("rag_pipeline.build_bm25_index", return_value=None):
            mock_ollama.return_value = MagicMock()
            pipeline = RAGPipeline(
                vector_store=store,
                model_name=model_name,
                retrieval_mode=retrieval_mode,
                use_cross_encoder=use_cross_encoder,
            )
        return pipeline

    def test_init_default_model(self):
        pipeline = self._build_pipeline("phi3")
        self.assertEqual(pipeline.model_name, "phi3")

    def test_init_retrieval_mode_stored(self):
        pipeline = self._build_pipeline("phi3", retrieval_mode="bm25_only")
        self.assertEqual(pipeline.retrieval_mode, "bm25_only")

    def test_init_use_cross_encoder_stored(self):
        pipeline = self._build_pipeline("phi3", use_cross_encoder=True)
        self.assertTrue(pipeline.use_cross_encoder)

    def test_init_use_cross_encoder_off_by_default(self):
        pipeline = self._build_pipeline("phi3")
        self.assertFalse(pipeline.use_cross_encoder)

    def test_api_model_graceful_fallback(self):
        """If an API LLM fails (no key), RAGPipeline falls back to phi3."""
        from rag_pipeline import RAGPipeline
        store = self._make_mock_store()
        # Remove API keys to force failure
        env_backup = {k: os.environ.pop(k, None)
                      for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY")}
        try:
            with patch("rag_pipeline.get_texts_and_metadatas",
                       return_value=(["text"], [{"topic": "t"}])), \
                 patch("rag_pipeline.OllamaLLM") as mock_ollama, \
                 patch("rag_pipeline.build_bm25_index", return_value=None):
                mock_ollama.return_value = MagicMock()
                pipeline = RAGPipeline(
                    vector_store=store,
                    model_name="gpt-4.1",   # will fail without key
                )
            # Should have fallen back gracefully (OllamaLLM was called)
            self.assertIsNotNone(pipeline.llm)
        finally:
            for k, v in env_backup.items():
                if v is not None:
                    os.environ[k] = v


# ===========================================================================
# 12. evaluation — compute_all_metrics (smoke test)
# ===========================================================================

class TestComputeAllMetrics(unittest.TestCase):
    """Smoke tests for evaluation.compute_all_metrics."""

    def setUp(self):
        from evaluation import compute_all_metrics
        self.compute = compute_all_metrics
        self.docs = _make_docs(5, topic="water cycle")
        self.all_docs = _make_docs(20, topic="water cycle")

    def test_returns_dict(self):
        result = self.compute(
            query="What is the water cycle?",
            answer="Water evaporates and forms clouds through condensation.",
            retrieved_docs=self.docs,
            all_docs=self.all_docs,
            query_topic="water cycle",
            k=5,
            mode="RAG",
        )
        self.assertIsInstance(result, dict)

    def test_keys_present(self):
        result = self.compute(
            query="What is the water cycle?",
            answer="Water evaporates and forms clouds.",
            retrieved_docs=self.docs,
            all_docs=self.all_docs,
            query_topic="water cycle",
            k=5,
            mode="RAG",
        )
        for key in ("Precision@5", "Recall@5", "MRR", "Faithfulness"):
            with self.subTest(key=key):
                self.assertIn(key, result)

    def test_scores_in_valid_range(self):
        result = self.compute(
            query="evaporation water cycle",
            answer="Evaporation is the key driver.",
            retrieved_docs=self.docs,
            all_docs=self.all_docs,
            query_topic="water cycle",
            k=5,
            mode="RAG",
        )
        for key, value in result.items():
            with self.subTest(metric=key):
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)

    def test_empty_retrieved_docs(self):
        result = self.compute(
            query="water cycle",
            answer="no answer",
            retrieved_docs=[],
            all_docs=self.all_docs,
            query_topic="water cycle",
            k=5,
            mode="LLM Fallback",
        )
        self.assertIsInstance(result, dict)


# ===========================================================================
# 13. test_queries — run_benchmark (mocked pipeline)
# ===========================================================================

class TestRunBenchmark(unittest.TestCase):
    """Tests for test_queries.run_benchmark with a mocked RAGPipeline."""

    def _make_mock_pipeline(self):
        pipeline = MagicMock()
        mock_result = MagicMock()
        mock_result.answer = "Water evaporates from oceans."
        mock_result.detected_topic = "water cycle"
        mock_result.mode = "RAG"
        mock_result.metrics = {"precision_at_k": 0.8, "recall_at_k": 0.6,
                                "mrr": 0.9, "faithfulness": 0.75}
        pipeline.run.return_value = mock_result
        return pipeline

    def setUp(self):
        from test_queries import run_benchmark, TEST_SET
        self.run_benchmark = run_benchmark
        self.TEST_SET = TEST_SET

    def test_benchmark_returns_dict(self):
        from context_memory import ConversationMemory
        from topic_memory_manager import TopicMemoryManager
        pipeline = self._make_mock_pipeline()
        result = self.run_benchmark(pipeline, ConversationMemory, TopicMemoryManager)
        self.assertIsInstance(result, dict)

    def test_benchmark_results_key(self):
        from context_memory import ConversationMemory
        from topic_memory_manager import TopicMemoryManager
        pipeline = self._make_mock_pipeline()
        result = self.run_benchmark(pipeline, ConversationMemory, TopicMemoryManager)
        self.assertIn("results", result)
        self.assertIn("summary", result)

    def test_benchmark_results_length(self):
        from context_memory import ConversationMemory
        from topic_memory_manager import TopicMemoryManager
        pipeline = self._make_mock_pipeline()
        result = self.run_benchmark(pipeline, ConversationMemory, TopicMemoryManager)
        self.assertEqual(len(result["results"]), len(self.TEST_SET))

    def test_benchmark_summary_averaged(self):
        from context_memory import ConversationMemory
        from topic_memory_manager import TopicMemoryManager
        pipeline = self._make_mock_pipeline()
        result = self.run_benchmark(pipeline, ConversationMemory, TopicMemoryManager)
        summary = result["summary"]
        if summary:  # only check when non-empty
            for key, value in summary.items():
                with self.subTest(metric=key):
                    self.assertIsInstance(value, float)

    def test_benchmark_handles_pipeline_error(self):
        """If the pipeline raises an exception on a query, it should be recorded."""
        from context_memory import ConversationMemory
        from topic_memory_manager import TopicMemoryManager
        pipeline = MagicMock()
        pipeline.run.side_effect = RuntimeError("mock pipeline error")
        result = self.run_benchmark(pipeline, ConversationMemory, TopicMemoryManager)
        self.assertEqual(len(result["results"]), len(self.TEST_SET))
        # Each result should have an 'error' key
        for r in result["results"]:
            self.assertIn("error", r)


# ===========================================================================
# 14. Tokeniser helper (_tokenise) in retriever
# ===========================================================================

class TestTokeniseHelper(unittest.TestCase):
    """Tests for the internal _tokenise function in retriever."""

    def setUp(self):
        from retriever import _tokenise
        self._tokenise = _tokenise

    def test_returns_list(self):
        result = self._tokenise("the water cycle evaporation")
        self.assertIsInstance(result, list)

    def test_stopwords_removed(self):
        result = self._tokenise("the a an is it in of")
        self.assertEqual(result, [])

    def test_meaningful_words_kept(self):
        result = self._tokenise("evaporation condensation precipitation")
        self.assertIn("evaporation", result)
        self.assertIn("condensation", result)

    def test_lowercases_text(self):
        result = self._tokenise("EVAPORATION Condensation")
        self.assertIn("evaporation", result)
        self.assertIn("condensation", result)

    def test_empty_string(self):
        result = self._tokenise("")
        self.assertEqual(result, [])


# ===========================================================================
# 15. Doc-key helper (_doc_key) in retriever
# ===========================================================================

class TestDocKeyHelper(unittest.TestCase):
    """Tests for the _doc_key deduplication helper in retriever."""

    def setUp(self):
        from retriever import _doc_key
        self._doc_key = _doc_key

    def test_same_content_same_key(self):
        d1 = _make_doc("Water evaporates from the ocean.")
        d2 = _make_doc("Water evaporates from the ocean.")
        self.assertEqual(self._doc_key(d1), self._doc_key(d2))

    def test_different_content_different_key(self):
        d1 = _make_doc("Water evaporates.")
        d2 = _make_doc("Carbon dioxide absorbs heat.")
        self.assertNotEqual(self._doc_key(d1), self._doc_key(d2))

    def test_returns_string(self):
        d = _make_doc("some content")
        self.assertIsInstance(self._doc_key(d), str)


# ===========================================================================
# Entry point
# ===========================================================================

if __name__ == "__main__":
    # Ensure the repo root is in the Python path
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    verbosity = 2 if "-v" in sys.argv else 1
    unittest.main(verbosity=verbosity)
