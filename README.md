# 🎓 EduSLM-RAG — Educational Conversational QA with Contextual Retrieval

> **Python 3.11+** | **LangChain** | **ChromaDB** | **Groq API** | **Streamlit** | **BGE / nomic / OpenAI Embeddings** | **BM25 + Dense + Semantic Search** | **Cross-Encoder Reranking**

A research-grade **Retrieval-Augmented Generation (RAG)** system for educational question answering using Small Language Models (SLMs) and API-hosted LLMs. It handles multi-turn conversations, resolves pronouns and ambiguous follow-ups, detects topic shifts, and falls back gracefully when a question is out of scope.

> **Important (current setup):** the repository supports Ollama, Groq, OpenAI, Anthropic, and Google model providers. Set only the API keys you need in `.env`.

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
GROQ_API_KEY=...
```

### ✅ Latest reliability/testing updates

- Uploaded images are now captioned directly and injected into context, so visual queries still work even when no prebuilt image index exists.
- Evaluation summaries now include **hallucination rate** (`1 - Faithfulness`) in addition to latency/accuracy.
- Default evaluation outputs are written to `results/`:
  - `results/research_results.txt`
  - `results/ablation_results.txt`
  - `results/model_comparison_results.txt`
  - `results/embedding_comparison_results.txt`
  - `results/full_matrix_results.txt`
  - `results/token_comparison_results.txt`
  - `results/slm_vs_llm_results.txt`
- Graphs are generated in research format under `results/graphs/` with accuracy, latency, and hallucination-rate visuals.

---

## 📌 Table of Contents

1. [What This Project Does](#-what-this-project-does)
2. [Architecture Overview](#️-architecture-overview)
3. [Corpus Statistics](#-corpus-statistics)
4. [Models](#-models)
5. [Embedding Models](#-embedding-models)
6. [Embedding Techniques & Chunking Strategies](#-embedding-techniques--chunking-strategies)
7. [RAG Improvements](#-rag-improvements)
8. [Bonus Features](#-bonus-features)
9. [Tech Stack](#️-tech-stack)
10. [Project Structure](#-project-structure)
11. [Setup & Installation](#-setup--installation)
12. [How to Run](#-how-to-run)
13. [Evaluation Commands](#-evaluation-commands)
14. [Generate Evaluation Graphs](#generate-evaluation-graphs)
15. [Final Evaluation Script — Dataset-Driven Model Comparison](#final-evaluation-script--dataset-driven-model-comparison)
16. [Example Conversation Flows](#-example-conversation-flows)
17. [Research Overview](#-research-overview)
18. [Requirements](#-requirements)

---

## 🎯 What This Project Does

EduSLM-RAG is a **conversational educational QA system** that combines a Small Language Model with a Retrieval-Augmented Generation pipeline. Students can ask multi-turn questions — including vague follow-ups like *"what about it?"* or *"give an example"* — and the system resolves those references through contextual memory before querying the knowledge base.

### The Two Problems It Solves

| Problem | Solution |
|---|---|
| SLMs hallucinate on knowledge-intensive questions | **RAG** — ground every answer in retrieved educational documents |
| SLMs lose track of conversation context | **Contextual Query Builder** — rewrite each query using conversation history before retrieval |

### Three Retrieval Modes

| Mode | How It Works |
|---|---|
| `vector_only` | Semantic similarity search via BGE embeddings + ChromaDB |
| `bm25_only` | Exact keyword matching via BM25Okapi |
| `hybrid` | Weighted merge of BM25 + vector results, reranked by token overlap |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│          Streamlit Chat (app.py)  ·  CLI (main.py)              │
└─────────────────────────┬───────────────────────────────────────┘
                          │ raw query + conversation history
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    10-Step RAG Pipeline                         │
│                      (rag_pipeline.py)                          │
│                                                                 │
│  Step 1  ──  Receive user question                              │
│  Step 2  ──  Check conversation memory (context_memory.py)      │
│  Step 3  ──  Contextual Query Builder                           │
│              ├─ Normalise query (lowercase, contractions)       │
│              ├─ Score topic confidence per keyword              │
│              ├─ Detect topic shift vs. continuation             │
│              ├─ Resolve ambiguous pronouns / short fragments    │
│              └─ Rewrite query with full context                 │
│  Step 4  ──  Final ambiguity detection on rewritten query       │
│  Step 5  ──  Query classification: subject + topic              │
│  Step 6  ──  Glossary mapping: synonym / concept expansion      │
│  Step 7  ──  Retrieval                                          │
│              ├─ BM25 keyword index  (rank_bm25)                 │
│              ├─ Vector search       (ChromaDB + BGE)            │
│              └─ Hybrid merge + MMR reranking                    │
│  Step 8  ──  Top-K document selection (reranker)                │
│  Step 9  ──  Answer generation (SLM via Ollama)                 │
│  Step 10 ──  Evaluation metrics + memory update                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │ answer + metrics + step log
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Response to User                            │
│  answer · mode (RAG / Partial RAG / LLM Fallback)               │
│  metrics (Precision@5, Recall@5, MRR, Faithfulness, ...)        │
│  grounding score · estimated cost · topic confidence bars       │
└─────────────────────────────────────────────────────────────────┘
```

### Retrieval Sub-Pipeline

```
Query (rewritten)
      │
      ├──── BM25 index ─────────────────────┐
      │     (keyword matching)               │
      │                                      ▼
      └──── ChromaDB vector search ──► Weighted merge
            (BGE-small embeddings)           │
                                             ▼
                                    Candidate pool (top 4×K)
                                             │
                                             ▼
                                    Reranker
                                    (token overlap + topic bonus)
                                             │
                                             ▼
                                    Top-K chunks → SLM prompt
```

---

## 📊 Corpus Statistics

Corpus statistics are computed **dynamically at runtime** from `EDUCATIONAL_DOCUMENTS` defined across all corpus modules. Run the following command to see live counts:

```bash
python -c "from data_loader import get_corpus_stats; import json; print(json.dumps(get_corpus_stats(), indent=2))"
```

The `get_corpus_stats()` function returns:

| Field | Description |
|---|---|
| `total_documents` | Total number of educational text entries |
| `unique_topics` | Number of distinct topic labels |
| `unique_subjects` | Number of distinct subject areas |
| `topic_distribution` | Per-topic document counts |
| `subject_distribution` | Per-subject document counts |
| `grade_distribution` | Per-grade document counts |
| `average_text_length` | Mean character length across all documents |
| `topics_under_5` | Topics with fewer than 5 documents (coverage warnings) |
| `topics_over_10` | Topics with more than 10 documents |

Corpus data is spread across versioned modules:

| Module | Approx. Lines | Description |
|---|---|---|
| `extended_corpus_v2.py` | ~4,022 | First large extension — trigonometry, genetics, ML, electricity |
| `extended_corpus_v3.py` | ~1,883 | Second extension — sound waves, cybersecurity, digestion |
| `extended_corpus_v4.py` | ~1,251 | Third extension — additional STEM topics |
| `extended_corpus_v5.py` | ~1,407 | Fourth extension |
| `extended_corpus_v6.py` | ~3,035 | Fifth extension |
| `extended_corpus_v7.py` | ~2,796 | Sixth extension |
| `extended_corpus_v8.py` | ~4,004 | Seventh extension |
| `extended_corpus_v9.py` | ~4,265 | Eighth extension — latest additions |

Core topics in the original dataset include: **Water Cycle**, **Carbon Cycle**, **Bicycle**, **Photosynthesis**, **Nitrogen Cycle**, **Trigonometry**, **Genetics**, **Machine Learning**, **Electricity**, **Magnetism**, **Nervous System**, **Evolution**, **Cell Structure**, **Cellular Respiration**, **Digestion**, **Immune System**, **Sound Waves**, **Cybersecurity**, and 130+ more.

Each document carries structured metadata used for retrieval filtering:

```json
{
  "text": "The water cycle describes how water moves through evaporation...",
  "topic": "water_cycle",
  "subject": "geography",
  "grade": "6"
}
```

---

## 🤖 Models

All models are registered in `MODEL_REGISTRY` in `research_config.py`.

### 🧠 SLMs (Small Language Models)

- `phi3` / `phi3-mini` (Phi-3 Mini)
- `gemma2` (Gemma 2B)
- `tinyllama`
- `mistral` / `mistral-7b-instruct`

### 🧠 Open-Source LLMs

- `llama3-8b`
- `llama3-70b`
- `mixtral-8x7b`
- `qwen2.5-7b`
- `deepseek-llm`

### 🧠 Commercial API LLMs

- `gpt-4o` (OpenAI)
- `claude-3.5-sonnet` (Anthropic)
- `gemini-1.5-pro` (Google)

### 🖼️ Vision / Multimodal

- Vision model: **LLaVA** (Ollama fallback in vision analyzer)
- API vision path: Groq vision (`llama-3.2-11b-vision-preview`)

---

## 🔢 Embedding Models

All embeddings are defined in `EMBEDDING_MODELS` in `research_config.py`. Each embedding/chunking-strategy pair gets its own isolated ChromaDB collection and persist directory to avoid dimension-mismatch errors.

### Dense Embedding Models

| Key | Model ID | Dimensions | Backend | Description |
|---|---|---|---|---|
| `bge-small` ⭐ | `BAAI/bge-small-en-v1.5` | 384 | HuggingFace | BGE Small — fast, **current default** |
| `bge-base-en` | `BAAI/bge-base-en-v1.5` | 768 | HuggingFace | **Benchmark model** — balanced quality/speed |
| `bge-large` | `BAAI/bge-large-en-v1.5` | 1024 | HuggingFace | BGE Large — highest retrieval quality |
| `all-MiniLM-L6-v2` | `sentence-transformers/all-MiniLM-L6-v2` | 384 | HuggingFace | **Benchmark model** — very fast, lightweight |
| `mpnet` | `sentence-transformers/all-mpnet-base-v2` | 768 | HuggingFace | Strong general-purpose embeddings |
| `e5-small` | `intfloat/e5-small-v2` | 384 | HuggingFace | E5 Small — instruction-tuned |
| `e5-base` | `intfloat/e5-base-v2` | 768 | HuggingFace | E5 Base — instruction-tuned, larger |
| `nomic-embed-text` | `nomic-embed-text` | 768 | Ollama | **Benchmark model** — high quality, local |
| `text-embedding-3-large` | `text-embedding-3-large` | 3072 | OpenAI API | **Benchmark model** — state-of-the-art |
| `siglip` | `google/siglip-base-patch16-224` | 768 | HuggingFace | **Primary multimodal option** — improved alignment/accuracy |
| `openclip` | `laion/CLIP-ViT-B-32-laion2B-s34B-b79K` | 512 | HuggingFace | **Alternative multimodal option** — flexible pretrained variants |

> `nomic-embed-text` requires: `ollama pull nomic-embed-text`  
> `text-embedding-3-large` requires: `OPENAI_API_KEY`

### Sparse Embeddings (BM25)

BM25 keyword retrieval is built into the pipeline via `rank-bm25`.  
Select retrieval mode `bm25_only` to use BM25 exclusively, or `hybrid` to merge BM25 scores with dense vector scores.

### Hybrid Search (Dense + Sparse)

With retrieval mode `hybrid` (the default), the pipeline:
1. Retrieves top candidates via BM25 (sparse keyword matching)
2. Retrieves top candidates via ChromaDB vector search (dense embeddings)
3. Merges both result sets with a weighted score: `combined = (1-α)×BM25 + α×vector`
4. Reranks the merged pool with MMR or cross-encoder (see below)

---

## 🧩 Embedding Techniques & Chunking Strategies

### Chunking Strategies

Chunking strategy is selected per vector store build. Each `(embedding, strategy)` pair uses its own isolated ChromaDB directory.

| Strategy | Description | Config |
|---|---|---|
| `fixed` ⭐ | RecursiveCharacterTextSplitter, 400-char chunks, 50-char overlap — **default** | `CHUNK_SIZE=400`, `CHUNK_OVERLAP=50` |
| `sliding_window` | Overlapping sliding windows: 400-char window, 200-char step (50 % overlap) | `SLIDING_WINDOW_SIZE=400`, `SLIDING_WINDOW_STEP=200` |
| `semantic` | Sentence-level cosine-similarity grouping — splits when similarity drops below threshold | `SEMANTIC_SIMILARITY_THRESHOLD=0.75` |

Select strategy in the Streamlit sidebar under **Chunking Strategy**, or via code:

```python
from retriever import build_vector_store
store = build_vector_store(
    persist=True,
    embedding_name="bge-base-en",
    chunking_strategy="sliding_window",   # or "fixed" / "semantic"
)
```

### Cross-Encoder Re-ranking

After initial retrieval, candidates can be re-ranked using a neural **cross-encoder** model (`cross-encoder/ms-marco-MiniLM-L-6-v2`) that jointly encodes each (query, document) pair for a more accurate relevance score.

- **Enable in UI:** Toggle "🔁 Cross-Encoder Reranking" in the Streamlit sidebar
- **Enable in code:** pass `use_cross_encoder=True` to `RAGPipeline` or `hybrid_search()`
- **Fallback:** if `sentence-transformers` is not installed or the model fails, MMR reranking is used automatically

```python
from rag_pipeline import RAGPipeline
pipeline = RAGPipeline(
    vector_store=store,
    model_name="gpt-4.1",
    retrieval_mode="hybrid",
    use_cross_encoder=True,
)
```

> Switch embedding with: `python research_evaluator.py --mode single --embedding bge-large`

---

## 🚀 RAG Improvements

The following improvements were implemented on top of the baseline vector-search RAG to increase retrieval precision, faithfulness, and conversational coherence. References indicate which source file each improvement lives in.

1. **Topic-based query expansion** (`glossary_mapper.py`) — Appends topic-specific synonyms and related concepts to queries before embedding, broadening recall for technical terms (e.g., "RuBisCO" → photosynthesis synonyms added).

2. **Grade-aware retrieval** (`glossary_mapper.py`) — Retrieval parameters (chunk size, similarity threshold) are tuned based on the inferred grade level of the query, so Grade 6 answers are pitched at the right level.

3. **Subject-aware chunking** (`glossary_mapper.py`) — Chunk sizes are adjusted per subject: science content uses larger chunks to preserve context; mathematics uses smaller chunks to isolate individual worked examples.

4. **Subject-specific RAG thresholds** (`glossary_mapper.py`) — Each subject has a calibrated minimum similarity score before a document is included. Technical subjects (physics, chemistry) use stricter thresholds than broad humanities queries.

5. **Context budget per model** (`glossary_mapper.py`) — Maximum tokens forwarded to the SLM are capped per-model to avoid prompt overflow, with model-specific limits for TinyLlama (tight) vs. Mistral (generous).

6. **Contextual query rewriting** (`contextual_query_builder.py`) — Short or vague queries are rewritten into descriptive search strings before hitting the vector store, improving BGE embedding alignment.

7. **Pronoun and co-reference resolution** (`contextual_query_builder.py`) — Follow-up queries like *"what about it?"* or *"give its limitations"* are expanded by substituting the conversation topic for pronouns before retrieval.

8. **Grade-aware metadata filtering** (`retriever.py`) — ChromaDB `where` clauses filter by grade range so that retrieved documents match the inferred student level.

9. **MMR reranking** (`retriever.py`) — Maximal Marginal Relevance is applied after the initial vector search to reduce redundancy among retrieved chunks, ensuring the top-K set covers diverse aspects.

10. **Topic-anchored query expansion** (`retriever.py`, `glossary_mapper.py`) — The resolved topic label is prepended to the rewritten query before embedding, giving the vector store a strong topical anchor.

11. **Hybrid BM25 + vector retrieval** (`retriever.py`) — BM25 keyword scores are merged with vector similarity scores using a weighted average, then deduplicated and sorted. This catches exact-term matches that semantic search can miss.

12. **Token-overlap reranker** (`retriever.py`) — After hybrid search collects a 4× candidate pool, a lightweight reranker scores each candidate by token overlap with the (rewritten) query. A `TOPIC_MATCH_BONUS = 0.3` is added for documents whose `topic` metadata matches the resolved topic.

13. **Hierarchical retrieval** (`retriever.py`) — Topic routing first narrows the candidate set to documents matching the detected topic via metadata filtering, then performs chunk-level vector search within that subset.

14. **Grounding score** (`rag_pipeline.py`) — After generation, the answer is scored against the retrieved context by token overlap. If the grounding score falls below a configurable threshold, a low-grounding warning is logged and surfaced in the UI.

15. **Context budget manager** (`rag_pipeline.py`, `glossary_mapper.py`) — Retrieved chunks are truncated to fit within a per-model token budget before being inserted into the prompt, preventing silent truncation by the SLM tokenizer.

16. **Dynamic RAG threshold** (`glossary_mapper.py`) — The minimum retrieval similarity score before the system switches to LLM Fallback mode is computed dynamically based on subject and grade level, rather than using a single global constant.

17. **Conversation-aware prompting** (`rag_pipeline.py`) — The prompt template includes the last N conversation turns (formatted as dialogue) alongside retrieved context, so the SLM can produce answers that reference prior exchanges.

18. **API cost tracking** (`rag_pipeline.py`) — For LLM-mode queries (OpenAI models), the estimated USD cost is computed from input/output token counts and the per-model pricing from `MODEL_REGISTRY`, then displayed in the UI.

19. **Topic shift detection** (`contextual_query_builder.py`) — A 5-step algorithm detects when a query is a genuine topic change vs. a continuation of the current topic, preventing the rewriter from contaminating a new topic with stale context.

20. **Topic confidence scoring with decay** (`topic_memory_manager.py`) — Per-topic confidence scores accumulate as evidence appears across turns and decay when the topic is not mentioned, enabling the system to track the *most active* topic across a long conversation.

21. **LLM Fallback mode** (`rag_pipeline.py`) — When no document crosses the RAG threshold (or the query is classified as out-of-scope), the pipeline bypasses retrieval entirely and calls the SLM with a knowledge-only prompt, clearly flagging the response as a fallback.

22. **Partial RAG mode** (`rag_pipeline.py`) — When some documents are retrieved but with low confidence scores, a dedicated `PARTIAL_CONTEXT_PROMPT` informs the SLM that the context may be incomplete and asks it to flag uncertainty, instead of confabulating.

23. **Retrieval mode ablation** (`retriever.py`, `research_evaluator.py`) — The pipeline supports three swappable retrieval modes (`vector_only`, `bm25_only`, `hybrid`) to enable systematic ablation studies with identical prompts and evaluation metrics.

24. **Grounding score UI display** (`app.py`) — The Streamlit sidebar shows the grounding score for every response as a labelled metric, giving users immediate feedback on how well-grounded each answer is.

25. **Cost display** (`app.py`) — For LLM API calls, the sidebar shows the estimated cost and token breakdown (input / output / total) per query.

---

## ⭐ Bonus Features

1. **Multi-model selector UI** — The Streamlit sidebar includes a dropdown to switch between all registered SLMs at runtime. The pipeline re-initialises automatically when the model changes, preserving conversation history.

2. **Multi-embedding research evaluation** — `research_evaluator.py` supports `--embedding` selection across all 7 embedding models and can run full comparison studies with `--mode embedding_comparison`, producing a ranked summary table.

3. **Topic Confidence UI** (`app.py`) — After each response, an expandable "🎯 Topic Confidence" panel shows progress bars for the top-3 candidate topics with their confidence scores, visualising how the system chose its topic.

4. **Corpus Coverage Checker** (`app.py`) — An expandable "📊 Corpus Coverage" panel in the sidebar calls `get_corpus_stats()` live, showing total documents, topics, subjects, and a warning listing all topics with fewer than 5 documents.

5. **Session Export (JSON)** (`app.py`) — A "📥 Export Session (JSON)" button in the sidebar becomes active once the conversation contains at least one turn. It downloads a timestamped JSON file containing every query, answer, mode, detected topic, grounding score, cost, and latency for the session.

---

## 🛠️ Tech Stack

| Component | Library / Tool | Why It Was Chosen |
|---|---|---|
| **SLM runtime** | [Ollama](https://ollama.com/) | One-command local LLM server; LangChain native integration; zero API cost |
| **LLM integration** | `langchain-ollama`, `openai` | Unified interface for local and API models |
| **RAG framework** | [LangChain](https://python.langchain.com/) | Connects embeddings → vector store → prompt → LLM; swappable components |
| **Vector store** | [ChromaDB](https://www.trychroma.com/) | Lightweight, embeddable; supports metadata `where` filtering for topic routing |
| **Embeddings** | [sentence-transformers](https://www.sbert.net/) (BGE, MiniLM, MPNet, E5) | State-of-the-art open-source models; no API cost; MTEB top performers |
| **Keyword search** | [rank-bm25](https://github.com/dorianbrown/rank_bm25) | Gold-standard exact-term retrieval (BM25Okapi); complements semantic search |
| **Token counting** | [tiktoken](https://github.com/openai/tiktoken) | Accurate token counts for context budget management (cl100k_base encoding) |
| **UI** | [Streamlit](https://streamlit.io/) | Zero-boilerplate Python chat UI; rapid research prototyping |
| **Numerics** | NumPy | Cosine similarity, score normalisation |

### Why BGE over OpenAI Embeddings?

BGE (BAAI General Embeddings) consistently rank at the top of the [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) and run entirely locally:

```
"The water cycle involves evaporation"
         ↓  BGE-small-en-v1.5
[0.021, -0.143, 0.287, ..., 0.094]   ← 384 floats

"How does water move in nature?"
         ↓  BGE-small-en-v1.5
[0.018, -0.139, 0.291, ..., 0.091]   ← 384 floats

cosine similarity ≈ 0.94  ← semantically aligned
```

### Why ChromaDB over FAISS?

FAISS is faster for pure ANN search, but ChromaDB supports metadata `where` filtering — essential for hierarchical retrieval that first narrows by `topic` then searches within that subset.

---

## 📁 Project Structure

```
EduSLM-RAG/                                  (~30,720 total lines of Python)
│
├── app.py                     ~487 lines  ← Streamlit chat UI + pipeline viewer + metrics
├── main.py                    ~221 lines  ← CLI demo runner + ablation study (--ablation)
│
├── rag_pipeline.py           ~1,104 lines ← 10-step pipeline orchestrator; multi-model support
├── research_evaluator.py     ~1,657 lines ← CLI evaluation suite (all experiment modes)
├── research_config.py          ~499 lines ← MODEL_REGISTRY, EMBEDDING_MODELS, TEST_QUERIES
│
├── contextual_query_builder.py ~1,378 lines ← THE CORE CONVERSATIONAL MODULE
│   ├── QueryNormalizer              Lowercase, contraction expansion, cleanup
│   ├── TopicConfidenceScorer        Weighted keyword scoring per topic
│   ├── TopicShiftDetector           Semantic shift detection (prevents contamination)
│   │   ├── compute_similarity()         Keyword-overlap score [0, 1]
│   │   ├── is_topic_shift()             5-step shift detection algorithm
│   │   └── would_contaminate()          Rewrite safety guard
│   ├── AmbiguityResolver            Shift-aware topic disambiguation
│   └── ContextualQueryBuilder       Orchestrator → returns rewritten query + confidence
│
├── topic_memory_manager.py     ~230 lines ← Per-topic confidence with turn-based decay
├── context_memory.py            ~88 lines ← Sliding-window conversation history (last N turns)
│
├── retriever.py                ~497 lines ← Full retrieval stack
│   ├── build_vector_store()         ChromaDB setup + persistence per embedding
│   ├── BM25Index                    BM25 keyword index (rank_bm25)
│   ├── hybrid_search()              BM25 + vector weighted merge
│   ├── rerank_documents()           Token-overlap reranker (4× pool → top-K)
│   └── hierarchical_retrieve()      Topic-route → chunk-level retrieval
│
├── query_classifier.py         ~230 lines ← Subject + topic keyword heuristics
├── glossary_mapper.py          ~524 lines ← Synonym expansion, disambiguation, thresholds
├── embeddings.py               ~132 lines ← get_embeddings() factory (7 models)
│
├── data_loader.py              ~312 lines ← Corpus loader + get_corpus_stats() + chunker
├── extended_corpus_v2.py     ~4,022 lines ← Large corpus extension (trigonometry, genetics…)
├── extended_corpus_v3.py     ~1,883 lines ← Sound waves, cybersecurity, digestion…
├── extended_corpus_v4.py     ~1,251 lines ← Additional STEM topics
├── extended_corpus_v5.py     ~1,407 lines ← Additional topics
├── extended_corpus_v6.py     ~3,035 lines ← Additional topics
├── extended_corpus_v7.py     ~2,796 lines ← Additional topics
├── extended_corpus_v8.py     ~4,004 lines ← Additional topics
├── extended_corpus_v9.py     ~4,265 lines ← Latest corpus additions
│
├── evaluation.py               ~357 lines ← 6 eval metric implementations (Precision@5 etc.)
├── test_queries.py             ~341 lines ← 25+ benchmark test cases + run_benchmark()
│
├── requirements.txt                       ← Python dependencies
└── chroma_db_{embedding_name}/            ← Persisted vector store (auto-generated at runtime)
```

> **Repository size:** ~30,720 lines of Python across 22 source files.

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running
- (Optional) API keys for GPT-4.1 / Claude 3 Sonnet / Gemini 1.5 Pro

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-org/SLM-with-RAG-for-Educational-QA.git
cd SLM-with-RAG-for-Educational-QA
```

### Step 2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

**Optional: API LLM / OpenAI embedding support**

```bash
# For GPT-4.1, GPT-4o-mini, or text-embedding-3-large
pip install langchain-openai

# For Claude 3 Sonnet, Claude Haiku
pip install langchain-anthropic

# For Gemini 1.5 Pro, Gemini 1.5 Flash
pip install langchain-google-genai
```

### Step 3 — Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` and set the APIs/models you want to benchmark:

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
GROQ_API_KEY=...
DEFAULT_SLM=mistral-7b-instruct
DEFAULT_OPEN_MODEL=llama3-8b
DEFAULT_API_MODEL=gpt-4o
MULTIMODAL_EMBEDDING_MODEL=siglip
MAX_TOKENS=2048
```

To use the `nomic-embed-text` embedding model locally (optional):

```bash
ollama pull nomic-embed-text
```

### Step 4 — Verify keys are loaded

```bash
python -c "import os; print('OPENAI', bool(os.environ.get('OPENAI_API_KEY')), 'ANTHROPIC', bool(os.environ.get('ANTHROPIC_API_KEY')), 'GOOGLE', bool(os.environ.get('GOOGLE_API_KEY')), 'GROQ', bool(os.environ.get('GROQ_API_KEY')))"
```

### Step 5 — Verify corpus stats

```bash
python -c "from data_loader import get_corpus_stats; import json; print(json.dumps(get_corpus_stats(), indent=2))"
```

---

## ▶️ How to Run

### Quickstart (copy-paste)

```bash
cd /home/runner/work/SLM-with-RAG-for-Educational-QA/SLM-with-RAG-for-Educational-QA
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add only the keys/models you plan to use
streamlit run app.py
```

Open `http://localhost:8501`.

### Streamlit Chat UI

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`. The sidebar lets you select the SLM, clear the conversation, export the session as JSON, and view live corpus coverage.

### CLI Demo (6 sample queries)

```bash
python main.py
```

Runs a pre-defined conversation showing pronoun resolution, topic shifts, and LLM fallback.

### CLI Ablation Study

```bash
python main.py --ablation
```

Runs the same set of queries in `vector_only`, `bm25_only`, and `hybrid` modes and prints a comparative metrics table.

### Print Corpus Statistics

```bash
python -c "from data_loader import get_corpus_stats; import json; print(json.dumps(get_corpus_stats(), indent=2))"
```

### List Available Embedding Models

```bash
python research_evaluator.py --list-embeddings
```

### Run the Test Suite

```bash
# Run all unit tests (no API keys required for core tests)
python test.py

# Verbose output
python test.py -v

# With pytest (if installed)
pytest test.py -v
```

Tests are divided into 15 classes covering: `research_config`, `embeddings`, chunking strategies (`chunk_fixed`, `chunk_sliding_window`, `chunk_semantic`, `get_chunks`), `BM25Index`, `mmr_rerank`, `cross_encoder_rerank`, `build_vector_store` (mocked), `hybrid_search` (mocked), `hierarchical_retrieve` (mocked), `retrieve_top_k` (mocked), `_build_llm` factory, `RAGPipeline.__init__` (mocked), `compute_all_metrics`, and the benchmark runner in `test_queries.py`.

Tests that require API keys (OpenAI / Anthropic / Google) are automatically **skipped** when the corresponding environment variable is not set.

---

## 📈 Evaluation Commands

All experiments are run via `research_evaluator.py` with the `--mode` flag.

### Single Model Experiment

Run one model with the default embedding:

```bash
python research_evaluator.py --mode single --model mistral-7b-instruct
```

With a different embedding:

```bash
python research_evaluator.py --mode single --model llama3-8b --embedding siglip
```

### Retrieval Ablation Study

Run all retrieval modes for a single model and compare:

```bash
python research_evaluator.py --mode ablation --model groq-llama3-8b
```

### Model Comparison

Run all available models in `MODEL_REGISTRY` with the same retrieval mode and embedding:

```bash
python research_evaluator.py --mode model_comparison --retrieval hybrid
```

### Embedding Comparison

Run the same model across all embedding models:

```bash
python research_evaluator.py --mode embedding_comparison --model mistral-7b-instruct
```

### Full Matrix

Run every available model × every embedding combination:

```bash
python research_evaluator.py --mode full_matrix
```

### Token Comparison

Analyse token usage and cost across models:

```bash
python research_evaluator.py --mode token_comparison
```

### SLM vs. LLM Comparison

Compare model groups based on registry type (SLMs vs LLMs):

```bash
python research_evaluator.py --mode slm_vs_llm
```

### Full Evaluation Suite

Run all experiments in sequence:

```bash
python research_evaluator.py --mode full
```

### Custom Output File

```bash
python research_evaluator.py --mode single --model groq-llama3-8b --output my_results.txt
```

All results are written to the `results/` folder by default (or to a custom `--output` path).

### Generate Evaluation Graphs

After running comparison experiments, generate PNG graphs from result files.

Default behavior (recommended) reads all standard comparison outputs from `results/` and writes publication-style PNGs to `results/graphs/`:

```bash
python evaluation_graphs/generate_evaluation_graphs.py
```

Ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

Custom input/output paths:

```bash
python evaluation_graphs/generate_evaluation_graphs.py \
  --input results/model_comparison_results.txt results/token_comparison_results.txt \
  --output-dir results/graphs/research
```

### Research-grade graph workflow

```bash
# 1) Produce comparison result tables
python research_evaluator.py --mode model_comparison --retrieval hybrid --embedding bge-small
python research_evaluator.py --mode embedding_comparison --model mistral-7b-instruct
python research_evaluator.py --mode token_comparison

# 2) Generate high-quality graph set (300 DPI savefig)
python evaluation_graphs/generate_evaluation_graphs.py \
  --input results/model_comparison_results.txt \
          results/embedding_comparison_results.txt \
          results/token_comparison_results.txt \
  --output-dir results/graphs/research
```

Generated graphs include grouped accuracy charts, latency plots, hallucination-rate plots, token/cost plots, and latency-vs-accuracy scatter plots suitable for research reporting.

### Final Evaluation Script — Dataset-Driven Model Comparison

> **`final_evaluation.py` runs the actual RAG pipeline** against the
> `TEST_QUERIES` dataset defined in `research_config.py` and computes all
> metrics from real pipeline outputs — **no hardcoded or sample data**.
>
> You can also load pre-computed metrics from a CSV/JSON file using `--input`.

#### What it computes

All metrics are derived from running the pipeline on the dataset:

| # | Metric | Source | Description |
|---|--------|--------|-------------|
| 1 | **Faithfulness** | `evaluation.py` token-overlap | How well the answer stays grounded in retrieved context (0–1) |
| 2 | **Answer Relevance** | `evaluation.py` query-term recall | How directly the answer addresses the question (0–1) |
| 3 | **Context Precision** | `evaluation.py` context relevance | How relevant the retrieved context is to the question (0–1) |
| 4 | **Context Recall** | `evaluation.py` recall@K | What fraction of relevant documents were retrieved (0–1) |
| 5 | **Hallucination Rate** | Derived: `1 − Faithfulness` | Fraction of answer not grounded in context (0–1) |
| 6 | **Cost per Query** | Token counts × MODEL_REGISTRY rates | Estimated USD cost per query |
| 7 | **Cost per Token** | `cost_per_query / avg_total_tokens` | Normalised cost efficiency |
| 8 | **Final Score** | Weighted combination | `0.28×Faith + 0.24×AnsRel + 0.18×CtxPrec + 0.15×CtxRec + 0.10×CostEff − 0.05×Halluc` |

#### How to run

```bash
# 1. Run live evaluation on all available models (default)
python final_evaluation.py

# 2. Evaluate specific models only
python final_evaluation.py --models phi3 groq-llama3-8b

# 3. Custom retrieval mode and embedding
python final_evaluation.py --retrieval hybrid --embedding bge-small

# 4. Load from a pre-computed CSV/JSON (skips live evaluation)
python final_evaluation.py --input results/final_metrics.csv

# 5. Custom output directory
python final_evaluation.py --output-dir my_eval
```

#### CLI options

| Option | Default | Description |
|--------|---------|-------------|
| `--models` | All available models | Space-separated list of model names to evaluate |
| `--retrieval` | `hybrid` | Retrieval mode: `vector_only`, `bm25_only`, or `hybrid` |
| `--embedding` | `bge-small` | Embedding model for vector retrieval |
| `--input` | *(none — live eval)* | Path to pre-computed CSV/JSON; skips live evaluation |
| `--output-dir` | `results/final_evaluation` | Directory for output files |

#### Input format (for `--input` mode)

When using `--input`, the CSV/JSON must have these **required columns**:

| Column | Type | Description |
|--------|------|-------------|
| `model` | string | Model name |
| `faithfulness` | float | Faithfulness score (0–1) |
| `answer_relevance` | float | Answer relevance score (0–1) |
| `context_precision` | float | Context precision score (0–1) |
| `context_recall` | float | Context recall score (0–1) |
| `cost_per_query` | float | USD cost per query |

**Optional columns** (used when present):

| Column | Type | Description |
|--------|------|-------------|
| `model_type` | string | `"SLM"` or `"LLM"` — used for colour-coding graphs |
| `avg_input_tokens` | int | Average input tokens per query |
| `avg_output_tokens` | int | Average output tokens per query |
| `avg_total_tokens` | int | Average total tokens per query (enables per-token cost) |
| `latency_ms` | float | Average latency in milliseconds |
| `topic_accuracy` | float | Topic classification accuracy (0–1) |
| `mode_accuracy` | float | RAG mode classification accuracy (0–1) |

#### Graphs generated (8 publication-quality PNGs at 300 DPI)

| # | File | Description |
|---|------|-------------|
| 1 | `01_final_score_by_model.png` | Bar chart of weighted final scores |
| 2 | `02_five_metrics_comparison.png` | Grouped bars: Faithfulness, Answer Relevance, Context Precision, Context Recall, Hallucination Rate |
| 3 | `03_cost_per_query.png` | Cost per query (USD) |
| 4 | `04_cost_per_token.png` | Cost per token (USD) — only when `avg_total_tokens` is provided |
| 5 | `05_hallucination_rate.png` | Hallucination rate (%) per model |
| 6 | `06_avg_tokens_input_vs_output.png` | Grouped bar: input vs output tokens per query |
| 7 | `07_latency_vs_accuracy.png` | Scatter plot: latency (ms) vs topic accuracy (%) |
| 8 | `08_radar_quality_metrics.png` | Radar/spider chart of normalised quality metrics |

#### Full outputs

```
results/final_evaluation/
├── computed_metrics.csv               # Raw metrics from live evaluation (only in live mode)
├── final_evaluation_results.csv       # Ranked results with all computed columns
├── evaluation_report.txt              # Plain-text summary report
├── 01_final_score_by_model.png
├── 02_five_metrics_comparison.png
├── 03_cost_per_query.png
├── 04_cost_per_token.png
├── 05_hallucination_rate.png
├── 06_avg_tokens_input_vs_output.png
├── 07_latency_vs_accuracy.png
└── 08_radar_quality_metrics.png
```

#### Dependencies

All dependencies are in `requirements.txt`:

```bash
pip install -r requirements.txt
```

For live evaluation, you also need:
- **Ollama** running locally (for SLM models: tinyllama, phi3, gemma2, etc.)
- **API keys** set as environment variables (for LLM models: `GROQ_API_KEY`, `OPENAI_API_KEY`, etc.)

#### Example end-to-end workflow

```bash
# Step 1 — Run final evaluation directly (computes everything from the dataset)
python final_evaluation.py --models phi3 groq-llama3-8b --retrieval hybrid

# Step 2 — Or evaluate all available models at once
python final_evaluation.py

# Step 3 — (Optional) Also run research evaluator for detailed comparison tables
python research_evaluator.py --mode model_comparison --retrieval hybrid

# Step 4 — (Optional) Generate additional graph sets from comparison tables
python evaluation_graphs/generate_evaluation_graphs.py
```

#### Console output example

```
Running live evaluation on 30 test queries...
Models: ['phi3', 'groq-llama3-8b']
Retrieval: hybrid | Embedding: bge-small

============================================================
  Evaluating: phi3  |  Embedding: bge-small  |  Retrieval: hybrid
============================================================
  ...
  ✓ phi3: faith=0.612  ans_rel=0.534  ctx_prec=0.487  ctx_rec=0.891  cost/q=$0.000000  latency=3241ms

════════════════════════════════════════════════════════════════════════════════
  FINAL MODEL EVALUATION — 5 Metrics + Per-Token Cost
════════════════════════════════════════════════════════════════════════════════
         model model_type faithfulness answer_relevance context_precision ...
          phi3        SLM       0.6120           0.5340            0.4870 ...
groq-llama3-8b        LLM       0.7230           0.6210            0.5540 ...

  🏆 Best model: groq-llama3-8b  (final_score = 0.5824)
════════════════════════════════════════════════════════════════════════════════
```

### Multimodal Master Prompt (SLM-optimized)

The multimodal answer prompt is configured in `rag_pipeline.py` (`MULTIMODAL_PROMPT`) and is designed to:
- force long, structured responses (700–1000 words),
- maximize faithfulness to retrieved text/image context,
- explicitly report missing information as **"Not found in context"**,
- improve output-token depth for SLMs.

### Strategy to maximize output tokens with high SLM metrics

1. Use `siglip` first for multimodal retrieval quality, and benchmark `openclip`.
2. Keep retrieval mode `hybrid` with clean top-K context.
3. Use structured prompts with sections (Final Answer, Evidence, Explanation, Multimodal Insight, Limitations).
4. Keep `MAX_TOKENS` high (2048+) and avoid overly short prompts.
5. Track token output and quality jointly in `final_evaluation.py`.

---

## 💬 Example Conversation Flows

### Flow 1 — Pronoun Resolution

```
User:  explain water cycle
Bot:   [RAG] The water cycle describes how water moves through the
       environment via evaporation, condensation, and precipitation...

User:  how does it work
       ↑ "it" resolved to "water cycle" via conversation memory
Bot:   [RAG] The water cycle works by solar energy heating surface water,
       causing evaporation...

User:  what are its main components
       ↑ "its" resolved to "water cycle"
Bot:   [RAG] The main components of the water cycle are:
       1. Evaporation — water → water vapour
       2. Condensation — water vapour → clouds
       3. Precipitation — rain / snow falls...
```

### Flow 2 — Topic Shift Detection

```
User:  how does photosynthesis work
Bot:   [RAG] Photosynthesis is the process by which plants use sunlight,
       water, and CO₂ to produce glucose and oxygen...

User:  now explain bicycle brakes
       ↑ Topic shift detected: photosynthesis → bicycle
       ↑ Context NOT carried over (would contaminate new topic)
Bot:   [RAG] Bicycle brakes work by applying friction to the wheel rim
       or disc via brake pads, converting kinetic energy to heat...

User:  what about carbon cycle now
       ↑ Another topic shift detected: bicycle → carbon cycle
Bot:   [RAG] The carbon cycle describes how carbon moves between the
       atmosphere, living organisms, and the Earth's crust...
```

### Flow 3 — Out-of-Scope Fallback with Memory

```
User:  how does a car engine work
       ↑ No corpus documents match this topic
Bot:   [LLM Fallback] A car engine converts fuel into mechanical energy
       via internal combustion. The four strokes are: intake, compression,
       power, and exhaust...
       ⚠️  Note: This answer is based on the model's training knowledge,
           not retrieved documents.

User:  what are advantages of it
       ↑ "it" resolved to "car engine" via conversation memory
       ↑ Still no relevant documents found
Bot:   [LLM Fallback] Advantages of car engines include high power output,
       availability of fuel infrastructure...
```

---

## 🔬 Research Overview

This project frames educational QA as a **retrieval-augmented conversational NLP problem** with the following research dimensions:

| Axis | Values Studied |
|---|---|
| **Model size** | TinyLlama 1.1B → Mistral 7B → GPT-3.5/4o-mini |
| **Retrieval mode** | vector-only · BM25-only · hybrid |
| **Embedding model** | 7 models from 384-dim to 1024-dim |
| **Conversation handling** | single-turn · multi-turn with pronoun resolution |
| **Retrieval mode** | RAG · Partial RAG · LLM Fallback |

### Evaluation Metrics

Six metrics are computed after every query (`evaluation.py`):

| Metric | What It Measures |
|---|---|
| **Precision@5** | Fraction of retrieved documents that match the detected topic |
| **Recall@5** | Fraction of relevant corpus documents that were retrieved |
| **MRR** | Mean Reciprocal Rank — position of the first relevant document |
| **Faithfulness** | Token overlap between the generated answer and retrieved context |
| **Answer Relevance** | Fraction of query terms covered by the answer |
| **Context Relevance** | Average query-term coverage per retrieved document |

Score thresholds: ✓ ≥ 0.7 · ⚠ ≥ 0.5 · ✗ < 0.5

### Test Query Suite

`research_config.py` defines **35 structured test queries** across 10 categories:

| Category | Examples |
|---|---|
| `direct` | "explain water cycle", "how does photosynthesis work" |
| `followup_pronoun` | "how does it work", "what are its components" |
| `followup_short` | "advantages", "limitations?", "give example" |
| `continuation` | "and what are its stages", "what about applications" |
| `ambiguous` | "what is cycle", "explain the process" |
| `topic_shift` | "now explain bicycle brakes", "what about carbon cycle now" |
| `out_of_scope` | "how does a car engine work", "explain agriculture" |
| `partial_rag` | "explain dispersion of light" |
| `vague` | "cycle", "explain", "   " |
| `compound` | "explain photosynthesis and also bicycle gears" |

---

## 📦 Requirements

```
# Core RAG stack
langchain>=0.2.0
langchain-community>=0.2.0
langchain-core>=0.2.0

# Vector store
chromadb>=0.5.0

# Embeddings (BGE / MiniLM / mpnet / E5 — also used for cross-encoder)
sentence-transformers>=3.0.0
huggingface-hub>=0.23.0
transformers>=4.40.0

# Optional local embeddings via Ollama
ollama>=0.2.0
langchain-ollama>=0.1.0

# Streamlit UI
streamlit>=1.35.0
python-dotenv>=1.0.1

# Hybrid search — BM25 keyword retrieval (Sparse Embeddings)
rank-bm25>=0.2.2

# Token counting
tiktoken>=0.7.0

# Multimodal extension
Pillow>=10.2.0
faiss-cpu>=1.7.4
pypdf>=4.0.0
torch>=2.2.0

# Utilities
numpy>=1.26.0

# Groq API LLM
langchain-groq>=0.1.0
```

Install all core dependencies:

```bash
pip install -r requirements.txt
```

Install optional API provider packages as needed:

```bash
pip install langchain-openai      # OpenAI
pip install langchain-anthropic   # Anthropic
pip install langchain-google-genai # Google
```

---

*EduSLM-RAG is a research prototype. Corpus coverage, model behaviour, and evaluation results will vary by Ollama version and hardware.*
