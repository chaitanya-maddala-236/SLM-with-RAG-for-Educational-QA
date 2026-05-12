from __future__ import annotations

import itertools
import json
from pathlib import Path
from statistics import mean
from typing import Any

import matplotlib.pyplot as plt

from project.app.config.loader import load_settings
from project.app.rag.pipeline import EduSLMRAGPipeline
from project.app.evaluation.runner import EvaluationRunner


def ablation_grid() -> list[dict[str, Any]]:
    hyde_opts = [False, True]
    retrieval_opts = ["bm25_only", "hybrid_rrf"]
    packing_opts = ["topk", "mmr"]
    rows = []
    for hyde, retrieval, packing in itertools.product(hyde_opts, retrieval_opts, packing_opts):
        rows.append({"hyde": hyde, "retrieval": retrieval, "packing": packing})
    return rows


async def run_ablation(dataset: list[dict[str, Any]], output_dir: str = "project/experiments/outputs") -> list[dict[str, Any]]:
    settings = load_settings()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for cfg in ablation_grid():
        settings.retrieval.hyde_enabled = cfg["hyde"]
        if cfg["retrieval"] == "bm25_only":
            settings.retrieval.dense_weight = 0.0
            settings.retrieval.bm25_weight = 1.0
        else:
            settings.retrieval.dense_weight = 0.6
            settings.retrieval.bm25_weight = 0.4

        settings.retrieval.mmr_lambda = 0.7 if cfg["packing"] == "mmr" else 1.0
        pipeline = EduSLMRAGPipeline(settings=settings)
        runner = EvaluationRunner(pipeline, output_dir=output_dir)
        exp_name = f"hyde_{int(cfg['hyde'])}_{cfg['retrieval']}_{cfg['packing']}"
        rows = await runner.run(dataset, experiment_name=exp_name)

        summary = {
            **cfg,
            "mean_precision@k": mean(r["precision@k"] for r in rows) if rows else 0.0,
            "mean_recall@k": mean(r["recall@k"] for r in rows) if rows else 0.0,
            "mean_mrr": mean(r["mrr"] for r in rows) if rows else 0.0,
            "mean_ndcg@k": mean(r["ndcg@k"] for r in rows) if rows else 0.0,
            "mean_latency_s": mean(r["latency_s"] for r in rows) if rows else 0.0,
            "mean_bertscore_f1": mean(r["bertscore_f1"] for r in rows if r["bertscore_f1"] is not None) if rows else 0.0,
        }
        results.append(summary)

    with (output_path / "ablation_summary.json").open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    _plot_ablation(results, output_path)
    return results


def _plot_ablation(results: list[dict[str, Any]], output_dir: Path) -> None:
    labels = [f"H{int(r['hyde'])}-{r['retrieval']}-{r['packing']}" for r in results]
    scores = [r["mean_ndcg@k"] for r in results]

    plt.figure(figsize=(12, 5))
    plt.bar(labels, scores)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Mean NDCG@K")
    plt.title("2x2x2 Ablation Comparison")
    plt.tight_layout()
    plt.savefig(output_dir / "ablation_ndcg.png")
    plt.close()
