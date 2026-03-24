# EduSLM-RAG — Educational Conversational QA with Contextual Retrieval

A research-grade conversational Retrieval-Augmented Generation (RAG) system for
educational question answering using a Small Language Model (SLM).  The system
resolves ambiguous queries (e.g. *"What is cycle?"*) using conversation context,
and only switches topics when strong new keywords appear.

---

## Architecture

```
User Question
     ↓
[Step 1]  Receive question
     ↓
[Step 2]  Conversation Memory  ←──────────────────────────┐
     ↓                                                     │
[Step 3]  Contextual Query Builder ── NEW ──               │
          ├─ QueryNormalizer        (lowercase, contractions)
          ├─ TopicConfidenceScorer  (weighted keyword scores)
          ├─ AmbiguityResolver      (cycle / cell / model / system …)
          └─ Query Rewriter         (inject topic, make explicit)
     ↓
[Step 4]  Ambiguity Detection  (final safety check)
     ↓
[Step 5]  Query Classification (subject + topic scoring)
     ↓
[Step 6]  Glossary / Concept Mapping
     ↓
[Step 7]  Vector Retrieval  (BGE embeddings + Chroma)
     ↓
[Step 8]  Top-K Document Selection (3–5 chunks)
     ↓
[Step 9]  Answer Generation (Phi-3 via Ollama)
     ↓
[Step 10] Answer + Evaluation Metrics ──────────────────────┘
```

---

## Stack

| Component      | Tool                              |
|----------------|-----------------------------------|
| LLM (SLM)      | Phi-3 via Ollama (local)          |
| Embeddings     | BGE-small-en-v1.5 (HuggingFace)  |
| Vector DB      | Chroma (persisted to disk)        |
| RAG framework  | LangChain                         |
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
├── contextual_query_builder.py ← NEW: Contextual Query Builder module
│   ├── QueryNormalizer             lowercase + contraction expansion
│   ├── TopicConfidenceScorer       weighted keyword scoring per topic
│   ├── AmbiguityResolver           resolve cycle/cell/model/system via context
│   └── ContextualQueryBuilder      orchestrates and rewrites the query
│
├── topic_memory_manager.py     ← NEW: Topic tracking with confidence decay
│
├── context_memory.py           ← Conversation history (last N turns)
├── query_classifier.py         ← Subject + topic keyword classifier
├── glossary_mapper.py          ← Synonym / concept expansion
│
├── retriever.py                ← Chroma vector store + retrieval
├── embeddings.py               ← BGE embeddings setup
├── data_loader.py              ← Educational knowledge base (14 documents)
├── evaluation.py               ← Precision@K, Recall@K, MRR, Faithfulness…
│
├── requirements.txt
└── README.md
```

---

## New Modules Explained

### `contextual_query_builder.py`

The central upgrade.  Sits at **Step 3** of the pipeline, before ambiguity
detection and query classification.

#### `QueryNormalizer`
Cleans raw user input:
- Lowercases and strips whitespace
- Expands contractions (`what's` → `what is`, `it's` → `it is`, …)
- Removes stray punctuation while preserving hyphens inside words
- Collapses repeated whitespace

#### `TopicConfidenceScorer`
Assigns a **weighted keyword score** to each topic using `TOPIC_KEYWORD_WEIGHTS`.
Keywords directly associated with a topic (e.g. `chlorophyll` → photosynthesis)
get higher weights than generic ones (e.g. `water` → water cycle).

A score ≥ `TOPIC_SWITCH_THRESHOLD` (default **2.0**) is "high confidence" and
allows the pipeline to override memory with a new topic.

```
"explain evaporation and condensation"
  → water cycle: 3.0 + 3.0 = 6.0  → HIGH CONFIDENCE  ✓
"what is cycle?"
  → no weighted keyword fires       → LOW CONFIDENCE   (use memory)
```

#### `AmbiguityResolver`
Handles these ambiguous terms (and more):

| Term     | Possible topics                               |
|----------|-----------------------------------------------|
| `cycle`  | water cycle, carbon cycle, bicycle            |
| `cell`   | photosynthesis, carbon cycle                  |
| `model`  | any topic                                     |
| `system` | water cycle, carbon cycle, photosynthesis     |
| `it`, `this`, `that` | resolved via memory only         |

**Resolution priority:**

1. High-confidence topic from weighted keywords → use directly
2. In-query disambiguation signals
   (`move` / `ride` / `pedal` near `cycle` → bicycle)
3. Last topic from conversation memory
4. Unresolved → pipeline requests clarification

#### `ContextualQueryBuilder`
Orchestrates the three components and then **rewrites** the query:

```
"What is cycle?"  (last topic = water cycle)
    → normalise:  "what is cycle"
    → score:      no strong signal (score=0)
    → resolve:    "cycle" is ambiguous → memory → "water cycle"
    → rewrite:    "What is the water cycle"
```

```
"How does a cycle move?"  (last topic = water cycle)
    → normalise:  "how does a cycle move"
    → score:      bicycle: 1.5 (move keyword)
    → resolve:    "move" signal → bicycle  (topic switch)
    → rewrite:    "How does a bicycle move"
```

### `topic_memory_manager.py`

Tracks topic history across turns with **confidence decay**.

| Event                        | Effect on confidence       |
|------------------------------|----------------------------|
| Topic mentioned in a turn    | Reset to **1.0**           |
| Topic absent for one turn    | Subtract **0.25**          |
| Confidence falls below **0.3** | Topic is no longer "active" |

`get_active_topic()` returns the topic with the highest confidence ≥ 0.3,
tie-broken by frequency (more-discussed topic wins).

This prevents an old topic from dominating context resolution after the user
has clearly moved on.

---

## Knowledge Base

14 documents across 4 topics:

| Topic           | Subject                        | Grades |
|-----------------|--------------------------------|--------|
| Water cycle     | Geography, Biology             | 6–7    |
| Carbon cycle    | Biology, Environmental Science | 8–9    |
| Bicycle         | Transportation, Physics        | 5–9    |
| Photosynthesis  | Biology                        | 7–11   |

---

## Example Conversation Run

```
User: Explain water cycle
─────────────────────────────────────────────────────────────────────
[ Step  1] User question received: 'Explain water cycle'
[ Step  2] Conversation memory → last topic: 'None' | recent: []
[ Step  3] Contextual Query Builder → normalised: 'explain water cycle' |
           topic confidence: 'water cycle' (score=2.0) | topic switched: False
[ Step  5] Query classification → subject: 'geography' | topic: 'water cycle'
[ Step  7] Vector retrieval (top-5) on: 'explain water cycle'
[ Step  9] Sending context + question to Phi-3 via Ollama …
[Step 10] Answer generated (312 chars).

Answer: The water cycle (hydrological cycle) describes how water continuously
moves through Earth's systems via evaporation, condensation, and precipitation…

─────────────────────────────────────────────────────────────────────
User: What is cycle?
─────────────────────────────────────────────────────────────────────
[ Step  1] User question received: 'What is cycle?'
[ Step  2] Conversation memory → last topic: 'water cycle'
[ Step  3] Contextual Query Builder
           → Ambiguous terms: ['cycle'] resolved via 'memory' → 'water cycle'
           → Rewritten query: 'What is the water cycle'
[ Step  4] Ambiguity detection → terms: none (already resolved)
[ Step  9] Sending context + question to Phi-3 via Ollama …
[Step 10] Answer generated (289 chars).

Answer: The water cycle is the continuous movement of water…

─────────────────────────────────────────────────────────────────────
User: How does a cycle move?
─────────────────────────────────────────────────────────────────────
[ Step  3] Contextual Query Builder
           → 'move' signal detected → topic switch: 'water cycle' → 'bicycle'
           → Rewritten query: 'How does a bicycle move'
[ Step  9] Sending context + question to Phi-3 via Ollama …

Answer: A bicycle moves by the rider pushing pedals, which rotate a chain…
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

| Metric            | Definition                                                  |
|-------------------|-------------------------------------------------------------|
| **Precision@K**   | Fraction of top-K retrieved docs matching the query topic   |
| **Recall@K**      | Fraction of all relevant corpus docs retrieved in top-K     |
| **MRR**           | 1 / rank of the first relevant document                     |
| **Faithfulness**  | Token overlap between answer and retrieved context (×2.5 boost) |
| **Answer Relevance** | Token overlap between answer and query (×3.0 boost)      |
| **Context Relevance** | Average token overlap of retrieved docs with query (×4.0)|

The Streamlit UI shows these as metric cards and as a collapsible ASCII table.

---

## Topic Confidence & Switch Logic

The system uses three layers to prevent spurious topic switches:

1. **TopicConfidenceScorer** – only switches topic when weighted score ≥ 2.0
2. **AmbiguityResolver** – resolves ambiguous terms via signals first,
   memory second
3. **TopicMemoryManager** – confidence-decayed topic history prevents stale
   topics from mis-directing resolution after many turns

A topic switch only occurs when one of these conditions is met:
- Weighted score ≥ `TOPIC_SWITCH_THRESHOLD` (2.0) and topic differs from memory
- An explicit in-query signal (e.g. `move`, `pedal`, `chlorophyll`) matches a
  different topic
- Classifier score ≥ 2 on the rewritten query and topic differs from memory

