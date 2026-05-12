# EduSLM-RAG Thesis Documentation

## 1) Architecture Diagram

```mermaid
flowchart TD
A[User + Chat History + Filters] --> B[Stage 1: Input Analysis]
B --> C[Stage 2: Conversation Memory]
C --> D[Stage 3: HyDE Query Rewriting]
D --> E[Stage 4: Dense + BM25 Retrieval]
E --> F[Stage 5: RRF Fusion]
F --> G[Stage 6: MMR Reranking]
G --> H[Stage 7: Context Packing]
H --> I[Stage 8: SLM Generation]
I --> J[Stage 9: Fallback Policy]
J --> K[Stage 10: Evaluation + Logging]
K --> L[Answer + Citations + Diagnostics]
```

## 2) Data Flow Diagram

```mermaid
flowchart LR
Q[Question] --> N[Normalization + Typo/Abbrev]
N --> H[HyDE Passage <=40 tokens]
H --> R[Retrieval Query]
R --> D1[Dense Chroma]
R --> D2[BM25]
D1 --> F[RRF]
D2 --> F
F --> M[MMR + Compression]
M --> P[Packed Context]
P --> G[SLM Prompted Generation]
G --> O[Grounded Answer + Citations]
```

## 3) Sequence Diagram

```mermaid
sequenceDiagram
participant U as User
participant API as FastAPI
participant PIPE as EduSLMRAGPipeline
participant RET as Hybrid Retriever
participant SLM as Small LLM
U->>API: ask(question, history, filters)
API->>PIPE: run(user_input)
PIPE->>RET: dense + BM25 retrieval
RET-->>PIPE: ranked documents
PIPE->>PIPE: RRF + MMR + packing
PIPE->>SLM: grounded prompt
SLM-->>PIPE: answer
PIPE-->>API: answer + diagnostics
API-->>U: final response
```

## 4) Evaluation Methodology

- Retrieval: Precision@K, Recall@K, MRR, NDCG@K.
- Generation: BERTScore F1, RAGAS Faithfulness, Answer Relevancy, Context Precision, Context Recall.
- System: latency, token usage, peak memory.
- All runs export JSON and CSV and maintain experiment logs.

## 5) Experimental Setup

- Models: TinyLlama 1.1B, Llama 3.2 1B, Llama 3.2 3B.
- Embedding: BAAI/bge-small-en-v1.5 (optional MiniLM comparison).
- Retrieval: BM25 + Chroma dense search, weighted RRF.
- Context packing: model-aware token budgets.
- Ablation: 2x2x2 (HyDE x Retrieval x Packing).

## 6) Research Contributions

1. SLM-optimized 10-stage RAG stack with configurable fallback policy.
2. Hybrid dense+sparse retrieval with weighted RRF and diversity reranking.
3. Memory-aware conversational design with decay and summarization.
4. End-to-end automated evaluation and ablation framework.

## 7) Limitations

- RAGAS/BERTScore are optional dependencies and may be unavailable in constrained environments.
- Latency depends on local model serving and hardware.
- Heuristic ambiguity detection can underperform on complex discourse.

## 8) Future Work

- Learned reranker fine-tuned on educational QA.
- Adaptive fallback based on calibration models.
- Teacher rubric-aware answer scoring and pedagogy alignment.
- Distributed retrieval and caching for large-scale classrooms.
