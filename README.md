# 🎓 EduSLM-RAG — Educational Conversational QA with Contextual Retrieval

> A research-grade **Retrieval-Augmented Generation (RAG)** system built for educational question answering using a Small Language Model (SLM). Designed to be smart about *context*, honest about *ambiguity*, and scalable to *large document collections*.

---

## 📌 Table of Contents

- [What This Project Does](#-what-this-project-does)
- [The Two Problems It Solves](#-the-two-problems-it-solves)
- [Architecture Overview](#-architecture-overview)
- [Pipeline — Step by Step](#-pipeline--step-by-step)
- [Component Deep Dives](#-component-deep-dives)
- [Tech Stack & Why Each Tool Was Chosen](#-tech-stack--why-each-tool-was-chosen)
- [Knowledge Base](#-knowledge-base)
- [Evaluation Metrics](#-evaluation-metrics)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Running the App](#-running-the-app)
- [Example Conversation Flows](#-example-conversation-flows)

---

## 🧠 What This Project Does

EduSLM-RAG is a **conversational educational assistant** that answers student questions about science topics using a local Small Language Model (Phi-3). Unlike a basic chatbot, it:

- **Remembers conversation context** — "What is cycle?" after discussing water → correctly resolves to "water cycle"
- **Detects when you've changed topics** — prevents blending two unrelated topics like "nervous photosynthesis"
- **Retrieves relevant documents** before answering — grounds responses in real educational content, not hallucinations
- **Evaluates itself** — computes 6 quality metrics per response, visible in the UI

```
Without this system:
  User: "Explain photosynthesis"
  User: "What is nervous system?"
  System: ← "nervous photosynthesis"  🚫 WRONG

With this system:
  User: "Explain photosynthesis"
  User: "What is nervous system?"
  System: ← Correctly identifies this is a new, unknown topic 
           and answers without blending contexts  ✅ CORRECT
```

---

## 🔥 The Two Problems It Solves

### Problem 1 — Context Contamination

**What goes wrong in naïve RAG:** When a student says "What is cycle?" the system needs to use conversation memory to figure out if they mean *water cycle*, *carbon cycle*, or *bicycle*. That's good design. But a naïve implementation will also use memory for completely unrelated queries like "What is the nervous system?" — leading to absurd outputs.

```
❌ Naïve Behaviour:
   Turn 1: "Explain photosynthesis"   → memory topic = photosynthesis
   Turn 2: "What is nervous system?"
           System sees "system" is ambiguous
           System checks memory → photosynthesis
           System outputs: "nervous photosynthesis"   ← CATASTROPHIC BUG
```

**The fix — Three-layer protection:**

```
✅ Fixed Behaviour:
   Turn 1: "Explain photosynthesis"   → memory topic = photosynthesis
   Turn 2: "What is nervous system?"
           ┌─ TopicShiftDetector: "nervous" is NOT in any known topic vocabulary
           │   → SHIFT DETECTED
           ├─ AmbiguityResolver: skips memory, leaves "system" unresolved
           └─ Rewrite safety rule: blocks "nervous photosynthesis" substitution
           System outputs: "What is nervous system?" (no contamination) ✅
```

---

### Problem 2 — Scaling to Large Document Collections

A basic RAG system performs a single vector search across the entire corpus. As documents grow to thousands, this becomes slow and imprecise. EduSLM-RAG handles scale via a layered retrieval stack:

| Challenge | Solution |
|---|---|
| Too many irrelevant documents | **Metadata filtering** — Chroma `where` clauses on `topic`, `subject`, `grade` |
| Keyword queries miss semantic matches | **Hybrid Search** — BM25 keyword search + BGE vector search, merged by weighted score |
| Top candidates are noisy | **Reranking** — Collect top-20, score by token overlap + topic bonus, return top-5 |
| Full corpus grows too large | **Hierarchical Retrieval** — Stage 1 topic-routes to narrow corpus, Stage 2 chunks it |
| Long documents have uneven relevance | **Document Chunking** — `chunk_size=400, chunk_overlap=50` via `RecursiveCharacterTextSplitter` |

---

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EduSLM-RAG System                                 │
│                                                                             │
│  ┌──────────────┐     ┌───────────────────────────────────────────────┐    │
│  │  Streamlit   │     │              RAG Pipeline (10 Steps)           │    │
│  │    UI        │────▶│                                               │    │
│  │  (app.py)    │     │  ① Receive Question                          │    │
│  └──────────────┘     │  ② Load Conversation Memory                 │    │
│                        │  ③ Contextual Query Builder ◀── NEW         │    │
│                        │     ├─ QueryNormalizer                      │    │
│  ┌──────────────┐     │     ├─ TopicConfidenceScorer                │    │
│  │ Conversation  │     │     ├─ TopicShiftDetector ◀── KEY FIX      │    │
│  │   Memory      │◀───│     ├─ AmbiguityResolver                    │    │
│  │(context_     │     │     └─ Rewrite Safety Guard                 │    │
│  │ memory.py)   │     │  ④ Ambiguity Detection                      │    │
│  └──────────────┘     │  ⑤ Query Classification                     │    │
│                        │  ⑥ Glossary / Concept Mapping               │    │
│  ┌──────────────┐     │  ⑦ Hierarchical Retrieval ◀── UPGRADED     │    │
│  │    Topic      │     │     ├─ Stage 1: Topic Routing               │    │
│  │   Memory      │◀───│     ├─ Stage 2: Hybrid BM25 + Vector        │    │
│  │  Manager      │     │     └─ Reranking (top-20 → top-5)          │    │
│  └──────────────┘     │  ⑧ Top-K Document Selection                 │    │
│                        │  ⑨ Answer Generation (Phi-3 via Ollama)    │    │
│  ┌──────────────┐     │  ⑩ Evaluation Metrics + Memory Update      │    │
│  │  Chroma DB   │◀───│                                               │    │
│  │ (Vector Store)│     └───────────────────────────────────────────────┘    │
│  └──────────────┘                                                           │
│         ▲                                                                   │
│  ┌──────┴───────┐                                                          │
│  │  BGE-small   │  ← Embeds all 14 documents into 384-dim vectors          │
│  │  Embeddings  │                                                          │
│  └──────────────┘                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔁 Pipeline — Step by Step

```
USER QUESTION
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 1 — Receive Question                              │
│  Raw text from the user is captured.                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 2 — Conversation Memory                           │
│  Load last N turns (topics, answers) from session.      │
│  TopicMemoryManager applies confidence decay to stale   │
│  topics (−0.25/turn without mention).                   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 3 — Contextual Query Builder                      │
│                                                         │
│  A. QueryNormalizer                                     │
│     lowercase + expand contractions + strip punctuation │
│                                                         │
│  B. TopicConfidenceScorer                               │
│     Weighted keyword scan → score per topic             │
│     Score ≥ 2.0 = high confidence → can override memory │
│                                                         │
│  C. TopicShiftDetector  ◀── KEY INNOVATION              │
│     Computes keyword-overlap similarity between query   │
│     and memory topic. Checks for:                       │
│       - Direct topic keyword match → no shift           │
│       - Content words match a DIFFERENT topic → shift   │
│       - Unknown domain words (len≥5) → shift            │
│                                                         │
│  D. AmbiguityResolver                                   │
│     Priority 1: High-confidence query keywords          │
│     Priority 2: Disambiguation signals (pedal→bicycle)  │
│     Priority 3: Memory (only if NO shift detected)      │
│     Priority 4: Unresolved → request clarification      │
│                                                         │
│  E. Rewrite Safety Guard (would_contaminate)            │
│     Blocks nonsensical substitutions before rewriting   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 4 — Ambiguity Detection (safety net)              │
│  Final check: any still-unresolved ambiguous terms?     │
│  If yes + no context → ask user for clarification       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 5 — Query Classification                          │
│  Subject detection: geography / biology / physics…      │
│  Topic scoring using keyword heuristics                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 6 — Glossary Mapping                              │
│  Synonym expansion: "chlorophyll" → photosynthesis      │
│  Appends canonical topic to query for retrieval boost   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 7 — Hierarchical Retrieval                        │
│                                                         │
│  Stage 1 — Topic Routing:                              │
│    If topic known → Chroma metadata filter on "topic"  │
│    → Narrows search to topically relevant chunks only   │
│                                                         │
│  Stage 2 — Hybrid Search (within filtered scope):      │
│    BM25 (keyword) → top-20 candidates                  │
│    Vector (BGE)   → top-20 candidates                  │
│    Merge: combined score = 0.5×BM25 + 0.5×vector       │
│                                                         │
│  Reranking:                                             │
│    Score each candidate by token-overlap + topic bonus  │
│    Return top-5 highest-scoring documents               │
│                                                         │
│  Fallback: if Stage 1 < 2 results → full-corpus search  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 8 — Top-K Document Selection                      │
│  Final top-5 documents selected. Grade + topic logged.  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 9 — Answer Generation (Phi-3 via Ollama)          │
│                                                         │
│  Mode RAG:         Retrieved context injected into      │
│                    prompt. Phi-3 answers grounded in    │
│                    documents.                           │
│                                                         │
│  Mode LLM Fallback: Retrieval score < 0.6 threshold.   │
│                     Phi-3 answers from own knowledge.   │
│                     (Faithfulness score = 0.0)          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 10 — Evaluation + Memory Update                   │
│  Compute 6 metrics. Update ConversationMemory and       │
│  TopicMemoryManager. Display in Streamlit right panel.  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 Component Deep Dives

### `TopicShiftDetector` — The Core Innovation

This is the module that prevents context contamination. It answers the question: *"Is this new query about the same topic we were discussing, or has the user changed subjects?"*

**The 5-step decision algorithm:**

```
Given: query = "What is nervous system?"
       last_topic = "photosynthesis"
       ambiguous_terms = ["system"]

Step 1: Does query contain any photosynthesis keywords?
        → "nervous" ∉ {photosynthesis, chlorophyll, glucose, …}
        → No match → continue

Step 2: Extract non-ambiguous content words (excluding "system" and stop-words)
        → content_words = ["nervous"]

Step 3: Any content words match a DIFFERENT known topic?
        → "nervous" ∉ {water, evaporation, …}  (water cycle)
        → "nervous" ∉ {carbon, co2, fossil, …}  (carbon cycle)
        → "nervous" ∉ {bicycle, pedal, gear, …}  (bicycle)
        → No known topic match → continue

Step 4: Any content words ≥ 5 chars that don't appear in ANY topic vocabulary?
        → "nervous" has 7 chars, appears in no topic vocabulary
        → SHIFT DETECTED ✅ (reason: "unknown_domain_words")

Result: is_shift = True → memory is NOT used → no contamination
```

**Counter-example (correctly NOT a shift):**

```
Given: query = "What is cycle?"
       last_topic = "water cycle"
       ambiguous_terms = ["cycle"]

Step 1: Does query contain water cycle keywords?
        → No direct match → continue

Step 2: Extract non-ambiguous content words (excluding "cycle")
        → After removing "cycle" and stop-words: content_words = []

Step 3: No non-ambiguous content words → cannot determine shift
        → SHIFT NOT DETECTED (reason: "no_unambiguous_content")

Result: is_shift = False → memory IS used → resolved to "water cycle" ✅
```

---

### Hybrid Search Architecture

```
                         Query
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
    ┌─────────────────┐       ┌─────────────────────┐
    │   BM25 Search   │       │   Vector Search      │
    │  (rank_bm25)    │       │  (BGE + Chroma)      │
    │                 │       │                      │
    │ Tokenise query  │       │ Embed query → 384-d  │
    │ Score by term   │       │ Cosine similarity    │
    │ frequency +     │       │ with stored vectors  │
    │ inverse doc freq│       │                      │
    │                 │       │ Optional: metadata   │
    │ Good at:        │       │ filter on topic/     │
    │ exact keywords  │       │ subject/grade        │
    │ technical terms │       │                      │
    │                 │       │ Good at: paraphrases │
    │                 │       │ semantic meaning     │
    └────────┬────────┘       └──────────┬───────────┘
             │   top-20 candidates        │   top-20 candidates
             │                            │
             └────────────┬───────────────┘
                          │
                          ▼
               ┌────────────────────┐
               │   Score Merging    │
               │                    │
               │ Normalise both     │
               │ score ranges [0,1] │
               │                    │
               │ combined =         │
               │  0.5 × BM25_score  │
               │ + 0.5 × vec_score  │
               │                    │
               │ (alpha=0.5 gives   │
               │  equal weight)     │
               └─────────┬──────────┘
                         │
                         ▼
               ┌────────────────────┐
               │     Reranker       │
               │                    │
               │ Token-overlap score│
               │ + topic_bonus=0.3  │
               │   if metadata match│
               │ - short chunks     │
               │   × 0.5 penalty    │
               │                    │
               │ top-20 → top-5     │
               └─────────┬──────────┘
                         │
                         ▼
                    Top-5 Documents
```

---

### Topic Confidence Decay Model

```
Topic Confidence over Conversation Turns

Confidence
    │
1.0 ┤ ●────●                          ●────
    │      │                          │
0.75┤      │                          │
    │      │                          │
0.5 ┤      │                          │
    │      ╲                          │
0.25┤       ╲                         │
    │        ●  (0.75)                │
0.0 ┤         ╲─────────●────●  (new topic mentioned here) 
    └──────────┬─────┬──┬────┬────────┬──────
              T1    T2  T3   T4      T5
              
Turn 1: water cycle mentioned   → confidence = 1.0
Turn 2: water cycle again       → confidence = 1.0 (reset)
Turn 3: no topic                → confidence = 0.75 (−0.25 decay)
Turn 4: no topic                → confidence = 0.50 (−0.25 decay)
Turn 5: photosynthesis          → water cycle = 0.25; photosynthesis = 1.0

Active Topic Threshold = 0.30
→ Topic considered "stale" and no longer drives disambiguation
```

---

## ⚙️ Tech Stack & Why Each Tool Was Chosen

### LLM — Phi-3 via Ollama

**Why Phi-3:** A Small Language Model (SLM) from Microsoft, optimised for reasoning tasks. Runs entirely locally — no API keys, no cloud costs, no data leaving your machine. Suited for educational use cases where responses should be concise and factual.

**Why Ollama:** The simplest way to run LLMs locally. One command to install, one command to pull the model. LangChain has a first-class integration.

```
User Query + Context
        │
        ▼
   Ollama Server
   (localhost:11434)
        │
        ▼
     Phi-3 SLM
   (runs on CPU/GPU)
        │
        ▼
   Generated Answer
```

---

### Embeddings — BGE-small-en-v1.5

**Why BGE:** BAAI General Embeddings are a family of state-of-the-art open-source embedding models consistently ranking at the top of the MTEB benchmark. The "small" variant offers an excellent accuracy/speed tradeoff, producing 384-dimensional vectors that capture semantic meaning well.

**Why not OpenAI embeddings:** BGE runs fully locally. No API costs. No data leaves the system.

```
Text → [BGE-small-en-v1.5] → 384-dimensional vector

"The water cycle involves evaporation"
         ↓ embed
[0.021, -0.143, 0.287, ..., 0.094]   ← 384 floats

"How does water move in nature?"
         ↓ embed
[0.018, -0.139, 0.291, ..., 0.091]   ← 384 floats

cosine similarity = 0.94  ← semantically similar!
```

---

### Vector Database — Chroma

**Why Chroma:** A lightweight, embeddable vector database perfect for research and local deployment. Supports:
- Persistent storage to disk (survives restarts)
- Metadata filtering (`where` clauses) — essential for topic routing
- Python-native API
- Built-in LangChain integration

**Alternative considered:** FAISS is faster at pure ANN search but has no metadata filtering. Chroma's filtering is the key feature enabling hierarchical retrieval.

---

### RAG Framework — LangChain

**Why LangChain:** Provides the plumbing that connects all components (embeddings → vector store → LLM → prompt templates). Allows switching any component without rewriting the pipeline. The abstractions for `Document`, `PromptTemplate`, and vector store interfaces are all from LangChain.

---

### Keyword Search — BM25 via rank-bm25

**Why BM25:** Vector search is excellent at semantic similarity but can miss exact keyword matches (e.g., a student asking about "RuBisCO" — a precise technical term). BM25 (Best Match 25) is the gold-standard classical information retrieval algorithm that excels at exact term frequency matching. Combining both gives the best of both worlds.

---

### UI — Streamlit

**Why Streamlit:** Zero-boilerplate Python web UI. A chat interface, metrics table, and step-by-step debug panel can be built in ~100 lines. Ideal for a research prototype where iteration speed matters more than production polish.

---

## 📚 Knowledge Base

14 documents across 4 topics, manually curated for educational clarity:

```
┌─────────────────┬──────────────────────────────┬─────────┬───────────┐
│ Topic           │ Subject                       │ Grade   │ Docs      │
├─────────────────┼──────────────────────────────┼─────────┼───────────┤
│ Water Cycle     │ Geography, Biology            │ 6–7     │ 4         │
│ Carbon Cycle    │ Biology, Environmental Science│ 8–9     │ 3         │
│ Bicycle         │ Transportation, Physics       │ 5–9     │ 4         │
│ Photosynthesis  │ Biology                       │ 7–11    │ 4 (+ 1)   │
└─────────────────┴──────────────────────────────┴─────────┴───────────┘
```

Each document includes metadata used for retrieval filtering:

```json
{
  "text": "The water cycle describes evaporation and condensation…",
  "topic": "water_cycle",
  "subject": "geography",
  "grade": "6"
}
```

At ingestion time, each document is chunked (`chunk_size=400, overlap=50`) so that:
- Long documents don't dilute retrieval relevance
- Each chunk covers one focused concept
- Chunk boundaries overlap so context isn't lost at edges

---

## 📊 Evaluation Metrics

After every query, 6 metrics are computed and displayed in the Streamlit sidebar:

```
┌─────────────────────┬──────────────────────────────────────────────────────┐
│ Metric              │ What It Measures                                     │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ Precision@5         │ Of 5 retrieved docs, what fraction match the topic?  │
│                     │ High = system retrieved the right subject matter      │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ Recall@5            │ Of all relevant docs in corpus, what % was retrieved?│
│                     │ High = system found most of the available evidence    │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ MRR                 │ 1 / rank of first relevant doc (1.0 = it's #1)       │
│                     │ Measures whether the BEST doc appears first           │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ Faithfulness        │ Token overlap: answer vs. retrieved context           │
│                     │ High = answer stays grounded in retrieved docs        │
│                     │ Note: always 0.0 in LLM Fallback mode                │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ Answer Relevance    │ Fraction of query terms covered by the answer         │
│                     │ High = answer actually addresses what was asked       │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ Context Relevance   │ Average query-term coverage per retrieved document    │
│                     │ High = retrieved docs are genuinely related to query  │
└─────────────────────┴──────────────────────────────────────────────────────┘

Status thresholds:
  ✓ good   — score ≥ 0.7
  ⚠ check  — score ≥ 0.5
  ✗ low    — score < 0.5
```

---

## 📁 Project Structure

```
EduSLM-RAG/
│
├── app.py                       ← Streamlit UI (chat + pipeline viewer + metrics)
├── main.py                      ← CLI demo runner (6 sample queries)
│
├── rag_pipeline.py              ← 10-step pipeline orchestrator
│
├── contextual_query_builder.py  ← THE CORE MODULE
│   ├── QueryNormalizer              Lowercase + contraction expansion + cleanup
│   ├── TopicConfidenceScorer        Weighted keyword scoring per topic
│   ├── TopicShiftDetector           ★ Semantic shift detection (prevents contamination)
│   │   ├── compute_similarity()         Keyword-overlap [0,1]
│   │   ├── is_topic_shift()             5-step shift detection algorithm
│   │   └── would_contaminate()          Rewrite safety guard
│   ├── AmbiguityResolver            Shift-aware topic disambiguation
│   └── ContextualQueryBuilder       Orchestrator → returns rewritten query
│
├── topic_memory_manager.py      ← Per-topic confidence with decay over turns
├── context_memory.py            ← Conversation history (last N turns)
│
├── retriever.py                 ← Full retrieval stack
│   ├── build_vector_store()         Chroma setup + persistence
│   ├── BM25Index                    BM25 keyword index (rank_bm25)
│   ├── hybrid_search()              BM25 + vector, weighted merge
│   ├── rerank_documents()           Token-overlap reranker (top-20 → top-5)
│   └── hierarchical_retrieve()      Topic-route → chunk-level retrieval
│
├── query_classifier.py          ← Subject + topic keyword heuristics
├── glossary_mapper.py           ← Synonym expansion + disambiguation signals
├── embeddings.py                ← BGE embedding model setup
│
├── data_loader.py               ← 14-document educational knowledge base
│   └── get_chunked_texts_and_metadatas()  chunk_size=400, overlap=50
│
├── evaluation.py                ← 6 evaluation metric implementations
│
├── requirements.txt             ← Python dependencies
└── chroma_db/                   ← Persisted vector store (auto-generated)
```

---

## 🚀 Setup & Installation

### Prerequisites

| Requirement | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Runtime |
| Ollama | Latest | Local LLM serving |
| ~3 GB disk | — | Phi-3 model weights |
| ~2 GB RAM | — | BGE embeddings + Chroma |

---

### Step 1 — Install Ollama

Ollama is the local LLM runtime. Install it once, then pull models on demand.

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** Download the installer from [https://ollama.com/download](https://ollama.com/download)

After installation, start the server and pull Phi-3:
```bash
# Start the Ollama server (keep this terminal open)
ollama serve

# In a new terminal, pull the Phi-3 model (~2 GB download)
ollama pull phi3
```

Verify the model is available:
```bash
ollama list
# Should show: phi3   ...   2.2 GB
```

---

### Step 2 — Clone and Set Up Python Environment

```bash
# Clone the repository
git clone https://github.com/your-org/eduslm-rag.git
cd eduslm-rag

# Create and activate a virtual environment (strongly recommended)
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

---

### Step 3 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:

```
langchain>=0.2.0              # RAG pipeline framework
langchain-community>=0.2.0    # Ollama + HuggingFace + Chroma integrations
chromadb>=0.5.0               # Vector database
sentence-transformers>=3.0.0  # BGE embedding model
huggingface-hub>=0.23.0       # Model download from HuggingFace
transformers>=4.40.0          # Tokeniser + model internals
ollama>=0.2.0                 # Ollama Python client
streamlit>=1.35.0             # Web UI
rank-bm25>=0.3.1              # BM25 keyword search
tiktoken>=0.7.0               # Token counting
numpy>=1.26.0                 # Numerical utilities
```

> **First run note:** `sentence-transformers` will automatically download the BGE model (~130 MB) from HuggingFace on first use.

---

### Step 4 — Verify Everything Works

```bash
# Quick check: can Python find all dependencies?
python -c "import langchain, chromadb, streamlit, rank_bm25; print('All dependencies OK')"

# Check Ollama is serving Phi-3
curl http://localhost:11434/api/tags
# Should include "phi3" in the response
```

---

## ▶️ Running the App

### Option A — Streamlit Web UI (Recommended)

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

```
UI Layout:
┌──────────────────────────────────────────────────────────────┐
│ ⚙️ Sidebar           │ Chat (60%)     │ Pipeline (40%)       │
│                      │                │                      │
│ [Clear Chat]         │ 🎓 EduRAG     │ 🔍 Pipeline Steps    │
│                      │                │  [Step  1] ...       │
│ Stack info:          │ User: ...      │  [Step  3] ...       │
│ Phi-3 · BGE · Chroma │ Bot:  ...      │  [Step  7] ...       │
│                      │                │                      │
│ 💡 Example queries   │ [Ask a Q...]   │ 📊 Evaluation        │
│                      │                │  Precision@5: 0.8    │
│                      │                │  Recall@5:    1.0    │
│                      │                │  MRR:         1.0    │
└──────────────────────────────────────────────────────────────┘
```

---

### Option B — Command Line Demo

```bash
python main.py
```

Runs 6 pre-set queries demonstrating:
1. Basic topic resolution
2. Ambiguity resolution via memory ("What is cycle?" → water cycle)
3. Topic shift detection ("How does a cycle move?" → bicycle)
4. Direct query handling (photosynthesis)
5. Sub-topic within topic (Calvin cycle)
6. Fresh query (bicycle gears)

Prints debug logs for every pipeline step plus evaluation metrics.

---

## 💬 Example Conversation Flows

### Flow 1 — Ambiguity Resolution via Context

```
Turn 1:  User: "Explain water cycle"
         → memory: water_cycle, confidence=1.0
         → Answer: [water cycle explanation]

Turn 2:  User: "What is cycle?"
         → ambiguous: ["cycle"]
         → TopicShiftDetector: no content words except "cycle" → NO SHIFT
         → AmbiguityResolver: memory used → "water cycle"
         → Rewritten: "What is the water cycle?"
         → Answer: [water cycle answer]

Turn 3:  User: "How does a cycle move?"
         → ambiguous: ["cycle"]
         → disambiguation signal: "move" → "bicycle"
         → Rewritten: "How does a bicycle move?"
         → Topic switched: water_cycle → bicycle
         → Answer: [bicycle movement explanation]
```

---

### Flow 2 — Context Contamination Prevention

```
Turn 1:  User: "Explain photosynthesis"
         → memory: photosynthesis, confidence=1.0
         → Answer: [photosynthesis explanation]

Turn 2:  User: "What is nervous system?"
         → ambiguous: ["system"]
         → TopicShiftDetector:
              ✗ "nervous" ∉ photosynthesis keywords
              → content word "nervous" (7 chars, unknown domain)
              → SHIFT DETECTED
         → AmbiguityResolver: memory SKIPPED
         → Rewritten: "What is nervous system?" (unchanged)
         → Retrieval: full-corpus (no topic routing)
         → Answer: "The provided context does not contain information
                    about the nervous system..." ← CORRECT
```

---

### Flow 3 — High-Confidence Topic Switch

```
Turn 1:  User: "Explain the water cycle"
         → memory: water_cycle

Turn 2:  User: "What is the Calvin cycle?"
         → TopicConfidenceScorer:
              "calvin" → photosynthesis score = 3.0  (≥ 2.0 threshold)
              → HIGH CONFIDENCE switch to photosynthesis
         → Rewritten: "What is the Calvin cycle? (photosynthesis)"
         → Topic switched: water_cycle → photosynthesis
         → Answer: [Calvin cycle / light-independent reactions explanation]
```

---

## 🛠️ Configuration & Tuning

Key constants you can adjust:

```python
# In contextual_query_builder.py
TOPIC_SWITCH_THRESHOLD = 2.0        # Minimum score to switch topics (lower = more switches)
MIN_DOMAIN_SPECIFIC_WORD_LENGTH = 5 # Words shorter than this aren't treated as domain terms

# In retriever.py  
TOPIC_MATCH_BONUS = 0.3             # Extra score for topic-matching docs during reranking
CANDIDATE_POOL_MULTIPLIER = 4       # 4× pool before reranking (higher = more thorough)

# In rag_pipeline.py
RAG_SIMILARITY_THRESHOLD = 0.6      # Below this → LLM Fallback mode
RETRIEVAL_CANDIDATES = 20           # Candidates collected before top-K selection
TOP_K = 5                           # Final documents passed to LLM

# In topic_memory_manager.py
DECAY_RATE = 0.25                   # Confidence lost per turn without topic mention
ACTIVE_THRESHOLD = 0.3              # Below this → topic no longer drives disambiguation
```

---

## 🔍 Adding New Topics / Documents

To extend the knowledge base, add entries to `EDUCATIONAL_DOCUMENTS` in `data_loader.py`:

```python
{
    "text": "Your educational content here...",
    "subject": "biology",           # Must match SUBJECT_KEYWORDS in query_classifier.py
    "topic": "cell_biology",        # New topic name
    "grade": "9",
}
```

Then update keyword maps in:
- `contextual_query_builder.py` → `TOPIC_KEYWORD_WEIGHTS`
- `query_classifier.py` → `TOPIC_KEYWORDS` and `SUBJECT_KEYWORDS`
- `glossary_mapper.py` → `GLOSSARY` and `TOPICS`

Finally, delete the `chroma_db/` directory to force a rebuild of the vector store on the next run.

---

## 📝 License

This project is for educational and research purposes.

---

*Built with Phi-3 · BGE-small · Chroma · LangChain · BM25 · Streamlit*
