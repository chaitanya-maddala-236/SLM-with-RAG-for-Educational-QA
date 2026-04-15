"""
tests/test_all_models.py
------------------------
Parameterized tests for every model entry in research_config.MODEL_REGISTRY.

All test parameters are read dynamically from MODEL_REGISTRY — no values are
hardcoded in this file.  Tests cover:

  - Registry schema validation (required fields, valid types, non-negative costs)
  - get_model_config() lookup for every registered model
  - _build_llm dispatch: correct LLM class selected for each provider
    (Ollama / Groq / OpenAI / Anthropic / Google)
  - API key guard: loading a cloud-provider model without the required API key
    raises a ValueError (or equivalent) before hitting the network
  - Cost computation: estimated_cost_usd is non-negative for every model
    given fixed token counts derived from TEST_QUERIES lengths

Run:
    python tests/test_all_models.py
    python tests/test_all_models.py -v
    pytest tests/test_all_models.py -v
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
    MODEL_REGISTRY,
    SLM_MODELS,
    LLM_MODELS,
    GROQ_MODELS,
    get_model_config,
    TEST_QUERIES,
)


# ── Registry schema requirements ────────────────────────────────────────────

_REQUIRED_FIELDS = {
    "name",
    "type",
    "provider",
    "model_id",
    "cost_per_1k_input_tokens",
    "cost_per_1k_output_tokens",
}

_VALID_TYPES = {"SLM", "LLM"}
_VALID_PROVIDERS = {"ollama", "groq", "openai", "anthropic", "google"}

# Provider → environment variable name for the API key
_PROVIDER_KEY_ENV = {
    "groq": "GROQ_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
}


# ── Helper ───────────────────────────────────────────────────────────────────

def _avg_query_length_tokens() -> int:
    """
    Estimate average token count for TEST_QUERIES by word-split approximation.
    Returns an int derived from the dataset.

    Fallback: when TEST_QUERIES is empty (e.g. the dataset file is missing in
    a stripped CI environment) the function returns the constant ``1`` — a safe
    non-zero minimum that lets cost tests run without dividing by zero.  This
    fallback constant is intentional and is clearly documented here rather than
    pretending it is "purely computed".
    """
    if not TEST_QUERIES:
        return 1  # intentional minimum — avoids divide-by-zero in cost tests
    total_words = sum(len(q["query"].split()) for q in TEST_QUERIES)
    avg_words = total_words / len(TEST_QUERIES)
    # ~1.3 tokens per word is a standard approximation for English text
    return max(1, int(avg_words * 1.3))


# ═══════════════════════════════════════════════════════════════════════════════
#  1.  Registry schema — one test class, parameterized via sub-tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestModelRegistrySchema(unittest.TestCase):
    """Each entry in MODEL_REGISTRY must satisfy the required schema."""

    def test_registry_is_non_empty(self):
        self.assertGreater(len(MODEL_REGISTRY), 0,
                           "MODEL_REGISTRY must contain at least one entry")

    def test_required_fields_present(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry.get("name", "<unnamed>")):
                missing = _REQUIRED_FIELDS - entry.keys()
                self.assertFalse(
                    missing,
                    f"Model '{entry.get('name')}' is missing fields: {missing}",
                )

    def test_type_is_valid(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                self.assertIn(
                    entry["type"], _VALID_TYPES,
                    f"Model '{entry['name']}' has invalid type '{entry['type']}'. "
                    f"Must be one of {_VALID_TYPES}.",
                )

    def test_provider_is_valid(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                self.assertIn(
                    entry["provider"], _VALID_PROVIDERS,
                    f"Model '{entry['name']}' has invalid provider "
                    f"'{entry['provider']}'. Must be one of {_VALID_PROVIDERS}.",
                )

    def test_model_id_is_non_empty_string(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                self.assertIsInstance(entry["model_id"], str)
                self.assertGreater(
                    len(entry["model_id"].strip()), 0,
                    f"Model '{entry['name']}' has empty model_id",
                )

    def test_input_cost_is_non_negative(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                self.assertGreaterEqual(
                    entry["cost_per_1k_input_tokens"], 0.0,
                    f"Model '{entry['name']}' input cost is negative",
                )

    def test_output_cost_is_non_negative(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                self.assertGreaterEqual(
                    entry["cost_per_1k_output_tokens"], 0.0,
                    f"Model '{entry['name']}' output cost is negative",
                )

    def test_slm_models_have_zero_cost(self):
        """All SLM (local Ollama) models should have zero cost."""
        for entry in MODEL_REGISTRY:
            if entry["type"] == "SLM":
                with self.subTest(model=entry["name"]):
                    self.assertEqual(
                        entry["cost_per_1k_input_tokens"], 0.0,
                        f"SLM '{entry['name']}' should have zero input cost",
                    )
                    self.assertEqual(
                        entry["cost_per_1k_output_tokens"], 0.0,
                        f"SLM '{entry['name']}' should have zero output cost",
                    )

    def test_names_are_unique(self):
        names = [entry["name"] for entry in MODEL_REGISTRY]
        duplicates = {n for n in names if names.count(n) > 1}
        self.assertFalse(
            duplicates,
            f"Duplicate model names found in MODEL_REGISTRY: {duplicates}",
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  2.  get_model_config lookup
# ═══════════════════════════════════════════════════════════════════════════════

class TestGetModelConfig(unittest.TestCase):
    """get_model_config must resolve every registered model by name."""

    def test_lookup_returns_entry_for_every_model(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                cfg = get_model_config(entry["name"])
                self.assertIsNotNone(
                    cfg,
                    f"get_model_config('{entry['name']}') returned None",
                )
                self.assertEqual(cfg["name"], entry["name"])

    def test_lookup_unknown_model_returns_none(self):
        self.assertIsNone(get_model_config("__no_such_model_xyz__"))

    def test_lookup_preserves_all_fields(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                cfg = get_model_config(entry["name"])
                for field in _REQUIRED_FIELDS:
                    self.assertIn(
                        field, cfg,
                        f"get_model_config('{entry['name']}') missing field '{field}'",
                    )

    def test_slm_list_matches_registry(self):
        """SLM_MODELS must equal all model names where type=='SLM'."""
        expected_slms = [m["name"] for m in MODEL_REGISTRY if m["type"] == "SLM"]
        self.assertEqual(
            SLM_MODELS, expected_slms,
            "SLM_MODELS does not match MODEL_REGISTRY type=='SLM' entries",
        )

    def test_llm_list_matches_registry(self):
        """LLM_MODELS must equal all model names where type=='LLM'."""
        expected_llms = [m["name"] for m in MODEL_REGISTRY if m["type"] == "LLM"]
        self.assertEqual(
            LLM_MODELS, expected_llms,
            "LLM_MODELS does not match MODEL_REGISTRY type=='LLM' entries",
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  3.  Cost computation
# ═══════════════════════════════════════════════════════════════════════════════

class TestCostComputation(unittest.TestCase):
    """
    Verify that estimated_cost_usd is non-negative for every model when
    token counts are derived from TEST_QUERIES lengths (no hardcoded values).
    """

    def setUp(self):
        self._avg_tokens = _avg_query_length_tokens()
        # Typical QA responses are ~3× longer than the input question: short
        # factual questions yield ≈2-3 sentence answers while explanation
        # requests yield multi-paragraph answers; 3× is a conservative middle
        # ground that gives a realistic estimated_cost_usd for every model.
        self._avg_output_tokens = self._avg_tokens * 3

    def test_cost_non_negative_for_all_models(self):
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                input_cost = (
                    self._avg_tokens
                    * entry["cost_per_1k_input_tokens"]
                    / 1000
                )
                output_cost = (
                    self._avg_output_tokens
                    * entry["cost_per_1k_output_tokens"]
                    / 1000
                )
                total_cost = input_cost + output_cost
                self.assertGreaterEqual(
                    total_cost, 0.0,
                    f"Negative cost computed for model '{entry['name']}'",
                )

    def test_slm_cost_is_zero(self):
        """SLMs (Ollama) must always have zero estimated cost."""
        for entry in MODEL_REGISTRY:
            if entry["type"] == "SLM":
                with self.subTest(model=entry["name"]):
                    total_cost = (
                        self._avg_tokens * entry["cost_per_1k_input_tokens"] / 1000
                        + self._avg_output_tokens * entry["cost_per_1k_output_tokens"] / 1000
                    )
                    self.assertEqual(
                        total_cost, 0.0,
                        f"SLM '{entry['name']}' should have zero cost",
                    )

    def test_groq_models_have_positive_cost(self):
        """Cloud LLM models on Groq should have non-zero cost per query."""
        for entry in MODEL_REGISTRY:
            if entry.get("provider") == "groq":
                with self.subTest(model=entry["name"]):
                    total_cost_rate = (
                        entry["cost_per_1k_input_tokens"]
                        + entry["cost_per_1k_output_tokens"]
                    )
                    self.assertGreater(
                        total_cost_rate, 0.0,
                        f"Groq model '{entry['name']}' should have positive cost rate",
                    )


# ═══════════════════════════════════════════════════════════════════════════════
#  4.  _build_llm dispatch (mocked — no network, no API keys required)
# ═══════════════════════════════════════════════════════════════════════════════

class TestBuildLLMDispatch(unittest.TestCase):
    """
    For every model in MODEL_REGISTRY, verify that RAGPipeline._build_llm
    selects the correct LLM class for the provider.

    All external LLM constructors are mocked — no network calls are made.
    """

    def _build_with_mock(self, model_name: str, extra_env: dict | None = None):
        """
        Call RAGPipeline._build_llm for *model_name* with all LLM constructors
        mocked out and optional extra environment variables set.
        Returns the mock instance that was returned by _build_llm.
        """
        mock_ollama = MagicMock(name="OllamaLLM")
        mock_groq = MagicMock(name="ChatGroq")
        mock_openai = MagicMock(name="ChatOpenAI")
        mock_anthropic = MagicMock(name="ChatAnthropic")
        mock_google = MagicMock(name="ChatGoogleGenerativeAI")

        env_patch = dict(os.environ)
        # Strip real API keys so tests are hermetic unless explicitly provided
        for key in ("GROQ_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"):
            env_patch.pop(key, None)
        if extra_env:
            env_patch.update(extra_env)

        # Use create=True because these module-level names only exist when the
        # optional package is installed; patch must create them when absent.
        # build_bm25_index is patched on retriever (where rag_pipeline imports
        # it from) so we don't need to target rag_pipeline.build_bm25_index.
        with patch.dict(os.environ, env_patch, clear=True), \
             patch("rag_pipeline.OllamaLLM", mock_ollama), \
             patch("rag_pipeline._GROQ_AVAILABLE", True), \
             patch("rag_pipeline._ChatGroq", mock_groq, create=True), \
             patch("rag_pipeline._OPENAI_AVAILABLE", True), \
             patch("rag_pipeline._ChatOpenAI", mock_openai, create=True), \
             patch("rag_pipeline._ANTHROPIC_AVAILABLE", True), \
             patch("rag_pipeline._ChatAnthropic", mock_anthropic, create=True), \
             patch("rag_pipeline._GOOGLE_AVAILABLE", True), \
             patch("rag_pipeline._ChatGoogleGenerativeAI", mock_google, create=True):
            import rag_pipeline as _rag_mod
            # _build_llm is a module-level function
            llm = _rag_mod._build_llm(model_name)

        return llm, mock_ollama, mock_groq, mock_openai, mock_anthropic, mock_google

    def test_ollama_models_use_ollama_llm(self):
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "ollama":
                with self.subTest(model=entry["name"]):
                    llm, mock_ollama, *_ = self._build_with_mock(entry["name"])
                    mock_ollama.assert_called_once()

    def test_groq_models_use_chatgroq(self):
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "groq":
                with self.subTest(model=entry["name"]):
                    fake_key = {"GROQ_API_KEY": "gsk_test_key_for_unit_test"}
                    llm, _, mock_groq, *_ = self._build_with_mock(
                        entry["name"], extra_env=fake_key
                    )
                    mock_groq.assert_called_once()

    def test_openai_models_use_chatopenai(self):
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "openai":
                with self.subTest(model=entry["name"]):
                    fake_key = {"OPENAI_API_KEY": "sk-test-unit-test"}
                    llm, _, _, mock_openai, *_ = self._build_with_mock(
                        entry["name"], extra_env=fake_key
                    )
                    mock_openai.assert_called_once()

    def test_anthropic_models_use_chatanthropic(self):
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "anthropic":
                with self.subTest(model=entry["name"]):
                    fake_key = {"ANTHROPIC_API_KEY": "ant-test-unit-test"}
                    llm, _, _, _, mock_anthropic, _ = self._build_with_mock(
                        entry["name"], extra_env=fake_key
                    )
                    mock_anthropic.assert_called_once()

    def test_google_models_use_chatgoogle(self):
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "google":
                with self.subTest(model=entry["name"]):
                    fake_key = {"GOOGLE_API_KEY": "AIza_test_unit_test"}
                    llm, _, _, _, _, mock_google = self._build_with_mock(
                        entry["name"], extra_env=fake_key
                    )
                    mock_google.assert_called_once()


# ═══════════════════════════════════════════════════════════════════════════════
#  5.  API key guard — missing keys raise before hitting the network
# ═══════════════════════════════════════════════════════════════════════════════

class TestAPIKeyGuard(unittest.TestCase):
    """
    Cloud-provider models must raise (ValueError or similar) when the
    required API key is absent — not silently return None or call the network.

    Only non-Ollama providers are tested here.  Tests are SKIPPED (not failed)
    when the API key is actually present in the environment, because in that
    case no error is expected.
    """

    def _provider_has_key(self, provider: str) -> bool:
        env_var = _PROVIDER_KEY_ENV.get(provider, "")
        val = os.environ.get(env_var, "").strip()
        return bool(val) and not any(
            x in val.lower()
            for x in ("replace_with", "your_", "example", "placeholder")
        )

    def _skip_if_key_present(self, provider: str):
        if self._provider_has_key(provider):
            raise unittest.SkipTest(
                f"{_PROVIDER_KEY_ENV[provider]} is set — skipping key-guard test"
            )

    def test_groq_models_raise_without_key(self):
        """groq-* models should raise ValueError when GROQ_API_KEY is not set."""
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "groq":
                with self.subTest(model=entry["name"]):
                    self._skip_if_key_present("groq")
                    import rag_pipeline as _rag_mod
                    with patch.dict(os.environ, {}, clear=True), \
                         patch.object(_rag_mod, "_GROQ_AVAILABLE", True, create=True), \
                         patch.object(_rag_mod, "_ChatGroq", MagicMock(), create=True):
                        with self.assertRaises(ValueError):
                            _rag_mod._build_llm(entry["name"])

    def test_openai_models_raise_without_key(self):
        """openai models should raise ValueError when OPENAI_API_KEY is not set."""
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "openai":
                with self.subTest(model=entry["name"]):
                    self._skip_if_key_present("openai")
                    import rag_pipeline as _rag_mod
                    with patch.dict(os.environ, {}, clear=True), \
                         patch.object(_rag_mod, "_OPENAI_AVAILABLE", True, create=True), \
                         patch.object(_rag_mod, "_ChatOpenAI", MagicMock(), create=True):
                        with self.assertRaises(ValueError):
                            _rag_mod._build_llm(entry["name"])

    def test_anthropic_models_raise_without_key(self):
        """anthropic models should raise ValueError when ANTHROPIC_API_KEY is not set."""
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "anthropic":
                with self.subTest(model=entry["name"]):
                    self._skip_if_key_present("anthropic")
                    import rag_pipeline as _rag_mod
                    with patch.dict(os.environ, {}, clear=True), \
                         patch.object(_rag_mod, "_ANTHROPIC_AVAILABLE", True, create=True), \
                         patch.object(_rag_mod, "_ChatAnthropic", MagicMock(), create=True):
                        with self.assertRaises(ValueError):
                            _rag_mod._build_llm(entry["name"])

    def test_google_models_raise_without_key(self):
        """google models should raise ValueError when GOOGLE_API_KEY is not set."""
        for entry in MODEL_REGISTRY:
            if entry["provider"] == "google":
                with self.subTest(model=entry["name"]):
                    self._skip_if_key_present("google")
                    import rag_pipeline as _rag_mod
                    with patch.dict(os.environ, {}, clear=True), \
                         patch.object(_rag_mod, "_GOOGLE_AVAILABLE", True, create=True), \
                         patch.object(_rag_mod, "_ChatGoogleGenerativeAI", MagicMock(), create=True):
                        with self.assertRaises(ValueError):
                            _rag_mod._build_llm(entry["name"])


# ═══════════════════════════════════════════════════════════════════════════════
#  6.  Model availability check helper
# ═══════════════════════════════════════════════════════════════════════════════

class TestModelAvailabilityHelper(unittest.TestCase):
    """
    ResearchEvaluator._is_model_available must exist and return a bool
    for every model name in MODEL_REGISTRY.
    """

    def test_is_model_available_returns_bool_for_all_models(self):
        from research_evaluator import ResearchEvaluator
        for entry in MODEL_REGISTRY:
            with self.subTest(model=entry["name"]):
                # Method should not raise and must return a bool
                result = ResearchEvaluator._is_model_available(entry["name"])
                self.assertIsInstance(
                    result, bool,
                    f"_is_model_available('{entry['name']}') returned non-bool: {result!r}",
                )

    def test_is_model_available_unknown_returns_false(self):
        from research_evaluator import ResearchEvaluator
        result = ResearchEvaluator._is_model_available("__no_such_model_xyz__")
        self.assertFalse(result)


# ═══════════════════════════════════════════════════════════════════════════════
#  7.  TEST_QUERIES consistency with model metadata
# ═══════════════════════════════════════════════════════════════════════════════

class TestQueryDataset(unittest.TestCase):
    """Sanity checks on TEST_QUERIES used by the evaluator."""

    def test_test_queries_non_empty(self):
        self.assertGreater(len(TEST_QUERIES), 0)

    def test_every_query_has_required_fields(self):
        required = {"id", "query", "expected_topic", "expected_mode"}
        for q in TEST_QUERIES:
            with self.subTest(query_id=q.get("id", "<no id>")):
                missing = required - q.keys()
                self.assertFalse(
                    missing,
                    f"Query '{q.get('id')}' is missing fields: {missing}",
                )

    def test_query_ids_are_unique(self):
        ids = [q["id"] for q in TEST_QUERIES]
        duplicates = {i for i in ids if ids.count(i) > 1}
        self.assertFalse(duplicates, f"Duplicate query IDs: {duplicates}")

    def test_query_strings_are_non_empty_or_intentional(self):
        """
        Every query string must be a string.  Intentionally blank queries
        (whitespace-only, used to test empty-input handling) are permitted
        when the entry has 'conversation_reset': True or expected_topic is None.
        """
        for q in TEST_QUERIES:
            with self.subTest(query_id=q["id"]):
                self.assertIsInstance(q["query"], str,
                                      f"Query '{q['id']}' has non-string query field")
                is_blank = not q["query"].strip()
                is_intentional_blank = is_blank and (
                    q.get("conversation_reset") is True
                    or q.get("expected_topic") is None
                )
                if is_blank and not is_intentional_blank:
                    self.fail(
                        f"Query '{q['id']}' has unexpectedly empty query string"
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
