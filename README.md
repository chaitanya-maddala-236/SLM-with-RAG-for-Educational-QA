# 🎓 EduSLM-RAG — Educational Conversational QA with Contextual Retrieval

> A research-grade **Retrieval-Augmented Generation (RAG)** system built for educational question answering using a Small Language Model (SLM). Designed to be smart about *context*, honest about *ambiguity*, and scalable to *large document collections*.

---

## 📌 Table of Contents

- [What This Project Does](#-what-this-project-does)
- [The Two Problems It Solves](#-the-two-problems-it-solves)
- [Architecture Overview](#-architecture-overview)
- [Pipeline — Step by Step](#-pipeline--step-by-step)
- [Component Deep Dives](#-component-deep-dives)
- [Retrieval Quality Improvements](#-retrieval-quality-improvements)
- [Tech Stack & Why Each Tool Was Chosen](#-tech-stack--why-each-tool-was-chosen)
- [Knowledge Base](#-knowledge-base)
- [Evaluation Metrics](#-evaluation-metrics)
- [Project Structure](#-project-structure)
- [Module Documentation](#-module-documentation)
- [Setup & Installation](#-setup--installation)
- [Running the App](#-running-the-app)
- [Example Conversation Flows](#-example-conversation-flows)
- [Research Overview](#-research-overview)
- [System Architecture](#-system-architecture)
- [Ablation Study](#-ablation-study)
- [Multi-Model Comparison](#-multi-model-comparison)
- [How to Run](#-how-to-run)
- [Requirements](#-requirements)
- [Research Contribution](#-research-contribution)

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

## 🚀 Retrieval Quality Improvements

These improvements were added to increase retrieval precision and faithfulness when scaling the document corpus to thousands of educational documents while keeping token usage low.

### 1 — Query Rewriting

Before hitting the vector store, short or vague queries are expanded into more descriptive search strings using a lightweight prompt-based rewrite step. This helps BGE embeddings find the right chunks even when the original query is ambiguous.

| Original query | Rewritten query |
|---|---|
| `"cycle"` | `"Explain the water cycle including evaporation, condensation, and precipitation"` |
| `"sin cos"` | `"Explain sine, cosine and tangent in trigonometry right-angle triangles"` |
| `"dna"` | `"Describe the structure and role of DNA in genetics and heredity"` |

The rewrite is applied by `ContextualQueryBuilder` before the query reaches the retriever.  The original query is always preserved for logging and fallback.

### 2 — Post-Retrieval Reranking

After vector retrieval collects the top-20 candidates, a lightweight **token-overlap reranker** scores each candidate against the (rewritten) query.  A topic-match bonus is added for documents whose metadata `topic` field matches the resolved topic, then only the best 3–5 chunks are forwarded to the Phi-3 model.

```
Vector search (top-20 candidates)
       │
       ▼
Reranker — score = token_overlap(query, doc) + topic_bonus (0.3 if topic matches)
       │
       ▼
Top-5 highest-scoring chunks → Phi-3 prompt
```

Key constants (tunable in `retriever.py`):

```python
TOPIC_MATCH_BONUS        = 0.3   # Extra score for topic-matching docs
CANDIDATE_POOL_MULTIPLIER = 4    # 4× pool before reranking
```

### 3 — Improved Chunking Strategy

Documents are split with `RecursiveCharacterTextSplitter` before embedding so that each chunk covers one focused concept.

```python
chunk_size    = 400   # tokens — balances context completeness and precision
chunk_overlap = 50    # tokens — prevents concepts from being cut at chunk edges
```

These values ensure that long documents (e.g. multi-section biology articles) don't dilute retrieval relevance while still preserving sentence continuity across chunk boundaries.

### 4 — Pipeline Logging for Research Evaluation

Every query emits a structured log to the console (and to the Streamlit right panel as tagged entries) so retrieval quality can be monitored and tuned:

```
[Query]          original_query   : "what is sin"
[Query]          rewritten_query  : "Explain the sine function in trigonometry"
[Mode]           retrieval_mode   : RAG | LLM Fallback
[Retrieval]      similarity scores: [0.87, 0.83, 0.79, 0.71, 0.68]
[Reranker]       reranker scores  : [0.91, 0.85, 0.80, 0.73, 0.61]
[Tokens Used]    prompt + context : 412 tokens
[Pipeline Stats] top_k=5, docs retrieved=20, reranked to=5
```

These log tags are consumed by `PipelineResult.tag_log` and rendered with icons in the Streamlit right panel (`app.py`).

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

14 core documents across 4 original topics, plus **500+ extended documents** across 18 actively classified topics (and 150+ total topics across the full corpus):

**Core topics (original):**

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

**Extended topics (added via `extended_corpus_v2.py` and `extended_corpus_v3.py`):**

```
┌────────────────────────┬──────────────────────┬──────────┐
│ Topic                  │ Subject              │ Grade    │
├────────────────────────┼──────────────────────┼──────────┤
│ Trigonometry           │ Mathematics          │ 9–10     │
│ Genetics               │ Biology              │ 9–10     │
│ Machine Learning       │ Technology           │ 10–11    │
│ Electricity            │ Physics              │ 8–9      │
│ Magnetism              │ Physics              │ 7–10     │
│ Nervous System         │ Biology              │ 8–10     │
│ Evolution              │ Biology              │ 9–10     │
│ Cell Structure         │ Biology              │ 8–9      │
│ Cellular Respiration   │ Biology              │ 9–11     │
│ Nitrogen Cycle         │ Biology              │ 9        │
│ Digestion              │ Biology              │ 8–9      │
│ Immune System          │ Biology              │ 8–9      │
│ Sound Waves            │ Physics              │ 8–9      │
│ Cybersecurity          │ Technology           │ 9–10     │
│ … and 130+ more        │ Multiple             │ 4–12     │
└────────────────────────┴──────────────────────┴──────────┘
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
├── main.py                      ← CLI demo runner (6 sample queries) + ablation study (--ablation)
│
├── rag_pipeline.py              ← 10-step pipeline orchestrator + MLflow logging + multi-model support
├── test_queries.py              ← 25+ benchmark test cases + run_benchmark() function
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
├── evaluation.py                ← 6 evaluation metric implementations + optional RAGAS metrics
│
├── requirements.txt             ← Python dependencies
└── chroma_db/                   ← Persisted vector store (auto-generated)
```

---

## 📖 Module Documentation

This section documents every Python module in the project — its responsibility, key classes and functions, and how it fits into the overall pipeline.

---

### `app.py` — Streamlit Web Interface

**Purpose:** Provides the interactive browser-based UI for the entire system. Renders the chat interface, the step-by-step pipeline viewer, and the per-query evaluation metrics table.

**Layout:**
- **Left sidebar** — model selector (Phi-3, TinyLlama, LLaMA 3.2, Mistral), clear-conversation button, example queries.
- **Left column (60 %)** — conversational chat display with user and assistant turns.
- **Right column (40 %)** — pipeline step log with tagged icons, and a live evaluation metrics table.

**Key functions:**

| Function | Description |
|---|---|
| `load_vector_store()` | Cached: builds or reloads the Chroma vector store via `retriever.build_vector_store()`. Runs once per session. |
| `load_pipeline(vector_store, model_name)` | Cached: initialises `RAGPipeline` with the chosen SLM. Re-runs when the model selection changes. |
| `init_session_state()` | Sets up Streamlit session keys: `chat_history`, `memory_data`, `topic_manager_data`, `last_step_log`, `last_metrics`. |
| `render_controls()` | Draws the sidebar controls and returns the currently selected model name. |
| `render_chat(pipeline, memory, topic_manager)` | Handles user input, calls `pipeline.run()`, appends the result to chat history, and re-renders the full conversation. |
| `render_pipeline_steps(step_log)` | Formats the `PipelineResult.step_log` list with emoji icons matched by log-tag prefix (`[Query]`, `[Mode]`, etc.). |
| `render_metrics(metrics)` | Renders a colour-coded table (✓ / ⚠ / ✗) for the 6 evaluation metrics. |

**Run with:**
```bash
streamlit run app.py
```

---

### `main.py` — Command-Line Entry Point

**Purpose:** A script-based alternative to the Streamlit UI. Runs a pre-defined demonstration conversation and prints all pipeline debug output to the terminal. Also exposes an `--ablation` flag for retrieval-mode comparison experiments.

**Demo queries (6):** Water cycle explanation → ambiguous "cycle" (resolved via memory) → "How does a cycle move?" (topic shift to bicycle) → photosynthesis → Calvin cycle → bicycle gears.

**Key functions:**

| Function | Description |
|---|---|
| `run_demo()` | Executes `DEMO_QUERIES` one by one through the full pipeline, printing per-step logs and a final averaged evaluation metrics table. |
| `run_ablation()` | Runs `ABLATION_QUERIES` three times — once each in `vector_only`, `bm25_only`, and `hybrid` retrieval modes — and prints a comparative metrics summary. |

**Usage:**
```bash
python main.py              # demo conversation (default)
python main.py --ablation   # retrieval ablation study
```

---

### `rag_pipeline.py` — 10-Step Pipeline Orchestrator

**Purpose:** The central module that wires all components together. Every user query passes through exactly 10 ordered steps: receive → memory → query building → ambiguity → classification → glossary → retrieval → top-K selection → answer generation → evaluation/memory update.

**Key classes:**

| Class / Function | Description |
|---|---|
| `PipelineResult` | Dataclass returned by `RAGPipeline.run()`. Fields: `answer`, `step_log` (list of debug strings), `metrics` (dict), `latency_ms`, `mode` (`"RAG"` or `"LLM Fallback"`), `retrieved_docs`, `resolved_topic`. |
| `RAGPipeline` | Main orchestrator. Constructor: `RAGPipeline(vector_store, model_name, top_k, retrieval_mode)`. |
| `RAGPipeline.run(query, memory, topic_manager)` | Executes all 10 steps and returns a `PipelineResult`. Records wall-clock latency on all return paths. |
| `RAGPipeline.run_with_mode(query, memory, topic_manager, mode)` | Same as `run()` but forces a specific retrieval mode (`hybrid`, `vector_only`, `bm25_only`). Used by the ablation study. |

**Important constants (tunable):**

```python
RAG_SIMILARITY_THRESHOLD  = 0.6   # Below this → LLM Fallback mode
RETRIEVAL_CANDIDATES      = 20    # Candidate pool size before top-K selection
TOP_K                     = 5     # Documents passed to the LLM prompt
```

**Optional integrations:** MLflow experiment tracking (auto-detected; skipped silently if `mlflow` is not installed).

---

### `contextual_query_builder.py` — Contextual Query Builder

**Purpose:** The core NLP pre-processing module. Transforms a raw user query into a clean, unambiguous, context-enriched search string before it reaches the retriever.

**Key classes:**

| Class | Description |
|---|---|
| `QueryNormalizer` | Lowercases input, expands contractions (`don't` → `do not`), strips stray punctuation. |
| `TopicConfidenceScorer` | Scans query for weighted topic keywords. Returns a `{topic: score}` dict. A score ≥ `TOPIC_SWITCH_THRESHOLD` (default 2.0) means the query is explicitly about that topic. |
| `TopicShiftDetector` | **The core innovation.** Detects whether the current query has moved to a new topic, preventing context contamination. Uses a 5-step algorithm: keyword match against memory topic → non-ambiguous content words → cross-topic match → unknown-domain word detection → shift verdict. |
| `AmbiguityResolver` | Resolves ambiguous terms (e.g. `"cycle"`) using priority order: (1) high-confidence query keywords, (2) in-query disambiguation signals, (3) conversation memory (only if no shift detected), (4) unresolved. |
| `ContextualQueryBuilder` | Orchestrator. Calls the above in sequence and returns a `ContextualQueryResult` with `rewritten_query`, `resolved_topic`, `confidence`, and debug metadata. |

**Key constants:**

```python
TOPIC_SWITCH_THRESHOLD          = 2.0   # Min keyword score to override memory
MIN_DOMAIN_SPECIFIC_WORD_LENGTH = 5     # Words shorter than this are ignored by shift detector
TOPICS                                  # List of 18 canonical topic names
```

---

### `context_memory.py` — Conversation Memory

**Purpose:** Stores the last N conversation turns in a sliding window. Each turn records the raw user query, the resolved topic, and a short answer snippet. Provides helper methods to retrieve recent topics for ambiguity resolution.

**Key classes:**

| Class / Method | Description |
|---|---|
| `Turn` | Dataclass: `user_query`, `resolved_topic`, `answer_snippet` (first 120 chars). |
| `ConversationMemory(max_turns)` | Maintains a `deque` of up to `max_turns` (default 5) `Turn` objects. |
| `add_turn(query, topic, snippet)` | Appends a completed turn to the history. |
| `get_recent_topics(n)` | Returns the `n` most recently resolved topics (most recent first). |
| `get_last_topic()` | Convenience wrapper — returns the single most recent topic, or `None`. |
| `get_context_string()` | Returns a human-readable summary of the recent turns, used for prompt injection. |
| `to_list() / from_list()` | Serialise / deserialise to a plain list for Streamlit session state persistence. |

---

### `topic_memory_manager.py` — Topic Confidence Tracker

**Purpose:** Maintains a registry of topics that have appeared in the conversation, with a **confidence decay model**. Prevents stale topics from persisting when the user has clearly moved on.

**Key classes:**

| Class / Method | Description |
|---|---|
| `TopicRecord` | Dataclass: `topic`, `frequency` (turns with mention), `last_turn`, `confidence` ∈ [0, 1]. |
| `TopicMemoryManager` | Maintains `_registry: dict[str, TopicRecord]` and a turn counter. |
| `update(topic)` | Advances the turn counter. If `topic` is not `None`, resets its confidence to 1.0 and increments frequency. All other topics lose `DECAY_RATE` (0.25) confidence. |
| `get_active_topic()` | Returns the topic with the highest confidence above `ACTIVE_THRESHOLD` (0.30), tie-broken by frequency. Returns `None` when all topics have decayed below the threshold. |
| `to_dict() / from_dict()` | Serialise / deserialise for Streamlit session state persistence. |

---

### `retriever.py` — Retrieval Stack

**Purpose:** Builds and manages the Chroma vector store, and provides all retrieval functions used by the pipeline. Implements vector search, BM25 keyword search, score-merging hybrid search, token-overlap reranking, and hierarchical topic-routed retrieval.

**Key functions / classes:**

| Function / Class | Description |
|---|---|
| `build_vector_store(persist)` | Initialises (or reloads) the Chroma collection. On first run, calls `get_texts_and_metadatas()`, splits documents into chunks (`chunk_size=400, overlap=50`), embeds with BGE, and persists to `./chroma_db/`. |
| `BM25Index` | Wraps `rank_bm25.BM25Okapi`. Tokenises corpus at build time, filtering stop-words. `search(query, k)` returns the top-k `Document` objects by BM25 score. |
| `build_bm25_index(docs)` | Factory — constructs a `BM25Index` from a list of `Document` objects. |
| `retrieve_top_k(query, store, k, filter)` | Baseline vector-only retrieval using Chroma cosine similarity with optional metadata `filter`. |
| `rerank_documents(query, docs, topic, k)` | Scores each candidate by `token_overlap(query, doc) + TOPIC_MATCH_BONUS` (if topic metadata matches). Penalises short chunks (< 40 chars). Returns top-k. |
| `hybrid_search(query, store, bm25, k, filter)` | Collects `k × CANDIDATE_POOL_MULTIPLIER` candidates from both BM25 and vector search, normalises scores to [0, 1], merges with `combined = 0.5 × BM25 + 0.5 × vector`, then reranks to top-k. |
| `hierarchical_retrieve(query, store, bm25, topic, k)` | Stage 1: runs `hybrid_search` with a topic metadata filter. If fewer than 2 results, falls back to full-corpus hybrid search (Stage 2). |

**Key constants:**

```python
CHROMA_PERSIST_DIR        = "./chroma_db"
CHUNK_SIZE                = 400    # Characters per chunk
CHUNK_OVERLAP             = 50     # Overlap between chunks
TOPIC_MATCH_BONUS         = 0.3    # Extra reranker score for topic-matching docs
CANDIDATE_POOL_MULTIPLIER = 4      # Candidate pool = top_k × 4 before reranking
```

---

### `embeddings.py` — Embedding Model

**Purpose:** Initialises and returns the BGE (BAAI General Embedding) model wrapped for use with LangChain and Chroma. Provides a single factory function used throughout the retrieval stack.

**Key function:**

| Function | Description |
|---|---|
| `get_bge_embeddings(model_name)` | Loads `BAAI/bge-small-en-v1.5` (default) via `HuggingFaceEmbeddings`. Sets `normalize_embeddings=True` for cosine similarity. Can be switched to `bge-base` for higher accuracy at the cost of speed. Pass `device="cuda"` in `model_kwargs` to use a GPU. |

---

### `query_classifier.py` — Query Classifier

**Purpose:** Assigns a **subject** (e.g. `"biology"`, `"physics"`, `"mathematics"`) and detects the most likely **topic** (e.g. `"photosynthesis"`, `"trigonometry"`) from the query text using lightweight keyword heuristics — no model inference required.

**Key functions:**

| Function | Description |
|---|---|
| `classify_query(query)` | Returns `(subject: str, topic: str | None)`. Scans `SUBJECT_KEYWORDS` and `TOPIC_KEYWORDS` for the highest-scoring match. |
| `detect_topic_shift(query, last_topic)` | Returns `True` if the query's top-scoring topic differs from `last_topic` by more than a small margin. Used as a lightweight pre-check before `TopicShiftDetector`. |

**Subject categories covered:** geography, biology, environmental science, physics, transportation, mathematics, technology, chemistry, health science, history, arts.

---

### `glossary_mapper.py` — Glossary and Synonym Mapper

**Purpose:** Provides three data structures and one utility function used across the pipeline to enrich queries and resolve ambiguous terms.

**Key exports:**

| Export | Type | Description |
|---|---|---|
| `TOPICS` | `list[str]` | Canonical list of 18 topic names (single source of truth shared with `query_classifier.py` and `contextual_query_builder.py`). |
| `AMBIGUOUS_TERMS` | `dict[str, list[str]]` | Maps a word to the list of topics it could refer to (e.g. `"cycle"` → `["water cycle", "carbon cycle", "bicycle"]`). |
| `GLOSSARY` | `dict[str, str]` | Maps synonym/alias to canonical topic (e.g. `"hydrological cycle"` → `"water cycle"`). |
| `DISAMBIGUATION_SIGNALS` | `dict[str, str]` | Maps an in-query signal word to a definitive topic (e.g. `"pedal"` → `"bicycle"`, `"chlorophyll"` → `"photosynthesis"`). |
| `OUT_OF_SCOPE_SIGNALS` | `set[str]` | Words that indicate the query is outside the knowledge base (e.g. `"politics"`, `"sports"`). |
| `expand_query(query)` | function | Replaces glossary synonyms in the query with their canonical topic name to improve retrieval. |
| `get_ambiguous_terms(query)` | function | Returns all ambiguous words found in the query. |
| `disambiguate_with_signals(query, ambiguous_term)` | function | Checks for disambiguation signals in the query to pick the most likely topic for an ambiguous term. |

---

### `data_loader.py` — Educational Knowledge Base

**Purpose:** Defines the core educational document corpus and provides chunked texts and metadata for ingestion into the vector store.

**Key exports:**

| Export | Description |
|---|---|
| `EDUCATIONAL_DOCUMENTS` | List of 14 base documents spanning 4 topics (water cycle, carbon cycle, bicycle, photosynthesis) with `text`, `subject`, `topic`, and `grade` fields. |
| `get_texts_and_metadatas()` | Returns `(texts: list[str], metadatas: list[dict])` after merging base documents with `EXTENDED_DOCUMENTS_V2` and `EXTENDED_DOCUMENTS_V3`. Called by `retriever.build_vector_store()`. |
| `get_chunked_texts_and_metadatas(chunk_size, chunk_overlap)` | Same as above but splits long documents using `RecursiveCharacterTextSplitter` before returning. Default `chunk_size=400`, `chunk_overlap=50`. |

---

### `extended_corpus_v2.py` — Extended Corpus V2

**Purpose:** Provides `EXTENDED_DOCUMENTS_V2` — a list of 5 000+ additional educational documents covering 150+ topics across grades 4–12 in multiple subjects (science, mathematics, geography, history, technology, arts). Imported by `data_loader.py` to augment the base knowledge base.

**Topics added (selection):** human reproduction, DNA replication, protein synthesis, cellular respiration, osmosis, diffusion, ecosystems, quantum mechanics, astrophysics, organic chemistry, number theory, complex numbers, matrices, financial mathematics, cybersecurity, machine learning, and many more.

---

### `extended_corpus_v3.py` — Extended Corpus V3

**Purpose:** Provides `EXTENDED_DOCUMENTS_V3` — 300+ additional documents that add depth coverage for topics already partially represented in V1/V2, plus new topics. Imported by `data_loader.py`.

**Topics added (selection):** cell structure, mitosis/meiosis, genetics, evolution, electricity, magnetism, EM spectrum, sound waves, trigonometry, circle theorems, data handling, normal distribution, differentiation, integration, urbanisation, climate change solutions, ancient civilisations (Egypt, Greece, Rome), WWI/WWII/Cold War, neural networks, ethical AI, digital privacy, Impressionism, Cubism.

---

### `evaluation.py` — Evaluation Metrics

**Purpose:** Computes all 6 per-query evaluation metrics after every pipeline run. Also optionally wraps the RAGAS evaluation framework for LLM-judge metrics.

**Key functions:**

| Function | Description |
|---|---|
| `compute_all_metrics(query, answer, docs, topic)` | Master function. Returns a dict with all 6 metrics below. |
| `precision_at_k(docs, topic, k)` | Fraction of the top-k retrieved documents whose metadata `topic` matches the resolved topic. |
| `recall_at_k(docs, topic, k, corpus_size)` | Fraction of all relevant corpus documents that appear in the top-k results. |
| `mean_reciprocal_rank(docs, topic)` | `1 / rank` of the first relevant document in the retrieved list. |
| `faithfulness(answer, docs)` | Token-overlap between the generated answer and the concatenated retrieved context. 0.0 in LLM Fallback mode. |
| `answer_relevance(query, answer)` | Fraction of meaningful query tokens that appear in the answer. |
| `context_relevance(query, docs)` | Average query-token coverage across all retrieved documents. |
| `format_metrics_table(metrics)` | Formats a `dict` of metrics into a human-readable console table with ✓/⚠/✗ status symbols. |

**Optional RAGAS metrics** (requires `pip install ragas`): Faithfulness, Answer Relevancy, Context Precision, Context Recall — computed alongside the built-in metrics when RAGAS is available.

---

### `test_queries.py` — Benchmark Test Set

**Purpose:** Defines `TEST_SET`, a curated list of 25+ structured test cases for offline benchmarking of the pipeline. Each test case specifies the input query, expected resolved topic, and expected keywords that should appear in the answer.

**Key export:**

| Export | Description |
|---|---|
| `TEST_SET` | `list[dict]` — each entry has `query`, `expected_topic`, `expected_keywords`. Covers all major topics, including follow-up and ambiguous queries. |

**Usage:**
```bash
python test_queries.py
```
Runs each test case through the pipeline and prints pass/fail results for topic resolution and keyword coverage.

---

### `research_config.py` — Research Evaluation Configuration

**Purpose:** Centralises all configuration for the multi-model, multi-mode research evaluation. Imports from here rather than hard-coding values in `research_evaluator.py`.

**Key exports:**

| Export | Description |
|---|---|
| `MODELS_TO_EVALUATE` | `["tinyllama", "phi3", "llama3.2", "mistral"]` |
| `RETRIEVAL_MODES` | `["vector_only", "bm25_only", "hybrid"]` |
| `RESULTS_FILE` | `"research_results.txt"` — output file for evaluation results |
| `TEST_QUERIES` | Structured list of 40+ test queries with `id`, `category`, `query`, `expected_topic`, `expected_keywords`, `expected_mode`, and optional `depends_on` (for multi-turn sequences). |

---

### `research_evaluator.py` — Research Evaluation Runner

**Purpose:** Runs the full pipeline across **all combinations** of models × retrieval modes using the `TEST_QUERIES` suite from `research_config.py`. Writes per-query results and aggregate statistics to `RESULTS_FILE`.

**Key classes and functions:**

| Class / Function | Description |
|---|---|
| `QueryResult` | Dataclass: `query_id`, `model`, `mode`, `latency_ms`, `metrics`, `topic_match` (bool), `mode_match` (bool). |
| `run_evaluation(model, mode)` | Runs all `TEST_QUERIES` through `RAGPipeline` for the given `(model, mode)` pair. Handles multi-turn sequences via `depends_on` chaining. Returns a list of `QueryResult` objects. |
| `aggregate_results(results)` | Computes mean values for all 6 metrics plus `topic_accuracy`, `mode_accuracy`, and `avg_latency_ms` over a result list. |
| `write_results(all_results, filepath)` | Formats and writes per-query rows and per-`(model, mode)` aggregate tables to the results file. |

**Usage:**
```bash
python research_evaluator.py                            # all models × modes
python research_evaluator.py --model phi3               # single model, all modes
python research_evaluator.py --model phi3 --mode hybrid # single combination
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

### Option C — Ablation Study

```bash
python main.py --ablation
```

Compares vector-only, BM25-only, and hybrid retrieval on a fixed query set and prints a side-by-side average metrics comparison table.

### Option D — MLflow Experiment Dashboard (optional)

```bash
mlflow ui
```

Open **http://localhost:5000** to browse logged runs, compare metrics across queries and models, and filter by `query_topic` or `pipeline_mode` tags.

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

## 🔬 Research Overview

**SLM with RAG for Educational QA** investigates whether Small Language Models (SLMs) — models with 1–7 B parameters that run locally without a GPU cluster — can deliver high-quality, grounded answers for educational use when paired with a well-engineered Retrieval-Augmented Generation (RAG) pipeline.

**Core contribution:** Rather than relying on a large, expensive model to memorise all knowledge, this system combines a *compact local SLM* (Phi-3, TinyLlama, LLaMA 3.2, or Mistral via Ollama) with a *structured educational knowledge base* and a multi-layer retrieval stack. The model only needs to reason over retrieved evidence — it does not need to store facts.

Key research questions addressed:
1. Can an SLM running locally answer multi-turn educational questions accurately when given retrieved context?
2. Does hybrid BM25 + vector retrieval outperform either method alone in an educational domain?
3. How well does contextual memory and ambiguity resolution maintain coherent multi-turn conversations?

---

## 🏗️ System Architecture

The pipeline processes each user question in **10 ordered steps**:

1. **Receive user question** — raw text input from the student
2. **Check conversation memory** — retrieve recent topics from `ConversationMemory` and `TopicMemoryManager`; detect context drift via embedding cosine similarity
3. **Contextual Query Builder** — normalise the query, score topic confidence, detect topic shifts, and rewrite the query with resolved context
4. **Ambiguity detection** — identify multi-meaning terms (e.g. "cycle") and request clarification or resolve via conversation signals
5. **Query classification** — assign a subject (e.g. Biology) and topic (e.g. photosynthesis) using keyword heuristics
6. **Glossary mapping** — expand synonyms and domain-specific terms to enrich the retrieval query
7. **Hierarchical retrieval** — topic-route to a filtered sub-corpus, then run hybrid BM25 + BGE-vector search across up to 20 candidates
8. **Top-K document selection** — rerank candidates by token overlap + topic bonus; keep top-5
9. **SLM answer generation** — Phi-3 (or other model) generates an answer grounded in the retrieved context; falls back to LLM-only when retrieval score is low
10. **Evaluation + memory update** — compute 6 quality metrics, log to MLflow (optional), update conversation memory and topic decay tracker

---

## 📊 Evaluation Metrics

After every query, **6 metrics** are computed and displayed in the Streamlit sidebar:

| Metric | Definition |
|---|---|
| **Precision@K** | Fraction of the top-K retrieved documents whose topic matches the query topic |
| **Recall@K** | Fraction of all relevant corpus documents that appear in the top-K results |
| **MRR** | Mean Reciprocal Rank — 1 / position of the first relevant document (1.0 = first) |
| **Faithfulness** | Fraction of answer tokens that are grounded in the retrieved context |
| **Answer Relevance** | Fraction of meaningful query terms that appear in the generated answer |
| **Context Relevance** | Average fraction of query terms covered by each retrieved document |

Optional **RAGAS metrics** (requires `pip install ragas`) provide a second evaluation layer:
- RAGAS Faithfulness, RAGAS Answer Relevancy, RAGAS Context Precision, RAGAS Context Recall

---

## 🧪 Ablation Study

Run `python main.py --ablation` to compare three retrieval configurations on the same query set:

| Retrieval Mode | BM25 | Vector Search | Description |
|---|---|---|---|
| **vector-only** | ✗ | ✓ | Semantic similarity only (BGE embeddings + Chroma) |
| **BM25-only** | ✓ | ✗ | Keyword frequency matching only (alpha=0.0) |
| **hybrid** | ✓ | ✓ | Weighted merge of BM25 + vector scores (alpha=0.5) — default |

The study prints an average-metrics comparison table across all three modes, showing which retrieval strategy delivers the best Precision@K, Recall@K, MRR, Faithfulness, Answer Relevance, and Context Relevance for the educational domain.

---

## 🤖 Multi-Model Comparison

The pipeline supports swapping the local SLM. The following models are configured for evaluation via the `MODELS_TO_EVALUATE` list in `rag_pipeline.py`:

| Model | Size | Notes |
|---|---|---|
| **tinyllama** | ~1.1 B | Ultra-lightweight; fastest inference |
| **phi3** | ~3.8 B | Default model; strong reasoning for its size |
| **llama3.2** | ~3 B | Meta's compact Llama 3 variant |
| **mistral** | ~7 B | Strong instruction-following; highest quality |

Use the `run_model_comparison(queries, models)` helper in `rag_pipeline.py` to benchmark all four models on the same query list and receive averaged metric dictionaries per model.

---

## ▶️ How to Run

### Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Optional: RAGAS evaluation metrics
pip install ragas

# Optional: MLflow experiment tracking
pip install mlflow

# Install and start Ollama, then pull the model
ollama pull phi3
```

> **First run note:** `sentence-transformers` will automatically download the BGE-small model (~130 MB) from HuggingFace. The Chroma vector store is built and persisted to `./chroma_db/` on first run; subsequent runs reuse the cached store.

### Run the Streamlit Web UI

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser for the full interactive chat interface with pipeline visualisation and live evaluation metrics.

### Run the CLI Demo

```bash
python main.py
```

Runs 6 pre-set demonstration queries showing ambiguity resolution, context tracking, and topic-shift detection. Prints per-query and average evaluation metrics.

### Run the Ablation Study

```bash
python main.py --ablation
```

Compares vector-only, BM25-only, and hybrid retrieval on a fixed query set and prints a side-by-side metrics table.

### Run the Benchmark Test Set

```bash
python test_queries.py
```

Executes the 25+ structured test cases from `TEST_SET` through the pipeline and prints pass/fail results for topic resolution and expected keyword coverage.

### Run the Research Evaluator

```bash
# Evaluate all models across all retrieval modes (writes results to research_results.txt)
python research_evaluator.py

# Single model, all retrieval modes
python research_evaluator.py --model phi3

# Single model + single mode
python research_evaluator.py --model phi3 --mode hybrid
```

Runs the structured `TEST_QUERIES` suite from `research_config.py` across every configured `(model, retrieval_mode)` combination and writes per-query results plus aggregate statistics to `research_results.txt`.

### Launch MLflow Dashboard (optional)

```bash
mlflow ui
```

Open **http://localhost:5000** to browse experiment runs, compare metrics across models, and filter by tags such as `query_topic` and `pipeline_mode`.

---

## 📦 Requirements

All required packages are listed in `requirements.txt`:

```
langchain>=0.2.0           # RAG orchestration framework
langchain-community>=0.2.0 # Chroma + OllamaLLM integrations
langchain-core>=0.2.0      # Core abstractions
chromadb>=0.5.0            # Local vector store with metadata filtering
sentence-transformers>=3.0.0 # BGE embeddings
huggingface-hub>=0.23.0    # Model hub access
transformers>=4.40.0       # Tokeniser utilities
ollama>=0.2.0              # Local LLM runtime
streamlit>=1.35.0          # Web UI
rank-bm25>=0.2.2           # BM25 keyword retrieval
tiktoken>=0.7.0            # Token counting
numpy>=1.26.0              # Numerical operations
```

Optional (not in `requirements.txt`):
```
mlflow      # Experiment tracking — pip install mlflow
ragas       # LLM-based evaluation metrics — pip install ragas
```

---

## 💡 Research Contribution

This project makes the following novel contributions relative to a baseline RAG system:

| Contribution | Description |
|---|---|
| **Hybrid retrieval** | BM25 keyword search and BGE semantic vector search are merged with a weighted score, outperforming either method alone in the educational domain |
| **Contextual memory** | `ConversationMemory` + `TopicMemoryManager` track topic history with exponential decay, enabling accurate follow-up query resolution |
| **Ambiguity resolution** | A multi-signal disambiguation pipeline resolves ambiguous terms (e.g. "cycle" → water/carbon/bicycle) using conversation context, keyword signals, and glossary mappings |
| **SLM focus** | The system is designed for models with 1–7 B parameters, making it deployable on consumer hardware without cloud APIs |
| **Context drift protection** | Embedding-based context similarity detection prevents topic contamination across unrelated conversation turns |
| **Optional advanced metrics** | RAGAS integration provides LLM-judge metrics (faithfulness, answer relevancy, context precision) alongside the built-in keyword-overlap metrics |
