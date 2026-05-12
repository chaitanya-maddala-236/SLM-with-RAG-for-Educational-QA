from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from project.app.evaluation.ablation import run_ablation
from project.app.evaluation.runner import EvaluationRunner
from project.app.rag.pipeline import EduSLMRAGPipeline


def load_dataset(path: str) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run EduSLM-RAG evaluations")
    parser.add_argument("--dataset", required=True, help="Path to JSON dataset")
    parser.add_argument("--mode", choices=["single", "ablation"], default="single")
    parser.add_argument("--model", default="tinyllama")
    parser.add_argument("--output-dir", default="project/experiments/outputs")
    args = parser.parse_args()

    dataset = load_dataset(args.dataset)

    if args.mode == "ablation":
        await run_ablation(dataset, output_dir=args.output_dir)
        return

    pipeline = EduSLMRAGPipeline(model_key=args.model)
    runner = EvaluationRunner(pipeline, output_dir=args.output_dir)
    await runner.run(dataset, experiment_name=f"single_{args.model}")


if __name__ == "__main__":
    asyncio.run(main())
