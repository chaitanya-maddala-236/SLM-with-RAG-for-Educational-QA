"""
final_evaluation.py
-------------------
Final model-evaluation utility for multimodal RAG experiments.

Outputs:
  1) A model-vs-metrics table with:
     - Faithfulness
     - Answer Relevance
     - Context Precision
     - Context Recall
     - Cost per query
  2) A weighted final score ranking
  3) Graphs for quick comparison

Input formats:
  - CSV with columns:
      model,faithfulness,answer_relevance,context_precision,context_recall,cost_per_query[,avg_output_tokens]
  - JSON list of the same objects
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("results/final_evaluation")
DEFAULT_INPUT = Path("results/final_metrics.csv")
METRIC_COLUMNS = [
    "faithfulness",
    "answer_relevance",
    "context_precision",
    "context_recall",
    "cost_per_query",
]
# Small floor value used to avoid divide-by-zero in cost normalization.
EPSILON = 1e-9
FAITHFULNESS_WEIGHT = 0.28
ANSWER_RELEVANCE_WEIGHT = 0.24
CONTEXT_PRECISION_WEIGHT = 0.18
CONTEXT_RECALL_WEIGHT = 0.15
COST_EFFICIENCY_WEIGHT = 0.15
OUTPUT_TOKEN_WEIGHT = 0.05

_PD = None


def _require_pandas():
    global _PD
    if _PD is None:
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for final evaluation. Install with: pip install pandas"
            ) from exc
        _PD = pd
    return _PD


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run final evaluation table + graphs for multimodal RAG models."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Input CSV/JSON path with per-model metrics.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for final evaluation outputs.",
    )
    return parser.parse_args()


def _load_metrics(path: Path) -> "pd.DataFrame":
    pd = _require_pandas()

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}. "
            "Provide --input with CSV/JSON model metrics."
        )

    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        df = pd.DataFrame(payload)
    else:
        df = pd.read_csv(path)

    missing = [c for c in ["model", *METRIC_COLUMNS] if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. "
            "Expected: model, faithfulness, answer_relevance, context_precision, "
            "context_recall, cost_per_query."
        )
    return df


def evaluate_results(df: "pd.DataFrame") -> "pd.DataFrame":
    pd = _require_pandas()
    out = df.copy()
    for col in METRIC_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0.0)

    all_zero_cost = bool((out["cost_per_query"] <= EPSILON).all())
    if all_zero_cost:
        out["cost_efficiency"] = 1.0
        effective_cost_weight = 0.0
    else:
        min_cost = max(out["cost_per_query"].min(), EPSILON)
        out["cost_efficiency"] = min_cost / out["cost_per_query"].clip(lower=EPSILON)
        effective_cost_weight = COST_EFFICIENCY_WEIGHT

    if "avg_output_tokens" in out.columns:
        out["avg_output_tokens"] = pd.to_numeric(
            out["avg_output_tokens"], errors="coerce"
        ).fillna(0.0)
        max_out = max(out["avg_output_tokens"].max(), EPSILON)
        out["output_token_score"] = out["avg_output_tokens"] / max_out
        token_weight = OUTPUT_TOKEN_WEIGHT
    else:
        out["output_token_score"] = 0.0
        token_weight = 0.0

    out["final_score"] = (
        FAITHFULNESS_WEIGHT * out["faithfulness"]
        + ANSWER_RELEVANCE_WEIGHT * out["answer_relevance"]
        + CONTEXT_PRECISION_WEIGHT * out["context_precision"]
        + CONTEXT_RECALL_WEIGHT * out["context_recall"]
        + effective_cost_weight * out["cost_efficiency"]
        + token_weight * out["output_token_score"]
    )
    return out.sort_values(by="final_score", ascending=False).reset_index(drop=True)


def _save_graphs(df: "pd.DataFrame", output_dir: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for graph generation. Install with: pip install matplotlib"
        ) from exc

    output_dir.mkdir(parents=True, exist_ok=True)

    # Graph 1: Final score by model
    plt.figure(figsize=(max(8, len(df) * 0.8), 5))
    plt.bar(df["model"], df["final_score"], color="#4F81BD")
    plt.title("Final Evaluation Score by Model")
    plt.ylabel("Final Score")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "final_score_by_model.png", dpi=300)
    plt.close()

    # Graph 2: Metrics comparison (excluding cost)
    plt.figure(figsize=(max(8, len(df) * 0.9), 5))
    x = range(len(df))
    width = 0.18
    plt.bar([i - 1.5 * width for i in x], df["faithfulness"], width=width, label="Faithfulness")
    plt.bar([i - 0.5 * width for i in x], df["answer_relevance"], width=width, label="Answer Relevance")
    plt.bar([i + 0.5 * width for i in x], df["context_precision"], width=width, label="Context Precision")
    plt.bar([i + 1.5 * width for i in x], df["context_recall"], width=width, label="Context Recall")
    plt.xticks(list(x), df["model"], rotation=35, ha="right")
    plt.ylabel("Score")
    plt.title("Final Evaluation Metrics by Model")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "metrics_by_model.png", dpi=300)
    plt.close()

    # Graph 3: Cost per query
    plt.figure(figsize=(max(8, len(df) * 0.8), 5))
    plt.bar(df["model"], df["cost_per_query"], color="#8064A2")
    plt.title("Cost per Query by Model")
    plt.ylabel("USD / query")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "cost_per_query_by_model.png", dpi=300)
    plt.close()


def main() -> None:
    args = _parse_args()
    _require_pandas()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    raw = _load_metrics(input_path)
    ranked = evaluate_results(raw)

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_out = output_dir / "final_evaluation_results.csv"
    ranked.to_csv(csv_out, index=False)

    table_cols = [
        "model",
        "faithfulness",
        "answer_relevance",
        "context_precision",
        "context_recall",
        "cost_per_query",
        "final_score",
    ]
    if "avg_output_tokens" in ranked.columns:
        table_cols.insert(6, "avg_output_tokens")

    print("\nFINAL EVALUATION TABLE")
    print(ranked[table_cols].to_string(index=False))
    print(f"\nSaved table: {csv_out}")

    _save_graphs(ranked, output_dir)
    print(f"Saved graphs to: {output_dir}")


if __name__ == "__main__":
    main()
