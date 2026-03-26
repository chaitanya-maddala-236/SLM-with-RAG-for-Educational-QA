"""
research_evaluator.py
---------------------
Research evaluation system for the SLM-with-RAG Educational QA pipeline.

Runs the full RAG pipeline across multiple models and retrieval modes using
the structured TEST_QUERIES test suite defined in research_config.py and
writes per-query results plus aggregate statistics to RESULTS_FILE.

Usage:
    python research_evaluator.py                          # all models × modes
    python research_evaluator.py --model phi3             # single model, all modes
    python research_evaluator.py --model phi3 --mode hybrid
"""

from __future__ import annotations

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


# ── ResearchEvaluator ─────────────────────────────────────────────────────────

class ResearchEvaluator:
    """
    Orchestrates a single (model, retrieval_mode) experiment.

    Builds the vector store once, creates a RAGPipeline, then runs
    every query in TEST_QUERIES while managing ConversationMemory and
    TopicMemoryManager according to each query's ``conversation_reset`` flag.
    """

    def __init__(self, model: str, retrieval_mode: str) -> None:
        vector_store = build_vector_store()
        self.pipeline = RAGPipeline(
            vector_store,
            model_name=model,
            retrieval_mode=retrieval_mode,
        )
        self.model = model
        self.retrieval_mode = retrieval_mode
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
    ) -> None:
        """
        Append a full experiment block (header + per-query rows + summary)
        to the results file.

        Args:
            model:          Ollama model name (e.g. "phi3").
            retrieval_mode: Retrieval mode used (e.g. "hybrid").
            results:        List of QueryResult objects from run_experiment().
            summary:        Summary dict from compute_summary().
        """
        with open(self.filepath, "a", encoding="utf-8") as f:
            # ── Experiment header ─────────────────────────────────────────────
            self._write_line(f)
            self._write_line(f, "=" * 80)
            self._write_line(
                f,
                f"{self.BLOCK_MARKER} EXPERIMENT  model={model}"
                f"  mode={retrieval_mode}"
                f"  timestamp={datetime.now().isoformat(timespec='seconds')}",
            )
            self._write_line(f, "=" * 80)

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


# ── CLI entry point ───────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the research evaluation suite for SLM-with-RAG."
    )
    parser.add_argument(
        "--model",
        choices=MODELS_TO_EVALUATE + ["all"],
        default="all",
        help="Model to evaluate (default: all).",
    )
    parser.add_argument(
        "--mode",
        choices=RETRIEVAL_MODES + ["all"],
        default="all",
        help="Retrieval mode to use (default: all).",
    )
    parser.add_argument(
        "--output",
        default=RESULTS_FILE,
        help=f"Results file path (default: {RESULTS_FILE}).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    models = MODELS_TO_EVALUATE if args.model == "all" else [args.model]
    modes = RETRIEVAL_MODES if args.mode == "all" else [args.mode]

    writer = ResultsWriter(filepath=args.output)
    writer.write_run_header(models=models, modes=modes)

    for model in models:
        if not ResearchEvaluator._is_model_available(model):
            print(f"\n[Skip] Model '{model}' not available in ollama list.")
            continue

        for mode in modes:
            print(f"\n{'=' * 60}")
            print(f"  Model: {model}  |  Retrieval mode: {mode}")
            print(f"{'=' * 60}")

            evaluator = ResearchEvaluator(model=model, retrieval_mode=mode)
            results = evaluator.run_experiment()
            summary = evaluator.compute_summary()

            writer.write_experiment(
                model=model,
                retrieval_mode=mode,
                results=results,
                summary=summary,
            )

            print(f"\n  ✓ Results appended to {args.output}")
            print(
                f"  topic_accuracy={summary['topic_accuracy']}%"
                f"  mode_accuracy={summary['mode_accuracy']}%"
                f"  avg_latency={summary['avg_latency_ms']}ms"
            )


if __name__ == "__main__":
    main()
