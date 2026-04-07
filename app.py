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

import os
import json
import datetime

# Suppress torchvision file-watcher warnings
os.environ.setdefault("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "none")

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
from research_config import (
    EMBEDDING_MODELS, DEFAULT_EMBEDDING, MODEL_REGISTRY,
    CHUNKING_STRATEGIES, DEFAULT_CHUNKING_STRATEGY,
)
from data_loader import get_corpus_stats, get_topic_coverage_warnings
# Multimodal extension: optional — degrades gracefully when deps are absent
_MM_IMPORT_OK = False
load_or_build_image_index = None
try:
    from multimodal_processor import (
        load_or_build_image_index,
        multimodal_available,
        get_missing_dependencies,
    )
    _MM_IMPORT_OK = True
except ImportError:
    def multimodal_available() -> bool:
        return False

    def get_missing_dependencies() -> list:
        return ["multimodal_processor (not found)"]

# ── Cached resources (load once, reuse across reruns) ────────────────────────

# Cache separately per (embedding_name, chunking_strategy)
@st.cache_resource(show_spinner="🔧 Building vector store...")
def load_vector_store(
    embedding_name: str = DEFAULT_EMBEDDING,
    chunking_strategy: str = DEFAULT_CHUNKING_STRATEGY,
) -> Chroma:
    """Load or build the Chroma vector store for the given embedding + chunking."""
    return build_vector_store(
        persist=True,
        embedding_name=embedding_name,
        chunking_strategy=chunking_strategy,
    )


@st.cache_resource(show_spinner="🖼️ Loading image index…")
def load_image_index():
    """Load the FAISS image index if it exists on disk, otherwise return None."""
    if not _MM_IMPORT_OK or load_or_build_image_index is None:
        return None
    return load_or_build_image_index()  # loads from disk; None if not built yet


@st.cache_resource(show_spinner="🤖 Loading model…")
def load_pipeline(
    _vector_store: Chroma,
    model_name: str,
    retrieval_mode: str,
    top_k: int,
    embedding_name: str,
    use_cross_encoder: bool,
    _image_index=None,
) -> RAGPipeline:
    """Initialise the RAG pipeline."""
    return RAGPipeline(
        vector_store=_vector_store,
        model_name=model_name,
        retrieval_mode=retrieval_mode,
        top_k=top_k,
        image_index=_image_index,
        use_cross_encoder=use_cross_encoder,
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
    if "selected_chunking" not in st.session_state:
        st.session_state.selected_chunking = DEFAULT_CHUNKING_STRATEGY
    if "use_cross_encoder" not in st.session_state:
        st.session_state.use_cross_encoder = False
    if "session_export_data" not in st.session_state:
        st.session_state.session_export_data = []
    if "last_grounding_score" not in st.session_state:
        st.session_state.last_grounding_score = None
    if "last_cost" not in st.session_state:
        st.session_state.last_cost = None
    if "last_image_captions" not in st.session_state:
        st.session_state.last_image_captions = []


# ── Sidebar: Controls only ────────────────────────────────────────────────────

def render_controls() -> tuple[str, str, int, str, str, bool]:
    with st.sidebar:
        st.title("⚙️ Controls")
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.memory_data = []
            st.session_state.topic_manager_data = {"turn": 0, "registry": {}}
            st.session_state.last_step_log = []
            st.session_state.last_metrics = {}
            st.session_state.last_result_meta = {}
            st.session_state.session_export_data = []
            st.rerun()

        # Bonus Feature 5: Session Export
        if st.session_state.get("session_export_data"):
            export_json = json.dumps({
                "exported_at": datetime.datetime.now().isoformat(),
                "turns": st.session_state.session_export_data,
            }, indent=2, default=str)
            st.download_button(
                "📥 Export Session (JSON)",
                data=export_json,
                file_name=f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )

        st.divider()
        st.subheader("🤖 Model Settings")

        # ── SLM / LLM selector ─────────────────────────────────────────────
        slm_models = [m["name"] for m in MODEL_REGISTRY if m["type"] == "SLM"]
        llm_models = [m["name"] for m in MODEL_REGISTRY if m["type"] == "LLM"]

        model_type_choice = st.radio(
            "Model type",
            ["SLM (local Ollama)", "LLM (API)"],
            help="SLMs run locally via Ollama (free). LLMs use paid APIs.",
            horizontal=True,
        )

        if model_type_choice == "SLM (local Ollama)":
            default_idx = slm_models.index("phi3") if "phi3" in slm_models else 0
            selected_model = st.selectbox(
                "SLM Model",
                slm_models,
                index=default_idx,
                help="Must be installed via: ollama pull <model>",
            )
        else:
            selected_model = st.selectbox(
                "LLM (API) Model",
                llm_models,
                index=0,
                help="Requires the corresponding API key set as an env var.",
            )
            # Show which API key is needed
            cfg = next((m for m in MODEL_REGISTRY if m["name"] == selected_model), {})
            provider = cfg.get("provider", "")
            key_map = {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "google": "GOOGLE_API_KEY",
            }
            if provider in key_map:
                import os as _os
                env_var = key_map[provider]
                if _os.environ.get(env_var):
                    st.success(f"✅ {env_var} is set")
                else:
                    st.warning(f"⚠️ {env_var} not set — queries will fail")

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
        st.subheader("🔢 Embedding & Chunking")
        # Embedding support: let the user pick which embedding to use
        emb_names = [e["name"] for e in EMBEDDING_MODELS]
        selected_embedding = st.selectbox(
            "Embedding Model",
            emb_names,
            index=emb_names.index(DEFAULT_EMBEDDING),
            help=(
                "Each embedding builds its own vector store on first use.\n"
                "nomic-embed-text needs `ollama pull nomic-embed-text`.\n"
                "text-embedding-3-large needs OPENAI_API_KEY."
            ),
        )

        selected_chunking = st.selectbox(
            "Chunking Strategy",
            CHUNKING_STRATEGIES,
            index=CHUNKING_STRATEGIES.index(DEFAULT_CHUNKING_STRATEGY),
            help=(
                "fixed: RecursiveCharacterTextSplitter (400 chars)\n"
                "sliding_window: 400-char window, 200-char step\n"
                "semantic: sentence-level cosine-similarity grouping"
            ),
        )

        use_cross_encoder = st.checkbox(
            "Cross-Encoder Re-ranking",
            value=False,
            help=(
                "Use a neural cross-encoder to rerank retrieved documents. "
                "More accurate but slower. Requires sentence-transformers."
            ),
        )

        st.divider()
        # Show active configuration at a glance
        st.info(
            f"**Active Config**\n\n"
            f"Model: `{selected_model}`\n\n"
            f"Embedding: `{selected_embedding}`\n\n"
            f"Chunking: `{selected_chunking}`\n\n"
            f"Retrieval: `{selected_retrieval}`\n\n"
            f"Top-K: `{selected_topk}`\n\n"
            f"Cross-Encoder: `{'on' if use_cross_encoder else 'off'}`"
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

        st.divider()
        # RAG Improvement: Corpus coverage checker - Bonus Feature 4
        with st.expander("📊 Corpus Coverage", expanded=False):
            try:
                stats = get_corpus_stats()
                st.metric("Total Documents", stats["total_documents"])
                st.metric("Topics", stats["unique_topics"])
                st.metric("Subjects", stats["unique_subjects"])
                warnings = get_topic_coverage_warnings()
                if warnings:
                    st.warning(f"⚠️ {len(warnings)} topics have <5 documents")
                    with st.expander("Show sparse topics"):
                        for topic in warnings[:10]:
                            count = stats["topic_distribution"].get(topic, 0)
                            st.text(f"• {topic}: {count} docs")
            except Exception as e:
                st.info("Corpus stats unavailable")

        # Multimodal status
        st.divider()
        with st.expander("🖼️ Multimodal Status", expanded=False):
            if multimodal_available():
                st.success("✅ Multimodal enabled (CLIP + FAISS)")
                st.caption(
                    "Upload an image in the chat to query via visual context. "
                    "To index PDF images run `build_image_index()` from "
                    "`multimodal_processor.py`."
                )
            else:
                missing = get_missing_dependencies()
                st.warning("⚠️ Multimodal not available")
                st.caption("Missing: " + ", ".join(missing))

        return (
            selected_model,
            selected_retrieval,
            selected_topk,
            selected_embedding,
            selected_chunking,
            use_cross_encoder,
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

            # RAG Improvement 28: Grounding score display
            grounding_score = result_meta.get("grounding_score")
            if grounding_score is not None:
                if grounding_score >= 0.6:
                    grounding_color = "🟢"
                    grounding_label = "High"
                elif grounding_score >= 0.3:
                    grounding_color = "🟡"
                    grounding_label = "Medium"
                else:
                    grounding_color = "🔴"
                    grounding_label = "Low"
                st.markdown(f"{grounding_color} **Grounding:** {grounding_label} ({grounding_score:.2f})")

            # RAG Improvement 29: Cost display
            cost = result_meta.get("estimated_cost_usd")
            token_counts = result_meta.get("token_counts") or {}
            if cost is not None:
                cost_str = f"${cost:.6f}" if cost > 0 else "Free (local)"
                total_tok = token_counts.get("total_tokens", "—")
                st.caption(f"💰 Cost: {cost_str} | Tokens: {total_tok}")

            # Bonus Feature 3: Topic Confidence UI
            topic_confidence = result_meta.get("topic_confidence_list")
            if topic_confidence:
                with st.expander("🎯 Topic Confidence", expanded=False):
                    for t_name, t_conf in topic_confidence[:3]:
                        bar_val = min(1.0, max(0.0, t_conf))
                        st.progress(bar_val, text=f"{t_name}: {t_conf:.2f}")

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

        # Multimodal: image captions retrieved for this query
        image_captions = result_meta.get("image_captions") or []
        if image_captions:
            with st.expander("🖼️ Visual Context (Image Captions)", expanded=True):
                for i, cap in enumerate(image_captions, 1):
                    st.markdown(f"**Image {i}:** {cap}")

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

    # Multimodal: optional image upload (shown above chat input)
    uploaded_image_bytes: bytes | None = None
    # Maximum permitted image upload: 5 MB.  Large files can exhaust server
    # memory; CLIP inference also benefits from reasonably-sized inputs.
    _MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB
    if multimodal_available():
        uploaded_file = st.file_uploader(
            "📎 Attach an image (optional — for visual queries)",
            type=["png", "jpg", "jpeg", "webp"],
            help="Upload a diagram or photo (max 5 MB) to include visual context in your query.",
            key="image_uploader",
        )
        if uploaded_file is not None:
            if uploaded_file.size > _MAX_IMAGE_BYTES:
                st.warning(
                    f"⚠️ Image too large ({uploaded_file.size / 1024 / 1024:.1f} MB). "
                    "Please upload an image smaller than 5 MB."
                )
            else:
                uploaded_image_bytes = uploaded_file.read()
                st.image(uploaded_image_bytes, caption="Attached image", use_column_width=True)

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

    # Run pipeline (pass image bytes when an image was uploaded)
    with st.spinner("🤔 Thinking…"):
        result = pipeline.run(
            user_query=user_input,
            memory=memory,
            topic_manager=topic_manager,
            image_input=uploaded_image_bytes,
        )

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
        "grounding_score": getattr(result, 'grounding_score', None),
        "estimated_cost_usd": getattr(result, 'estimated_cost_usd', None),
        "topic_confidence_list": getattr(result, 'topic_confidence_list', None),
        "image_captions": getattr(result, 'image_captions', []),
    }
    st.session_state.last_grounding_score = getattr(result, 'grounding_score', None)
    st.session_state.last_cost = getattr(result, 'estimated_cost_usd', None)
    st.session_state.last_image_captions = getattr(result, 'image_captions', [])
    # Build session export data for Bonus Feature 5
    st.session_state.session_export_data.append({
        "turn": len(st.session_state.chat_history),
        "query": user_input,
        "answer": result.answer,
        "mode": result.mode,
        "topic": result.detected_topic,
        "subject": result.detected_subject,
        "grounding_score": getattr(result, 'grounding_score', None),
        "estimated_cost_usd": getattr(result, 'estimated_cost_usd', None),
        "latency_ms": result.latency_ms,
        "has_image_context": getattr(result, 'has_image_context', False),
    })

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
    (
        selected_model,
        selected_retrieval,
        selected_topk,
        selected_embedding,
        selected_chunking,
        use_cross_encoder,
    ) = render_controls()

    # Persist selections to session state
    st.session_state.selected_model = selected_model
    st.session_state.selected_retrieval = selected_retrieval
    st.session_state.selected_topk = selected_topk
    st.session_state.selected_embedding = selected_embedding
    st.session_state.selected_chunking = selected_chunking
    st.session_state.use_cross_encoder = use_cross_encoder

    # Load vector store keyed on (embedding, chunking_strategy)
    vector_store = load_vector_store(
        st.session_state.selected_embedding,
        st.session_state.selected_chunking,
    )
    # Multimodal: load FAISS image index (None if not built yet or deps absent)
    image_index = load_image_index()
    pipeline = load_pipeline(
        vector_store,
        st.session_state.selected_model,
        st.session_state.selected_retrieval,
        st.session_state.selected_topk,
        st.session_state.selected_embedding,
        st.session_state.use_cross_encoder,
        image_index,
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

