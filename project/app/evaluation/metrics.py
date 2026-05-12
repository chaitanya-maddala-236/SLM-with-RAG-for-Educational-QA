from __future__ import annotations

import math
from typing import Sequence


def precision_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    top = retrieved[:k]
    if not top:
        return 0.0
    return sum(1 for d in top if d in relevant) / len(top)


def recall_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 0.0
    top = retrieved[:k]
    return sum(1 for d in top if d in relevant) / len(relevant)


def mrr(retrieved: Sequence[str], relevant: set[str]) -> float:
    for i, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at_k(retrieved: Sequence[str], relevant: set[str], k: int) -> float:
    dcg = 0.0
    for i, doc in enumerate(retrieved[:k], start=1):
        rel = 1.0 if doc in relevant else 0.0
        dcg += rel / math.log2(i + 1)
    ideal_hits = min(len(relevant), k)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 0.0


def bertscore_f1(prediction: str, reference: str) -> float | None:
    try:
        from bert_score import score  # type: ignore

        _, _, f1 = score([prediction], [reference], lang="en", verbose=False)
        return float(f1.mean().item())
    except Exception:
        return None


def ragas_metrics(sample: dict) -> dict[str, float | None]:
    try:
        from datasets import Dataset  # type: ignore
        from ragas import evaluate  # type: ignore
        from ragas.metrics import (
            answer_relevancy,
            context_precision,
            context_recall,
            faithfulness,
        )

        ds = Dataset.from_list([sample])
        result = evaluate(ds, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
        return {
            "ragas_faithfulness": float(result["faithfulness"]),
            "ragas_answer_relevancy": float(result["answer_relevancy"]),
            "ragas_context_precision": float(result["context_precision"]),
            "ragas_context_recall": float(result["context_recall"]),
        }
    except Exception:
        return {
            "ragas_faithfulness": None,
            "ragas_answer_relevancy": None,
            "ragas_context_precision": None,
            "ragas_context_recall": None,
        }
