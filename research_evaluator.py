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

from research_config import (
    MODEL_REGISTRY,
    RETRIEVAL_MODES,
    RESULTS_FILE,
    TEST_QUERIES,
    EMBEDDING_MODELS,
    DEFAULT_EMBEDDING,
)
from retriever import build_vector_store
from rag_pipeline import RAGPipeline
from context_memory import ConversationMemory
from topic_memory_manager import TopicMemoryManager


# ── Model registry helpers ────────────────────────────────────────────────────
#
# MODEL_REGISTRY is imported from research_config as a list of dicts.
# Allowed hardcoded values: cost rate constants in research_config.py only.
# All numeric values in comparison tables must be derived from real results.

MIN_ACCURACY: float = 0.0  # Threshold constant — not a table value


def get_model_config(model: str) -> dict | None:
    """Return the MODEL_REGISTRY entry for *model*, or None if not found."""
    for cfg in MODEL_REGISTRY:
        if cfg["name"] == model:
            return cfg
    return None


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
        """Return True if *model_name* is listed in ``ollama list`` output."""
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
        estimated_cost_usd: float = (
            input_tokens * cfg.get("cost_per_1k_input_tokens", 0.0) / 1000.0
            + output_tokens * cfg.get("cost_per_1k_output_tokens", 0.0) / 1000.0
        )

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

        Topic and mode accuracy are computed over ALL results (including
        errored queries).  Keyword coverage uses only successful results with
        at least one expected keyword.  Latency uses only successful results
        with a positive latency.  Returns all-zero dict if results is empty.
        """
        results = self.results
        if not results:
            return {
                "total_queries": 0,
                "successful_queries": 0,
                "failed_queries": 0,
                "topic_accuracy": 0.0,
                "mode_accuracy": 0.0,
                "avg_keyword_coverage": 0.0,
                "avg_latency_ms": 0.0,
                "avg_metrics": {},
                "rag_count": 0,
                "partial_rag_count": 0,
                "fallback_count": 0,
                "per_category": {},
            }

        successful = [r for r in results if not r.error]
        failed = [r for r in results if r.error]

        # Topic / mode accuracy — computed over ALL results
        topic_accuracy = (
            sum(1 for r in results if r.topic_correct) / len(results)
        )
        mode_accuracy = (
            sum(1 for r in results if r.mode_correct) / len(results)
        )

        # Keyword coverage — successful results that have expected keywords
        kw_r = [r for r in successful if r.keyword_total > 0]
        avg_keyword_coverage = (
            sum(r.keyword_coverage for r in kw_r) / len(kw_r)
            if kw_r else 0.0
        )

        # Latency — successful results with a positive latency value
        lat_r = [r for r in successful if r.latency_ms > 0]
        avg_latency_ms = (
            sum(r.latency_ms for r in lat_r) / len(lat_r)
            if lat_r else 0.0
        )

        # Average evaluation metrics — successful results only
        metric_keys = [
            "Precision@5", "Recall@5", "MRR",
            "Faithfulness", "Answer Relevance", "Context Relevance",
        ]
        metric_r = [r for r in successful if r.metrics]
        avg_metrics: dict[str, float] = {}
        for key in metric_keys:
            vals = [r.metrics[key] for r in metric_r if key in r.metrics]
            avg_metrics[key] = round(sum(vals) / len(vals), 3) if vals else 0.0
        # Include any additional metric keys found in results
        extra_keys = set()
        for r in metric_r:
            extra_keys.update(r.metrics.keys())
        for key in sorted(extra_keys - set(metric_keys)):
            vals = [r.metrics[key] for r in metric_r if key in r.metrics]
            avg_metrics[key] = round(sum(vals) / len(vals), 3) if vals else 0.0

        # Mode counts from real results (all results including errors)
        rag_count = sum(1 for r in results if r.actual_mode == "RAG")
        partial_rag_count = sum(
            1 for r in results if r.actual_mode == "Partial RAG"
        )
        fallback_count = sum(
            1 for r in results
            if r.actual_mode in ("LLM Fallback", "Out of Scope")
        )

        # Per-category breakdown from real results
        categories: dict[str, list[QueryResult]] = {}
        for r in results:
            categories.setdefault(r.category, []).append(r)

        per_category: dict[str, dict] = {}
        for cat, cat_r in categories.items():
            cat_s = [r for r in cat_r if not r.error]
            cat_kw = [r for r in cat_s if r.keyword_total > 0]
            cat_lat = [r for r in cat_s if r.latency_ms > 0]
            per_category[cat] = {
                "count": len(cat_r),
                "topic_accuracy": (
                    sum(1 for r in cat_r if r.topic_correct) / len(cat_r)
                ),
                "mode_accuracy": (
                    sum(1 for r in cat_r if r.mode_correct) / len(cat_r)
                ),
                "avg_keyword_coverage": (
                    sum(r.keyword_coverage for r in cat_kw) / len(cat_kw)
                    if cat_kw else 0.0
                ),
                "avg_latency_ms": (
                    sum(r.latency_ms for r in cat_lat) / len(cat_lat)
                    if cat_lat else 0.0
                ),
            }

        return {
            "total_queries": len(results),
            "successful_queries": len(successful),
            "failed_queries": len(failed),
            "topic_accuracy": round(topic_accuracy, 4),
            "mode_accuracy": round(mode_accuracy, 4),
            "avg_keyword_coverage": round(avg_keyword_coverage, 4),
            "avg_latency_ms": round(avg_latency_ms, 1),
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

    All values are computed from real QueryResult data.  Only non-errored
    results with at least one token recorded are included so that pipeline
    failures do not skew token/cost numbers.

    Args:
        results: List of QueryResult objects returned by run_experiment().

    Returns:
        Dict with keys:
            total_input_tokens, total_output_tokens, total_tokens,
            avg_input_per_query, avg_output_per_query, avg_total_per_query,
            total_cost_usd, avg_cost_per_query,
            tokens_per_ms,
            min_tokens_query (query_id str), max_tokens_query (query_id str),
            by_mode  (dict[mode, {count, avg_input, avg_output,
                                   avg_total, avg_cost}]),
            by_category (dict[category, {count, avg_tokens, avg_cost}]).
    """
    empty: dict = {
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_tokens": 0,
        "avg_input_per_query": 0.0,
        "avg_output_per_query": 0.0,
        "avg_total_per_query": 0.0,
        "total_cost_usd": 0.0,
        "avg_cost_per_query": 0.0,
        "tokens_per_ms": 0.0,
        "min_tokens_query": "N/A",
        "max_tokens_query": "N/A",
        "by_mode": {},
        "by_category": {},
    }
    if not results:
        return empty

    token_r = [r for r in results if not r.error and r.total_tokens > 0]
    if not token_r:
        return empty

    n = len(token_r)
    total_input = sum(r.input_tokens for r in token_r)
    total_output = sum(r.output_tokens for r in token_r)
    total_all = sum(r.total_tokens for r in token_r)
    total_cost = sum(r.estimated_cost_usd for r in token_r)

    # tokens_per_ms: output tokens produced per millisecond of pipeline time
    lat_r = [r for r in token_r if r.latency_ms > 0]
    tokens_per_ms = (
        sum(r.output_tokens for r in lat_r) / sum(r.latency_ms for r in lat_r)
        if lat_r else 0.0
    )

    min_r = min(token_r, key=lambda r: r.total_tokens)
    max_r = max(token_r, key=lambda r: r.total_tokens)

    # Per-mode breakdown from real data
    modes = set(r.actual_mode for r in token_r)
    by_mode: dict[str, dict] = {}
    for mode in modes:
        m_r = [r for r in token_r if r.actual_mode == mode]
        by_mode[mode] = {
            "count": len(m_r),
            "avg_input": sum(r.input_tokens for r in m_r) / len(m_r),
            "avg_output": sum(r.output_tokens for r in m_r) / len(m_r),
            "avg_total": sum(r.total_tokens for r in m_r) / len(m_r),
            "avg_cost": sum(r.estimated_cost_usd for r in m_r) / len(m_r),
        }

    # Per-category breakdown from real data
    cats = set(r.category for r in token_r)
    by_category: dict[str, dict] = {}
    for cat in cats:
        c_r = [r for r in token_r if r.category == cat]
        by_category[cat] = {
            "count": len(c_r),
            "avg_tokens": sum(r.total_tokens for r in c_r) / len(c_r),
            "avg_cost": sum(r.estimated_cost_usd for r in c_r) / len(c_r),
        }

    return {
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_tokens": total_all,
        "avg_input_per_query": total_input / n,
        "avg_output_per_query": total_output / n,
        "avg_total_per_query": total_all / n,
        "total_cost_usd": total_cost,
        "avg_cost_per_query": total_cost / n,
        "tokens_per_ms": tokens_per_ms,
        "min_tokens_query": min_r.query_id,
        "max_tokens_query": max_r.query_id,
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
                f" {'IN_TOK':<8} {'OUT_TOK':<9} {'TOT_TOK':<9}"
                f" {'COST_USD':<12} QUERY",
            )
            self._write_line(f, "  " + "-" * 130)
            for r in results:
                t_ok = "Y" if r.topic_correct else "N"
                m_ok = "Y" if r.mode_correct else "N"
                kw = f"{r.keyword_coverage:.2f}"
                lat = f"{r.latency_ms:.0f}"
                query_snippet = r.query[:40].replace("\n", " ")
                self._write_line(
                    f,
                    f"  {r.query_id:<6} {r.category:<20} {r.expected_mode:<14}"
                    f" {r.actual_mode:<14} {t_ok:<6} {m_ok:<6} {kw:<6}"
                    f" {lat:<8} {r.input_tokens:<8} {r.output_tokens:<9}"
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
                f"  avg_latency={summary['avg_latency_ms']}ms",
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
                f" {'MODE_ACC':<10} {'KW_COV':<8} {'LAT_MS'}",
            )
            self._write_line(f, "  " + "-" * 70)
            for cat, stats in summary.get("per_category", {}).items():
                self._write_line(
                    f,
                    f"  {cat:<22} {stats['count']:<5}"
                    f" {stats['topic_accuracy']*100:<12.1f}"
                    f" {stats['mode_accuracy']*100:<10.1f}"
                    f" {stats['avg_keyword_coverage']:<8.3f}"
                    f" {stats['avg_latency_ms']:.1f}",
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



# ── High-level experiment runners ─────────────────────────────────────────────

def run_single_model_experiment(
    model: str = "phi3",
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
    )
    return summary


def run_ablation_study(
    model: str = "phi3",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = RESULTS_FILE,
) -> None:
    """
    Run *model* across all retrieval modes with the given *embedding_name*.

    This is the ablation study: same model and embedding, varying retrieval.
    Prints a comparison table derived entirely from real experiment results.

    Args:
        model:          Ollama model name.
        embedding_name: Embedding model key (e.g. "bge-small").
        output:         Path to the results file.
    """
    print(f"\n{'═' * 60}")
    print(f"  ABLATION STUDY — Model: {model} | Embedding: {embedding_name}")
    print(f"  Retrieval modes: {RETRIEVAL_MODES}")
    print(f"{'═' * 60}")

    if not ResearchEvaluator._is_model_available(model):
        print(f"  [Skip] Model '{model}' not available in ollama list.")
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

    # STEP 3 — Print comparison table derived entirely from real data
    print(f"\n{'═' * 60} ABLATION RESULTS {'═' * 3}")
    print(f"  Model: {model} | Embedding: {embedding_name}")
    print(f"  {'─' * 76}")
    print(
        f"  {'Mode':<14} | {'TopicAcc':>8} | {'ModeAcc':>7} | "
        f"{'KwCov':>6} | {'Lat':>8} | {'AvgTok':>7} | {'AvgCost':>12}"
    )
    print(f"  {'─' * 76}")
    for mode in ran_modes:
        s = summaries[mode]
        t = token_summaries[mode]
        print(
            f"  {mode:<14} | {s['topic_accuracy']*100:>7.1f}% | "
            f"{s['mode_accuracy']*100:>6.1f}% | "
            f"{s['avg_keyword_coverage']:>6.3f} | "
            f"{s['avg_latency_ms']:>6.0f}ms | "
            f"{t['avg_total_per_query']:>7.0f} | "
            f"${t['avg_cost_per_query']:>11.6f}"
        )
    print(f"  {'═' * 76}")

    # STEP 4 — Print winners derived from real data
    print(
        f"  Winner (Accuracy) : {best_acc_mode} "
        f"({summaries[best_acc_mode]['topic_accuracy']*100:.1f}%)"
    )
    print(
        f"  Winner (Speed)    : {fastest_mode} "
        f"({summaries[fastest_mode]['avg_latency_ms']:.0f}ms)"
    )
    print(f"  All results saved to: {output}")
    print(f"{'═' * 80}")


def run_model_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = RESULTS_FILE,
) -> None:
    """
    Run all models in MODEL_REGISTRY with the given *retrieval_mode* and
    *embedding_name*.

    Skips models that are not installed in Ollama.
    Prints a comparison table derived entirely from real experiment results.

    Args:
        retrieval_mode: Retrieval mode to use for all models.
        embedding_name: Embedding model key.
        output:         Path to the results file.
    """
    all_model_names = [cfg["name"] for cfg in MODEL_REGISTRY]
    print(f"\n{'═' * 60}")
    print(f"  MODEL COMPARISON — Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {all_model_names}")
    print(f"{'═' * 60}")

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=all_model_names, modes=[retrieval_mode])

    # STEP 1 — Run experiments and collect real results
    summaries: dict[str, dict] = {}
    token_summaries: dict[str, dict] = {}
    ran_models: list[str] = []

    for cfg in MODEL_REGISTRY:
        model = cfg["name"]
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available in ollama list.")
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

    # STEP 3 — Print comparison table derived entirely from real data
    print(f"\n{'═' * 60} MODEL COMPARISON {'═' * 3}")
    print(f"  Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  {'─' * 84}")
    print(
        f"  {'Model':<16} | {'Type':<4} | {'TopicAcc':>8} | {'ModeAcc':>7} | "
        f"{'KwCov':>6} | {'Lat':>8} | {'AvgTok':>7} | {'AvgCost':>12}"
    )
    print(f"  {'─' * 84}")
    for model in ran_models:
        s = summaries[model]
        t = token_summaries[model]
        cfg = get_model_config(model) or {}
        print(
            f"  {model:<16} | {cfg.get('type','?'):<4} | "
            f"{s['topic_accuracy']*100:>7.1f}% | "
            f"{s['mode_accuracy']*100:>6.1f}% | "
            f"{s['avg_keyword_coverage']:>6.3f} | "
            f"{s['avg_latency_ms']:>6.0f}ms | "
            f"{t['avg_total_per_query']:>7.0f} | "
            f"${t['avg_cost_per_query']:>11.6f}"
        )
    print(f"  {'═' * 84}")

    # STEP 4 — Print winners derived from real data
    print(
        f"  Winner (Accuracy) : {best_accuracy_model} "
        f"({summaries[best_accuracy_model]['topic_accuracy']*100:.1f}%)"
    )
    print(
        f"  Winner (Speed)    : {fastest_model} "
        f"({summaries[fastest_model]['avg_latency_ms']:.0f}ms)"
    )
    print(f"  All results saved to: {output}")
    print(f"{'═' * 80}")


def run_embedding_comparison(
    model: str = "phi3",
    retrieval_mode: str = "hybrid",
    output: str = RESULTS_FILE,
) -> None:
    """
    Run TEST_QUERIES with every embedding in EMBEDDING_MODELS.

    Uses the given *model* and *retrieval_mode* for all embeddings so results
    are directly comparable.  Prints a summary comparison table derived from
    real experiment results at the end.

    Args:
        model:          Ollama model name.
        retrieval_mode: Retrieval mode.
        output:         Path to the results file.
    """
    print(f"\n{'═' * 56}")
    print(f"  EMBEDDING COMPARISON")
    print(f"  Model: {model} | Retrieval: {retrieval_mode}")
    print(f"  Testing {len(EMBEDDING_MODELS)} embeddings")
    print(f"{'═' * 56}")

    if not ResearchEvaluator._is_model_available(model):
        print(f"  [Skip] Model '{model}' not available in ollama list.")
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

    # STEP 3 — Print comparison table derived entirely from real data
    print(f"\n{'═' * 56} EMBEDDING COMPARISON {'═' * 3}")
    print(f"  Model: {model} | Retrieval: {retrieval_mode}")
    print(f"  {'─' * 84}")
    print(
        f"  {'Embedding':<12} | {'Dim':<5} | {'TopicAcc':>8} | "
        f"{'ModeAcc':>7} | {'KwCov':>6} | {'Lat':>8} | "
        f"{'AvgTok':>7} | {'AvgCost':>12}"
    )
    print(f"  {'─' * 84}")
    for name in ran_embeddings:
        s = summaries[name]
        t = token_summaries[name]
        print(
            f"  {name:<12} | {emb_dims[name]:<5} | "
            f"{s['topic_accuracy']*100:>7.1f}% | "
            f"{s['mode_accuracy']*100:>6.1f}% | "
            f"{s['avg_keyword_coverage']:>6.3f} | "
            f"{s['avg_latency_ms']:>6.0f}ms | "
            f"{t['avg_total_per_query']:>7.0f} | "
            f"${t['avg_cost_per_query']:>11.6f}"
        )
    print(f"  {'═' * 84}")

    # STEP 4 — Print winners derived from real data
    print(f"  Winner (Accuracy)       : {best_acc_emb} "
          f"({summaries[best_acc_emb]['topic_accuracy']*100:.1f}%)")
    print(f"  Winner (Speed)          : {fastest_emb} "
          f"({summaries[fastest_emb]['avg_latency_ms']:.0f}ms)")
    print(f"  Best Quality/Speed ratio: {best_ratio_emb}")
    print(f"  All results saved to: {output}")
    print(f"{'═' * 80}")


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
    output: str = RESULTS_FILE,
) -> None:
    """
    Run every MODEL × EMBEDDING combination (the full research matrix).

    Matrix = len(MODEL_REGISTRY) × len(EMBEDDING_MODELS).

    Skips a model entirely if it is not installed in Ollama.
    Skips a specific (model, embedding) pair if it is already present in the
    results file so that an interrupted run can be resumed safely.

    Prints a full matrix table derived from real experiment results at the end.

    Args:
        retrieval_mode: Retrieval mode used for all combinations.
        output:         Path to the results file.
    """
    emb_names = [e["name"] for e in EMBEDDING_MODELS]
    all_model_names = [cfg["name"] for cfg in MODEL_REGISTRY]
    total = len(MODEL_REGISTRY) * len(EMBEDDING_MODELS)

    print(f"\n{'═' * 56} FULL MATRIX EVALUATION {'═' * 1}")
    print(f"  Models     : {', '.join(all_model_names)}")
    print(f"  Embeddings : {', '.join(emb_names)}")
    print(f"  Retrieval  : {retrieval_mode}")
    print(f"  Total runs : up to {total}")
    print(f"{'═' * 80}")

    # STEP 1 — Run experiments and collect real results
    matrix_rows: list[dict] = []
    run_idx = 0

    for cfg in MODEL_REGISTRY:
        model = cfg["name"]
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not installed — skipping all embeddings.")
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

            writer = ResultsWriter(filepath=output)
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
                    "avg_tokens": tok["avg_total_per_query"],
                    "avg_cost": tok["avg_cost_per_query"],
                }
            )

    # STEP 2 — Determine winners using real data
    if not matrix_rows:
        return

    # STEP 3 — Print full matrix table derived entirely from real data
    print(f"\n{'═' * 56} FULL RESULTS MATRIX {'═' * 4}")
    print(
        f"  {'Model':<10} | {'Embedding':<10} | {'TopicAcc':>8} |"
        f" {'ModeAcc':>7} | {'KwCov':>6} | {'Lat':>8} | {'AvgTok':>7}"
    )
    print(f"  {'─' * 76}")
    for row in matrix_rows:
        print(
            f"  {row['model']:<10} | {row['embedding']:<10} |"
            f" {row['topic_acc']*100:>7.1f}% | {row['mode_acc']*100:>6.1f}% |"
            f" {row['kw_cov']:>6.3f} | {row['lat']:>6.0f}ms |"
            f" {row['avg_tokens']:>7.0f}"
        )
    print(f"  {'═' * 76}")

    # STEP 4 — Print winners derived from real data
    best_overall = max(matrix_rows, key=lambda r: r["topic_acc"] + r["mode_acc"])

    # SLM models are those with type "SLM" in the registry
    slm_model_names = [
        cfg["name"] for cfg in MODEL_REGISTRY
        if cfg.get("type") == "SLM"
    ]
    slm_rows = [r for r in matrix_rows if r["model"] in slm_model_names]
    best_slm = (
        max(slm_rows, key=lambda r: r["topic_acc"] + r["mode_acc"])
        if slm_rows
        else None
    )
    fastest = min(matrix_rows, key=lambda r: r["lat"])

    # Best value: highest accuracy-to-token ratio; skip rows with no tokens recorded
    value_rows = [r for r in matrix_rows if r["avg_tokens"] > 0]
    best_value = (
        max(value_rows, key=lambda r: (r["topic_acc"] + r["mode_acc"]) / r["avg_tokens"])
        if value_rows
        else best_overall
    )

    print(
        f"  Best overall      : {best_overall['model']} + {best_overall['embedding']}"
        f" ({best_overall['topic_acc']*100:.1f}% topic acc)"
    )
    if best_slm:
        print(
            f"  Best SLM combo    : {best_slm['model']} + {best_slm['embedding']}"
            f" ({best_slm['topic_acc']*100:.1f}% topic acc)"
        )
    print(
        f"  Fastest combo     : {fastest['model']} + {fastest['embedding']}"
        f" ({fastest['lat']:.0f}ms)"
    )
    print(
        f"  Best value combo  : {best_value['model']} + {best_value['embedding']}"
    )
    print(f"{'═' * 80}")
    print(f"  All results saved to: {output}")


def run_token_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = RESULTS_FILE,
) -> None:
    """
    Compare token usage and accuracy across all models in MODEL_REGISTRY.

    All numbers are derived from real QueryResult data via
    compute_token_summary() and compute_summary().  No hardcoded values
    appear in any print() table or f-string result line.

    Args:
        retrieval_mode: Retrieval mode to use for all models.
        embedding_name: Embedding model key.
        output:         Path to the results file.
    """
    all_model_names = [cfg["name"] for cfg in MODEL_REGISTRY]
    print(f"\n{'═' * 60}")
    print(f"  TOKEN COMPARISON — Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {all_model_names}")
    print(f"{'═' * 60}")

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=all_model_names, modes=[retrieval_mode])

    # STEP 1 — Run experiments and collect real results
    all_summaries: dict[str, dict] = {}
    all_token_summaries: dict[str, dict] = {}
    ran_models: list[str] = []

    for cfg in MODEL_REGISTRY:
        model = cfg["name"]
        ev = ResearchEvaluator(model, retrieval_mode, embedding_name)
        if not ev._is_model_available(model):
            print(f"[Skip] {model}")
            continue
        print(f"\nRunning: {model}")
        results = ev.run_experiment()
        all_summaries[model] = ev.compute_summary()
        all_token_summaries[model] = compute_token_summary(results)
        writer.write(model, retrieval_mode, results,
                     all_summaries[model], embedding_name)
        ran_models.append(model)

    if not ran_models:
        print("No models available.")
        return

    # STEP 2 — Find winners from real data
    best_acc = max(ran_models,
                   key=lambda m: all_summaries[m]["topic_accuracy"])
    fastest = min(ran_models,
                  key=lambda m: all_summaries[m]["avg_latency_ms"])
    above_80 = [m for m in ran_models
                if all_summaries[m]["topic_accuracy"] >= 0.80]
    cheapest_good = (
        min(above_80,
            key=lambda m: all_token_summaries[m]["avg_cost_per_query"])
        if above_80 else None
    )
    slm_ran = [m for m in ran_models
               if get_model_config(m) and
               get_model_config(m)["type"] == "SLM"]
    llm_ran = [m for m in ran_models
               if get_model_config(m) and
               get_model_config(m)["type"] == "LLM"]
    best_slm = (
        max(slm_ran, key=lambda m: all_summaries[m]["topic_accuracy"])
        if slm_ran else None
    )
    best_llm = (
        max(llm_ran, key=lambda m: all_summaries[m]["topic_accuracy"])
        if llm_ran else None
    )

    # STEP 3 — Print table — all values from real data
    sep = "═" * 88
    div = "─" * 88
    print(f"\n{sep}")
    print(
        f"TOKEN & COST COMPARISON | {retrieval_mode} | "
        f"{embedding_name} | {len(TEST_QUERIES)} queries"
    )
    print(div)
    print(
        f"{'Model':<16}|{'Type':<5}|{'TopicAcc':>9}|"
        f"{'AvgIn':>6}|{'AvgOut':>7}|"
        f"{'Total':>6}|{'Cost/Q':>11}|{'Latency':>9}"
    )
    print(div)
    for model in ran_models:
        s = all_summaries[model]
        t = all_token_summaries[model]
        c = get_model_config(model) or {}
        print(
            f"{model:<16}|"
            f"{c.get('type', '?'):<5}|"
            f"{s['topic_accuracy']*100:>8.1f}%|"
            f"{t['avg_input_per_query']:>6.0f}|"
            f"{t['avg_output_per_query']:>7.0f}|"
            f"{t['avg_total_per_query']:>6.0f}|"
            f"${t['avg_cost_per_query']:>10.6f}|"
            f"{s['avg_latency_ms']:>7.0f}ms"
        )
    print(sep)

    # STEP 4 — Print winners from real data
    print(
        f"Best Accuracy  : {best_acc} "
        f"({all_summaries[best_acc]['topic_accuracy']*100:.1f}%)"
    )
    print(
        f"Fastest        : {fastest} "
        f"({all_summaries[fastest]['avg_latency_ms']:.0f}ms)"
    )
    if cheapest_good:
        print(
            f"Cheapest >=80% : {cheapest_good} "
            f"(${all_token_summaries[cheapest_good]['avg_cost_per_query']:.6f}/q)"
        )
    if best_slm and best_llm:
        gap = (
            (all_summaries[best_llm]["topic_accuracy"] -
             all_summaries[best_slm]["topic_accuracy"]) * 100
        )
        slm_pct = (
            all_summaries[best_slm]["topic_accuracy"] /
            all_summaries[best_llm]["topic_accuracy"] * 100
        )
        print(
            f"Best SLM       : {best_slm} "
            f"({all_summaries[best_slm]['topic_accuracy']*100:.1f}%)"
        )
        print(
            f"Best LLM       : {best_llm} "
            f"({all_summaries[best_llm]['topic_accuracy']*100:.1f}%)"
        )
        print(
            f"SLM vs LLM gap : {gap:.1f}% "
            f"(SLM = {slm_pct:.1f}% of LLM accuracy)"
        )
    print(sep)

    # Token by mode — all from real data
    all_modes: set[str] = set()
    for t in all_token_summaries.values():
        all_modes.update(t["by_mode"].keys())
    if all_modes:
        print("\nTOKENS BY PIPELINE MODE (avg across all models)")
        print(div)
        print(
            f"{'Mode':<16}|{'AvgInput':>9}|"
            f"{'AvgOutput':>10}|{'AvgTotal':>9}|{'AvgCost':>11}"
        )
        print(div)
        for mode in sorted(all_modes):
            ins: list[float] = []
            outs: list[float] = []
            tots: list[float] = []
            costs: list[float] = []
            for t in all_token_summaries.values():
                if mode in t["by_mode"]:
                    m = t["by_mode"][mode]
                    ins.append(m["avg_input"])
                    outs.append(m["avg_output"])
                    tots.append(m["avg_total"])
                    costs.append(m["avg_cost"])
            if ins:
                print(
                    f"{mode:<16}|"
                    f"{sum(ins)/len(ins):>9.1f}|"
                    f"{sum(outs)/len(outs):>10.1f}|"
                    f"{sum(tots)/len(tots):>9.1f}|"
                    f"${sum(costs)/len(costs):>10.6f}"
                )

    print(f"\nResults saved to: {output}")


def run_slm_vs_llm_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = RESULTS_FILE,
) -> None:
    """
    Compare SLM models against LLM models using real experiment results.

    Model type (SLM / LLM) is determined by MODEL_REGISTRY.  All metric
    values in the output are derived from QueryResult objects returned by
    run_experiment().  No hardcoded numbers appear in any table line.

    Args:
        retrieval_mode: Retrieval mode to use for all models.
        embedding_name: Embedding model key.
        output:         Path to the results file.
    """
    all_model_names = [cfg["name"] for cfg in MODEL_REGISTRY]
    print(f"\n{'═' * 60}")
    print(f"  SLM vs LLM COMPARISON — Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {all_model_names}")
    print(f"{'═' * 60}")

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=all_model_names, modes=[retrieval_mode])

    # STEP 1 — Run experiments and collect real results
    slm_all: list[QueryResult] = []
    llm_all: list[QueryResult] = []
    slm_s: dict[str, dict] = {}
    llm_s: dict[str, dict] = {}

    for cfg in MODEL_REGISTRY:
        model = cfg["name"]
        ev = ResearchEvaluator(model, retrieval_mode, embedding_name)
        if not ev._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available in ollama list.")
            continue
        print(f"\nRunning: {model} ({cfg['type']})")
        results = ev.run_experiment()
        summary = ev.compute_summary()
        tok = compute_token_summary(results)
        writer.write(model, retrieval_mode, results, summary, embedding_name)
        data = {"summary": summary, "tokens": tok, "config": cfg}
        if cfg["type"] == "SLM":
            slm_all.extend(results)
            slm_s[model] = data
        else:
            llm_all.extend(results)
            llm_s[model] = data

    if not slm_s and not llm_s:
        print("No models available.")
        return

    def best_in(
        sdict: dict[str, dict],
        keys: list[str],
        highest: bool = True,
    ) -> tuple[str | None, float | None]:
        """Find best model in group by nested key path."""
        best_name: str | None = None
        best_val: float | None = None
        for name, d in sdict.items():
            current: dict | None = d
            val: object = None
            for k in keys:
                if not isinstance(current, dict):
                    current = None
                    break
                val = current.get(k)
                if isinstance(val, dict):
                    current = val
                else:
                    current = None
            if not isinstance(val, (int, float)):
                continue
            if (best_val is None
                    or (highest and val > best_val)
                    or (not highest and val < best_val)):
                best_name, best_val = name, float(val)
        return best_name, best_val

    metrics = [
        (
            "Topic Accuracy",
            ["summary", "topic_accuracy"],
            True,
            lambda v: f"{v*100:.1f}%",
        ),
        (
            "Mode Accuracy",
            ["summary", "mode_accuracy"],
            True,
            lambda v: f"{v*100:.1f}%",
        ),
        (
            "Avg Keyword Cov",
            ["summary", "avg_keyword_coverage"],
            True,
            lambda v: f"{v:.3f}",
        ),
        (
            "Avg Latency",
            ["summary", "avg_latency_ms"],
            False,
            lambda v: f"{v:.0f}ms",
        ),
        (
            "Avg Total Tokens",
            ["tokens", "avg_total_per_query"],
            False,
            lambda v: f"{v:.0f}",
        ),
        (
            "Avg Cost/Query",
            ["tokens", "avg_cost_per_query"],
            False,
            lambda v: f"${v:.6f}",
        ),
        (
            "Faithfulness",
            ["summary", "avg_metrics", "Faithfulness"],
            True,
            lambda v: f"{v:.3f}",
        ),
        (
            "Answer Relevance",
            ["summary", "avg_metrics", "Answer Relevance"],
            True,
            lambda v: f"{v:.3f}",
        ),
    ]

    sep = "═" * 68
    div = "─" * 68

    # STEP 3 — Print comparison table derived entirely from real data
    print(f"\n{sep}")
    print("SLM vs LLM — all values from real results")
    print(div)
    print(f"{'Metric':<22} | {'Best SLM':>20} | {'Best LLM':>20}")
    print(div)
    for label, keys, highest, fmt in metrics:
        sn, sv = best_in(slm_s, keys, highest)
        ln, lv = best_in(llm_s, keys, highest)
        ss = f"{sn} ({fmt(sv)})" if sn and sv is not None else "N/A"
        ls = f"{ln} ({fmt(lv)})" if ln and lv is not None else "N/A"
        print(f"{label:<22} | {ss:>20} | {ls:>20}")
    print(div)

    # STEP 4 — Print accuracy gap derived from real data
    if slm_s and llm_s:
        _, ba_slm = best_in(slm_s, ["summary", "topic_accuracy"], True)
        _, ba_llm = best_in(llm_s, ["summary", "topic_accuracy"], True)
        if ba_slm is not None and ba_llm is not None and ba_llm > 0:
            gap = (ba_llm - ba_slm) * 100
            pct = (ba_slm / ba_llm) * 100
            print(
                f"Accuracy gap : {gap:.1f}% "
                f"(SLM = {pct:.1f}% of LLM accuracy)"
            )

    # Per category from real results
    if slm_all and llm_all:
        cats = sorted(set(r.category for r in slm_all + llm_all))
        print(f"\nPER CATEGORY | SLM vs LLM Topic Accuracy")
        print(div)
        print(
            f"{'Category':<20}|{'SLM Acc':>9}|"
            f"{'LLM Acc':>9}|{'Gap':>7}"
        )
        print(div)
        for cat in cats:
            sc = [r for r in slm_all if r.category == cat]
            lc = [r for r in llm_all if r.category == cat]
            sa = (
                sum(1 for r in sc if r.topic_correct) / len(sc) * 100
                if sc else 0.0
            )
            la = (
                sum(1 for r in lc if r.topic_correct) / len(lc) * 100
                if lc else 0.0
            )
            print(
                f"{cat:<20}|{sa:>8.1f}%|"
                f"{la:>8.1f}%|{la-sa:>+6.1f}%"
            )
    print(sep)
    print(f"Results saved to: {output}")


# ── CLI entry point ───────────────────────────────────────────────────────────

_EXPERIMENT_MODES = [
    "single", "ablation", "model_comparison",
    "embedding_comparison", "full_matrix",
    "token_comparison", "slm_vs_llm", "full",
]


def _parse_args() -> argparse.Namespace:
    # Build choice lists from MODEL_REGISTRY and EMBEDDING_MODELS
    model_names = [cfg["name"] for cfg in MODEL_REGISTRY]
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
        choices=model_names,
        default="phi3",
        help="Model to evaluate (default: phi3).",
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
        default=RESULTS_FILE,
        help=f"Results file path (default: {RESULTS_FILE}).",
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
    output = args.output

    # Route to the appropriate function by mode
    if mode == "single":
        run_single_model_experiment(
            model=model,
            retrieval_mode=retrieval,
            embedding_name=embedding,
            output=output,
        )
    elif mode == "ablation":
        run_ablation_study(
            model=model,
            embedding_name=embedding,
            output=output,
        )
    elif mode == "model_comparison":
        run_model_comparison(
            retrieval_mode=retrieval,
            embedding_name=embedding,
            output=output,
        )
    elif mode == "embedding_comparison":
        run_embedding_comparison(
            model=model,
            retrieval_mode=retrieval,
            output=output,
        )
    elif mode == "full_matrix":
        run_full_matrix(
            retrieval_mode=retrieval,
            output=output,
        )
    elif mode == "token_comparison":
        run_token_comparison(
            retrieval_mode=retrieval,
            embedding_name=embedding,
            output=output,
        )
    elif mode == "slm_vs_llm":
        run_slm_vs_llm_comparison(
            retrieval_mode=retrieval,
            embedding_name=embedding,
            output=output,
        )
    elif mode == "full":
        run_ablation_study(model, embedding, output)
        run_model_comparison(retrieval, embedding, output)
        run_embedding_comparison(model, retrieval, output)
        run_full_matrix(retrieval, output)
        run_token_comparison(retrieval, embedding, output)
        run_slm_vs_llm_comparison(retrieval, embedding, output)


if __name__ == "__main__":
    main()
