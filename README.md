# 🎓 EduSLM-RAG — Educational Conversational QA with Contextual Retrieval

> **Python 3.11+** | **LangChain** | **ChromaDB** | **Ollama** | **Streamlit** | **BGE Embeddings** | **BM25 Hybrid Search**

A research-grade **Retrieval-Augmented Generation (RAG)** system for educational question answering using Small Language Models (SLMs). It handles multi-turn conversations, resolves pronouns and ambiguous follow-ups, detects topic shifts, and falls back gracefully when a question is out of scope.

---

## 📌 Table of Contents

1. [What This Project Does](#-what-this-project-does)
2. [Architecture Overview](#️-architecture-overview)
3. [Corpus Statistics](#-corpus-statistics)
4. [Models](#-models)
5. [Embedding Models](#-embedding-models)
6. [RAG Improvements](#-rag-improvements)
7. [Bonus Features](#-bonus-features)
8. [Tech Stack](#️-tech-stack)
9. [Project Structure](#-project-structure)
10. [Setup & Installation](#-setup--installation)
11. [How to Run](#-how-to-run)
12. [Evaluation Commands](#-evaluation-commands)
13. [Example Conversation Flows](#-example-conversation-flows)
14. [Research Overview](#-research-overview)
15. [Requirements](#-requirements)

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

### SLMs (free — run locally via Ollama)

| Model Key | Model | Cost | Description |
|---|---|---|---|
| `tinyllama` | TinyLlama 1.1B | Free | Very fast, minimal RAM — ideal for edge testing |
| `phi3` | Microsoft Phi-3 Mini | Free | Strong reasoning for its size; **default model** |
| `llama3.2` | Meta Llama 3.2 | Free | Compact multilingual model |
| `mistral` | Mistral 7B | Free | Balanced quality / speed for local inference |

### LLMs (paid — OpenAI API)

| Model Key | Model | Input Cost / 1K tokens | Output Cost / 1K tokens | Description |
|---|---|---|---|---|
| `gpt-3.5-turbo` | OpenAI GPT-3.5 Turbo | $0.0005 | $0.0015 | Fast, cost-effective API model |
| `gpt-4o-mini` | OpenAI GPT-4o Mini | $0.00015 | $0.0006 | Strong capability at low cost |

> **Default model:** `phi3`  
> All SLMs run free via [Ollama](https://ollama.com/). LLMs require an `OPENAI_API_KEY` environment variable.

`MODELS_TO_EVALUATE` is dynamically derived — it selects all entries from `MODEL_REGISTRY` where `type == "slm"`, so adding a new model to the registry automatically includes it in evaluations.

---

## 🔢 Embedding Models

All embeddings are defined in `EMBEDDING_MODELS` in `research_config.py`. Each embedding gets its own isolated ChromaDB collection and persist directory to avoid dimension-mismatch errors.

| Key | Model ID | Dimensions | Description |
|---|---|---|---|
| `bge-small` ⭐ | `BAAI/bge-small-en-v1.5` | 384 | BGE Small — fast, **current default** |
| `bge-base` | `BAAI/bge-base-en-v1.5` | 768 | BGE Base — balanced quality/speed |
| `bge-large` | `BAAI/bge-large-en-v1.5` | 1024 | BGE Large — highest retrieval quality |
| `minilm` | `sentence-transformers/all-MiniLM-L6-v2` | 384 | MiniLM — very fast, lightweight |
| `mpnet` | `sentence-transformers/all-mpnet-base-v2` | 768 | MPNet — strong general purpose |
| `e5-small` | `intfloat/e5-small-v2` | 384 | E5 Small — instruction-tuned |
| `e5-base` | `intfloat/e5-base-v2` | 768 | E5 Base — instruction-tuned, larger |

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
- (Optional) OpenAI API key for LLM comparison experiments

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-org/SLM-with-RAG-for-Educational-QA.git
cd SLM-with-RAG-for-Educational-QA
```

### Step 2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Pull the default SLM

```bash
ollama pull phi3
```

To also use other SLMs in multi-model mode:

```bash
ollama pull tinyllama
ollama pull llama3.2
ollama pull mistral
```

### Step 4 — (Optional) Set your OpenAI API key

Only required if you want to run `gpt-3.5-turbo` or `gpt-4o-mini` in evaluation experiments:

```bash
export OPENAI_API_KEY="sk-..."
```

### Step 5 — Verify corpus stats

```bash
python -c "from data_loader import get_corpus_stats; import json; print(json.dumps(get_corpus_stats(), indent=2))"
```

---

## ▶️ How to Run

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

---

## 📈 Evaluation Commands

All experiments are run via `research_evaluator.py` with the `--mode` flag.

### Single Model Experiment

Run one model across all retrieval modes (`vector_only`, `bm25_only`, `hybrid`) with the default embedding:

```bash
python research_evaluator.py --mode single --model phi3
```

With a different embedding:

```bash
python research_evaluator.py --mode single --model phi3 --embedding bge-base
```

### Retrieval Ablation Study

Run all retrieval modes for a single model and compare:

```bash
python research_evaluator.py --mode ablation --model phi3
```

### Model Comparison

Run all SLMs in `MODEL_REGISTRY` with the same retrieval mode and embedding:

```bash
python research_evaluator.py --mode model_comparison --retrieval hybrid
```

### Embedding Comparison

Run the same model across all 7 embedding models:

```bash
python research_evaluator.py --mode embedding_comparison --model phi3
```

### Full Matrix

Run every SLM × every retrieval mode combination:

```bash
python research_evaluator.py --mode full_matrix
```

### Token Comparison

Analyse token usage and cost across models:

```bash
python research_evaluator.py --mode token_comparison
```

### SLM vs. LLM Comparison

Compare local SLMs against OpenAI API models (requires `OPENAI_API_KEY`):

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
python research_evaluator.py --mode single --model mistral --output my_results.txt
```

All results are written to `research_results.txt` (or the specified output path) in a structured plain-text format.

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

# Embeddings (BGE via HuggingFace)
sentence-transformers>=3.0.0
huggingface-hub>=0.23.0
transformers>=4.40.0

# Local LLM (Ollama integration)
ollama>=0.2.0

# Streamlit UI
streamlit>=1.35.0

# Hybrid search — BM25 keyword retrieval
rank-bm25>=0.2.2

# Token counting (Phi-3 compatible tokenizer approximation)
tiktoken>=0.7.0

# Utilities
numpy>=1.26.0
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

*EduSLM-RAG is a research prototype. Corpus coverage, model behaviour, and evaluation results will vary by Ollama version and hardware.*
