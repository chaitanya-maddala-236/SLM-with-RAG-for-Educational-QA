from __future__ import annotations

import csv
import json
import logging
import time
import tracemalloc
from dataclasses import asdict
from pathlib import Path
from typing import Any

from project.app.evaluation.metrics import (
    bertscore_f1,
    mrr,
    ndcg_at_k,
    precision_at_k,
    ragas_metrics,
    recall_at_k,
)
from project.app.models.schemas import UserInput
from project.app.rag.pipeline import EduSLMRAGPipeline
from project.app.utils.text import simple_token_count

logger = logging.getLogger(__name__)


class EvaluationRunner:
    def __init__(self, pipeline: EduSLMRAGPipeline, output_dir: str = "project/experiments/outputs") -> None:
        self.pipeline = pipeline
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def run(self, dataset: list[dict[str, Any]], k: int = 5, experiment_name: str = "default") -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for sample in dataset:
            tracemalloc.start()
            start = time.perf_counter()
            response = await self.pipeline.run(
                UserInput(
                    question=sample["question"],
                    chat_history=sample.get("chat_history", []),
                    metadata_filters=sample.get("metadata_filters", {}),
                )
            )
            latency = time.perf_counter() - start
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            retrieved_ids = [d.metadata.get("source", d.doc_id) for d in response.retrieved_docs]
            relevant_ids = set(sample.get("relevant_docs", []))

            row = {
                "question": sample["question"],
                "answer": response.answer,
                "reference_answer": sample.get("reference_answer", ""),
                "precision@k": precision_at_k(retrieved_ids, relevant_ids, k),
                "recall@k": recall_at_k(retrieved_ids, relevant_ids, k),
                "mrr": mrr(retrieved_ids, relevant_ids),
                "ndcg@k": ndcg_at_k(retrieved_ids, relevant_ids, k),
                "bertscore_f1": bertscore_f1(response.answer, sample.get("reference_answer", "")),
                "latency_s": latency,
                "token_usage": simple_token_count(response.context) + simple_token_count(response.answer),
                "memory_peak_mb": peak_memory / (1024 * 1024),
                "retrieval_confidence": response.diagnostics.retrieval_confidence,
                "fallback_level": response.diagnostics.fallback_level,
            }
            row.update(
                ragas_metrics(
                    {
                        "question": sample["question"],
                        "answer": response.answer,
                        "contexts": [d.content for d in response.retrieved_docs],
                        "ground_truth": sample.get("reference_answer", ""),
                    }
                )
            )
            rows.append(row)

        self._export(rows, experiment_name)
        return rows

    def _export(self, rows: list[dict[str, Any]], experiment_name: str) -> None:
        json_path = self.output_dir / f"{experiment_name}.json"
        csv_path = self.output_dir / f"{experiment_name}.csv"

        with json_path.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)

        if rows:
            with csv_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)

        logger.info("Evaluation exported: %s and %s", json_path, csv_path)
