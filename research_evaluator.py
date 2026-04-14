"""
research_evaluator.py
---------------------
Research evaluation system for the SLM-with-RAG Educational QA pipeline.

Runs the full RAG pipeline across multiple models, retrieval modes, and
embedding models using the structured TEST_QUERIES test suite defined in
research_config.py and writes per-query results plus aggregate statistics
to RESULTS_FILE.

Usage:
    # List all embeddings:
    python research_evaluator.py --list-embeddings

    # Single run (phi3 + bge-small + hybrid):
    python research_evaluator.py --mode single

    # Single run with specific embedding:
    python research_evaluator.py --mode single --model phi3 --embedding bge-base

    # Compare all embeddings (phi3 + hybrid):
    python research_evaluator.py --mode embedding_comparison --model phi3

    # Compare all models (bge-small + hybrid):
    python research_evaluator.py --mode model_comparison --embedding bge-small

    # Full matrix (all models x all embeddings):
    python research_evaluator.py --mode full_matrix

    # Everything:
    python research_evaluator.py --mode full

    # Results → research_results.txt (appended on each run)
"""

from __future__ import annotations

import sys
import time
import subprocess
import argparse
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path

import research_config as _rc
from research_config import (
    ALL_MODELS,
    MODELS_TO_EVALUATE,
    RETRIEVAL_MODES,
    RESULTS_FILE,
    ABLATION_RESULTS_FILE,
    MODEL_COMPARISON_FILE,
    EMBEDDING_COMPARISON_FILE,
    FULL_MATRIX_FILE,
    TOKEN_COMPARISON_FILE,
    SLM_VS_LLM_FILE,
    TEST_QUERIES,
    EMBEDDING_MODELS,
    DEFAULT_EMBEDDING,
)
from retriever import build_vector_store
from rag_pipeline import RAGPipeline
from context_memory import ConversationMemory
from topic_memory_manager import TopicMemoryManager


# ── Model config helpers ──────────────────────────────────────────────────────
#
# All model metadata (type, provider, cost rates) is sourced from
# research_config.MODEL_REGISTRY so that Groq and any future providers are
# automatically included without duplicating data here.
#
# get_model_config() returns a normalised dict that maps the research_config
# key names (cost_per_1k_input_tokens / cost_per_1k_output_tokens) to the
# shorter names used by existing callers in this module
# (input_cost_per_1k / output_cost_per_1k).

MIN_ACCURACY: float = 0.0  # Threshold constant — not a table value


def _is_configured_secret(value: str | None) -> bool:
    v = (value or "").strip()
    if not v:
        return False
    lowered = v.lower()
    return not any(x in lowered for x in ("replace_with", "your_", "example", "placeholder"))


def get_model_config(model: str) -> dict | None:
    """Return metadata for *model* sourced from research_config.MODEL_REGISTRY.

    Returns a dict with keys: type, provider, input_cost_per_1k,
    output_cost_per_1k (and any other fields present in the registry).
    Returns None if the model is not found.
    """
    entry = _rc.get_model_config(model)
    if entry is None:
        return None
    # Expose cost fields under the short aliases expected by callers here.
    return {
        **entry,
        "input_cost_per_1k":  entry.get("cost_per_1k_input_tokens",  0.0),
        "output_cost_per_1k": entry.get("cost_per_1k_output_tokens", 0.0),
    }


# ── QueryResult dataclass ─────────────────────────────────────────────────────

@dataclass
class QueryResult:
    """Container for the outcome of evaluating one test query."""

    query_id: str
    category: str
    query: str
    model: str
    retrieval_mode: str
    expected_topic: str | None
    actual_topic: str | None
    topic_correct: bool
    expected_mode: str
    actual_mode: str
    mode_correct: bool
    rewritten_query: str
    answer: str
    answer_length: int
    keyword_hits: int
    keyword_total: int
    keyword_coverage: float
    latency_ms: float
    metrics: dict
    note: str = ""
    error: str = ""
    # Embedding support: track which embedding was used
    embedding_name: str = DEFAULT_EMBEDDING
    # Token tracking: populated from pipeline token_counts
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    hallucination_rate: float = 0.0


# ── ResearchEvaluator ─────────────────────────────────────────────────────────

class ResearchEvaluator:
    """
    Orchestrates a single (model, retrieval_mode, embedding_name) experiment.

    Builds the vector store once for the given embedding, creates a
    RAGPipeline, then runs every query in TEST_QUERIES while managing
    ConversationMemory and TopicMemoryManager according to each query's
    ``conversation_reset`` flag.
    """

    def __init__(
        self,
        model: str,
        retrieval_mode: str,
        embedding_name: str = DEFAULT_EMBEDDING,
    ) -> None:
        # Embedding support: build vector store for this specific embedding
        vector_store = build_vector_store(embedding_name=embedding_name)
        self.pipeline = RAGPipeline(
            vector_store,
            model_name=model,
            retrieval_mode=retrieval_mode,
        )
        self.model = model
        self.retrieval_mode = retrieval_mode
        self.embedding_name = embedding_name
        self.results: list[QueryResult] = []

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _check_keywords(
        answer: str,
        keywords: list[str],
    ) -> tuple[int, int, float]:
        """Case-insensitive substring keyword check.

        Returns:
            (hits, total, coverage_ratio) where coverage_ratio is in [0, 1].
            If keywords is empty, returns (0, 0, 1.0).
            If answer is empty and keywords is non-empty, returns (0, len, 0.0).
        """
        if not keywords:
            return (0, 0, 1.0)
        if not answer:
            return (0, len(keywords), 0.0)
        answer_lower = answer.lower()
        hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
        return (hits, len(keywords), hits / len(keywords))

    @staticmethod
    def _is_model_available(model_name: str) -> bool:
        """Return True if *model_name* is available.

        - For Groq models (provider="groq"): checks that GROQ_API_KEY is set.
        - For OpenAI models (provider="openai"): checks OPENAI_API_KEY.
        - For Anthropic models (provider="anthropic"): checks ANTHROPIC_API_KEY.
        - For Google models (provider="google"): checks GOOGLE_API_KEY.
        - For Ollama models: checks ``ollama list`` output.
        """
        import os as _os
        cfg = get_model_config(model_name) or {}
        provider = cfg.get("provider", "ollama")
        if provider == "groq":
            return _is_configured_secret(_os.environ.get("GROQ_API_KEY", ""))
        if provider == "openai":
            return _is_configured_secret(_os.environ.get("OPENAI_API_KEY", ""))
        if provider == "anthropic":
            return _is_configured_secret(_os.environ.get("ANTHROPIC_API_KEY", ""))
        if provider == "google":
            return _is_configured_secret(_os.environ.get("GOOGLE_API_KEY", ""))
        # Default: Ollama — check ollama list
        try:
            proc = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return model_name in proc.stdout
        except Exception:
            return False

    # ── Core query runner ─────────────────────────────────────────────────────

    def run_single_query(
        self,
        query_config: dict,
        memory: ConversationMemory,
        topic_manager: TopicMemoryManager,
    ) -> QueryResult:
        """
        Run the pipeline for one test query and return a QueryResult.

        Handles all edge cases:
        - Whitespace / empty query → error="EMPTY QUERY", latency_ms=0.
        - ConnectionRefusedError → error="OLLAMA NOT RUNNING", latency_ms=0.
        - Any other exception → error=str(e), answer="PIPELINE ERROR", latency_ms=0.
        - expected_topic=None and actual_topic=None → topic_correct=True.
        - expected_topic=None and actual_topic has value → topic_correct=False.
        - keywords=[] → keyword_coverage=1.0.
        - answer="" with non-empty keywords → keyword_coverage=0.0.
        """
        qid = query_config["id"]
        category = query_config["category"]
        query = query_config["query"]
        expected_topic: str | None = query_config.get("expected_topic")
        expected_mode: str = query_config.get("expected_mode", "RAG")
        expected_keywords: list[str] = query_config.get("expected_keywords", [])
        note: str = query_config.get("note", "")

        print(f"  [{qid}] {category}: '{query[:50]}'", end="", flush=True)

        # ── Edge case 1: whitespace / empty query ─────────────────────────────
        if not query.strip():
            topic_correct = (expected_topic is None)
            print(f" → LLM Fallback | topic=None | 0ms")
            return QueryResult(
                query_id=qid, category=category, query=query,
                model=self.model, retrieval_mode=self.retrieval_mode,
                expected_topic=expected_topic, actual_topic=None,
                topic_correct=topic_correct,
                expected_mode=expected_mode, actual_mode="LLM Fallback",
                mode_correct=(expected_mode == "LLM Fallback"),
                rewritten_query="", answer="", answer_length=0,
                keyword_hits=0, keyword_total=len(expected_keywords),
                keyword_coverage=0.0,
                latency_ms=0.0, metrics={}, note=note,
                error="EMPTY QUERY",
                embedding_name=self.embedding_name,
            )

        # ── Run pipeline ──────────────────────────────────────────────────────
        try:
            result = self.pipeline.run(
                user_query=query,
                memory=memory,
                topic_manager=topic_manager,
            )
        except ConnectionRefusedError:
            print(f" → ERROR | topic=None | 0ms")
            return QueryResult(
                query_id=qid, category=category, query=query,
                model=self.model, retrieval_mode=self.retrieval_mode,
                expected_topic=expected_topic, actual_topic=None,
                topic_correct=False,
                expected_mode=expected_mode, actual_mode="ERROR",
                mode_correct=False,
                rewritten_query="", answer="PIPELINE ERROR", answer_length=14,
                keyword_hits=0, keyword_total=len(expected_keywords),
                keyword_coverage=0.0,
                latency_ms=0.0, metrics={}, note=note,
                error="OLLAMA NOT RUNNING",
                embedding_name=self.embedding_name,
            )
        except Exception as exc:
            print(f" → ERROR | topic=None | 0ms")
            return QueryResult(
                query_id=qid, category=category, query=query,
                model=self.model, retrieval_mode=self.retrieval_mode,
                expected_topic=expected_topic, actual_topic=None,
                topic_correct=False,
                expected_mode=expected_mode, actual_mode="ERROR",
                mode_correct=False,
                rewritten_query="", answer="PIPELINE ERROR", answer_length=14,
                keyword_hits=0, keyword_total=len(expected_keywords),
                keyword_coverage=0.0,
                latency_ms=0.0, metrics={}, note=note,
                error=str(exc),
                embedding_name=self.embedding_name,
            )

        # ── Extract fields from pipeline result ───────────────────────────────
        actual_topic: str | None = result.detected_topic
        actual_mode: str = result.mode
        latency_ms: float = result.latency_ms
        answer: str = result.answer

        # ── Topic correctness ─────────────────────────────────────────────────
        if expected_topic is None and actual_topic is None:
            topic_correct = True
        elif expected_topic is None:
            # expected None but got a topic → incorrect
            topic_correct = False
        else:
            # Flexible match: either direction substring match (case-insensitive)
            topic_correct = (
                actual_topic is not None
                and (
                    expected_topic.lower() in actual_topic.lower()
                    or actual_topic.lower() in expected_topic.lower()
                )
            )

        # ── Mode correctness ──────────────────────────────────────────────────
        # Normalise pipeline "Out of Scope" mode to "LLM Fallback" for comparison
        normalised_actual_mode = (
            "LLM Fallback" if actual_mode == "Out of Scope" else actual_mode
        )
        mode_correct = (normalised_actual_mode == expected_mode)

        # ── Keyword analysis ──────────────────────────────────────────────────
        hits, total, coverage = self._check_keywords(answer, expected_keywords)

        # ── Token counts from pipeline ────────────────────────────────────────
        tc = result.token_counts  # {"input_tokens": int, "output_tokens": int, "total_tokens": int}
        input_tokens: int = tc.get("input_tokens", 0)
        output_tokens: int = tc.get("output_tokens", 0)
        total_tokens: int = tc.get("total_tokens", input_tokens + output_tokens)

        # Estimated cost derived from MODEL_REGISTRY rates (0.0 for local models)
        cfg = get_model_config(self.model) or {}
        input_rate = cfg.get("input_cost_per_1k", cfg.get("cost_per_1k_input_tokens", 0.0))
        output_rate = cfg.get("output_cost_per_1k", cfg.get("cost_per_1k_output_tokens", 0.0))
        estimated_cost_usd: float = (
            input_tokens * input_rate / 1000.0
            + output_tokens * output_rate / 1000.0
        )
        faithfulness = float(result.metrics.get("Faithfulness", 0.0))
        hallucination_rate = max(0.0, min(1.0, 1.0 - faithfulness))

        print(f" → {actual_mode} | topic={actual_topic} | {latency_ms:.0f}ms")

        return QueryResult(
            query_id=qid, category=category, query=query,
            model=self.model, retrieval_mode=self.retrieval_mode,
            expected_topic=expected_topic, actual_topic=actual_topic,
            topic_correct=topic_correct,
            expected_mode=expected_mode, actual_mode=actual_mode,
            mode_correct=mode_correct,
            rewritten_query=result.rewritten_query,
            answer=answer, answer_length=len(answer),
            keyword_hits=hits, keyword_total=total,
            keyword_coverage=coverage,
            latency_ms=latency_ms, metrics=result.metrics,
            note=note, error="",
            embedding_name=self.embedding_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=estimated_cost_usd,
            hallucination_rate=hallucination_rate,
        )

    # ── Experiment runner ─────────────────────────────────────────────────────

    def run_experiment(self) -> list[QueryResult]:
        """
        Run all TEST_QUERIES and return the list of QueryResult objects.

        Manages ConversationMemory and TopicMemoryManager resets according
        to each query's ``conversation_reset`` flag.
        """
        self.results = []
        memory: ConversationMemory | None = None
        topic_manager: TopicMemoryManager | None = None
        last_category: str | None = None

        for query_config in TEST_QUERIES:
            if query_config.get("conversation_reset", True) or memory is None:
                memory = ConversationMemory(max_turns=5)
                topic_manager = TopicMemoryManager()

            category = query_config["category"]
            if category != last_category:
                print(f"\n── {category.upper()} ──────────────────")
                last_category = category

            result = self.run_single_query(
                query_config,
                memory,
                topic_manager,  # type: ignore[arg-type]
            )
            self.results.append(result)

        return self.results

    # ── Summary computation ───────────────────────────────────────────────────

    def compute_summary(self) -> dict:
        """
        Compute aggregate statistics over self.results.

        Errored queries are excluded from metric averages but counted
        in failed_queries.  Returns all-zero dict if results is empty.
        """
        if not self.results:
            return {
                "total_queries": 0,
                "successful_queries": 0,
                "failed_queries": 0,
                "topic_accuracy": 0.0,
                "mode_accuracy": 0.0,
                "avg_keyword_coverage": 0.0,
                "avg_latency_ms": 0.0,
                "avg_hallucination_rate": 0.0,
                "avg_metrics": {},
                "rag_count": 0,
                "partial_rag_count": 0,
                "fallback_count": 0,
                "per_category": {},
            }

        total = len(self.results)
        errored = [r for r in self.results if r.error]
        successful = [r for r in self.results if not r.error]

        if successful:
            topic_accuracy = (
                sum(1 for r in successful if r.topic_correct) / len(successful)
            )
            mode_accuracy = (
                sum(1 for r in successful if r.mode_correct) / len(successful)
            )
            avg_keyword_coverage = (
                sum(r.keyword_coverage for r in successful) / len(successful)
            )
            avg_latency_ms = (
                sum(r.latency_ms for r in successful) / len(successful)
            )
            avg_hallucination_rate = (
                sum(r.hallucination_rate for r in successful) / len(successful)
            )
        else:
            topic_accuracy = mode_accuracy = avg_keyword_coverage = avg_latency_ms = 0.0
            avg_hallucination_rate = 0.0

        # Average evaluation metrics
        all_metric_keys: set[str] = set()
        for r in successful:
            all_metric_keys.update(r.metrics.keys())

        avg_metrics: dict[str, float] = {}
        for key in sorted(all_metric_keys):
            vals = [r.metrics[key] for r in successful if key in r.metrics]
            avg_metrics[key] = round(sum(vals) / len(vals), 3) if vals else 0.0

        # Mode counts across ALL results (including errors shown as "ERROR")
        rag_count = sum(1 for r in self.results if r.actual_mode == "RAG")
        partial_rag_count = sum(
            1 for r in self.results if r.actual_mode == "Partial RAG"
        )
        fallback_count = sum(
            1 for r in self.results
            if r.actual_mode in ("LLM Fallback", "Out of Scope")
        )

        # Per-category breakdown (skip errored rows from accuracy denominators)
        categories: dict[str, list[QueryResult]] = {}
        for r in self.results:
            categories.setdefault(r.category, []).append(r)

        per_category: dict[str, dict] = {}
        for cat, rows in categories.items():
            ok = [r for r in rows if not r.error]
            per_category[cat] = {
                "count": len(rows),
                "topic_accuracy": round(
                    sum(1 for r in ok if r.topic_correct) / len(ok), 3
                ) if ok else 0.0,
                "mode_accuracy": round(
                    sum(1 for r in ok if r.mode_correct) / len(ok), 3
                ) if ok else 0.0,
                "avg_keyword_coverage": round(
                    sum(r.keyword_coverage for r in ok) / len(ok), 3
                ) if ok else 0.0,
                "avg_latency_ms": round(
                    sum(r.latency_ms for r in ok) / len(ok), 1
                ) if ok else 0.0,
                "avg_hallucination_rate": round(
                    sum(r.hallucination_rate for r in ok) / len(ok), 3
                ) if ok else 0.0,
            }

        return {
            "total_queries": total,
            "successful_queries": len(successful),
            "failed_queries": len(errored),
            "topic_accuracy": round(topic_accuracy, 4),
            "mode_accuracy": round(mode_accuracy, 4),
            "avg_keyword_coverage": round(avg_keyword_coverage, 4),
            "avg_latency_ms": round(avg_latency_ms, 1),
            "avg_hallucination_rate": round(avg_hallucination_rate, 4),
            "avg_metrics": avg_metrics,
            "rag_count": rag_count,
            "partial_rag_count": partial_rag_count,
            "fallback_count": fallback_count,
            "per_category": per_category,
        }


# ── Token summary ─────────────────────────────────────────────────────────────

def compute_token_summary(results: list[QueryResult]) -> dict:
    """
    Compute token-usage statistics from a list of QueryResult objects.

    Only non-errored results are included in averages so that pipeline
    failures do not skew token/cost numbers.

    Args:
        results: List of QueryResult objects returned by run_experiment().

    Returns:
        Dict with keys:
            total_input_tokens, total_output_tokens, total_tokens,
            avg_input_per_query, avg_output_per_query, avg_total_per_query,
            total_cost_usd, avg_cost_per_query,
            tokens_per_ms,
            min_tokens_query, max_tokens_query,
            by_mode  (dict[mode, avg_total_tokens]),
            by_category (dict[category, avg_total_tokens]).
    """
    if not results:
        return {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0,
            "avg_input_per_query": 0.0,
            "avg_output_per_query": 0.0,
            "avg_total_per_query": 0.0,
            "total_cost_usd": 0.0,
            "avg_cost_per_query": 0.0,
            "tokens_per_ms": 0.0,
            "min_tokens_query": 0,
            "max_tokens_query": 0,
            "by_mode": {},
            "by_category": {},
        }

    ok = [r for r in results if not r.error]

    total_input = sum(r.input_tokens for r in ok)
    total_output = sum(r.output_tokens for r in ok)
    total_all = sum(r.total_tokens for r in ok)
    total_cost = sum(r.estimated_cost_usd for r in ok)
    n = len(ok)

    avg_input = total_input / n if n else 0.0
    avg_output = total_output / n if n else 0.0
    avg_total = total_all / n if n else 0.0
    avg_cost = total_cost / n if n else 0.0

    total_latency_ms = sum(r.latency_ms for r in ok)
    # tokens_per_ms: average tokens produced per millisecond of pipeline time
    tokens_per_ms = (avg_total / (total_latency_ms / n)) if (n > 0 and total_latency_ms > 0) else 0.0

    min_tokens = min((r.total_tokens for r in ok), default=0)
    max_tokens = max((r.total_tokens for r in ok), default=0)

    # Per-mode breakdown
    mode_groups: dict[str, list[int]] = {}
    for r in ok:
        mode_groups.setdefault(r.actual_mode, []).append(r.total_tokens)
    by_mode = {
        mode: round(sum(vals) / len(vals), 1)
        for mode, vals in mode_groups.items()
    }

    # Per-category breakdown
    cat_groups: dict[str, list[int]] = {}
    for r in ok:
        cat_groups.setdefault(r.category, []).append(r.total_tokens)
    by_category = {
        cat: round(sum(vals) / len(vals), 1)
        for cat, vals in cat_groups.items()
    }

    return {
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_tokens": total_all,
        "avg_input_per_query": round(avg_input, 1),
        "avg_output_per_query": round(avg_output, 1),
        "avg_total_per_query": round(avg_total, 1),
        "total_cost_usd": round(total_cost, 6),
        "avg_cost_per_query": round(avg_cost, 6),
        "tokens_per_ms": round(tokens_per_ms, 4),
        "min_tokens_query": min_tokens,
        "max_tokens_query": max_tokens,
        "by_mode": by_mode,
        "by_category": by_category,
    }


# ── ResultsWriter ─────────────────────────────────────────────────────────────

class ResultsWriter:
    """
    Appends experiment results to a plain-text log file (RESULTS_FILE).

    Sections inside the file are delimited by BLOCK_MARKER lines so that
    individual experiments can be located and parsed programmatically.
    """

    BLOCK_MARKER = "<<"

    def __init__(self, filepath: str = RESULTS_FILE) -> None:
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _write_line(self, f, text: str = "") -> None:
        f.write(text + "\n")

    def _section(self, f, title: str) -> None:
        self._write_line(f, f"\n{self.BLOCK_MARKER} {title}")

    # ── Public API ────────────────────────────────────────────────────────────

    def write_experiment(
        self,
        model: str,
        retrieval_mode: str,
        results: list[QueryResult],
        summary: dict,
        embedding_name: str = DEFAULT_EMBEDDING,
    ) -> None:
        """
        Append a full experiment block (header + per-query rows + summary)
        to the results file.

        Token statistics are computed internally from *results* via
        compute_token_summary() so the caller does not need to pre-compute them.

        Args:
            model:          Ollama model name (e.g. "phi3").
            retrieval_mode: Retrieval mode used (e.g. "hybrid").
            results:        List of QueryResult objects from run_experiment().
            summary:        Summary dict from compute_summary().
            embedding_name: Embedding model name used (e.g. "bge-small").
        """
        tok = compute_token_summary(results)

        with open(self.filepath, "a", encoding="utf-8") as f:
            # ── Experiment header ─────────────────────────────────────────────
            self._write_line(f)
            self._write_line(f, "=" * 80)
            # Embedding support: include embedding in header for duplicate detection
            self._write_line(
                f,
                f"{self.BLOCK_MARKER} EXPERIMENT  model={model}"
                f"  embedding={embedding_name}"
                f"  mode={retrieval_mode}"
                f"  timestamp={datetime.now().isoformat(timespec='seconds')}",
            )
            self._write_line(f, "=" * 80)
            self._write_line(f, f"  MODEL          : {model}")
            self._write_line(f, f"  EMBEDDING      : {embedding_name}")
            self._write_line(f, f"  RETRIEVAL      : {retrieval_mode}")

            # ── Per-query results ─────────────────────────────────────────────
            self._section(f, "QUERY RESULTS")
            self._write_line(
                f,
                f"  {'ID':<6} {'CAT':<20} {'EXP_MODE':<14} {'ACT_MODE':<14}"
                f" {'T_OK':<6} {'M_OK':<6} {'KW':<6} {'LAT_MS':<8}"
                f" {'HALL':<6}"
                f" {'IN_TOK':<8} {'OUT_TOK':<9} {'TOT_TOK':<9}"
                f" {'COST_USD':<12} QUERY",
            )
            self._write_line(f, "  " + "-" * 130)
            for r in results:
                t_ok = "Y" if r.topic_correct else "N"
                m_ok = "Y" if r.mode_correct else "N"
                kw = f"{r.keyword_coverage:.2f}"
                lat = f"{r.latency_ms:.0f}"
                hall = f"{r.hallucination_rate:.2f}"
                query_snippet = r.query[:40].replace("\n", " ")
                self._write_line(
                    f,
                    f"  {r.query_id:<6} {r.category:<20} {r.expected_mode:<14}"
                    f" {r.actual_mode:<14} {t_ok:<6} {m_ok:<6} {kw:<6}"
                    f" {lat:<8} {hall:<6} {r.input_tokens:<8} {r.output_tokens:<9}"
                    f" {r.total_tokens:<9} {r.estimated_cost_usd:<12.6f}"
                    f" {query_snippet!r}",
                )
                if r.error:
                    self._write_line(f, f"         ERROR: {r.error}")

            # ── Overall summary ───────────────────────────────────────────────
            self._section(f, "SUMMARY")
            self._write_line(
                f,
                f"  total={summary['total_queries']}"
                f"  successful={summary['successful_queries']}"
                f"  failed={summary['failed_queries']}",
            )
            self._write_line(
                f,
                f"  topic_accuracy={summary['topic_accuracy']*100:.2f}%"
                f"  mode_accuracy={summary['mode_accuracy']*100:.2f}%",
            )
            self._write_line(
                f,
                f"  avg_keyword_coverage={summary['avg_keyword_coverage']:.4f}"
                f"  avg_latency={summary['avg_latency_ms']}ms"
                f"  avg_hallucination_rate={summary.get('avg_hallucination_rate', 0.0):.4f}",
            )
            self._write_line(
                f,
                f"  rag={summary['rag_count']}"
                f"  partial_rag={summary['partial_rag_count']}"
                f"  fallback={summary['fallback_count']}",
            )

            # ── Token statistics ──────────────────────────────────────────────
            self._section(f, "TOKEN STATISTICS")
            self._write_line(f, f"  Total Input Tokens     : {tok['total_input_tokens']}")
            self._write_line(f, f"  Total Output Tokens    : {tok['total_output_tokens']}")
            self._write_line(f, f"  Total Tokens           : {tok['total_tokens']}")
            self._write_line(f, f"  Avg Input Per Query    : {tok['avg_input_per_query']:.1f}")
            self._write_line(f, f"  Avg Output Per Query   : {tok['avg_output_per_query']:.1f}")
            self._write_line(f, f"  Avg Total Per Query    : {tok['avg_total_per_query']:.1f}")
            self._write_line(f, f"  Total Cost             : ${tok['total_cost_usd']:.6f}")
            self._write_line(f, f"  Avg Cost Per Query     : ${tok['avg_cost_per_query']:.6f}")
            self._write_line(f, f"  Tokens Per Ms          : {tok['tokens_per_ms']:.4f}")

            # ── Evaluation metrics ────────────────────────────────────────────
            if summary.get("avg_metrics"):
                self._section(f, "AVG EVALUATION METRICS")
                for metric, value in summary["avg_metrics"].items():
                    self._write_line(f, f"  {metric}: {value:.3f}")

            # ── Per-category breakdown ────────────────────────────────────────
            self._section(f, "PER CATEGORY")
            self._write_line(
                f,
                f"  {'CATEGORY':<22} {'N':<5} {'TOPIC_ACC':<12}"
                f" {'MODE_ACC':<10} {'KW_COV':<8} {'LAT_MS':<8} {'HALL'}",
            )
            self._write_line(f, "  " + "-" * 70)
            for cat, stats in summary.get("per_category", {}).items():
                self._write_line(
                    f,
                    f"  {cat:<22} {stats['count']:<5}"
                    f" {stats['topic_accuracy']*100:<12.1f}"
                    f" {stats['mode_accuracy']*100:<10.1f}"
                    f" {stats['avg_keyword_coverage']:<8.3f}"
                    f" {stats['avg_latency_ms']:<8.1f}"
                    f" {stats.get('avg_hallucination_rate', 0.0):.3f}",
                )

            self._write_line(f, "=" * 80)

    def write(
        self,
        model: str,
        retrieval_mode: str,
        results: list[QueryResult],
        summary: dict,
        embedding_name: str = DEFAULT_EMBEDDING,
    ) -> None:
        """
        Alias for write_experiment() for a more concise call-site.

        Args:
            model:          Ollama model name (e.g. "phi3").
            retrieval_mode: Retrieval mode used (e.g. "hybrid").
            results:        List of QueryResult objects from run_experiment().
            summary:        Summary dict from compute_summary().
            embedding_name: Embedding model name used (e.g. "bge-small").
        """
        self.write_experiment(
            model=model,
            retrieval_mode=retrieval_mode,
            results=results,
            summary=summary,
            embedding_name=embedding_name,
        )

    def write_run_header(self, models: list[str], modes: list[str]) -> None:
        """Write a top-level header for a full evaluation run."""
        with open(self.filepath, "a", encoding="utf-8") as f:
            self._write_line(f)
            self._write_line(f, "#" * 80)
            self._write_line(
                f,
                f"{self.BLOCK_MARKER} RESEARCH RUN"
                f"  started={datetime.now().isoformat(timespec='seconds')}",
            )
            self._write_line(f, f"  models={models}")
            self._write_line(f, f"  retrieval_modes={modes}")
            self._write_line(f, "#" * 80)

    def write_comparison_table(
        self,
        title: str,
        headers: list[str],
        rows: list[list[str]],
        footer_lines: list[str] | None = None,
    ) -> None:
        """
        Append a formatted comparison table to the results file.

        Writes a section header, a column-header row, divider lines, data rows,
        and optional footer lines (winners / summary).  This captures the
        aggregated comparison output that is also printed to stdout so that the
        file is self-contained.

        Args:
            title:        Section title (e.g. "MODEL COMPARISON").
            headers:      Column header strings.
            rows:         Data rows — each a list of pre-formatted strings.
            footer_lines: Optional list of summary/winner lines.
        """
        with open(self.filepath, "a", encoding="utf-8") as f:
            self._section(f, title)
            header_line = "  " + " | ".join(headers)
            divider_width = max(len(header_line), 80)
            self._write_line(f, header_line)
            self._write_line(f, "  " + "-" * divider_width)
            for row in rows:
                self._write_line(f, "  " + " | ".join(row))
            self._write_line(f, "  " + "=" * divider_width)
            if footer_lines:
                for line in footer_lines:
                    self._write_line(f, f"  {line}")



# ── High-level experiment runners ─────────────────────────────────────────────

def run_single_model_experiment(
    model: str = "groq-llama3-8b",
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = RESULTS_FILE,
) -> dict:
    """
    Run a single (model, retrieval_mode, embedding_name) experiment.

    Builds the vector store for *embedding_name*, runs all TEST_QUERIES,
    saves results to *output*, and returns the summary dict.

    Args:
        model:          Ollama model name (e.g. "phi3").
        retrieval_mode: Retrieval mode (e.g. "hybrid").
        embedding_name: Embedding model to use (e.g. "bge-small").
        output:         Path to the results file.

    Returns:
        Summary dict from compute_summary().
    """
    print(f"\n{'=' * 60}")
    print(f"  Model: {model}  |  Embedding: {embedding_name}  |  Retrieval: {retrieval_mode}")
    print(f"{'=' * 60}")

    evaluator = ResearchEvaluator(
        model=model,
        retrieval_mode=retrieval_mode,
        embedding_name=embedding_name,
    )
    results = evaluator.run_experiment()
    summary = evaluator.compute_summary()

    writer = ResultsWriter(filepath=output)
    writer.write_experiment(
        model=model,
        retrieval_mode=retrieval_mode,
        results=results,
        summary=summary,
        embedding_name=embedding_name,
    )

    print(f"\n  ✓ Results appended to {output}")
    print(
        f"  topic_accuracy={summary['topic_accuracy']*100:.2f}%"
        f"  mode_accuracy={summary['mode_accuracy']*100:.2f}%"
        f"  avg_latency={summary['avg_latency_ms']}ms"
        f"  hallucination_rate={summary.get('avg_hallucination_rate', 0.0)*100:.2f}%"
    )
    return summary


def run_ablation_study(
    model: str = "groq-llama3-8b",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = ABLATION_RESULTS_FILE,
) -> None:
    """
    Run *model* across all retrieval modes with the given *embedding_name*.

    This is the ablation study: same model and embedding, varying retrieval.
    Prints a comparison table derived entirely from real experiment results
    and writes it to *output* (default: ablation_results.txt).

    Args:
        model:          Model name (Ollama or Groq).
        embedding_name: Embedding model key (e.g. "bge-small").
        output:         Path to the results file (default: ablation_results.txt).
    """
    print(f"\n{'═' * 60}")
    print(f"  ABLATION STUDY — Model: {model} | Embedding: {embedding_name}")
    print(f"  Retrieval modes: {RETRIEVAL_MODES}")
    print(f"{'═' * 60}")

    if not ResearchEvaluator._is_model_available(model):
        print(f"  [Skip] Model '{model}' not available.")
        return

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=[model], modes=RETRIEVAL_MODES)

    # STEP 1 — Run experiments and collect real results
    summaries: dict[str, dict] = {}
    token_summaries: dict[str, dict] = {}
    ran_modes: list[str] = []

    for mode in RETRIEVAL_MODES:
        evaluator = ResearchEvaluator(
            model=model,
            retrieval_mode=mode,
            embedding_name=embedding_name,
        )
        results = evaluator.run_experiment()
        summaries[mode] = evaluator.compute_summary()
        token_summaries[mode] = compute_token_summary(results)
        writer.write(
            model=model,
            retrieval_mode=mode,
            results=results,
            summary=summaries[mode],
            embedding_name=embedding_name,
        )
        ran_modes.append(mode)

    if not ran_modes:
        return

    # STEP 2 — Determine winners using real data
    best_acc_mode = max(ran_modes, key=lambda m: summaries[m]["topic_accuracy"])
    fastest_mode = min(ran_modes, key=lambda m: summaries[m]["avg_latency_ms"])

    # STEP 3 — Build comparison rows
    col_headers = [
        f"{'Mode':<14}", f"{'TopicAcc':>8}", f"{'ModeAcc':>7}",
        f"{'KwCov':>6}", f"{'Lat':>8}", f"{'Hall':>7}", f"{'AvgInTok':>8}",
        f"{'AvgOutTok':>9}", f"{'AvgTotTok':>9}", f"{'AvgCost':>12}",
    ]
    table_rows: list[list[str]] = []
    for mode in ran_modes:
        s = summaries[mode]
        t = token_summaries[mode]
        table_rows.append([
            f"{mode:<14}",
            f"{s['topic_accuracy']*100:>7.1f}%",
            f"{s['mode_accuracy']*100:>6.1f}%",
            f"{s['avg_keyword_coverage']:>6.3f}",
            f"{s['avg_latency_ms']:>6.0f}ms",
            f"{s.get('avg_hallucination_rate', 0.0)*100:>6.1f}%",
            f"{t['avg_input_per_query']:>8.0f}",
            f"{t['avg_output_per_query']:>9.0f}",
            f"{t['avg_total_per_query']:>9.0f}",
            f"${t['avg_cost_per_query']:>11.6f}",
        ])

    footer_lines = [
        f"Winner (Accuracy) : {best_acc_mode} ({summaries[best_acc_mode]['topic_accuracy']*100:.1f}%)",
        f"Winner (Speed)    : {fastest_mode} ({summaries[fastest_mode]['avg_latency_ms']:.0f}ms)",
        f"Results saved to  : {output}",
    ]

    # STEP 4 — Print to stdout
    print(f"\n{'═' * 60} ABLATION RESULTS {'═' * 3}")
    print(f"  Model: {model} | Embedding: {embedding_name}")
    print(f"  {'─' * 76}")
    print("  " + " | ".join(col_headers))
    print(f"  {'─' * 76}")
    for row in table_rows:
        print("  " + " | ".join(row))
    print(f"  {'═' * 76}")
    for line in footer_lines:
        print(f"  {line}")
    print(f"{'═' * 80}")

    # STEP 5 — Write comparison table to file
    writer.write_comparison_table(
        title=f"ABLATION COMPARISON  model={model}  embedding={embedding_name}",
        headers=col_headers,
        rows=table_rows,
        footer_lines=footer_lines,
    )


def run_model_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = MODEL_COMPARISON_FILE,
) -> None:
    """
    Run all models with the given *retrieval_mode* and *embedding_name*.

    Skips models that are not available (Ollama not installed or API key missing).
    Prints a comparison table derived entirely from real experiment results and
    writes it to *output* (default: model_comparison_results.txt).

    Args:
        retrieval_mode: Retrieval mode to use for all models.
        embedding_name: Embedding model key.
        output:         Path to the results file (default: model_comparison_results.txt).
    """
    print(f"\n{'═' * 60}")
    print(f"  MODEL COMPARISON — Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {MODELS_TO_EVALUATE}")
    print(f"{'═' * 60}")

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=MODELS_TO_EVALUATE, modes=[retrieval_mode])

    # STEP 1 — Run experiments and collect real results
    summaries: dict[str, dict] = {}
    token_summaries: dict[str, dict] = {}
    ran_models: list[str] = []

    for model in MODELS_TO_EVALUATE:
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available.")
            continue
        evaluator = ResearchEvaluator(
            model=model,
            retrieval_mode=retrieval_mode,
            embedding_name=embedding_name,
        )
        results = evaluator.run_experiment()
        summaries[model] = evaluator.compute_summary()
        token_summaries[model] = compute_token_summary(results)
        writer.write(
            model=model,
            retrieval_mode=retrieval_mode,
            results=results,
            summary=summaries[model],
            embedding_name=embedding_name,
        )
        ran_models.append(model)

    if not ran_models:
        return

    # STEP 2 — Determine winners using real data
    best_accuracy_model = max(ran_models, key=lambda m: summaries[m]["topic_accuracy"])
    fastest_model = min(ran_models, key=lambda m: summaries[m]["avg_latency_ms"])

    # STEP 3 — Build comparison rows
    col_headers = [
        f"{'Model':<16}", f"{'Type':<4}", f"{'TopicAcc':>8}", f"{'ModeAcc':>7}",
        f"{'KwCov':>6}", f"{'Lat':>8}", f"{'Hall':>7}", f"{'AvgInTok':>8}",
        f"{'AvgOutTok':>9}", f"{'AvgTotTok':>9}", f"{'AvgCost':>12}",
    ]
    table_rows: list[list[str]] = []
    for model in ran_models:
        s = summaries[model]
        t = token_summaries[model]
        cfg = get_model_config(model) or {}
        table_rows.append([
            f"{model:<16}",
            f"{cfg.get('type','?'):<4}",
            f"{s['topic_accuracy']*100:>7.1f}%",
            f"{s['mode_accuracy']*100:>6.1f}%",
            f"{s['avg_keyword_coverage']:>6.3f}",
            f"{s['avg_latency_ms']:>6.0f}ms",
            f"{s.get('avg_hallucination_rate', 0.0)*100:>6.1f}%",
            f"{t['avg_input_per_query']:>8.0f}",
            f"{t['avg_output_per_query']:>9.0f}",
            f"{t['avg_total_per_query']:>9.0f}",
            f"${t['avg_cost_per_query']:>11.6f}",
        ])

    footer_lines = [
        f"Winner (Accuracy) : {best_accuracy_model} ({summaries[best_accuracy_model]['topic_accuracy']*100:.1f}%)",
        f"Winner (Speed)    : {fastest_model} ({summaries[fastest_model]['avg_latency_ms']:.0f}ms)",
        f"Results saved to  : {output}",
    ]

    # STEP 4 — Print to stdout
    print(f"\n{'═' * 60} MODEL COMPARISON {'═' * 3}")
    print(f"  Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  {'─' * 84}")
    print("  " + " | ".join(col_headers))
    print(f"  {'─' * 84}")
    for row in table_rows:
        print("  " + " | ".join(row))
    print(f"  {'═' * 84}")
    for line in footer_lines:
        print(f"  {line}")
    print(f"{'═' * 80}")

    # STEP 5 — Write comparison table to file
    writer.write_comparison_table(
        title=f"MODEL COMPARISON  retrieval={retrieval_mode}  embedding={embedding_name}",
        headers=col_headers,
        rows=table_rows,
        footer_lines=footer_lines,
    )


def run_embedding_comparison(
    model: str = "groq-llama3-8b",
    retrieval_mode: str = "hybrid",
    output: str = EMBEDDING_COMPARISON_FILE,
) -> None:
    """
    Run TEST_QUERIES with every embedding in EMBEDDING_MODELS.

    Uses the given *model* and *retrieval_mode* for all embeddings so results
    are directly comparable.  Prints a summary comparison table derived from
    real experiment results at the end and writes it to *output*
    (default: embedding_comparison_results.txt).

    Args:
        model:          Model name (Ollama or Groq).
        retrieval_mode: Retrieval mode.
        output:         Path to the results file (default: embedding_comparison_results.txt).
    """
    print(f"\n{'═' * 56}")
    print(f"  EMBEDDING COMPARISON")
    print(f"  Model: {model} | Retrieval: {retrieval_mode}")
    print(f"  Testing {len(EMBEDDING_MODELS)} embeddings")
    print(f"{'═' * 56}")

    if not ResearchEvaluator._is_model_available(model):
        print(f"  [Skip] Model '{model}' not available.")
        return

    writer = ResultsWriter(filepath=output)

    # STEP 1 — Run experiments and collect real results
    summaries: dict[str, dict] = {}
    token_summaries: dict[str, dict] = {}
    emb_dims: dict[str, int] = {}
    ran_embeddings: list[str] = []

    for emb in EMBEDDING_MODELS:
        name = emb["name"]
        desc = emb["description"]
        dim = emb["dimension"]

        print(f"\nTesting embedding: {name} ({desc})")
        print(f"Building vector store for {name}...")

        try:
            evaluator = ResearchEvaluator(
                model=model,
                retrieval_mode=retrieval_mode,
                embedding_name=name,
            )
        except (OSError, ConnectionError) as exc:
            print(f"  Failed to load {name}: {exc}. Skipping.")
            continue

        results = evaluator.run_experiment()
        summaries[name] = evaluator.compute_summary()
        token_summaries[name] = compute_token_summary(results)
        emb_dims[name] = dim

        writer.write(
            model=model,
            retrieval_mode=retrieval_mode,
            results=results,
            summary=summaries[name],
            embedding_name=name,
        )
        ran_embeddings.append(name)

    if not ran_embeddings:
        return

    # STEP 2 — Determine winners using real data
    best_acc_emb = max(
        ran_embeddings,
        key=lambda e: summaries[e]["topic_accuracy"] + summaries[e]["mode_accuracy"],
    )
    fastest_emb = min(ran_embeddings, key=lambda e: summaries[e]["avg_latency_ms"])
    best_ratio_emb = max(
        ran_embeddings,
        key=lambda e: (
            (summaries[e]["topic_accuracy"] + summaries[e]["mode_accuracy"])
            / max(summaries[e]["avg_latency_ms"], 1)
        ),
    )

    # STEP 3 — Build comparison rows
    col_headers = [
        f"{'Embedding':<20}", f"{'Dim':<5}", f"{'TopicAcc':>8}", f"{'ModeAcc':>7}",
        f"{'KwCov':>6}", f"{'Lat':>8}", f"{'Hall':>7}", f"{'AvgInTok':>8}",
        f"{'AvgOutTok':>9}", f"{'AvgTotTok':>9}", f"{'AvgCost':>12}",
    ]
    table_rows: list[list[str]] = []
    for name in ran_embeddings:
        s = summaries[name]
        t = token_summaries[name]
        table_rows.append([
            f"{name:<20}",
            f"{emb_dims[name]:<5}",
            f"{s['topic_accuracy']*100:>7.1f}%",
            f"{s['mode_accuracy']*100:>6.1f}%",
            f"{s['avg_keyword_coverage']:>6.3f}",
            f"{s['avg_latency_ms']:>6.0f}ms",
            f"{s.get('avg_hallucination_rate', 0.0)*100:>6.1f}%",
            f"{t['avg_input_per_query']:>8.0f}",
            f"{t['avg_output_per_query']:>9.0f}",
            f"{t['avg_total_per_query']:>9.0f}",
            f"${t['avg_cost_per_query']:>11.6f}",
        ])

    footer_lines = [
        f"Winner (Accuracy)       : {best_acc_emb} ({summaries[best_acc_emb]['topic_accuracy']*100:.1f}%)",
        f"Winner (Speed)          : {fastest_emb} ({summaries[fastest_emb]['avg_latency_ms']:.0f}ms)",
        f"Best Quality/Speed ratio: {best_ratio_emb}",
        f"Results saved to        : {output}",
    ]

    # STEP 4 — Print to stdout
    print(f"\n{'═' * 56} EMBEDDING COMPARISON {'═' * 3}")
    print(f"  Model: {model} | Retrieval: {retrieval_mode}")
    print(f"  {'─' * 84}")
    print("  " + " | ".join(col_headers))
    print(f"  {'─' * 84}")
    for row in table_rows:
        print("  " + " | ".join(row))
    print(f"  {'═' * 84}")
    for line in footer_lines:
        print(f"  {line}")
    print(f"{'═' * 80}")

    # STEP 5 — Write comparison table to file
    writer.write_comparison_table(
        title=f"EMBEDDING COMPARISON  model={model}  retrieval={retrieval_mode}",
        headers=col_headers,
        rows=table_rows,
        footer_lines=footer_lines,
    )


def _is_already_in_results(
    filepath: str,
    model: str,
    embedding_name: str,
    retrieval_mode: str,
) -> bool:
    """
    Return True if a completed experiment block with matching model+embedding+mode
    exists in *filepath*.

    Used by run_full_matrix() to resume an interrupted run.

    Args:
        filepath:       Path to the results file.
        model:          Ollama model name.
        embedding_name: Embedding model key.
        retrieval_mode: Retrieval mode.

    Returns:
        True if the combination was already saved to the file.
    """
    path = Path(filepath)
    if not path.exists():
        return False
    needle = (
        f"model={model}  embedding={embedding_name}  mode={retrieval_mode}"
    )
    return needle in path.read_text(encoding="utf-8")


def run_full_matrix(
    retrieval_mode: str = "hybrid",
    output: str = FULL_MATRIX_FILE,
) -> None:
    """
    Run every MODEL × EMBEDDING combination (the full research matrix).

    Skips a model entirely if it is not available (Ollama/API key).
    Skips a specific (model, embedding) pair if it is already present in the
    results file so that an interrupted run can be resumed safely.

    Prints a full matrix table derived from real experiment results at the end.

    Args:
        retrieval_mode: Retrieval mode used for all combinations.
        output:         Path to the results file (default: full_matrix_results.txt).
    """
    emb_names = [e["name"] for e in EMBEDDING_MODELS]
    total = len(MODELS_TO_EVALUATE) * len(EMBEDDING_MODELS)

    print(f"\n{'═' * 56} FULL MATRIX EVALUATION {'═' * 1}")
    print(f"  Models     : {', '.join(MODELS_TO_EVALUATE)}")
    print(f"  Embeddings : {', '.join(emb_names)}")
    print(f"  Retrieval  : {retrieval_mode}")
    print(f"  Total runs : up to {total}")
    print(f"{'═' * 80}")

    # STEP 1 — Run experiments and collect real results
    matrix_rows: list[dict] = []
    run_idx = 0
    writer = ResultsWriter(filepath=output)

    for model in MODELS_TO_EVALUATE:
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available — skipping all embeddings.")
            continue

        for emb in EMBEDDING_MODELS:
            emb_name = emb["name"]
            run_idx += 1

            print(f"\n[{run_idx}/{total}] {model} + {emb_name} + {retrieval_mode}")

            # Embedding support: resume interrupted run
            if _is_already_in_results(output, model, emb_name, retrieval_mode):
                print(f"  Skipping {model}+{emb_name} — already in results")
                continue

            try:
                evaluator = ResearchEvaluator(
                    model=model,
                    retrieval_mode=retrieval_mode,
                    embedding_name=emb_name,
                )
            except (OSError, ConnectionError) as exc:
                print(f"  Failed to load {emb_name}: {exc}. Skipping.")
                continue

            results = evaluator.run_experiment()
            summary = evaluator.compute_summary()
            tok = compute_token_summary(results)

            writer.write(
                model=model,
                retrieval_mode=retrieval_mode,
                results=results,
                summary=summary,
                embedding_name=emb_name,
            )

            matrix_rows.append(
                {
                    "model": model,
                    "embedding": emb_name,
                    "topic_acc": summary["topic_accuracy"],
                    "mode_acc": summary["mode_accuracy"],
                    "kw_cov": summary["avg_keyword_coverage"],
                    "lat": summary["avg_latency_ms"],
                    "hall": summary.get("avg_hallucination_rate", 0.0),
                    "avg_input_tokens": tok["avg_input_per_query"],
                    "avg_tokens": tok["avg_total_per_query"],
                    "avg_cost": tok["avg_cost_per_query"],
                }
            )

    # STEP 2 — Determine winners using real data
    if not matrix_rows:
        return

    # STEP 3 — Build full matrix table
    col_headers = [
        f"{'Model':<14}", f"{'Embedding':<20}", f"{'TopicAcc':>8}",
        f"{'ModeAcc':>7}", f"{'KwCov':>6}", f"{'Lat':>8}", f"{'Hall':>7}",
        f"{'AvgInTok':>8}", f"{'AvgTotTok':>9}", f"{'AvgCost':>12}",
    ]
    table_rows_out: list[list[str]] = []
    for row in matrix_rows:
        table_rows_out.append([
            f"{row['model']:<14}",
            f"{row['embedding']:<20}",
            f"{row['topic_acc']*100:>7.1f}%",
            f"{row['mode_acc']*100:>6.1f}%",
            f"{row['kw_cov']:>6.3f}",
            f"{row['lat']:>6.0f}ms",
            f"{row.get('hall', 0.0)*100:>6.1f}%",
            f"{row.get('avg_input_tokens', 0):>8.0f}",
            f"{row['avg_tokens']:>9.0f}",
            f"${row['avg_cost']:>11.6f}",
        ])

    # STEP 4 — Determine winners derived from real data
    best_overall = max(matrix_rows, key=lambda r: r["topic_acc"] + r["mode_acc"])
    slm_model_names = [m for m in MODELS_TO_EVALUATE if (get_model_config(m) or {}).get("type") == "SLM"]
    slm_rows = [r for r in matrix_rows if r["model"] in slm_model_names]
    best_slm = (
        max(slm_rows, key=lambda r: r["topic_acc"] + r["mode_acc"])
        if slm_rows
        else None
    )
    fastest = min(matrix_rows, key=lambda r: r["lat"])
    value_rows = [r for r in matrix_rows if r["avg_tokens"] > 0]
    best_value = (
        max(value_rows, key=lambda r: (r["topic_acc"] + r["mode_acc"]) / r["avg_tokens"])
        if value_rows
        else best_overall
    )

    footer_lines = [
        f"Best overall   : {best_overall['model']} + {best_overall['embedding']} ({best_overall['topic_acc']*100:.1f}% topic acc)",
    ]
    if best_slm:
        footer_lines.append(
            f"Best SLM combo : {best_slm['model']} + {best_slm['embedding']} ({best_slm['topic_acc']*100:.1f}% topic acc)"
        )
    footer_lines += [
        f"Fastest combo  : {fastest['model']} + {fastest['embedding']} ({fastest['lat']:.0f}ms)",
        f"Best value     : {best_value['model']} + {best_value['embedding']}",
        f"Results saved to: {output}",
    ]

    # Print to stdout
    print(f"\n{'═' * 56} FULL RESULTS MATRIX {'═' * 4}")
    print("  " + " | ".join(col_headers))
    print(f"  {'─' * 76}")
    for row in table_rows_out:
        print("  " + " | ".join(row))
    print(f"  {'═' * 76}")
    for line in footer_lines:
        print(f"  {line}")
    print(f"{'═' * 80}")

    # Write comparison table to file (reuse the writer already created above)
    writer.write_comparison_table(
        title=f"FULL MATRIX  retrieval={retrieval_mode}",
        headers=col_headers,
        rows=table_rows_out,
        footer_lines=footer_lines,
    )


def run_token_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = TOKEN_COMPARISON_FILE,
) -> None:
    """
    Compare token usage across all available models.

    Runs every model in MODELS_TO_EVALUATE and prints a token-focused
    comparison table.  All numbers are derived from real QueryResult data
    via compute_token_summary().  Results are written to *output*
    (default: token_comparison_results.txt).

    Args:
        retrieval_mode: Retrieval mode to use for all models.
        embedding_name: Embedding model key.
        output:         Path to the results file (default: token_comparison_results.txt).
    """
    print(f"\n{'═' * 60}")
    print(f"  TOKEN COMPARISON — Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {MODELS_TO_EVALUATE}")
    print(f"{'═' * 60}")

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=MODELS_TO_EVALUATE, modes=[retrieval_mode])

    # STEP 1 — Run experiments and collect real results
    summaries: dict[str, dict] = {}
    token_summaries: dict[str, dict] = {}
    ran_models: list[str] = []

    for model in MODELS_TO_EVALUATE:
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available.")
            continue
        evaluator = ResearchEvaluator(
            model=model,
            retrieval_mode=retrieval_mode,
            embedding_name=embedding_name,
        )
        results = evaluator.run_experiment()
        summaries[model] = evaluator.compute_summary()
        token_summaries[model] = compute_token_summary(results)
        writer.write(
            model=model,
            retrieval_mode=retrieval_mode,
            results=results,
            summary=summaries[model],
            embedding_name=embedding_name,
        )
        ran_models.append(model)

    if not ran_models:
        return

    # STEP 2 — Determine token-usage leaders using real data
    most_efficient = min(ran_models, key=lambda m: token_summaries[m]["avg_total_per_query"])
    lowest_cost = min(ran_models, key=lambda m: token_summaries[m]["avg_cost_per_query"])
    highest_throughput = max(ran_models, key=lambda m: token_summaries[m]["tokens_per_ms"])

    # STEP 3 — Build token comparison rows
    col_headers = [
        f"{'Model':<16}", f"{'AvgInput':>8}", f"{'AvgOutput':>9}",
        f"{'AvgTotal':>8}", f"{'TotalTok':>9}", f"{'Tok/ms':>7}", f"{'AvgCost':>12}",
    ]
    table_rows: list[list[str]] = []
    for model in ran_models:
        t = token_summaries[model]
        table_rows.append([
            f"{model:<16}",
            f"{t['avg_input_per_query']:>8.0f}",
            f"{t['avg_output_per_query']:>9.0f}",
            f"{t['avg_total_per_query']:>8.0f}",
            f"{t['total_tokens']:>9}",
            f"{t['tokens_per_ms']:>7.4f}",
            f"${t['avg_cost_per_query']:>11.6f}",
        ])

    footer_lines = [
        f"Most efficient    : {most_efficient} ({token_summaries[most_efficient]['avg_total_per_query']:.0f} avg tokens/query)",
        f"Lowest cost       : {lowest_cost} (${token_summaries[lowest_cost]['avg_cost_per_query']:.6f}/query)",
        f"Highest throughput: {highest_throughput} ({token_summaries[highest_throughput]['tokens_per_ms']:.4f} tok/ms)",
        f"Results saved to  : {output}",
    ]

    # STEP 4 — Print to stdout
    print(f"\n{'═' * 60} TOKEN ANALYSIS {'═' * 5}")
    print(f"  Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  {'─' * 92}")
    print("  " + " | ".join(col_headers))
    print(f"  {'─' * 92}")
    for row in table_rows:
        print("  " + " | ".join(row))
    print(f"  {'═' * 92}")
    for line in footer_lines:
        print(f"  {line}")
    print(f"{'═' * 80}")

    # STEP 5 — Write comparison table to file
    writer.write_comparison_table(
        title=f"TOKEN COMPARISON  retrieval={retrieval_mode}  embedding={embedding_name}",
        headers=col_headers,
        rows=table_rows,
        footer_lines=footer_lines,
    )


def run_slm_vs_llm_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = SLM_VS_LLM_FILE,
) -> None:
    """
    Compare SLM models against LLM models using real experiment results.

    Model type (SLM / LLM) is determined by MODEL_REGISTRY.  All metric
    values in the output are derived from QueryResult objects returned by
    run_experiment().  Results are written to *output*
    (default: slm_vs_llm_results.txt).

    Args:
        retrieval_mode: Retrieval mode to use for all models.
        embedding_name: Embedding model key.
        output:         Path to the results file (default: slm_vs_llm_results.txt).
    """
    print(f"\n{'═' * 60}")
    print(f"  SLM vs LLM COMPARISON — Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {MODELS_TO_EVALUATE}")
    print(f"{'═' * 60}")

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=MODELS_TO_EVALUATE, modes=[retrieval_mode])

    # STEP 1 — Run experiments and collect real results
    summaries: dict[str, dict] = {}
    token_summaries: dict[str, dict] = {}
    ran_models: list[str] = []

    for model in MODELS_TO_EVALUATE:
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available.")
            continue
        evaluator = ResearchEvaluator(
            model=model,
            retrieval_mode=retrieval_mode,
            embedding_name=embedding_name,
        )
        results = evaluator.run_experiment()
        summaries[model] = evaluator.compute_summary()
        token_summaries[model] = compute_token_summary(results)
        writer.write(
            model=model,
            retrieval_mode=retrieval_mode,
            results=results,
            summary=summaries[model],
            embedding_name=embedding_name,
        )
        ran_models.append(model)

    if not ran_models:
        return

    # Separate into SLM and LLM groups based on MODEL_REGISTRY type
    slm_models = [m for m in ran_models if (get_model_config(m) or {}).get("type") == "SLM"]
    llm_models = [m for m in ran_models if (get_model_config(m) or {}).get("type") == "LLM"]
    other_models = [m for m in ran_models if m not in slm_models and m not in llm_models]

    # STEP 2 — Determine winners within each group using real data
    best_slm = (
        max(slm_models, key=lambda m: summaries[m]["topic_accuracy"])
        if slm_models else None
    )
    best_llm = (
        max(llm_models, key=lambda m: summaries[m]["topic_accuracy"])
        if llm_models else None
    )

    # Build row data for a group
    col_headers = [
        f"{'Model':<16}", f"{'TopicAcc':>8}", f"{'ModeAcc':>7}",
        f"{'KwCov':>6}", f"{'Lat':>8}", f"{'Hall':>7}", f"{'AvgInTok':>8}",
        f"{'AvgOutTok':>9}", f"{'AvgTotTok':>9}", f"{'AvgCost':>12}",
    ]

    def _build_group_rows(group: list[str]) -> list[list[str]]:
        rows = []
        for model in group:
            s = summaries[model]
            t = token_summaries[model]
            rows.append([
                f"{model:<16}",
                f"{s['topic_accuracy']*100:>7.1f}%",
                f"{s['mode_accuracy']*100:>6.1f}%",
                f"{s['avg_keyword_coverage']:>6.3f}",
                f"{s['avg_latency_ms']:>6.0f}ms",
                f"{s.get('avg_hallucination_rate', 0.0)*100:>6.1f}%",
                f"{t['avg_input_per_query']:>8.0f}",
                f"{t['avg_output_per_query']:>9.0f}",
                f"{t['avg_total_per_query']:>9.0f}",
                f"${t['avg_cost_per_query']:>11.6f}",
            ])
        return rows

    def _print_group(label: str, group: list[str]) -> None:
        if not group:
            return
        print(f"\n  ── {label} ──")
        print(f"  {'─' * 84}")
        print("  " + " | ".join(col_headers))
        print(f"  {'─' * 84}")
        for row in _build_group_rows(group):
            print("  " + " | ".join(row))
        print(f"  {'─' * 84}")

    # STEP 3 — Print grouped comparison table derived entirely from real data
    print(f"\n{'═' * 60} SLM vs LLM COMPARISON {'═' * 1}")
    _print_group("Small Language Models (SLM)", slm_models)
    _print_group("Large Language Models (LLM)", llm_models)
    if other_models:
        _print_group("Other", other_models)
    print(f"  {'═' * 84}")

    # STEP 4 — Print / collect group winners derived from real data
    footer_lines: list[str] = []
    if best_slm:
        footer_lines.append(
            f"Best SLM: {best_slm} ({summaries[best_slm]['topic_accuracy']*100:.1f}% topic acc, {summaries[best_slm]['avg_latency_ms']:.0f}ms)"
        )
    if best_llm:
        footer_lines.append(
            f"Best LLM: {best_llm} ({summaries[best_llm]['topic_accuracy']*100:.1f}% topic acc, {summaries[best_llm]['avg_latency_ms']:.0f}ms)"
        )
    if best_slm and best_llm:
        winner = best_slm if (
            summaries[best_slm]["topic_accuracy"] >= summaries[best_llm]["topic_accuracy"]
        ) else best_llm
        footer_lines.append(f"Overall winner: {winner} ({(get_model_config(winner) or {}).get('type','?')})")
    footer_lines.append(f"Results saved to: {output}")

    for line in footer_lines:
        print(f"  {line}")
    print(f"{'═' * 80}")

    # STEP 5 — Write all groups + footer to file
    all_rows: list[list[str]] = []
    for label, group in [
        ("SLM", slm_models),
        ("LLM", llm_models),
        ("Other", other_models),
    ]:
        if group:
            all_rows.append([f"── {label} ──"] + [""] * (len(col_headers) - 1))
            all_rows.extend(_build_group_rows(group))

    writer.write_comparison_table(
        title=f"SLM vs LLM COMPARISON  retrieval={retrieval_mode}  embedding={embedding_name}",
        headers=col_headers,
        rows=all_rows,
        footer_lines=footer_lines,
    )


# ── CLI entry point ───────────────────────────────────────────────────────────

_EXPERIMENT_MODES = [
    "single", "ablation", "model_comparison",
    "embedding_comparison", "full_matrix",
    "token_comparison", "slm_vs_llm", "full",
]


def _parse_args() -> argparse.Namespace:
    # Embedding support: list all embedding names for --embedding choices
    emb_names = [e["name"] for e in EMBEDDING_MODELS]

    parser = argparse.ArgumentParser(
        description="Run the research evaluation suite for SLM-with-RAG."
    )
    parser.add_argument(
        "--mode",
        choices=_EXPERIMENT_MODES,
        default="single",
        help=(
            "Experiment mode: single | ablation | model_comparison | "
            "embedding_comparison | full_matrix | "
            "token_comparison | slm_vs_llm | full  (default: single)."
        ),
    )
    parser.add_argument(
        "--model",
        choices=ALL_MODELS,
        default=MODELS_TO_EVALUATE[0] if MODELS_TO_EVALUATE else "groq-llama3-8b",
        help=(
            "Model to evaluate. Accepts any registered model (Ollama SLMs or "
            "Groq LLMs). In multi-model comparison modes, unavailable models "
            "are skipped automatically. In --mode single, availability is not "
            "pre-checked here and pipeline-specific fallback behavior may apply. "
            f"(default: {MODELS_TO_EVALUATE[0] if MODELS_TO_EVALUATE else 'groq-llama3-8b'})"
        ),
    )
    parser.add_argument(
        "--retrieval",
        choices=RETRIEVAL_MODES,
        default="hybrid",
        help="Retrieval mode to use (default: hybrid).",
    )
    # Embedding support: --embedding selects the embedding model
    parser.add_argument(
        "--embedding",
        choices=emb_names,
        default=DEFAULT_EMBEDDING,
        help=f"Embedding model to use (default: {DEFAULT_EMBEDDING}).",
    )
    # Embedding support: --list-embeddings prints all available embeddings
    parser.add_argument(
        "--list-embeddings",
        action="store_true",
        help="Print all available embedding models and exit.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Override results file path. If omitted, each comparison mode writes "
            "to its own default file (e.g. model_comparison_results.txt)."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    # Embedding support: --list-embeddings flag
    if args.list_embeddings:
        print("Available embeddings:")
        for emb in EMBEDDING_MODELS:
            print(
                f"  {emb['name']:<12} | {emb['dimension']}d | {emb['description']}"
            )
        sys.exit(0)

    mode = args.mode
    model = args.model
    retrieval = args.retrieval
    embedding = args.embedding
    # When --output is omitted, each comparison function uses its own default file.
    # _out is passed as **kwargs so that None output is simply not forwarded.
    _out: dict = {} if args.output is None else {"output": args.output}

    # Route to the appropriate function by mode
    if mode == "single":
        run_single_model_experiment(
            model=model, retrieval_mode=retrieval, embedding_name=embedding, **_out
        )
    elif mode == "ablation":
        run_ablation_study(model=model, embedding_name=embedding, **_out)
    elif mode == "model_comparison":
        run_model_comparison(retrieval_mode=retrieval, embedding_name=embedding, **_out)
    elif mode == "embedding_comparison":
        run_embedding_comparison(model=model, retrieval_mode=retrieval, **_out)
    elif mode == "full_matrix":
        run_full_matrix(retrieval_mode=retrieval, **_out)
    elif mode == "token_comparison":
        run_token_comparison(retrieval_mode=retrieval, embedding_name=embedding, **_out)
    elif mode == "slm_vs_llm":
        run_slm_vs_llm_comparison(retrieval_mode=retrieval, embedding_name=embedding, **_out)
    elif mode == "full":
        # Each comparison writes to its own default file unless --output is given.
        run_ablation_study(model, embedding, **_out)
        run_model_comparison(retrieval, embedding, **_out)
        run_embedding_comparison(model, retrieval, **_out)
        run_full_matrix(retrieval, **_out)
        run_token_comparison(retrieval, embedding, **_out)
        run_slm_vs_llm_comparison(retrieval, embedding, **_out)


if __name__ == "__main__":
    main()
