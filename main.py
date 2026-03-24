"""
main.py
-------
Command-line entry point for the RAG system.
Runs a demo conversation demonstrating ambiguity resolution and context tracking,
then prints evaluation metrics.

Usage:
    python main.py
"""

from retriever import build_vector_store
from rag_pipeline import RAGPipeline
from context_memory import ConversationMemory
from evaluation import format_metrics_table

DEMO_QUERIES = [
    "Explain water cycle",
    "What is cycle?",           # should infer water cycle from memory
    "How does a cycle move?",   # should detect intent shift → bicycle
    "How does photosynthesis work?",
    "What is the Calvin cycle?",
    "Explain bicycle gears",
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

    all_metrics: list[dict] = []

    for i, query in enumerate(DEMO_QUERIES, 1):
        print(f"\n{SEPARATOR}")
        print(f"  DEMO QUERY {i}/{len(DEMO_QUERIES)}: '{query}'")
        print(SEPARATOR)

        result = pipeline.run(user_query=query, memory=memory)

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


if __name__ == "__main__":
    run_demo()
