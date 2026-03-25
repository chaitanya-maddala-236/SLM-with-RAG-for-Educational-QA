"""
main.py
-------
Command-line entry point for the RAG system.
Runs a demo conversation demonstrating ambiguity resolution and context tracking,
then prints evaluation metrics.

Usage:
    python main.py              # demo mode (default)
    python main.py --ablation   # ablation study: vector vs BM25 vs hybrid
"""

import argparse

from retriever import build_vector_store
from rag_pipeline import RAGPipeline
from context_memory import ConversationMemory
from topic_memory_manager import TopicMemoryManager
from evaluation import format_metrics_table

DEMO_QUERIES = [
    "Explain water cycle",
    "What is cycle?",           # should infer water cycle from memory
    "How does a cycle move?",   # should detect intent shift → bicycle
    "How does photosynthesis work?",
    "What is the Calvin cycle?",
    "Explain bicycle gears",
]

# Research addition: queries used for the ablation study
ABLATION_QUERIES = [
    "Explain the water cycle",
    "How does photosynthesis work?",
    "What is cellular respiration?",
    "Explain the carbon cycle",
    "How does the nervous system work?",
]

SEPARATOR = "=" * 70


def run_demo() -> None:
    print(SEPARATOR)
    print("  Educational Conversational RAG System — Demo Mode")
    print("  SLM: Phi-3 via Ollama  |  Embeddings: BGE  |  DB: Chroma")
    print(SEPARATOR)

    print("\n[Init] Building vector store …")
    vector_store = build_vector_store(persist=True)

    print("[Init] Loading RAG pipeline …")
    pipeline = RAGPipeline(vector_store=vector_store, model_name="phi3", top_k=5)

    memory = ConversationMemory(max_turns=5)
    topic_manager = TopicMemoryManager()

    all_metrics: list[dict] = []

    for i, query in enumerate(DEMO_QUERIES, 1):
        print(f"\n{SEPARATOR}")
        print(f"  DEMO QUERY {i}/{len(DEMO_QUERIES)}: '{query}'")
        print(SEPARATOR)

        result = pipeline.run(user_query=query, memory=memory,
                              topic_manager=topic_manager)

        if result.clarification_needed:
            print(f"\n  ⚠ Clarification requested: {result.clarification_message}")
        else:
            print(f"\n  📝 ANSWER:\n{result.answer}\n")

        if result.metrics:
            all_metrics.append(result.metrics)
            print("\n  Metrics for this query:")
            print(format_metrics_table(result.metrics))

    # Average metrics across all queries
    if all_metrics:
        avg_metrics = {
            key: round(sum(m[key] for m in all_metrics) / len(all_metrics), 3)
            for key in all_metrics[0]
        }
        print(f"\n{SEPARATOR}")
        print("  AVERAGE EVALUATION METRICS (all demo queries)")
        print(SEPARATOR)
        print(format_metrics_table(avg_metrics))

    print(f"\n{SEPARATOR}")
    print("  Demo complete. Run 'streamlit run app.py' for the interactive UI.")
    print(SEPARATOR)


# Research addition: ablation study comparing vector-only, BM25-only, hybrid retrieval
def run_ablation_study() -> None:
    """
    Run the same set of queries under three retrieval modes and print a
    comparison table of average evaluation metrics:
      a) vector-only  — BM25 index disabled (bm25_index=None)
      b) BM25-only    — vector weight set to 0 (alpha=0.0)
      c) hybrid       — current default (BM25 + vector, alpha=0.5)
    """
    print(SEPARATOR)
    print("  Educational RAG System — Ablation Study Mode")
    print("  Comparing: vector-only | BM25-only | hybrid retrieval")
    print(SEPARATOR)

    print("\n[Init] Building vector store …")
    vector_store = build_vector_store(persist=True)

    # Import the modules whose functions the pipeline calls by reference
    import rag_pipeline as _rag_mod
    from retriever import hybrid_search as _orig_hybrid_search

    # Save the original function reference so we can restore it
    _orig_hierarchical = _rag_mod.hierarchical_retrieve

    def _hierarchical_vector_only(vector_store, bm25_index, query, topic=None, k=5):
        """Stage-1+2 retrieval using vector search only (bm25_index ignored)."""
        return _orig_hybrid_search(
            vector_store=vector_store,
            bm25_index=None,   # disable BM25
            query=query,
            k=k,
            topic_filter=topic,
        )

    def _hierarchical_bm25_only(vector_store, bm25_index, query, topic=None, k=5):
        """Stage-1+2 retrieval using BM25 search only (alpha=0 → pure BM25 ranking)."""
        return _orig_hybrid_search(
            vector_store=vector_store,
            bm25_index=bm25_index,
            query=query,
            k=k,
            alpha=0.0,         # zero vector weight → pure BM25
            topic_filter=topic,
        )

    mode_patches = {
        "vector-only": _hierarchical_vector_only,
        "BM25-only":   _hierarchical_bm25_only,
        "hybrid":      _orig_hierarchical,
    }

    mode_results: dict[str, dict[str, float]] = {}

    for mode_name, patch_fn in mode_patches.items():
        print(f"\n{SEPARATOR}")
        print(f"  MODE: {mode_name}")
        print(SEPARATOR)

        # Patch the function reference used inside rag_pipeline module
        _rag_mod.hierarchical_retrieve = patch_fn

        pipeline = RAGPipeline(vector_store=vector_store, model_name="phi3", top_k=5)

        all_metrics: list[dict] = []
        for query in ABLATION_QUERIES:
            memory = ConversationMemory(max_turns=5)
            topic_manager = TopicMemoryManager()
            try:
                result = pipeline.run(
                    user_query=query,
                    memory=memory,
                    topic_manager=topic_manager,
                )
                if result.metrics:
                    all_metrics.append(result.metrics)
                    print(f"  [{mode_name}] '{query[:40]}' → {result.metrics}")
            except Exception as exc:
                print(f"  [{mode_name}] '{query[:40]}' → ERROR: {exc}")

        if all_metrics:
            avg = {
                key: round(sum(m[key] for m in all_metrics) / len(all_metrics), 3)
                for key in all_metrics[0]
            }
        else:
            avg = {}
        mode_results[mode_name] = avg

    # Restore original function reference
    _rag_mod.hierarchical_retrieve = _orig_hierarchical

    # Print comparison table
    print(f"\n{SEPARATOR}")
    print("  ABLATION STUDY — AVERAGE METRICS COMPARISON")
    print(SEPARATOR)

    if mode_results:
        metric_keys = list(next(iter(mode_results.values())).keys())
        col_w = 22
        header = f"{'Mode':<{col_w}}" + "".join(f"{k:<{col_w}}" for k in metric_keys)
        print(header)
        print("-" * len(header))
        for mode_name, avg in mode_results.items():
            row = f"{mode_name:<{col_w}}" + "".join(
                f"{avg.get(k, 0.0):<{col_w}.3f}" for k in metric_keys
            )
            print(row)

    print(f"\n{SEPARATOR}")
    print("  Ablation study complete.")
    print(SEPARATOR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Educational RAG System — Demo or Ablation Study"
    )
    # Research addition: --ablation flag to trigger ablation study mode
    parser.add_argument(
        "--ablation",
        action="store_true",
        help="Run ablation study comparing vector-only, BM25-only, and hybrid retrieval",
    )
    args = parser.parse_args()

    if args.ablation:
        run_ablation_study()
    else:
        run_demo()
