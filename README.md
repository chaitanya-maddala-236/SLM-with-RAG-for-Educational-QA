# EduSLM-RAG — Educational Conversational QA with Contextual Retrieval

A research-grade conversational Retrieval-Augmented Generation (RAG) system for
educational question answering using a Small Language Model (SLM).  The system
resolves ambiguous queries (e.g. *"What is cycle?"*) using conversation context,
detects topic shifts to prevent context contamination (e.g. preventing
*"nervous photosynthesis"* when asking about the nervous system after a
photosynthesis discussion), and scales to large document collections through
hybrid BM25 + vector search, reranking, and hierarchical retrieval.

---

## Problems Solved

### Problem 1 — Context Contamination

**Root cause:** Naïve memory-based disambiguation blindly applies the last
conversation topic to any ambiguous term in the current query — even when
the new query is clearly about a different subject.

**Example bug (before fix):**

```
User: Explain photosynthesis    → memory topic = photosynthesis
User: What is nervous system?
System output: "Interpreted as: nervous photosynthesis"   ← WRONG
```

**Fix — three-layer protection:**

1. **`TopicShiftDetector`** — lightweight semantic similarity using keyword
   overlap between the current query and the memory topic.  If the query has
   content words that match a *different* topic's keyword vocabulary (or an
   out-of-scope domain), a shift is flagged.

2. **`AmbiguityResolver` enhancement** — runs `TopicShiftDetector` *before*
   applying memory-based disambiguation (Priority 3).  If a shift is
   detected, the ambiguous term is left unresolved rather than being forced
   into the wrong topic.

3. **Rewrite safety rule** (`would_contaminate`) — an extra guard in the
   query rewriter that blocks substitutions which would produce semantically
   incoherent phrases (e.g. "nervous photosynthesis", "water photosynthesis").

```
User: Explain photosynthesis    → memory topic = photosynthesis
User: What is nervous system?
  → TopicShiftDetector: "nervous" not in any known topic → shift detected
  → AmbiguityResolver: skip memory, leave "system" unresolved
  → Rewriter: original query returned as-is
System output: "What is nervous system?" (no contamination)   ← CORRECT
```

### Problem 2 — Scaling When Dataset Becomes Large

The retrieval stack has been upgraded to handle thousands of documents:

| Feature | Description |
|---|---|
| **Metadata filtering** | Chroma `where` clauses on `topic`, `subject`, `grade` |
| **Hybrid Search** | BM25 keyword search + vector (BGE) search, merged by weighted score |
| **Reranking** | Retrieve top-20 candidates, score with token-overlap, return top-5 |
| **Hierarchical Retrieval** | Stage 1: topic-route to narrow corpus; Stage 2: chunk-level retrieval |
| **Document Chunking** | `chunk_size=400`, `chunk_overlap=50` via `RecursiveCharacterTextSplitter` |
| **Topic Routing** | Resolved topic used as metadata filter before vector search |

---

## Architecture

```
User Question
     ↓
[Step  1]  Receive question
     ↓
[Step  2]  Conversation Memory  ←──────────────────────────────────────┐
     ↓                                                                  │
[Step  3]  Contextual Query Builder                                     │
           ├─ QueryNormalizer        (lowercase, contractions, punct)   │
           ├─ TopicConfidenceScorer  (weighted keyword scores)          │
           ├─ TopicShiftDetector  ← NEW                                 │
           │    └─ Semantic similarity via keyword overlap              │
           │    └─ Prevents "nervous photosynthesis"-style merges       │
           ├─ AmbiguityResolver      (shift-aware; cycle/cell/system …) │
           └─ Rewrite safety rule  ← NEW  (would_contaminate guard)    │
     ↓
[Step  4]  Ambiguity Detection  (final safety check)
     ↓
[Step  5]  Query Classification (subject + topic scoring)
     ↓
[Step  6]  Glossary / Concept Mapping
     ↓
[Step  7]  Hierarchical Retrieval  ← UPGRADED
           ├─ Stage 1: Topic Routing (metadata filter on Chroma)
           ├─ Stage 2: Hybrid BM25 + Vector search
           │    ├─ BM25 keyword search  (rank_bm25)
           │    └─ Vector search  (BGE embeddings + Chroma)
           └─ Reranking  (top-20 → score → top-5)
     ↓
[Step  8]  Top-K Document Selection (reranked, 3–5 chunks)
     ↓
[Step  9]  Answer Generation (Phi-3 via Ollama)
     ↓
[Step 10]  Answer + Evaluation Metrics ─────────────────────────────────┘
```

---

## Stack

| Component      | Tool                              |
|----------------|-----------------------------------|
| LLM (SLM)      | Phi-3 via Ollama (local)          |
| Embeddings     | BGE-small-en-v1.5 (HuggingFace)  |
| Vector DB      | Chroma (persisted to disk)        |
| RAG framework  | LangChain                         |
| Keyword search | BM25 via rank-bm25                |
| UI             | Streamlit                         |

---

## Setup

### 1. Install Ollama and pull Phi-3

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model (≈2 GB)
ollama pull phi3

# Keep the server running in a terminal
ollama serve
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

> Python 3.11+ recommended.  Use a virtual environment:
> ```bash
> python -m venv .venv && source .venv/bin/activate
> ```

---

## Running

### Streamlit UI (recommended)

```bash
streamlit run app.py
```

Open <http://localhost:8501> in your browser.

### Command-line demo

```bash
python main.py
```

Runs 6 demo queries demonstrating ambiguity resolution and conversational context.

---

## Project Structure

```
├── app.py                      ← Streamlit UI
├── main.py                     ← CLI demo
│
├── rag_pipeline.py             ← 10-step pipeline orchestrator
│
├── contextual_query_builder.py ← Contextual Query Builder module
│   ├── QueryNormalizer             lowercase + contraction expansion
│   ├── TopicConfidenceScorer       weighted keyword scoring per topic
│   ├── TopicShiftDetector       ← NEW: semantic similarity-based shift detection
│   │   ├── compute_similarity()    keyword-overlap similarity [0,1]
│   │   ├── is_topic_shift()        detects domain change before memory use
│   │   └── would_contaminate()     rewrite safety guard
│   ├── AmbiguityResolver           shift-aware: cycle/cell/model/system …
│   └── ContextualQueryBuilder      orchestrates and rewrites the query
│
├── topic_memory_manager.py     ← Topic tracking with confidence decay
│
├── context_memory.py           ← Conversation history (last N turns)
├── query_classifier.py         ← Subject + topic keyword classifier
├── glossary_mapper.py          ← Synonym / concept expansion
│
├── retriever.py                ← Upgraded retrieval stack
│   ├── build_vector_store()        Chroma vector store
│   ├── BM25Index                ← NEW: BM25 keyword index (rank_bm25)
│   ├── hybrid_search()          ← NEW: BM25 + vector merged search
│   ├── rerank_documents()       ← NEW: top-20 → token-overlap score → top-5
│   ├── hierarchical_retrieve()  ← NEW: topic-route → chunk-level retrieval
│   └── retrieve_top_k()            baseline vector retrieval (backward compat)
│
├── embeddings.py               ← BGE embeddings setup
├── data_loader.py              ← Educational knowledge base (14 documents)
│   └── get_chunked_texts_and_metadatas()  ← NEW: chunk_size=400, overlap=50
│
├── evaluation.py               ← Precision@K, Recall@K, MRR, Faithfulness…
│
├── requirements.txt            ← Added rank-bm25>=0.3.1
└── README.md
```

---

## New Modules Explained

### `TopicShiftDetector` (in `contextual_query_builder.py`)

The key fix for context contamination.  Detects whether the current query is
about the same topic as the previous turn using keyword-overlap as a proxy for
semantic similarity.

#### `compute_similarity(query, topic)`
Scans the query for keywords from `TOPIC_KEYWORD_WEIGHTS[topic]` and returns
the fraction of maximum possible weight that is matched.  Returns a float in
[0, 1].

#### `is_topic_shift(query, last_topic, ambiguous_terms)`
Five-step detection algorithm:

1. If direct keyword overlap with memory topic → **no shift**.
2. Extract non-ambiguous content words (exclude ambiguous terms + stop-words).
3. If no non-ambiguous content words → **no shift** (cannot determine).
4. If content words match a **different** topic's keywords → **shift**.
5. If content words match **no** known topic and are ≥ 5 chars long → **shift** (unknown domain).

```
"What is nervous system?"  (memory: photosynthesis)
  → "nervous" not in photosynthesis keywords
  → "nervous" not in any known topic keywords (≥5 chars) → SHIFT ✓

"What is cycle?"  (memory: water cycle)
  → only "cycle" is a content word, but it is ambiguous (excluded)
  → no non-ambiguous content words → NO SHIFT, use memory ✓

"What is the Calvin cycle?"  (memory: water cycle)
  → TopicConfidenceScorer fires first: "calvin" → photosynthesis score=3.0
  → HIGH CONFIDENCE topic switch to photosynthesis ✓
```

#### `would_contaminate(query, resolved_topic, amb_term)`
Safety guard in the query rewriter.  Checks that non-ambiguous content words
in the query are semantically compatible with the resolved topic before
substituting the ambiguous term.  Blocks rewrites like:

```
"nervous system" + resolved_topic="photosynthesis"
  → "nervous" belongs to no topic (unknown domain, ≥5 chars) → BLOCK ✓
```

### Hybrid Search (`retriever.py`)

```
Query
  ↓
BM25 search  ──────────────────────┐   top-20 candidates
  ↓                                 ├─→ Merge (weighted average scores)
Vector search ─────────────────────┘   ↓
                                    Reranking (token-overlap scorer)
                                        ↓
                                    Top-5 documents
```

`alpha` parameter controls the vector/BM25 balance (default `0.5` = equal weight).

### Document Chunking (`data_loader.py`)

```python
get_chunked_texts_and_metadatas(chunk_size=400, chunk_overlap=50)
```

Uses `RecursiveCharacterTextSplitter` to split long documents.  Each chunk
retains the full metadata (`topic`, `subject`, `grade`) plus `chunk_index`
and `source_doc_index` for provenance tracking.

### Hierarchical Retrieval (`retriever.py`)

```
Stage 1 — Topic Routing:
  If topic is known → Chroma metadata filter on "topic"
  → Narrows the search space to topically relevant chunks

Stage 2 — Chunk-level Hybrid Search:
  BM25 + vector within routed topic scope
  → Reranked to top-5

Fallback: if Stage 1 returns < 2 results → full-corpus search
```

---

## Knowledge Base

14 documents across 4 topics:

| Topic           | Subject                        | Grades |
|-----------------|--------------------------------|--------|
| Water cycle     | Geography, Biology             | 6–7    |
| Carbon cycle    | Biology, Environmental Science | 8–9    |
| Bicycle         | Transportation, Physics        | 5–9    |
| Photosynthesis  | Biology                        | 7–11   |

**Metadata format per document:**
```json
{
  "text": "The water cycle describes evaporation and condensation…",
  "topic": "water_cycle",
  "subject": "geography",
  "grade": "6"
}
```

---

## Example Conversation Run

```
User: Explain photosynthesis
──────────────────────────────────────────────────────────────────────
[ Step  1] User question received: 'Explain photosynthesis'
[ Step  2] Conversation memory → last topic: 'None' | recent: []
[ Step  3] Contextual Query Builder → normalised: 'explain photosynthesis'
           topic confidence: 'photosynthesis' (score=4.0) | topic switched: False
           shift detected: False
[ Step  5] Query classification → subject: 'biology' | topic: 'photosynthesis'
[ Step  7] Hierarchical retrieval (top-20 candidates, hybrid BM25+vector)
           topic route: 'photosynthesis'
           Retrieved 5 document(s) after reranking.
[ Step  9] Sending context + question to Phi-3 via Ollama …
[Step 10] Answer generated (312 chars).

Answer: Photosynthesis is the process by which plants convert sunlight,
water, and CO₂ into glucose and oxygen…

──────────────────────────────────────────────────────────────────────
User: What is nervous system?   ← After photosynthesis
──────────────────────────────────────────────────────────────────────
[ Step  3] Contextual Query Builder
           → Ambiguous terms: ['system']
           → TopicShiftDetector: 'nervous' not in any known topic keywords
           → shift detected: True (unknown_domain_words)
           → AmbiguityResolver: memory skipped, topic unresolved
           → Rule 5 in _decide_topic: shift flag → memory cleared
           → Rewritten query: 'What is nervous system?' (no contamination)
[ Step  7] Full-corpus retrieval (no topic route)

Answer: The provided context does not contain information about the
nervous system…   ← Correct: system not in knowledge base

──────────────────────────────────────────────────────────────────────
User: What is cycle?   ← After water cycle
──────────────────────────────────────────────────────────────────────
[ Step  3] Contextual Query Builder
           → Ambiguous terms: ['cycle']
           → TopicShiftDetector: no non-ambiguous content words → no shift
           → AmbiguityResolver: resolved via memory → 'water cycle'
           → Rewritten query: 'What is the water cycle'

Answer: The water cycle is the continuous movement of water…
```

---

## Debug Step Output

The pipeline prints labelled debug lines for every step:

```
[ Step  1] User question received: 'What is cycle?'
[ Step  2] Conversation memory → last topic: 'water cycle' | recent: ['water cycle']
[ Step  3] Contextual Query Builder → normalised: 'what is cycle' |
           topic confidence: None (score=0) | topic switched: False |
           shift detected: False
[ Step  3]   → Normalised query: 'what is cycle'
[ Step  3]   → Topic confidence → no topic signal detected
[ Step  3]   → Ambiguous terms: ['cycle'] → resolved via 'memory' → 'water cycle'
[ Step  3]   → Rewritten query: 'What is the water cycle'
[ Step  4] Ambiguity detection → terms: none (already resolved)
[ Step  5] Query classification → subject: 'geography' (score=1), topic: 'water cycle' (score=2)
[ Step  6] Glossary mapping → topic from glossary: 'water cycle' | enriched query: '…'
[ Step  7] Hierarchical retrieval (top-20 candidates, hybrid BM25+vector) | topic route: 'water cycle'
[ Step  7] Retrieved 5 document(s) after reranking.
[ Step  8] Selected 5 top-K documents: …
[ Step  9] Sending context + question to Phi-3 via Ollama …
[Step 10] Answer generated (289 chars).
```

---

## Evaluation Metrics

After every query the system computes six metrics:

```
+---------------------+---------+
| Evaluation Metric   | Score   |
+---------------------+---------+
| Precision@5         | 0.800   |
| Recall@5            | 1.000   |
| MRR                 | 1.000   |
| Faithfulness        | 0.875   |
| Answer Relevance    | 0.900   |
| Context Relevance   | 0.840   |
+---------------------+---------+
```

| Metric               | Definition                                                   |
|----------------------|--------------------------------------------------------------|
| **Precision@K**      | Fraction of top-K retrieved docs matching the query topic    |
| **Recall@K**         | Fraction of all relevant corpus docs retrieved in top-K      |
| **MRR**              | 1 / rank of the first relevant document                      |
| **Faithfulness**     | Token overlap between answer and retrieved context (×2.5)    |
| **Answer Relevance** | Query-term recall in the answer                              |
| **Context Relevance**| Average query-term recall per retrieved doc                  |

Status indicators used in the Streamlit UI:
- **✓ good** — score ≥ 0.7
- **⚠ check** — score ≥ 0.5
- **✗ low** — score < 0.5

---

## Topic Confidence & Switch Logic

The system uses four layers to prevent spurious topic switches and contamination:

1. **`TopicConfidenceScorer`** — only switches topic when weighted keyword score ≥ 2.0
2. **`TopicShiftDetector`** — blocks memory-based disambiguation when the query's
   non-ambiguous content words signal a different or unknown domain
3. **`AmbiguityResolver`** — shift-aware Priority 3; unresolved result propagates
   a `shift_detected` flag through the pipeline
4. **Rewrite safety (`would_contaminate`)** — final guard in the query rewriter
   that blocks semantically incoherent substitutions

A topic switch occurs only when **one** of these conditions is met:
- Weighted keyword score ≥ `TOPIC_SWITCH_THRESHOLD` (2.0) and topic differs from memory
- An explicit in-query disambiguation signal (e.g. `move`, `pedal`, `chlorophyll`)
  matches a different topic
- Classifier score ≥ 2 on the rewritten query and topic differs from memory

Context contamination is blocked when:
- `TopicShiftDetector` identifies unknown-domain words (≥ 5 chars, not in any topic vocabulary)
- A content word matches a **different** topic's keyword list
- `would_contaminate` detects that a substitution would merge unrelated concepts

---

## Scalability Design

For datasets with thousands to millions of documents:

```
Document ingestion
    ↓
RecursiveCharacterTextSplitter (chunk_size=400, chunk_overlap=50)
    ↓
Embed chunks with BGE and store in Chroma (with topic/subject/grade metadata)
    ↓
At query time:
  Topic Routing → filter by topic metadata (reduces search space)
    ↓
  BM25 on filtered corpus + Vector search on filtered corpus
    ↓
  Merge results → Reranker (top-20 → top-5)
    ↓
  Answer Generation (Phi-3)
```

This design ensures sub-linear retrieval cost as the corpus grows, with
metadata filtering as the primary scale lever.

