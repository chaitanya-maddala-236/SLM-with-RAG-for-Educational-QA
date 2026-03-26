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
# Embedding support: import embedding config for the sidebar selector
from research_config import EMBEDDING_MODELS, DEFAULT_EMBEDDING

# ── Cached resources (load once, reuse across reruns) ────────────────────────

# Embedding support: cache separately per embedding_name (Streamlit caches by args)
@st.cache_resource(show_spinner="🔧 Building vector store...")
def load_vector_store(embedding_name: str = DEFAULT_EMBEDDING) -> Chroma:
    """Load or build the Chroma vector store for the given embedding model."""
    return build_vector_store(persist=True, embedding_name=embedding_name)


@st.cache_resource(show_spinner="🤖 Loading model via Ollama…")
def load_pipeline(
    _vector_store: Chroma,
    model_name: str,
    retrieval_mode: str,
    top_k: int,
    embedding_name: str,
) -> RAGPipeline:
    """Initialise the RAG pipeline (model connection check)."""
    return RAGPipeline(
        vector_store=_vector_store,
        model_name=model_name,
        retrieval_mode=retrieval_mode,
        top_k=top_k,
    )


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
    # Embedding support: persist selected embedding across reruns
    if "selected_embedding" not in st.session_state:
        st.session_state.selected_embedding = DEFAULT_EMBEDDING
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "phi3"
    if "selected_retrieval" not in st.session_state:
        st.session_state.selected_retrieval = "hybrid"
    if "selected_topk" not in st.session_state:
        st.session_state.selected_topk = 5


# ── Sidebar: Controls only ────────────────────────────────────────────────────

def render_controls() -> tuple[str, str, str, int]:
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
        st.subheader("🤖 Model Settings")
        selected_model = st.selectbox(
            "SLM Model",
            ["phi3", "tinyllama", "llama3.2", "mistral"],
            index=0,
            help="Must be installed via: ollama pull <model>",
        )

        selected_retrieval = st.selectbox(
            "Retrieval Mode",
            ["hybrid", "vector_only", "bm25_only"],
            index=0,
            help="How documents are retrieved from the vector store",
        )

        selected_topk = st.slider(
            "Top-K Documents",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of documents to retrieve per query",
        )

        st.divider()
        st.subheader("🔢 Embedding Model")
        # Embedding support: let the user pick which embedding to use
        emb_names = [e["name"] for e in EMBEDDING_MODELS]
        selected_embedding = st.selectbox(
            "Embedding Model",
            emb_names,
            index=emb_names.index(DEFAULT_EMBEDDING),
            help="Each embedding builds its own vector store on first use",
        )

        st.divider()
        # Embedding support: show active configuration at a glance
        st.info(
            f"**Active Config**\n\n"
            f"Model: `{selected_model}`\n\n"
            f"Embedding: `{selected_embedding}`\n\n"
            f"Retrieval: `{selected_retrieval}`\n\n"
            f"Top-K: `{selected_topk}`"
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

        return selected_model, selected_retrieval, selected_topk, selected_embedding


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
            # Bugfix: three-colour mode indicator — green (RAG), blue (Partial RAG), orange (fallback)
            if mode == "RAG":
                mode_color = "🟢"
            elif mode == "Partial RAG":
                mode_color = "🔵"
            else:
                mode_color = "🟠"
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

def render_chat_column(pipeline: RAGPipeline, embedding_name: str = DEFAULT_EMBEDDING) -> None:
    st.title("🎓 EduRAG — Educational Conversational QA")
    st.caption(
        f"Powered by {pipeline.model_name} (Ollama) · {embedding_name} Embeddings · Chroma · LangChain  \n"
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

    # Sidebar: controls + model/embedding/retrieval selection
    selected_model, selected_retrieval, selected_topk, selected_embedding = render_controls()

    # Persist selections to session state
    st.session_state.selected_model = selected_model
    st.session_state.selected_retrieval = selected_retrieval
    st.session_state.selected_topk = selected_topk
    st.session_state.selected_embedding = selected_embedding

    # Embedding support: load vector store and pipeline keyed on embedding
    vector_store = load_vector_store(st.session_state.selected_embedding)
    pipeline = load_pipeline(
        vector_store,
        st.session_state.selected_model,
        st.session_state.selected_retrieval,
        st.session_state.selected_topk,
        st.session_state.selected_embedding,
    )

    # Main area: chat (left) | pipeline + metrics (right)
    chat_col, right_col = st.columns([3, 2], gap="large")

    with chat_col:
        render_chat_column(pipeline, st.session_state.selected_embedding)

    with right_col:
        render_right_panel(
            step_log=st.session_state.last_step_log,
            result_meta=st.session_state.last_result_meta,
            metrics=st.session_state.last_metrics,
        )


if __name__ == "__main__":
    main()

