"""
final_evaluation.py
-------------------
Final evaluation script for the EduSLM-RAG project.

This script **runs the actual RAG pipeline** against the structured
TEST_QUERIES dataset defined in ``research_config.py`` and computes all
metrics from real pipeline outputs — no hardcoded or sample data.

What it does
~~~~~~~~~~~~
1.  Runs each requested model through the RAG pipeline on every test query.
2.  Computes **5 core metrics** per model from real pipeline results:
        • Faithfulness       — from evaluation.py token-overlap metric
        • Answer Relevance   — from evaluation.py query-term recall
        • Context Precision  — from evaluation.py context relevance
        • Context Recall     — from evaluation.py recall@K
        • Hallucination Rate — 1 − Faithfulness
3.  Computes **per-token cost** (cost_per_token = cost_per_query / avg_total_tokens).
4.  Produces a **weighted final score** ranking.
5.  Generates **8 publication-quality graphs** (300 DPI PNGs):
        • Final score comparison (bar)
        • 5-metric grouped bar chart
        • Cost per query (bar)
        • Cost per token (bar)
        • Hallucination rate (bar)
        • Avg tokens breakdown — input vs output (grouped bar)
        • Latency vs accuracy scatter
        • Radar / spider chart of normalized metrics

Usage
~~~~~
    # Run live evaluation on all available models (default: hybrid retrieval)
    python final_evaluation.py

    # Evaluate specific models
    python final_evaluation.py --models phi3 groq-llama3-8b

    # Custom retrieval mode and embedding
    python final_evaluation.py --retrieval hybrid --embedding bge-small

    # Load from a pre-existing CSV/JSON instead of running live
    python final_evaluation.py --input results/final_metrics.csv

    # Custom output directory
    python final_evaluation.py --output-dir my_graphs

Dependencies
~~~~~~~~~~~~
    pip install pandas matplotlib
    # Plus all RAG pipeline dependencies (see requirements.txt)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import textwrap
from pathlib import Path

# ── Project imports ──────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research_config import (
    TEST_QUERIES,
    MODELS_TO_EVALUATE,
    MODEL_REGISTRY,
    DEFAULT_EMBEDDING,
    get_model_config,
)
from research_evaluator import (
    ResearchEvaluator,
    compute_token_summary,
)

# ── Constants ────────────────────────────────────────────────────────────────

DEFAULT_OUTPUT_DIR = Path("results/final_evaluation")
DEFAULT_INPUT = Path("results/final_metrics.csv")

REQUIRED_COLUMNS = [
    "model",
    "faithfulness",
    "answer_relevance",
    "context_precision",
    "context_recall",
    "cost_per_query",
]

METRIC_COLUMNS = [
    "faithfulness",
    "answer_relevance",
    "context_precision",
    "context_recall",
    "cost_per_query",
]

QUALITY_METRICS = [
    "faithfulness",
    "answer_relevance",
    "context_precision",
    "context_recall",
]

# Small floor value used to avoid divide-by-zero in cost normalization.
EPSILON = 1e-9

# Weighted-score coefficients (sum to ~1.0).
FAITHFULNESS_WEIGHT = 0.28
ANSWER_RELEVANCE_WEIGHT = 0.24
CONTEXT_PRECISION_WEIGHT = 0.18
CONTEXT_RECALL_WEIGHT = 0.15
COST_EFFICIENCY_WEIGHT = 0.10
HALLUCINATION_PENALTY_WEIGHT = 0.05

# ── Lazy imports ─────────────────────────────────────────────────────────────

_pd = None
_plt = None


def _require_pandas():
    global _pd
    if _pd is None:
        try:
            import pandas as pd
        except ImportError as exc:
            raise SystemExit(
                "ERROR: pandas is required.  Install with:  pip install pandas"
            ) from exc
        _pd = pd
    return _pd


def _require_matplotlib():
    global _plt
    if _plt is None:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt_mod
            plt_mod.style.use("seaborn-v0_8-whitegrid")
            plt_mod.rcParams.update({
                "figure.dpi": 150,
                "savefig.dpi": 300,
                "axes.titlesize": 14,
                "axes.labelsize": 12,
                "xtick.labelsize": 10,
                "ytick.labelsize": 10,
                "legend.fontsize": 10,
            })
        except ImportError as exc:
            raise SystemExit(
                "ERROR: matplotlib is required.  Install with:  pip install matplotlib"
            ) from exc
        _plt = plt_mod
    return _plt


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════════════

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Final evaluation: run models against the TEST_QUERIES dataset, "
            "compute metrics from real pipeline outputs, and generate "
            "publication-quality graphs."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              # Run live evaluation on all available models
              python final_evaluation.py

              # Evaluate specific models only
              python final_evaluation.py --models phi3 groq-llama3-8b

              # Custom retrieval mode and embedding
              python final_evaluation.py --retrieval hybrid --embedding bge-small

              # Load from a pre-computed CSV/JSON instead of running live
              python final_evaluation.py --input results/final_metrics.csv

              # Custom output directory
              python final_evaluation.py --output-dir my_eval
        """),
    )
    parser.add_argument(
        "--input",
        default=None,
        help=(
            "Input CSV or JSON file with pre-computed per-model metrics. "
            "When provided, skips live evaluation and uses these values directly."
        ),
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=None,
        help=(
            "Model names to evaluate (default: all available models from "
            "research_config.MODELS_TO_EVALUATE). Example: --models phi3 groq-llama3-8b"
        ),
    )
    parser.add_argument(
        "--retrieval",
        default="hybrid",
        choices=["vector_only", "bm25_only", "hybrid"],
        help="Retrieval mode for live evaluation (default: hybrid).",
    )
    parser.add_argument(
        "--embedding",
        default=DEFAULT_EMBEDDING,
        help=f"Embedding model for live evaluation (default: {DEFAULT_EMBEDDING}).",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for output CSV + PNG graphs (default: %(default)s).",
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
#  Live evaluation — run models against TEST_QUERIES dataset
# ═══════════════════════════════════════════════════════════════════════════════

def _run_live_evaluation(
    models: list[str],
    retrieval_mode: str,
    embedding_name: str,
):
    """
    Run each model through the RAG pipeline on TEST_QUERIES and compute
    real metrics.  Returns a pandas DataFrame with one row per model.

    All metrics are computed from actual pipeline outputs — no hardcoded
    or sample values.
    """
    pd = _require_pandas()

    rows: list[dict] = []
    for model_name in models:
        if not ResearchEvaluator._is_model_available(model_name):
            print(f"  [Skip] Model '{model_name}' not available.")
            continue

        print(f"\n{'=' * 60}")
        print(f"  Evaluating: {model_name}  |  Embedding: {embedding_name}"
              f"  |  Retrieval: {retrieval_mode}")
        print(f"{'=' * 60}")

        evaluator = ResearchEvaluator(
            model=model_name,
            retrieval_mode=retrieval_mode,
            embedding_name=embedding_name,
        )
        results = evaluator.run_experiment()
        summary = evaluator.compute_summary()
        tok = compute_token_summary(results)

        # Look up model type from registry
        cfg = get_model_config(model_name) or {}
        model_type = cfg.get("type", "unknown")

        # Extract avg evaluation metrics computed from real pipeline outputs.
        # These come from evaluation.py's compute_all_metrics() which is
        # called inside RAGPipeline.run() for every query.
        avg_metrics = summary.get("avg_metrics", {})

        faithfulness = avg_metrics.get("Faithfulness", 0.0)
        answer_relevance = avg_metrics.get("Answer Relevance", 0.0)
        context_precision = avg_metrics.get("Context Relevance", 0.0)
        # Use Recall@5 as context_recall (from evaluation.py recall_at_k)
        context_recall = avg_metrics.get("Recall@5", 0.0)

        rows.append({
            "model": model_name,
            "model_type": model_type,
            "faithfulness": round(faithfulness, 4),
            "answer_relevance": round(answer_relevance, 4),
            "context_precision": round(context_precision, 4),
            "context_recall": round(context_recall, 4),
            "cost_per_query": round(tok["avg_cost_per_query"], 8),
            "avg_input_tokens": round(tok["avg_input_per_query"], 1),
            "avg_output_tokens": round(tok["avg_output_per_query"], 1),
            "avg_total_tokens": round(tok["avg_total_per_query"], 1),
            "latency_ms": round(summary["avg_latency_ms"], 1),
            "topic_accuracy": round(summary["topic_accuracy"], 4),
            "mode_accuracy": round(summary["mode_accuracy"], 4),
        })

        print(f"  ✓ {model_name}: faith={faithfulness:.3f}"
              f"  ans_rel={answer_relevance:.3f}"
              f"  ctx_prec={context_precision:.3f}"
              f"  ctx_rec={context_recall:.3f}"
              f"  cost/q=${tok['avg_cost_per_query']:.6f}"
              f"  latency={summary['avg_latency_ms']:.0f}ms")

    if not rows:
        raise SystemExit(
            "ERROR: No models were available for evaluation.\n"
            "  Ensure Ollama is running (for SLM models) or API keys are set "
            "(GROQ_API_KEY, OPENAI_API_KEY, etc.)."
        )

    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════════
#  Data loading
# ═══════════════════════════════════════════════════════════════════════════════

def _load_metrics(path: Path):
    """Load metrics from CSV or JSON into a pandas DataFrame."""
    pd = _require_pandas()

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}\n"
            "  Provide --input with a valid CSV/JSON file, or run without\n"
            "  --input to perform live evaluation against the dataset."
        )

    suffix = path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        df = pd.DataFrame(payload)
    elif suffix in (".csv", ".tsv"):
        df = pd.read_csv(path)
    else:
        # Try CSV first
        df = pd.read_csv(path)

    # Validate required columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"  Expected: {', '.join(REQUIRED_COLUMNS)}\n"
            "  Run without --input for live evaluation instead."
        )

    return df


# ═══════════════════════════════════════════════════════════════════════════════
#  Core evaluation logic
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_results(df):
    """
    Compute derived metrics and a weighted final score for each model.

    Adds the following columns:
        hallucination_rate   = 1 - faithfulness
        cost_per_token       = cost_per_query / avg_total_tokens  (or 0.0)
        cost_efficiency      = min_cost / cost  (normalized, 1 = cheapest)
        final_score          = weighted combination of all metrics

    Returns a new DataFrame sorted by final_score descending.
    """
    pd = _require_pandas()
    out = df.copy()

    # Coerce metric columns to numeric
    for col in METRIC_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)

    # ── Hallucination rate ────────────────────────────────────────────────────
    out["hallucination_rate"] = (1.0 - out["faithfulness"]).clip(lower=0.0, upper=1.0)

    # ── Per-token cost ────────────────────────────────────────────────────────
    if "avg_total_tokens" in out.columns:
        out["avg_total_tokens"] = pd.to_numeric(
            out["avg_total_tokens"], errors="coerce"
        ).fillna(0.0)
        out["cost_per_token"] = out.apply(
            lambda r: (
                r["cost_per_query"] / r["avg_total_tokens"]
                if r["avg_total_tokens"] > EPSILON
                else 0.0
            ),
            axis=1,
        )
    else:
        out["cost_per_token"] = 0.0

    # ── Optional numeric columns ──────────────────────────────────────────────
    for opt_col in ["avg_input_tokens", "avg_output_tokens", "avg_total_tokens",
                    "latency_ms", "topic_accuracy", "mode_accuracy"]:
        if opt_col in out.columns:
            out[opt_col] = pd.to_numeric(out[opt_col], errors="coerce").fillna(0.0)

    # ── Cost efficiency (normalized) ──────────────────────────────────────────
    all_zero_cost = (out["cost_per_query"] <= EPSILON).all()
    if all_zero_cost:
        out["cost_efficiency"] = 1.0
        effective_cost_weight = 0.0
    else:
        min_cost = max(out["cost_per_query"].min(), EPSILON)
        out["cost_efficiency"] = min_cost / out["cost_per_query"].clip(lower=EPSILON)
        effective_cost_weight = COST_EFFICIENCY_WEIGHT

    # ── Final weighted score ──────────────────────────────────────────────────
    out["final_score"] = (
        FAITHFULNESS_WEIGHT * out["faithfulness"]
        + ANSWER_RELEVANCE_WEIGHT * out["answer_relevance"]
        + CONTEXT_PRECISION_WEIGHT * out["context_precision"]
        + CONTEXT_RECALL_WEIGHT * out["context_recall"]
        + effective_cost_weight * out["cost_efficiency"]
        - HALLUCINATION_PENALTY_WEIGHT * out["hallucination_rate"]
    )

    return out.sort_values(by="final_score", ascending=False).reset_index(drop=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  Graph generation  (8 charts)
# ═══════════════════════════════════════════════════════════════════════════════

def _model_colors(df):
    """Assign colours based on model_type column if present."""
    plt = _require_matplotlib()
    if "model_type" not in df.columns:
        return ["#4F81BD"] * len(df)
    cmap = {"SLM": "#4F81BD", "LLM": "#C0504D"}
    return [cmap.get(t, "#9BBB59") for t in df["model_type"]]


def _save_graphs(df, output_dir: Path) -> list[Path]:
    """Generate all evaluation graphs and return list of created file paths."""
    plt = _require_matplotlib()
    import numpy as np

    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    models = df["model"].tolist()
    n = len(models)
    colors = _model_colors(df)

    # ── 1. Final score by model ───────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(max(8, n * 0.9), 5))
    bars = ax.bar(models, df["final_score"], color=colors)
    ax.set_title("Final Evaluation Score by Model")
    ax.set_ylabel("Final Score")
    ax.set_ylim(0, 1.05)
    for bar, val in zip(bars, df["final_score"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.3f}", ha="center", va="bottom", fontsize=8)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    p = output_dir / "01_final_score_by_model.png"
    plt.savefig(p)
    plt.close()
    created.append(p)

    # ── 2. Five-metric grouped bar chart ──────────────────────────────────────
    metric_labels = ["Faithfulness", "Answer\nRelevance", "Context\nPrecision",
                     "Context\nRecall", "Hallucination\nRate"]
    metric_keys = ["faithfulness", "answer_relevance", "context_precision",
                   "context_recall", "hallucination_rate"]
    x = np.arange(n)
    width = 0.15
    fig, ax = plt.subplots(figsize=(max(10, n * 1.2), 6))
    palette = ["#4F81BD", "#9BBB59", "#F79646", "#8064A2", "#C0504D"]
    for i, (key, label, col) in enumerate(zip(metric_keys, metric_labels, palette)):
        offset = (i - 2) * width
        ax.bar(x + offset, df[key], width=width, label=label, color=col)
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=35, ha="right")
    ax.set_ylabel("Score (0–1)")
    ax.set_title("5-Metric Comparison Across Models")
    ax.set_ylim(0, 1.15)
    ax.legend(loc="upper right", fontsize=8, ncol=3)
    plt.tight_layout()
    p = output_dir / "02_five_metrics_comparison.png"
    plt.savefig(p)
    plt.close()
    created.append(p)

    # ── 3. Cost per query ─────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(max(8, n * 0.9), 5))
    bars = ax.bar(models, df["cost_per_query"], color="#8064A2")
    ax.set_title("Cost per Query by Model")
    ax.set_ylabel("USD / query")
    for bar, val in zip(bars, df["cost_per_query"]):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ax.get_ylim()[1] * 0.01,
                    f"${val:.6f}", ha="center", va="bottom", fontsize=7, rotation=45)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    p = output_dir / "03_cost_per_query.png"
    plt.savefig(p)
    plt.close()
    created.append(p)

    # ── 4. Cost per token ─────────────────────────────────────────────────────
    if "cost_per_token" in df.columns and df["cost_per_token"].sum() > 0:
        fig, ax = plt.subplots(figsize=(max(8, n * 0.9), 5))
        bars = ax.bar(models, df["cost_per_token"], color="#4BACC6")
        ax.set_title("Cost per Token by Model")
        ax.set_ylabel("USD / token")
        for bar, val in zip(bars, df["cost_per_token"]):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ax.get_ylim()[1] * 0.01,
                        f"${val:.8f}", ha="center", va="bottom", fontsize=7, rotation=45)
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()
        p = output_dir / "04_cost_per_token.png"
        plt.savefig(p)
        plt.close()
        created.append(p)

    # ── 5. Hallucination rate ─────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(max(8, n * 0.9), 5))
    bars = ax.bar(models, df["hallucination_rate"] * 100, color="#C0504D")
    ax.set_title("Hallucination Rate by Model")
    ax.set_ylabel("Hallucination Rate (%)")
    ax.set_ylim(0, 105)
    for bar, val in zip(bars, df["hallucination_rate"] * 100):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=8)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    p = output_dir / "05_hallucination_rate.png"
    plt.savefig(p)
    plt.close()
    created.append(p)

    # ── 6. Avg tokens: input vs output (grouped bar) ─────────────────────────
    has_tokens = ("avg_input_tokens" in df.columns and "avg_output_tokens" in df.columns
                  and df["avg_input_tokens"].sum() > 0)
    if has_tokens:
        fig, ax = plt.subplots(figsize=(max(8, n * 0.9), 5))
        w = 0.35
        ax.bar(x - w / 2, df["avg_input_tokens"], width=w,
               label="Avg Input Tokens", color="#4BACC6")
        ax.bar(x + w / 2, df["avg_output_tokens"], width=w,
               label="Avg Output Tokens", color="#C0504D")
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=35, ha="right")
        ax.set_ylabel("Tokens / query")
        ax.set_title("Average Token Usage — Input vs Output")
        ax.legend()
        plt.tight_layout()
        p = output_dir / "06_avg_tokens_input_vs_output.png"
        plt.savefig(p)
        plt.close()
        created.append(p)

    # ── 7. Latency vs Accuracy scatter ────────────────────────────────────────
    has_scatter = ("latency_ms" in df.columns and "topic_accuracy" in df.columns
                   and df["latency_ms"].sum() > 0)
    if has_scatter:
        fig, ax = plt.subplots(figsize=(8, 6))
        sc = ax.scatter(df["latency_ms"], df["topic_accuracy"] * 100,
                        c=range(n), cmap="viridis", s=100, alpha=0.9,
                        edgecolors="black", linewidths=0.5)
        for i, name in enumerate(models):
            ax.annotate(name, (df["latency_ms"].iloc[i], df["topic_accuracy"].iloc[i] * 100),
                        xytext=(6, 4), textcoords="offset points", fontsize=8)
        ax.set_xlabel("Latency (ms)")
        ax.set_ylabel("Topic Accuracy (%)")
        ax.set_title("Latency vs Topic Accuracy")
        plt.tight_layout()
        p = output_dir / "07_latency_vs_accuracy.png"
        plt.savefig(p)
        plt.close()
        created.append(p)

    # ── 8. Radar / spider chart (normalized quality metrics) ──────────────────
    radar_keys = [k for k in QUALITY_METRICS if k in df.columns]
    if len(radar_keys) >= 3 and n <= 12:
        labels = [k.replace("_", "\n") for k in radar_keys]
        num_vars = len(radar_keys)
        angles = [i / float(num_vars) * 2 * math.pi for i in range(num_vars)]
        angles += angles[:1]  # close the polygon

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        radar_colors = plt.cm.tab10(np.linspace(0, 1, min(n, 10)))
        for idx in range(min(n, 8)):  # limit to 8 models for readability
            values = [float(df[k].iloc[idx]) for k in radar_keys]
            values += values[:1]
            ax.plot(angles, values, "o-", linewidth=1.5,
                    label=models[idx], color=radar_colors[idx % 10])
            ax.fill(angles, values, alpha=0.08, color=radar_colors[idx % 10])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylim(0, 1.05)
        ax.set_title("Quality Metrics Radar — Model Comparison", y=1.08)
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=8)
        plt.tight_layout()
        p = output_dir / "08_radar_quality_metrics.png"
        plt.savefig(p, bbox_inches="tight")
        plt.close()
        created.append(p)

    return created


# ═══════════════════════════════════════════════════════════════════════════════
#  Console output
# ═══════════════════════════════════════════════════════════════════════════════

def _print_table(df) -> None:
    """Print a readable evaluation table to stdout."""
    pd = _require_pandas()

    print("\n" + "═" * 100)
    print("  FINAL MODEL EVALUATION — 5 Metrics + Per-Token Cost")
    print("═" * 100)

    # Core display columns
    cols = ["model"]
    for c in ["model_type", "faithfulness", "answer_relevance", "context_precision",
              "context_recall", "hallucination_rate", "cost_per_query",
              "cost_per_token", "final_score"]:
        if c in df.columns:
            cols.append(c)

    display = df[cols].copy()

    # Format numeric columns for display
    fmt_map = {
        "faithfulness": "{:.4f}",
        "answer_relevance": "{:.4f}",
        "context_precision": "{:.4f}",
        "context_recall": "{:.4f}",
        "hallucination_rate": "{:.4f}",
        "cost_per_query": "${:.8f}",
        "cost_per_token": "${:.10f}",
        "final_score": "{:.4f}",
    }
    for col, fmt in fmt_map.items():
        if col in display.columns:
            display[col] = display[col].map(lambda v, f=fmt: f.format(v))

    print(display.to_string(index=False))

    # Winner summary
    best_idx = df["final_score"].idxmax()
    best_model = df.loc[best_idx, "model"]
    best_score = df.loc[best_idx, "final_score"]
    print(f"\n  🏆 Best model: {best_model}  (final_score = {best_score:.4f})")

    # Print per-metric winners
    for metric in QUALITY_METRICS:
        best_m_idx = df[metric].idxmax()
        print(f"     Best {metric}: {df.loc[best_m_idx, 'model']} ({df.loc[best_m_idx, metric]:.4f})")

    if df["cost_per_query"].sum() > 0:
        cheapest_idx = df.loc[df["cost_per_query"] > 0, "cost_per_query"].idxmin()
        if cheapest_idx is not None:
            print(f"     Cheapest (non-free): {df.loc[cheapest_idx, 'model']} "
                  f"(${df.loc[cheapest_idx, 'cost_per_query']:.8f}/query)")

    free_models = df.loc[df["cost_per_query"] <= EPSILON, "model"].tolist()
    if free_models:
        print(f"     Free models: {', '.join(free_models)}")

    print("═" * 100)


# ═══════════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    args = _parse_args()

    pd = _require_pandas()
    output_dir = Path(args.output_dir)

    # Decide data source: --input (pre-computed CSV/JSON) or live evaluation
    if args.input is not None:
        # Load from pre-computed file
        input_path = Path(args.input)
        raw = _load_metrics(input_path)
        print(f"Loaded {len(raw)} model entries from: {input_path}")
    else:
        # Run live evaluation against TEST_QUERIES dataset
        models = args.models if args.models else MODELS_TO_EVALUATE
        print(f"Running live evaluation on {len(TEST_QUERIES)} test queries...")
        print(f"Models: {models}")
        print(f"Retrieval: {args.retrieval} | Embedding: {args.embedding}")
        raw = _run_live_evaluation(
            models=models,
            retrieval_mode=args.retrieval,
            embedding_name=args.embedding,
        )
        # Save the computed metrics CSV for reproducibility
        output_dir.mkdir(parents=True, exist_ok=True)
        metrics_csv = output_dir / "computed_metrics.csv"
        raw.to_csv(metrics_csv, index=False)
        print(f"\n✓ Saved computed metrics to: {metrics_csv}")

    ranked = evaluate_results(raw)

    # Save CSV
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_out = output_dir / "final_evaluation_results.csv"
    ranked.to_csv(csv_out, index=False)
    print(f"✓ Saved ranked results CSV: {csv_out}")

    # Print console table
    _print_table(ranked)

    # Generate graphs
    created = _save_graphs(ranked, output_dir)
    if created:
        print(f"\n✓ Generated {len(created)} graphs in: {output_dir}")
        for p in created:
            print(f"    • {p.name}")
    else:
        print("\n⚠ No graphs were generated.")

    # Save a summary text report
    report_path = output_dir / "evaluation_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        if args.input is not None:
            f.write(f"FINAL MODEL EVALUATION REPORT\n")
            f.write(f"Data source: {args.input}\n")
        else:
            f.write(f"FINAL MODEL EVALUATION REPORT\n")
            f.write(f"Data source: live evaluation (TEST_QUERIES dataset)\n")
            f.write(f"Retrieval mode: {args.retrieval}\n")
            f.write(f"Embedding: {args.embedding}\n")
            f.write(f"Test queries: {len(TEST_QUERIES)}\n")
        f.write(f"Models evaluated: {len(ranked)}\n")
        f.write("=" * 80 + "\n\n")

        f.write("RANKING (by weighted final score):\n")
        f.write("-" * 80 + "\n")
        for i, row in ranked.iterrows():
            f.write(f"  #{i+1}  {row['model']:<20}  final_score={row['final_score']:.4f}"
                    f"  faith={row['faithfulness']:.4f}"
                    f"  ans_rel={row['answer_relevance']:.4f}"
                    f"  ctx_prec={row['context_precision']:.4f}"
                    f"  ctx_rec={row['context_recall']:.4f}"
                    f"  halluc={row['hallucination_rate']:.4f}"
                    f"  cost/q=${row['cost_per_query']:.8f}"
                    f"  cost/tok=${row['cost_per_token']:.10f}\n")
        f.write("=" * 80 + "\n\n")

        f.write("METRIC WEIGHTS:\n")
        f.write(f"  Faithfulness:          {FAITHFULNESS_WEIGHT}\n")
        f.write(f"  Answer Relevance:      {ANSWER_RELEVANCE_WEIGHT}\n")
        f.write(f"  Context Precision:     {CONTEXT_PRECISION_WEIGHT}\n")
        f.write(f"  Context Recall:        {CONTEXT_RECALL_WEIGHT}\n")
        f.write(f"  Cost Efficiency:       {COST_EFFICIENCY_WEIGHT}\n")
        f.write(f"  Hallucination Penalty: {HALLUCINATION_PENALTY_WEIGHT}\n")
        f.write("\n")

        f.write("GRAPHS GENERATED:\n")
        for p in created:
            f.write(f"  • {p.name}\n")

    print(f"✓ Saved text report: {report_path}")


if __name__ == "__main__":
    main()
