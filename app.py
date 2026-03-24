"""
app.py
------
Streamlit UI for the Educational Conversational RAG System.

Layout:
  ● Left sidebar  – pipeline step viewer (live debug log)
  ● Main area     – chat interface
  ● Bottom panel  – evaluation metrics table

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
        # List of dicts: {"role": "user"|"assistant", "content": str}
        st.session_state.chat_history = []
    if "memory_data" not in st.session_state:
        st.session_state.memory_data = []          # serialised ConversationMemory
    if "topic_manager_data" not in st.session_state:
        st.session_state.topic_manager_data = {}   # serialised TopicMemoryManager
    if "last_step_log" not in st.session_state:
        st.session_state.last_step_log = []        # step log from latest pipeline run
    if "last_metrics" not in st.session_state:
        st.session_state.last_metrics = {}
    if "last_result_meta" not in st.session_state:
        st.session_state.last_result_meta = {}     # topic, subject, retrieved docs


# ── Sidebar: Pipeline Step Viewer ─────────────────────────────────────────────

def render_sidebar(step_log: list[str], result_meta: dict) -> None:
    st.sidebar.title("🔍 Pipeline Viewer")
    st.sidebar.caption("Live debug output from the last query")

    if not step_log:
        st.sidebar.info("Ask a question to see the pipeline in action.")
        return

    # Key facts at a glance
    with st.sidebar.container():
        col1, col2 = st.sidebar.columns(2)
        col1.metric("Topic", result_meta.get("topic") or "—")
        col2.metric("Subject", result_meta.get("subject") or "—")
        if result_meta.get("clarification"):
            st.sidebar.warning(f"⚠️ {result_meta['clarification']}")

    st.sidebar.divider()

    # Step-by-step log
    for entry in step_log:
        # Colour-code by step number
        step_num = int(entry.split("]")[0].replace("[Step", "").strip()) \
            if entry.startswith("[Step") else 0
        if step_num in (1,):
            st.sidebar.markdown(f"🟣 `{entry}`")
        elif step_num in (2, 4, 7):
            st.sidebar.markdown(f"🔵 `{entry}`")
        elif step_num in (3,):
            st.sidebar.markdown(f"🟡 `{entry}`")
        elif step_num in (9, 10):
            st.sidebar.markdown(f"🟢 `{entry}`")
        else:
            st.sidebar.markdown(f"⚪ `{entry}`")

    # Retrieved documents
    if result_meta.get("retrieved_docs"):
        st.sidebar.divider()
        st.sidebar.subheader("📄 Retrieved Documents")
        for i, doc in enumerate(result_meta["retrieved_docs"], 1):
            with st.sidebar.expander(
                f"Doc {i} · {doc.metadata.get('topic')} · Grade {doc.metadata.get('grade')}"
            ):
                st.write(doc.page_content)
                st.caption(f"Subject: {doc.metadata.get('subject')}")


# ── Main chat area ────────────────────────────────────────────────────────────

def render_chat(pipeline: RAGPipeline) -> None:
    st.title("🎓 EduRAG — Educational Conversational QA")
    st.caption(
        "Powered by Phi-3 (Ollama) · BGE Embeddings · Chroma · LangChain\n\n"
        "Topics: water cycle, carbon cycle, bicycle, photosynthesis"
    )

    # Example queries
    with st.expander("💡 Try these example queries (demonstrates conversational context)"):
        st.markdown(
            """
**Sequence 1 – Ambiguity resolved via context:**
1. `Explain water cycle`
2. `What is cycle?`  ← system infers *water cycle* from memory
3. `How does a cycle move?`  ← system detects intent shift → *bicycle*

**Sequence 2 – Direct topic queries:**
- `How does photosynthesis work?`
- `What is the Calvin cycle?`
- `Explain bicycle gears`
- `What causes carbon emissions?`
            """
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

    # Persist step log and metadata
    st.session_state.last_step_log = result.step_log
    st.session_state.last_metrics = result.metrics
    st.session_state.last_result_meta = {
        "topic": result.detected_topic,
        "subject": result.detected_subject,
        "retrieved_docs": result.retrieved_docs,
        "clarification": result.clarification_message,
    }

    # Build assistant message
    if result.clarification_needed and result.clarification_message:
        assistant_msg = f"🤔 {result.clarification_message}"
    else:
        # Show rewritten query if it changed
        note = ""
        if result.rewritten_query != user_input:
            note = (
                f"\n\n> *Interpreted as: \"{result.rewritten_query}\"*\n\n"
            )
        assistant_msg = note + result.answer

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_msg}
    )
    with st.chat_message("assistant"):
        st.markdown(assistant_msg)


# ── Evaluation metrics panel ──────────────────────────────────────────────────

def render_metrics(metrics: dict) -> None:
    if not metrics:
        return

    st.divider()
    st.subheader("📊 Evaluation Metrics (last query)")

    cols = st.columns(len(metrics))
    colours = {
        "high":   "normal",
        "medium": "off",
        "low":    "inverse",
    }

    for col, (name, score) in zip(cols, metrics.items()):
        delta_colour = "normal" if score >= 0.7 else ("off" if score >= 0.5 else "inverse")
        col.metric(
            label=name,
            value=f"{score:.3f}",
            delta=f"{'✓ good' if score >= 0.7 else '⚠ check'}",
            delta_color=delta_colour,
        )

    # Also show the ASCII table (collapsible)
    with st.expander("View as text table"):
        st.code(format_metrics_table(metrics), language=None)


# ── Controls ──────────────────────────────────────────────────────────────────

def render_controls() -> None:
    with st.sidebar:
        st.divider()
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.memory_data = []
            st.session_state.topic_manager_data = {}
            st.session_state.last_step_log = []
            st.session_state.last_metrics = {}
            st.session_state.last_result_meta = {}
            st.rerun()

        st.caption(
            "**Stack:** Phi-3 · BGE-small · Chroma · LangChain\n\n"
            "Ensure Ollama is running:\n```\nollama serve\nollama pull phi3\n```"
        )


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    init_session_state()

    # Load resources
    vector_store = load_vector_store()
    pipeline = load_pipeline(vector_store)

    # Render UI
    render_sidebar(
        step_log=st.session_state.last_step_log,
        result_meta=st.session_state.last_result_meta,
    )
    render_controls()

    render_chat(pipeline)
    render_metrics(st.session_state.last_metrics)


if __name__ == "__main__":
    main()
