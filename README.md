# EduRAG — Educational Conversational RAG System

A research-grade conversational Retrieval-Augmented Generation (RAG) system
for educational question answering using a Small Language Model (SLM).

---

## Architecture

```
User Question
     ↓
[Step 1]  Receive question
     ↓
[Step 2]  Conversation Memory (track recent topics)
     ↓
[Step 3]  Ambiguity Detection (Word Sense Disambiguation)
     ↓
[Step 4]  Query Classification (subject + topic detection)
     ↓
[Step 5]  Glossary / Concept Mapping
     ↓
[Step 6]  Query Rewriting (inject conversation context)
     ↓
[Step 7]  Vector Retrieval (BGE + Chroma)
     ↓
[Step 8]  Top-K Document Selection (3–5 chunks)
     ↓
[Step 9]  RAG Generation (Phi-3 via Ollama)
     ↓
[Step 10] Answer + Evaluation Metrics
```

---

## Stack

| Component | Tool |
|---|---|
| LLM (SLM) | Phi-3 via Ollama (runs locally) |
| Embeddings | BGE-small-en-v1.5 (HuggingFace) |
| Vector DB | Chroma (persisted to disk) |
| RAG framework | LangChain |
| UI | Streamlit |

---

## Setup

### 1. Install Ollama and pull the Phi-3 model

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model (≈2 GB)
ollama pull phi3

# Start the Ollama server (keep this running in a terminal)
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

Open http://localhost:8501 in your browser.

### Command-line demo

```bash
python main.py
```

Runs 6 demo queries demonstrating ambiguity resolution and conversational context.

---

## Project Structure

```
rag_project/
├── app.py               ← Streamlit UI
├── main.py              ← CLI demo
├── rag_pipeline.py      ← 10-step pipeline orchestrator
├── data_loader.py       ← Educational knowledge base (14 documents)
├── embeddings.py        ← BGE embeddings setup
├── retriever.py         ← Chroma vector store + retrieval
├── query_classifier.py  ← Subject / topic detection
├── glossary_mapper.py   ← Ambiguity detection + term expansion
├── context_memory.py    ← Conversation history tracking
├── evaluation.py        ← Precision@K, Recall@K, MRR, Faithfulness…
├── requirements.txt
└── README.md
```

---

## Knowledge Base

Topics covered (14 documents total):

| Topic | Subject | Grades |
|---|---|---|
| Water cycle | Geography, Biology | 6–7 |
| Carbon cycle | Biology, Environmental Science | 8–9 |
| Bicycle | Transportation, Physics | 5–9 |
| Photosynthesis | Biology | 7–11 |

---

## Conversational Ambiguity Demo

The system handles ambiguous terms using conversation context:

```
User: Explain water cycle
→ topic resolved: water cycle

User: What is cycle?
→ "cycle" is ambiguous (water cycle / carbon cycle / bicycle)
→ last topic was "water cycle" → resolved: water cycle ✓

User: How does a cycle move?
→ "move" signals intent shift → resolved: bicycle ✓
```

---

## Evaluation Metrics

After each query, the system computes:

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

- **Precision@K** – fraction of retrieved docs matching the query topic
- **Recall@K** – fraction of all relevant corpus docs retrieved
- **MRR** – position of first relevant document
- **Faithfulness** – how well the answer stays grounded in context
- **Answer Relevance** – how directly the answer addresses the question
- **Context Relevance** – semantic overlap of retrieved docs with query
