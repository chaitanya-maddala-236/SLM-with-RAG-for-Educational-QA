# 1. Title

Candidate titles:
1. **EduSLM-RAG: Contextual Hybrid Retrieval for Educational Conversational Question Answering**
2. **Grounded Classroom AI with Small Language Models: A Hybrid BM25–Dense RAG Framework**
3. **From Follow-up Ambiguity to Reliable Answers: EduSLM-RAG for Multi-Turn Educational QA**

**Final title:** **EduSLM-RAG: Contextual Hybrid Retrieval for Educational Conversational Question Answering**

---

# 2. Abstract (250–350 words)

Educational conversational QA systems built on small language models (SLMs) face two persistent limitations: weak factual grounding and poor handling of follow-up ambiguity. EduSLM-RAG addresses both by combining context-aware query rewriting with retrieval-augmented generation (RAG) and robust fallback logic. The system implements a production-style pipeline in which each user turn is normalized, context-resolved, topic-classified, glossary-expanded, and routed through configurable retrieval modes (`vector_only`, `bm25_only`, `hybrid`) before reranking and grounded response generation. The repository contains a broad educational corpus (2,802 documents, 335 topics, 20 subjects, 8 grade levels), and an evaluation harness (`research_evaluator.py`) supporting single-run, ablation, model-comparison, embedding-comparison, full-matrix, token-cost, and SLM-vs-LLM studies.

Methodologically, the retrieval stack fuses sparse BM25 and dense vector scores using weighted interpolation, followed by MMR or cross-encoder reranking. Conversational robustness is improved through topic-shift detection, ambiguity resolution, and memory-aware query rewriting, reducing retrieval drift in pronoun-heavy interactions. The framework is model-agnostic and supports local SLMs, open-source LLMs, and API-hosted models across multiple embedding backends.

In this checkout, the expected quantitative result artifacts (e.g., `results/model_comparison_results.txt`, `results/full_matrix_results.txt`) are not present; therefore, this manuscript reports the complete experimental protocol, equations, analysis framework, and graph specifications, while marking result-table numeric cells as pending artifact ingestion. The design still enables rigorous analysis once files are generated via `research_evaluator.py` and visualized through `evaluation_graphs/generate_evaluation_graphs.py`.

Core contributions are: (i) a reproducible conversational educational RAG architecture, (ii) hybrid retrieval with explicit controllable fusion and reranking, (iii) integrated evaluation of quality, faithfulness, latency, and cost, and (iv) a deployment-oriented discussion of SLM/LLM trade-offs for classroom assistants.

---

# 3. Keywords

Educational QA; Conversational RAG; Hybrid Retrieval; Query Rewriting; Small Language Models; BM25; Dense Embeddings; Hallucination Mitigation; Retrieval Evaluation; Classroom AI

---

# 4. Introduction

## 4.1 Educational QA challenges with SLMs

SLMs are attractive for educational deployment due to local inference, privacy, and low operating cost, but they often hallucinate on specialized curricular content and struggle with context continuity across turns. In classroom-like settings, students rarely ask fully specified one-shot questions; instead, they issue short references (“what about that?”), making standalone SLM generation unreliable.

## 4.2 Why retrieval grounding and context resolution are needed

Grounding generation in retrieved instructional content improves factual fidelity. However, retrieval quality depends on query quality. In conversational settings, unresolved pronouns and topic shifts degrade retrieval relevance. Thus, retrieval grounding and context resolution are complementary: one anchors factuality, the other ensures the retriever is asked the right question.

## 4.3 Gaps in prior educational RAG systems

Many educational QA systems focus on either retrieval engineering or conversation handling, but not both in a unified, reproducible evaluation framework. Existing work often under-reports latency/cost trade-offs and omits fallback behavior under low-confidence retrieval.

## 4.4 Research objectives and hypotheses

Objectives:
- Build a conversational educational RAG system with explicit control over retrieval mode and model class.
- Evaluate quality, grounding, latency, and cost under standardized protocols.
- Quantify SLM vs LLM operating trade-offs in the same pipeline.

Hypotheses:
- H1: Hybrid retrieval outperforms single-mode retrieval on topic accuracy and faithfulness.
- H2: Contextual query rewriting improves follow-up query handling and reduces ambiguity-driven errors.
- H3: SLMs provide superior cost/latency efficiency but lower absolute accuracy than larger LLMs.

## 4.5 Contributions

- Unified 10-step conversational educational RAG pipeline with explicit retrieval/generation decision logic.
- Hybrid sparse+dense retrieval with configurable score fusion and reranking.
- Contextual query builder with topic-shift detection and ambiguity resolution.
- Reproducible evaluation CLI supporting ablation, comparison, matrix, token, and group analyses.
- Graph-ready artifact generation for publication-style reporting.

---

# 5. Related Work

## 5.1 Retrieval-Augmented Generation

RAG couples non-parametric memory with generation to reduce hallucination and improve factuality [Lewis et al., 2020]. In educational domains, this is particularly valuable due to curriculum specificity and terminology drift across grade levels.

## 5.2 Hybrid retrieval (sparse + dense)

Sparse retrievers (e.g., BM25) excel at lexical precision; dense retrievers improve semantic recall. Hybrid fusion has repeatedly shown better robustness under vocabulary mismatch and paraphrase variance [Karpukhin et al., 2020; Gao et al., 2021].

## 5.3 Conversational query rewriting and context memory

Conversational QA literature emphasizes query reformulation and memory-aware retrieval [Vakulenko et al., 2021]. Topic-shift detection is critical to prevent context contamination across turns.

## 5.4 Educational QA systems

Educational assistants prioritize correctness, explainability, and age-appropriate scope [Holmes et al., 2019]. Grounded responses and uncertainty signaling are more important than open-ended creativity.

## 5.5 SLM vs LLM trade-offs in production

SLMs offer low-cost deployment and improved privacy, while LLMs often achieve stronger reasoning and broader factual coverage. Production decisions are constrained by latency budgets, token costs, and reliability thresholds [Bommasani et al., 2021].

**Positioning:** EduSLM-RAG is novel in combining conversational query rewriting, hybrid retrieval, explicit fallback modes, and a broad comparative evaluation framework in an educational QA setting.

---

# 6. System Overview and Architecture

## 6.1 End-to-end pipeline overview

The system is organized around `rag_pipeline.py` and integrates memory, rewriting, classification, retrieval, reranking, generation, and metric logging in a 10-step process.

## 6.2 Contextual query builder for follow-up questions

`contextual_query_builder.py` performs normalization, context reconstruction, and rewrite generation to convert ambiguous follow-ups into retrieval-ready standalone queries.

## 6.3 Topic shift detection and ambiguity handling

Topic confidence and shift heuristics are used to distinguish continuation from shift, reducing false carry-over of prior context and improving retrieval targeting.

## 6.4 Retrieval subsystem (BM25, dense retrieval, hybrid fusion)

`retriever.py` implements:
- BM25 retrieval (`bm25_only`),
- dense Chroma retrieval (`vector_only`),
- score-level fusion (`hybrid`).

## 6.5 Reranking strategy

Candidates are reranked with MMR-style diversification and optional cross-encoder reranking; a topic-match bonus is applied where relevant.

## 6.6 Generation and fallback modes

Pipeline modes include `RAG`, `Partial RAG`, and `LLM Fallback`, selected based on retrieval confidence and availability of useful context.

## 6.7 Logging and observability signals

Tagged logs include query transformations, selected mode, token usage, latency, and pipeline summary stats, enabling both debugging and research traceability.

**Architecture figure description:** Figure A should depict UI input flowing into memory+rewrite modules, then retrieval/reranking, then generation and evaluation output; arrows should label data objects (query, rewritten query, candidates, final answer, metrics).

**Retrieval flow figure description:** Figure B should show parallel BM25 and dense branches merged by weighted fusion, followed by reranking and top-\(k\) selection.

---

# 7. Methodology (with equations)

## 7.1 BM25 scoring

For query \(q\) and document \(d\):
\[
S_{\mathrm{BM25}}(q,d)=\sum_{t\in q} \mathrm{IDF}(t) \cdot \frac{f(t,d)(k_1+1)}{f(t,d)+k_1\left(1-b+b\frac{|d|}{\overline{|d|}}\right)}
\]
with
\[
\mathrm{IDF}(t)=\log\!\left(\frac{N-n(t)+0.5}{n(t)+0.5}\right)
\]
where \(N\) is corpus size, \(n(t)\) is the number of documents containing term \(t\), \(f(t,d)\) is term frequency, \(|d|\) document length, \(\overline{|d|}\) average document length, and \(k_1,b\) are BM25 hyperparameters.

## 7.2 Dense retrieval scoring

Given query embedding \(\mathbf{e}_q\) and document embedding \(\mathbf{e}_d\):
\[
S_{\mathrm{dense}}(q,d)=\cos(\mathbf{e}_q,\mathbf{e}_d)=\frac{\mathbf{e}_q\cdot\mathbf{e}_d}{\|\mathbf{e}_q\|\|\mathbf{e}_d\|}
\]

## 7.3 Hybrid score fusion

\[
S_{\mathrm{hybrid}}(q,d)=\alpha\,S_{\mathrm{dense}}(q,d)+(1-\alpha)\,S_{\mathrm{BM25}}(q,d)
\]
where \(\alpha\in[0,1]\) controls semantic vs lexical weight. Sensitivity analysis should sweep \(\alpha\) and track quality/latency changes.

## 7.4 MMR/diversity-aware reranking

\[
\mathrm{MMR}(d_i)=\lambda\,\mathrm{Rel}(q,d_i)-(1-\lambda)\max_{d_j\in S}\mathrm{Sim}(d_i,d_j)
\]
with \(S\) as already-selected set, \(\lambda\) controlling relevance-diversity trade-off.

## 7.5 Retrieval and generation decision logic

A simplified policy:
\[
\text{mode}=\begin{cases}
\mathrm{RAG}, & n_{\mathrm{ctx}}\ge k \land c\ge\tau_h\\
\mathrm{Partial\ RAG}, & 0<n_{\mathrm{ctx}}<k \land c\ge\tau_l\\
\mathrm{LLM\ Fallback}, & \text{otherwise}
\end{cases}
\]
where \(n_{\mathrm{ctx}}\) is retrieved context count and \(c\) confidence.
Conditions are mutually exclusive by construction.

## 7.6 Complexity and efficiency discussion

- Indexing: BM25 \(O(N\bar{L})\), vector indexing depends on backend but generally \(O(Nd_{emb})\) embedding + storage.
- Query-time: complexity varies by index implementation; practical inverted-index BM25 search is typically sublinear in \(N\), while dense retrieval depends on ANN/index strategy.
- Hybrid: additive retrieval cost plus reranking cost \(O(k^2)\) worst-case for MMR-like diversification.

Here, \(\bar{L}\) is average document length in tokens/terms and \(d_{emb}\) is embedding dimensionality.

---

# 8. Experimental Setup

## 8.1 Corpus and metadata schema (topic/subject/grade)

The corpus contains **2,802** educational documents with metadata fields: `topic`, `subject`, and `grade`. Distribution spans **335 topics**, **20 subjects**, and **8 grade levels**.

## 8.2 Models compared (SLMs, API LLMs, embedding variants)

`MODEL_REGISTRY` defines **20** models across local SLMs, open-source LLMs, and API providers (Groq/OpenAI/Anthropic/Google).

## 8.3 Embedding model matrix and retrieval modes

`EMBEDDING_MODELS` defines **13** embeddings; retrieval modes are `vector_only`, `bm25_only`, and `hybrid`.

## 8.4 Hardware/software environment

Reference stack: Python 3.11+, LangChain, ChromaDB, rank-bm25, sentence-transformers, Streamlit, optional provider SDKs, and optional Ollama runtime.

## 8.5 Reproducibility protocol (seeds, configs, run commands)

- Keep fixed retrieval mode and embedding for controlled comparisons.
- Use standardized test query set (`TEST_QUERIES`, 34 entries in current config).
- Run evaluator modes via CLI and persist text artifacts under `results/`.

---

# 9. Evaluation Protocol

## 9.1 Metrics and definitions (include equations)

\[
\mathrm{Precision@}k=\frac{|R_k\cap G|}{k}
\]
\[
\mathrm{Recall@}k=\frac{|R_k\cap G|}{|G|}
\]
\[
\mathrm{MRR}=\frac{1}{|Q|}\sum_{q\in Q}\frac{1}{\mathrm{rank}_q}
\]
\[
\mathrm{nDCG@}k=\frac{\mathrm{DCG@}k}{\mathrm{IDCG@}k},\quad \mathrm{DCG@}k=\sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}
\]
Hallucination rate is operationalized as:
\[
\mathrm{Hallucination\ Rate}=1-\mathrm{Faithfulness}
\]
Faithfulness is measured as answer-context grounding overlap (token-overlap proxy in the core evaluator and optional RAGAS faithfulness when available), normalized to \([0,1]\).
Latency is measured as end-to-end query wall-clock milliseconds, and cost is estimated from input/output token counts and per-model pricing.

## 9.2 Benchmark design

- Single-run evaluation (`single`)
- Retrieval ablation (`ablation`)
- Model comparison (`model_comparison`)
- Embedding comparison (`embedding_comparison`)
- Full matrix (`full_matrix`)
- Token/cost comparison (`token_comparison`)
- Group comparison (`slm_vs_llm`)

## 9.3 Fairness and validity controls

- Same query set across compared systems.
- Fixed retrieval and embedding settings per comparison axis.
- Same output parsing and metric computation functions.
- Availability checks skip missing models rather than silently failing.

---

# 10. Results

> **Artifact status in this checkout:** the expected files under `results/` are not present, so numeric values below are marked **PENDING** and should be auto-filled after running the evaluator.

## 10.1 Main quantitative results table

| Metric | Value |
|---|---|
| Topic Accuracy | PENDING (`results/research_results.txt`) |
| Avg Latency (ms) | PENDING (`results/research_results.txt`) |
| Hallucination Rate (%) | PENDING (`results/research_results.txt`) |

Interpretation: finalize after artifact ingestion; this table is the anchor for all downstream claims.

## 10.2 Ablation results interpretation

Expected comparison axis: `vector_only` vs `bm25_only` vs `hybrid` from `results/ablation_results.txt`. Primary interpretation should test whether hybrid improves both relevance and faithfulness without unacceptable latency inflation.

## 10.3 Model comparison insights

From `results/model_comparison_results.txt`, identify best model by topic accuracy, and characterize quality-latency-cost trade-offs across model classes.

## 10.4 Embedding comparison insights

From `results/embedding_comparison_results.txt`, compare retrieval quality vs embedding dimensionality/runtime effects; report dominant embedding for balanced deployment.

## 10.5 Full matrix insights

From `results/full_matrix_results.txt`, analyze interaction effects between model family and embedding choice; identify robust pairings.

## 10.6 Token-cost vs quality trade-off

From `results/token_comparison_results.txt`, map marginal quality gains against token and dollar costs to identify Pareto-efficient choices.

## 10.7 SLM vs LLM findings

From `results/slm_vs_llm_results.txt`, quantify where SLMs are sufficient and where LLM uplift justifies additional cost.

---

# 11. Graphs and Visual Analysis (required)

## G1: Accuracy comparison by model (bar chart)
- **Data source:** `results/model_comparison_results.txt`
- **X-axis:** Model name
- **Y-axis:** Topic accuracy (%)
- **Caption:** Compares per-model task performance under fixed retrieval/embedding settings. Highlights absolute quality spread and identifies top-performing models. Useful for selecting default model by pedagogical reliability.
- **Takeaway:** Choose highest-accuracy model subject to latency/cost constraints.

## G2: Latency comparison by model (bar chart)
- **Data source:** `results/model_comparison_results.txt`
- **X-axis:** Model name
- **Y-axis:** Average latency (ms/query)
- **Caption:** Quantifies responsiveness differences among models under identical benchmark conditions. Supports SLA-aware model selection for live classroom use.
- **Takeaway:** Fastest models are not always most accurate; deploy according to response-time budget.

## G3: Hallucination rate by retrieval mode (bar chart)
- **Data source:** `results/ablation_results.txt`
- **X-axis:** Retrieval mode (`vector_only`, `bm25_only`, `hybrid`)
- **Y-axis:** Hallucination rate (%)
- **Caption:** Measures grounding failure risk by retrieval strategy. Since hallucination is \(1-\)faithfulness, lower bars indicate stronger grounding.
- **Takeaway:** Prefer retrieval mode with minimum hallucination at acceptable recall.

## G4: Embedding model performance (grouped bars/radar)
- **Data source:** `results/embedding_comparison_results.txt`
- **X-axis:** Embedding model
- **Y-axis:** Accuracy (%), optional secondary axis for latency (ms)
- **Caption:** Compares retrieval representations under a fixed generator. Reveals whether larger embedding dimensions consistently improve educational QA outcomes.
- **Takeaway:** Select embedding that balances quality and compute footprint.

## G5: Cost vs accuracy scatter with Pareto frontier
- **Data source:** `results/token_comparison_results.txt` + `results/model_comparison_results.txt`
- **X-axis:** Estimated cost (USD/query)
- **Y-axis:** Topic accuracy (%)
- **Caption:** Plots economic efficiency against quality for deployment planning. Pareto frontier marks configurations where no dimension improves without degrading the other.
- **Takeaway:** Frontier points are primary candidates for production defaults.

## G6: Full matrix heatmap (model × retrieval/embedding)
- **Data source:** `results/full_matrix_results.txt`
- **X-axis:** Embedding (or retrieval mode)
- **Y-axis:** Model
- **Color:** Accuracy (%) or composite score
- **Caption:** Visualizes interaction effects across architecture choices. Highlights stable high-performing regions and brittle combinations.
- **Takeaway:** Use heatmap clusters to pick robust cross-setting configurations.

## G7: Topic-wise accuracy distribution
- **Data source:** `results/research_results.txt` (or per-topic logs)
- **X-axis:** Topic (or grouped subject)
- **Y-axis:** Accuracy (%)
- **Caption:** Shows variance in performance across curricular domains. Identifies weak-topic tails needing corpus expansion or improved retrieval routing.
- **Takeaway:** Topic-level variance is critical for equitable educational quality.

---

# 12. Discussion

## 12.1 Why hybrid retrieval helps (or not) under different conditions

Hybrid retrieval should improve robustness when user phrasing diverges from corpus wording (dense benefit) while preserving lexical precision for technical terms (BM25 benefit). Failure cases may arise when score calibration between sparse and dense components is poorly tuned.

## 12.2 Failure analysis and representative error cases

Likely failures include: (i) topic leakage across turns, (ii) weak retrieval under rare-topic coverage, (iii) overconfident generation in low-context conditions.

## 12.3 Effect of contextual rewriting on ambiguous follow-ups

Contextual rewriting is expected to improve retrieval hit quality for short and pronoun-based queries by restoring omitted entities and intent.

## 12.4 Practical implications for classroom assistants

Deployment should prioritize grounded responses, transparent uncertainty messaging, and bounded latency. Partial-RAG behavior is preferable to fabricated certainty.

## 12.5 Trade-offs: quality, latency, cost, and robustness

The production optimum is task- and budget-dependent; evaluation should prioritize Pareto-efficient points rather than a single global winner.

---

# 13. Limitations

- Dataset/topic coverage imbalance can bias topic-wise reliability.
- Automatic metrics may not fully capture pedagogical usefulness.
- Results may not transfer to non-English or non-STEM curricula.
- Real classroom interaction patterns may differ from benchmark prompts.

---

# 14. Ethical Considerations

- Hallucinations in education can propagate misconceptions.
- Topic/grade imbalance may produce uneven support quality.
- Student privacy requires strict handling of logs and session exports.
- Deploy with human oversight, uncertainty signaling, and safety filters.

---

# 15. Conclusion and Future Work

EduSLM-RAG provides a comprehensive framework for grounded educational conversational QA, combining context-aware rewriting, hybrid retrieval, reranking, and fallback-aware generation. The repository contributes a strong experimental harness for multi-axis quality/latency/cost analysis.

Future work:
- Better chunking and curriculum-aware segmentation.
- Confidence calibration for safer fallback decisions.
- Stronger multimodal retrieval-generation coupling.
- Continual index refresh and drift monitoring.
- Controlled classroom pilot studies with educator feedback.

---

# 16. Reproducibility Appendix

## 16.1 Key commands to rerun experiments

```bash
python research_evaluator.py --mode single --model mistral-7b-instruct
python research_evaluator.py --mode ablation --model groq-llama3-8b
python research_evaluator.py --mode model_comparison --retrieval hybrid
python research_evaluator.py --mode embedding_comparison --model mistral-7b-instruct
python research_evaluator.py --mode full_matrix
python research_evaluator.py --mode token_comparison
python research_evaluator.py --mode slm_vs_llm
python evaluation_graphs/generate_evaluation_graphs.py
```

## 16.2 Configuration table (models, embeddings, retrieval mode, top-k)

| Dimension | Source | Current value(s) |
|---|---|---|
| Models | `research_config.py` | 20 registered models |
| Embeddings | `research_config.py` | 13 registered embeddings |
| Retrieval modes | `research_config.py` | `vector_only`, `bm25_only`, `hybrid` |
| Default embedding | `research_config.py` | `bge-small` |
| Top-k retrieval | `retriever.py` | default `k=5` |

## 16.3 Output artifacts map (which script creates which file)

| Artifact | Producer |
|---|---|
| `results/research_results.txt` | `research_evaluator.py --mode single` |
| `results/ablation_results.txt` | `research_evaluator.py --mode ablation` |
| `results/model_comparison_results.txt` | `research_evaluator.py --mode model_comparison` |
| `results/embedding_comparison_results.txt` | `research_evaluator.py --mode embedding_comparison` |
| `results/full_matrix_results.txt` | `research_evaluator.py --mode full_matrix` |
| `results/token_comparison_results.txt` | `research_evaluator.py --mode token_comparison` |
| `results/slm_vs_llm_results.txt` | `research_evaluator.py --mode slm_vs_llm` |
| `results/graphs/*` | `evaluation_graphs/generate_evaluation_graphs.py` |

---

# 17. Equation Appendix

1. **BM25**
\[
S_{\mathrm{BM25}}(q,d)=\sum_{t\in q} \mathrm{IDF}(t) \cdot \frac{f(t,d)(k_1+1)}{f(t,d)+k_1\left(1-b+b\frac{|d|}{\overline{|d|}}\right)}
\]

2. **Cosine similarity**
\[
S_{\mathrm{dense}}(q,d)=\frac{\mathbf{e}_q\cdot\mathbf{e}_d}{\|\mathbf{e}_q\|\|\mathbf{e}_d\|}
\]

3. **Hybrid fusion**
\[
S_{\mathrm{hybrid}}(q,d)=\alpha\,S_{\mathrm{dense}}(q,d)+(1-\alpha)\,S_{\mathrm{BM25}}(q,d)
\]

4. **MMR reranking**
\[
\mathrm{MMR}(d_i)=\lambda\,\mathrm{Rel}(q,d_i)-(1-\lambda)\max_{d_j\in S}\mathrm{Sim}(d_i,d_j)
\]

5. **Precision@k**
\[
\mathrm{Precision@}k=\frac{|R_k\cap G|}{k}
\]

6. **Recall@k**
\[
\mathrm{Recall@}k=\frac{|R_k\cap G|}{|G|}
\]

7. **MRR**
\[
\mathrm{MRR}=\frac{1}{|Q|}\sum_{q\in Q}\frac{1}{\mathrm{rank}_q}
\]

8. **nDCG@k**
\[
\mathrm{nDCG@}k=\frac{\mathrm{DCG@}k}{\mathrm{IDCG@}k},\quad \mathrm{DCG@}k=\sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}
\]

9. **Hallucination relation**
\[
\mathrm{Hallucination\ Rate}=1-\mathrm{Faithfulness}
\]

**Symbol glossary:**

| Symbol | Meaning |
|---|---|
| \(q\) | Query |
| \(d\) | Document |
| \(t\) | Term |
| \(k\) | Top-\(k\) cut-off |
| \(R_k\) | Retrieved top-\(k\) set |
| \(G\) | Relevant set |
| \(\mathbf{e}_q\), \(\mathbf{e}_d\) | Query/document embeddings |
| \(S\) | Already-selected document set in MMR |
| \(\alpha\) | Hybrid fusion weight |
| \(\lambda\) | MMR relevance-diversity weight |
| \(N\) | Corpus size |
| \(n(t)\) | Document frequency of term \(t\) |
| \(f(t,d)\) | Term frequency |
| \(|d|\) | Document length |
| \(\overline{|d|}\) | Average document length (BM25 normalization) |
| \(\bar{L}\) | Average document length in tokens/terms (complexity notation) |
| \(k_1,b\) | BM25 hyperparameters |
| \(d_{emb}\) | Embedding dimension |
| \(rel_i\) | Graded relevance at rank \(i\) |
| \(n_{\mathrm{ctx}}\) | Retrieved context count |
| \(\tau_h,\tau_l\) | Confidence thresholds |
| \(c\) | Retrieval confidence |

Note: \(k\) (retrieval cut-off) and \(k_1\) (BM25 saturation parameter) are unrelated symbols. \(\overline{|d|}\) is used in BM25 normalization, while \(\bar{L}\) is used in complexity notation; both denote average length under different analytical contexts.

---

# 18. References

- [Lewis et al., 2020] Lewis, P., et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.
- [Karpukhin et al., 2020] Karpukhin, V., et al. Dense Passage Retrieval for Open-Domain Question Answering.
- [Gao et al., 2021] Gao, L., et al. Hybrid Retrieval for Robust Open-Domain QA.
- [Vakulenko et al., 2021] Vakulenko, S., et al. Question Rewriting for Conversational Question Answering.
- [Holmes et al., 2019] Holmes, W., et al. Ethics of AI in Education: Practices, Challenges, and Futures.
- [Bommasani et al., 2021] Bommasani, R., et al. On the Opportunities and Risks of Foundation Models.
- [Manning et al., 2008] Manning, C., et al. Introduction to Information Retrieval.
- [Reimers and Gurevych, 2019] Reimers, N., and Gurevych, I. Sentence-BERT.
- [Rajpurkar et al., 2016] Rajpurkar, P., et al. SQuAD: A Large-Scale Reading Comprehension Dataset.
- [Lin et al., 2021] Lin, J., et al. Pretrained Transformers for Text Ranking: BERT and Beyond.
