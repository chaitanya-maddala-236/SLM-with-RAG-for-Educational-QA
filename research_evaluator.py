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
    MODELS_TO_EVALUATE,
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
        else:
            topic_accuracy = mode_accuracy = avg_keyword_coverage = avg_latency_ms = 0.0

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
            }

        return {
            "total_queries": total,
            "successful_queries": len(successful),
            "failed_queries": len(errored),
            "topic_accuracy": round(topic_accuracy * 100, 2),
            "mode_accuracy": round(mode_accuracy * 100, 2),
            "avg_keyword_coverage": round(avg_keyword_coverage, 3),
            "avg_latency_ms": round(avg_latency_ms, 1),
            "avg_metrics": avg_metrics,
            "rag_count": rag_count,
            "partial_rag_count": partial_rag_count,
            "fallback_count": fallback_count,
            "per_category": per_category,
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

        Args:
            model:          Ollama model name (e.g. "phi3").
            retrieval_mode: Retrieval mode used (e.g. "hybrid").
            results:        List of QueryResult objects from run_experiment().
            summary:        Summary dict from compute_summary().
            embedding_name: Embedding model name used (e.g. "bge-small").
        """
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
                f" {'T_OK':<6} {'M_OK':<6} {'KW':<6} {'LAT_MS':<8} QUERY",
            )
            self._write_line(f, "  " + "-" * 100)
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
                    f" {lat:<8} {query_snippet!r}",
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
                f"  topic_accuracy={summary['topic_accuracy']}%"
                f"  mode_accuracy={summary['mode_accuracy']}%",
            )
            self._write_line(
                f,
                f"  avg_keyword_coverage={summary['avg_keyword_coverage']}"
                f"  avg_latency={summary['avg_latency_ms']}ms",
            )
            self._write_line(
                f,
                f"  rag={summary['rag_count']}"
                f"  partial_rag={summary['partial_rag_count']}"
                f"  fallback={summary['fallback_count']}",
            )

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
                    f" {stats['topic_accuracy']:<12.3f}"
                    f" {stats['mode_accuracy']:<10.3f}"
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
        f"  topic_accuracy={summary['topic_accuracy']}%"
        f"  mode_accuracy={summary['mode_accuracy']}%"
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

    for mode in RETRIEVAL_MODES:
        run_single_model_experiment(
            model=model,
            retrieval_mode=mode,
            embedding_name=embedding_name,
            output=output,
        )


def run_model_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    output: str = RESULTS_FILE,
) -> None:
    """
    Run all models with the given *retrieval_mode* and *embedding_name*.

    Skips models that are not installed in Ollama.

    Args:
        retrieval_mode: Retrieval mode to use for all models.
        embedding_name: Embedding model key.
        output:         Path to the results file.
    """
    print(f"\n{'═' * 60}")
    print(f"  MODEL COMPARISON — Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {MODELS_TO_EVALUATE}")
    print(f"{'═' * 60}")

    writer = ResultsWriter(filepath=output)
    writer.write_run_header(models=MODELS_TO_EVALUATE, modes=[retrieval_mode])

    for model in MODELS_TO_EVALUATE:
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available in ollama list.")
            continue
        run_single_model_experiment(
            model=model,
            retrieval_mode=retrieval_mode,
            embedding_name=embedding_name,
            output=output,
        )


def run_embedding_comparison(
    model: str = "phi3",
    retrieval_mode: str = "hybrid",
    output: str = RESULTS_FILE,
) -> None:
    """
    Run TEST_QUERIES with every embedding in EMBEDDING_MODELS.

    Uses the given *model* and *retrieval_mode* for all embeddings so results
    are directly comparable.  Prints a summary comparison table at the end.

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
    comparison_rows: list[dict] = []

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
        summary = evaluator.compute_summary()

        writer.write_experiment(
            model=model,
            retrieval_mode=retrieval_mode,
            results=results,
            summary=summary,
            embedding_name=name,
        )

        comparison_rows.append(
            {
                "name": name,
                "dim": dim,
                "topic_acc": summary["topic_accuracy"],
                "mode_acc": summary["mode_accuracy"],
                "kw_cov": summary["avg_keyword_coverage"],
                "lat": summary["avg_latency_ms"],
            }
        )

    # ── Print comparison table ─────────────────────────────────────────────
    if comparison_rows:
        print(f"\n{'═' * 56} EMBEDDING COMPARISON {'═' * 3}")
        print(f"  Model: {model} | Retrieval: {retrieval_mode}")
        print(f"  {'─' * 72}")
        print(
            f"  {'Embedding':<12} | {'Dim':<5} | {'TopicAcc':>8} |"
            f" {'ModeAcc':>7} | {'KwCov':>6} | {'Lat':>8}"
        )
        print(f"  {'─' * 72}")
        for row in comparison_rows:
            print(
                f"  {row['name']:<12} | {row['dim']:<5} |"
                f" {row['topic_acc']:>7.1f}% | {row['mode_acc']:>6.1f}% |"
                f" {row['kw_cov']:>6.3f} | {row['lat']:>6.0f}ms"
            )
        print(f"  {'═' * 72}")

        best_acc = max(comparison_rows, key=lambda r: r["topic_acc"] + r["mode_acc"])
        best_speed = min(comparison_rows, key=lambda r: r["lat"])
        # Quality/speed ratio: (topic_acc + mode_acc) / latency, normalized
        best_ratio = max(
            comparison_rows,
            key=lambda r: (r["topic_acc"] + r["mode_acc"]) / max(r["lat"], 1),
        )
        print(f"  Winner (Accuracy): {best_acc['name']}")
        print(f"  Winner (Speed):    {best_speed['name']}")
        print(f"  Best Quality/Speed ratio: {best_ratio['name']}")
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

    Matrix = len(MODELS_TO_EVALUATE) × len(EMBEDDING_MODELS)
    = 4 models × 7 embeddings = up to 28 combinations.

    Skips a model entirely if it is not installed in Ollama.
    Skips a specific (model, embedding) pair if it is already present in the
    results file so that an interrupted run can be resumed safely.

    Prints a full matrix table at the end.

    Args:
        retrieval_mode: Retrieval mode used for all combinations.
        output:         Path to the results file.
    """
    emb_names = [e["name"] for e in EMBEDDING_MODELS]
    total = len(MODELS_TO_EVALUATE) * len(EMBEDDING_MODELS)

    print(f"\n{'═' * 56} FULL MATRIX EVALUATION {'═' * 1}")
    print(f"  Models     : {', '.join(MODELS_TO_EVALUATE)}")
    print(f"  Embeddings : {', '.join(emb_names)}")
    print(f"  Retrieval  : {retrieval_mode}")
    print(f"  Total runs : up to {total}")
    print(f"{'═' * 80}")

    matrix_rows: list[dict] = []
    run_idx = 0

    for model in MODELS_TO_EVALUATE:
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
                # Still collect the summary for the final table by scanning file
                # (we just skip re-running; table row will be missing for skipped)
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

            writer = ResultsWriter(filepath=output)
            writer.write_experiment(
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
                }
            )

    # ── Print full matrix table ────────────────────────────────────────────
    if matrix_rows:
        print(f"\n{'═' * 56} FULL RESULTS MATRIX {'═' * 4}")
        print(
            f"  {'Model':<10} | {'Embedding':<10} | {'TopicAcc':>8} |"
            f" {'ModeAcc':>7} | {'KwCov':>6} | {'Lat':>8}"
        )
        print(f"  {'─' * 72}")
        for row in matrix_rows:
            print(
                f"  {row['model']:<10} | {row['embedding']:<10} |"
                f" {row['topic_acc']:>7.1f}% | {row['mode_acc']:>6.1f}% |"
                f" {row['kw_cov']:>6.3f} | {row['lat']:>6.0f}ms"
            )
        print(f"  {'═' * 72}")

        best_overall = max(
            matrix_rows, key=lambda r: r["topic_acc"] + r["mode_acc"]
        )
        slm_rows = [r for r in matrix_rows if r["model"] == "phi3"]
        best_slm = (
            max(slm_rows, key=lambda r: r["topic_acc"] + r["mode_acc"])
            if slm_rows
            else best_overall
        )
        fastest = min(matrix_rows, key=lambda r: r["lat"])
        best_value_rows = [r for r in matrix_rows if r["model"] == "phi3" and r["embedding"] == DEFAULT_EMBEDDING]
        best_value = best_value_rows[0] if best_value_rows else best_overall

        print(
            f"  Best overall      : {best_overall['model']} + {best_overall['embedding']}"
        )
        print(
            f"  Best SLM combo    : {best_slm['model']} + {best_slm['embedding']}"
        )
        print(
            f"  Fastest combo     : {fastest['model']} + {fastest['embedding']}"
        )
        print(
            f"  Best value combo  : {best_value['model']} + {best_value['embedding']}"
        )
        print(f"{'═' * 80}")
        print(f"  All results saved to: {output}")


# ── CLI entry point ───────────────────────────────────────────────────────────

_EXPERIMENT_MODES = [
    "single", "ablation", "model_comparison",
    "embedding_comparison", "full_matrix", "full",
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
            "embedding_comparison | full_matrix | full  (default: single)."
        ),
    )
    parser.add_argument(
        "--model",
        choices=MODELS_TO_EVALUATE,
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

    # Embedding support: route to the appropriate function by mode
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
    elif mode == "full":
        run_ablation_study("phi3", DEFAULT_EMBEDDING, output)
        run_model_comparison("hybrid", DEFAULT_EMBEDDING, output)
        run_embedding_comparison("phi3", "hybrid", output)
        run_full_matrix("hybrid", output)


if __name__ == "__main__":
    main()
