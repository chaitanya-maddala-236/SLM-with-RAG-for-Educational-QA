"""
app.py
------
Streamlit UI for the Educational Conversational RAG System.

Layout:
  ● Left sidebar   – controls (clear conversation, stack info)
  ● Left column    – chat interface (3/5 of page width)
  ● Right column   – pipeline step viewer + evaluation metrics table (2/5)

Run with:
    streamlit run app.py
"""

import streamlit as st
from langchain_community.vectorstores import Chroma

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="EduRAG – Conversational Educational QA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Lazy imports (after set_page_config) ─────────────────────────────────────
from context_memory import ConversationMemory
from topic_memory_manager import TopicMemoryManager
from retriever import build_vector_store
from rag_pipeline import RAGPipeline
from evaluation import format_metrics_table

# ── Cached resources (load once, reuse across reruns) ────────────────────────

@st.cache_resource(show_spinner="🔧 Building vector store (first run only)…")
def load_vector_store() -> Chroma:
    """Load or build the Chroma vector store with BGE embeddings."""
    return build_vector_store(persist=True)


@st.cache_resource(show_spinner="🤖 Connecting to Phi-3 via Ollama…")
def load_pipeline(_vector_store: Chroma) -> RAGPipeline:
    """Initialise the RAG pipeline (model connection check)."""
    return RAGPipeline(vector_store=_vector_store, model_name="phi3", top_k=5)


# ── Session state initialisation ──────────────────────────────────────────────

def init_session_state() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "memory_data" not in st.session_state:
        st.session_state.memory_data = []
    if "topic_manager_data" not in st.session_state:
        st.session_state.topic_manager_data = {"turn": 0, "registry": {}}
    if "last_step_log" not in st.session_state:
        st.session_state.last_step_log = []
    if "last_metrics" not in st.session_state:
        st.session_state.last_metrics = {}
    if "last_result_meta" not in st.session_state:
        st.session_state.last_result_meta = {}


# ── Sidebar: Controls only ────────────────────────────────────────────────────

def render_controls() -> None:
    with st.sidebar:
        st.title("⚙️ Controls")
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.memory_data = []
            st.session_state.topic_manager_data = {"turn": 0, "registry": {}}
            st.session_state.last_step_log = []
            st.session_state.last_metrics = {}
            st.session_state.last_result_meta = {}
            st.rerun()

        st.divider()
        st.caption(
            "**Stack:** Phi-3 · BGE-small · Chroma · LangChain\n\n"
            "Ensure Ollama is running:\n```\nollama serve\nollama pull phi3\n```"
        )

        st.divider()
        with st.expander("💡 Example queries"):
            st.markdown(
                """
**Sequence 1 – Ambiguity via context:**
1. `Explain water cycle`
2. `What is cycle?`  ← infers *water cycle*
3. `How does a cycle move?`  ← shifts to *bicycle*

**Sequence 2 – Direct queries:**
- `How does photosynthesis work?`
- `What is the Calvin cycle?`
- `Explain bicycle gears`
- `What causes carbon emissions?`
                """
            )


# ── Right panel: pipeline viewer + evaluation table ───────────────────────────

def render_right_panel(step_log: list[str], result_meta: dict, metrics: dict) -> None:
    """Render the pipeline processing steps and evaluation metrics table."""

    # ── Pipeline Processing ────────────────────────────────────────────────
    st.subheader("🔍 Pipeline Processing")

    if not step_log:
        st.info("Ask a question to see the pipeline steps here.")
    else:
        # Key facts at a glance
        topic = result_meta.get("topic")
        subject = result_meta.get("subject")
        mode = result_meta.get("mode")
        retrieval_score = result_meta.get("retrieval_score")
        token_counts = result_meta.get("token_counts") or {}

        if topic or subject:
            c1, c2 = st.columns(2)
            c1.metric("Topic", topic or "—")
            c2.metric("Subject", subject or "—")

        if mode:
            mode_color = "🟢" if mode == "RAG" else "🟠"
            score_str = (
                f"  _(score: {retrieval_score:.3f})_" if retrieval_score is not None else ""
            )
            ctx_sim = result_meta.get("context_similarity")
            ctx_sim_str = (
                f"  _(context similarity: {ctx_sim:.3f})_"
                if ctx_sim is not None
                else ""
            )
            st.markdown(f"{mode_color} **Mode:** {mode}{score_str}{ctx_sim_str}")

        if token_counts:
            tc1, tc2, tc3 = st.columns(3)
            tc1.metric("Input tokens", token_counts.get("input_tokens", "—"))
            tc2.metric("Output tokens", token_counts.get("output_tokens", "—"))
            tc3.metric("Total tokens", token_counts.get("total_tokens", "—"))

        if result_meta.get("clarification"):
            st.warning(f"⚠️ {result_meta['clarification']}")

        # Step-by-step log inside a scrollable container
        with st.container(height=300):
            for entry in step_log:
                # Custom tag entries (e.g. [Query], [Mode], [Tokens Used])
                if entry.startswith("[Context Similarity]"):
                    st.markdown(f"🔀 `{entry}`")
                    continue
                if entry.startswith("[Query]"):
                    st.markdown(f"🔍 `{entry}`")
                    continue
                if entry.startswith("[Retrieval Score]"):
                    st.markdown(f"📏 `{entry}`")
                    continue
                if entry.startswith("[Mode]"):
                    st.markdown(f"🏷️ `{entry}`")
                    continue
                if entry.startswith("[Tokens Used]"):
                    st.markdown(f"🔢 `{entry}`")
                    continue
                if entry.startswith("[Pipeline Stats]"):
                    st.markdown(f"📈 `{entry}`")
                    continue

                try:
                    step_num = int(entry.split("]")[0].replace("[Step", "").strip())
                except (ValueError, IndexError):
                    step_num = 0

                if step_num == 1:
                    st.markdown(f"🟣 `{entry}`")
                elif step_num in (2, 4, 7):
                    st.markdown(f"🔵 `{entry}`")
                elif step_num == 3:
                    st.markdown(f"🟡 `{entry}`")
                elif step_num in (9, 10):
                    st.markdown(f"🟢 `{entry}`")
                else:
                    st.markdown(f"⚪ `{entry}`")

        # Retrieved documents
        if result_meta.get("retrieved_docs"):
            with st.expander("📄 Retrieved Documents", expanded=False):
                for i, doc in enumerate(result_meta["retrieved_docs"], 1):
                    st.markdown(
                        f"**Doc {i}** · `{doc.metadata.get('topic')}` "
                        f"· Grade {doc.metadata.get('grade')}"
                    )
                    st.write(doc.page_content)
                    st.caption(f"Subject: {doc.metadata.get('subject')}")
                    if i < len(result_meta["retrieved_docs"]):
                        st.divider()

    # ── Evaluation Metrics ─────────────────────────────────────────────────
    if metrics:
        st.divider()
        st.subheader("📊 Evaluation Metrics")

        # Build a simple table as two lists
        metric_names = list(metrics.keys())
        metric_scores = [f"{v:.3f}" for v in metrics.values()]
        metric_status = [
            "✓ good" if v >= 0.7 else ("⚠ check" if v >= 0.5 else "✗ low")
            for v in metrics.values()
        ]

        # Render as a native Streamlit table (no pandas required)
        table_data = {
            "Metric": metric_names,
            "Score": metric_scores,
            "Status": metric_status,
        }
        st.table(table_data)


# ── Chat column ───────────────────────────────────────────────────────────────

def render_chat_column(pipeline: RAGPipeline) -> None:
    st.title("🎓 EduRAG — Educational Conversational QA")
    st.caption(
        "Powered by Phi-3 (Ollama) · BGE Embeddings · Chroma · LangChain  \n"
        "Topics: water cycle · carbon cycle · bicycle · photosynthesis"
    )

    # Render existing chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask an educational question…")
    if not user_input:
        return

    # Show user message immediately
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Rebuild memory from serialised session state
    memory = ConversationMemory.from_list(st.session_state.memory_data, max_turns=5)
    topic_manager = TopicMemoryManager.from_dict(st.session_state.topic_manager_data)

    # Run pipeline
    with st.spinner("🤔 Thinking…"):
        result = pipeline.run(user_query=user_input, memory=memory,
                              topic_manager=topic_manager)

    # Persist memory back to session state
    st.session_state.memory_data = memory.to_list()
    st.session_state.topic_manager_data = topic_manager.to_dict()

    # Persist step log and metadata for the right panel
    st.session_state.last_step_log = result.step_log
    st.session_state.last_metrics = result.metrics
    st.session_state.last_result_meta = {
        "topic": result.detected_topic,
        "subject": result.detected_subject,
        "retrieved_docs": result.retrieved_docs,
        "clarification": result.clarification_message,
        "mode": result.mode,
        "retrieval_score": result.retrieval_score,
        "token_counts": result.token_counts,
        "context_similarity": result.context_similarity,
    }

    # Build assistant message
    if result.clarification_needed and result.clarification_message:
        assistant_msg = f"🤔 {result.clarification_message}"
    else:
        note = ""
        if result.rewritten_query != user_input:
            note = f"\n\n> *Interpreted as: \"{result.rewritten_query}\"*\n\n"
        assistant_msg = note + result.answer

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_msg}
    )
    with st.chat_message("assistant"):
        st.markdown(assistant_msg)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    init_session_state()

    # Load resources
    vector_store = load_vector_store()
    pipeline = load_pipeline(vector_store)

    # Sidebar: controls + stack info
    render_controls()

    # Main area: chat (left) | pipeline + metrics (right)
    chat_col, right_col = st.columns([3, 2], gap="large")

    with chat_col:
        render_chat_column(pipeline)

    with right_col:
        render_right_panel(
            step_log=st.session_state.last_step_log,
            result_meta=st.session_state.last_result_meta,
            metrics=st.session_state.last_metrics,
        )


if __name__ == "__main__":
    main()

