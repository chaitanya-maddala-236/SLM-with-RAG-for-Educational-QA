from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Callable

from langchain_ollama import OllamaLLM

from project.app.config.loader import load_settings
from project.app.config.schema import Settings
from project.app.memory.conversation_memory import ConversationMemory
from project.app.models.schemas import (
    PipelineDiagnostics,
    PipelineResponse,
    QueryFeatures,
    RetrievedDoc,
    UserInput,
)
from project.app.prompts.templates import LLM_FALLBACK_PROMPT, PARTIAL_RAG_PROMPT, SLM_RAG_PROMPT
from project.app.rag.ambiguity import (
    classify_question_type,
    detect_ambiguity,
    detect_follow_up,
    detect_references,
)
from project.app.rag.context_packing import pack_context
from project.app.rag.fallback import FallbackLevel, select_fallback_level
from project.app.reranking.mmr import compress_context, mmr_rerank
from project.app.retrieval.hybrid import (
    ScoredDocument,
    dense_retrieve,
    reciprocal_rank_fusion,
    sparse_retrieve,
)
from project.app.retrieval.hyde import apply_hyde
from project.app.retrieval.indexing import build_chunked_corpus, build_dense_store, build_sparse_index
from project.app.retrieval.query_processing import preprocess_query

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PipelineState:
    query_features: QueryFeatures
    hyde_query: str
    fused_docs: list[ScoredDocument]
    packed_context: str
    selected_docs: list[ScoredDocument]
    confidence: float
    fallback_level: FallbackLevel


class EduSLMRAGPipeline:
    def __init__(
        self,
        model_key: str | None = None,
        embedding_name: str = "bge-small",
        settings: Settings | None = None,
        generator_fn: Callable[[str, int], str] | None = None,
    ) -> None:
        self.settings = settings or load_settings()
        self.model_key = model_key or self.settings.models.default_slm
        self.embedding_name = embedding_name
        self.memory = ConversationMemory(
            short_term_limit=self.settings.memory.short_term_limit,
            decay_rate=self.settings.memory.decay_rate,
        )

        docs = build_chunked_corpus(
            chunk_size=self.settings.retrieval.chunk_size,
            chunk_overlap=self.settings.retrieval.chunk_overlap,
        )
        self.vector_store = build_dense_store(docs, embedding_name=embedding_name)
        self.bm25_index = build_sparse_index(docs)

        self._generator_fn = generator_fn
        if self._generator_fn is None:
            model_name = self.settings.models.registry[self.model_key].model_name
            llm = OllamaLLM(
                model=model_name,
                temperature=self.settings.generation.temperature,
                top_p=self.settings.generation.top_p,
                repeat_penalty=self.settings.generation.repetition_penalty,
            )
            self._generator_fn = lambda prompt, max_tokens: llm.invoke(prompt)

    async def run(self, user_input: UserInput) -> PipelineResponse:
        state = await self._stage_1_to_7(user_input)
        answer, citations, uncertainty = await self._stage_8_and_9(user_input, state)

        self.memory.add_turn(user_input.question, answer, user_input.metadata_filters.get("topic", "general"))

        if uncertainty and "I don't know" not in answer:
            answer = f"{answer} (uncertain based on available context)"

        retrieved_docs = [
            RetrievedDoc(
                doc_id=str(i),
                content=item.doc.page_content,
                score=item.score,
                metadata=item.doc.metadata,
            )
            for i, item in enumerate(state.selected_docs, start=1)
        ]

        diagnostics = PipelineDiagnostics(
            retrieval_confidence=state.confidence,
            fallback_level=int(state.fallback_level),
            ambiguity_detected=detect_ambiguity(user_input.question),
            citations=citations,
        )

        return PipelineResponse(
            answer=answer,
            context=state.packed_context,
            retrieved_docs=retrieved_docs,
            diagnostics=diagnostics,
        )

    async def _stage_1_to_7(self, user_input: UserInput) -> PipelineState:
        normalized = preprocess_query(user_input.question)
        features = QueryFeatures(
            is_follow_up=detect_follow_up(user_input.question),
            has_reference=detect_references(user_input.question),
            question_type=classify_question_type(user_input.question),
            normalized_query=normalized,
        )

        hyde_result = apply_hyde(
            query=features.normalized_query,
            llm_generate=self._generator_fn,
            hyde_enabled=self.settings.retrieval.hyde_enabled,
        )

        dense = await asyncio.to_thread(
            dense_retrieve,
            self.vector_store,
            hyde_result.rewritten_query,
            self.settings.retrieval.dense_top_k,
            user_input.metadata_filters,
        )
        sparse = await asyncio.to_thread(
            sparse_retrieve,
            self.bm25_index,
            hyde_result.rewritten_query,
            self.settings.retrieval.bm25_top_k,
        )

        fused = reciprocal_rank_fusion(
            dense,
            sparse,
            rrf_k=self.settings.retrieval.rrf_k,
            dense_weight=self.settings.retrieval.dense_weight,
            sparse_weight=self.settings.retrieval.bm25_weight,
            pool_size=self.settings.retrieval.fusion_pool_size,
        )

        reranked = mmr_rerank(
            query=features.normalized_query,
            docs=fused,
            top_k=self.settings.models.registry[self.model_key].max_context_docs,
            lambda_mult=self.settings.retrieval.mmr_lambda,
        )
        compressed = compress_context(reranked)
        context, selected = pack_context(compressed, self.model_key, self.settings.models)

        confidence = self._confidence(selected)
        fallback_level = select_fallback_level(
            confidence,
            high=self.settings.retrieval.high_confidence,
            low=self.settings.retrieval.low_confidence,
        )

        return PipelineState(
            query_features=features,
            hyde_query=hyde_result.rewritten_query,
            fused_docs=fused,
            packed_context=context,
            selected_docs=selected,
            confidence=confidence,
            fallback_level=fallback_level,
        )

    async def _stage_8_and_9(self, user_input: UserInput, state: PipelineState) -> tuple[str, list[str], bool]:
        if state.fallback_level == FallbackLevel.full_rag:
            prompt = SLM_RAG_PROMPT.format(context=state.packed_context, question=user_input.question)
        elif state.fallback_level == FallbackLevel.partial_rag:
            prompt = PARTIAL_RAG_PROMPT.format(context=state.packed_context, question=user_input.question)
        else:
            prompt = LLM_FALLBACK_PROMPT.format(question=user_input.question)

        answer = await asyncio.to_thread(self._generator_fn, prompt, self.settings.generation.max_new_tokens)
        citations = self._extract_citations(state.selected_docs)
        uncertainty = self._detect_uncertainty(answer, state.confidence)
        return answer.strip(), citations, uncertainty

    def _confidence(self, docs: list[ScoredDocument]) -> float:
        if not docs:
            return 0.0
        scores = [max(0.0, min(1.0, d.score)) for d in docs]
        return sum(scores) / len(scores)

    def _extract_citations(self, docs: list[ScoredDocument]) -> list[str]:
        citations = []
        for doc in docs:
            source = doc.doc.metadata.get("source") or doc.doc.metadata.get("topic") or "unknown"
            citations.append(str(source))
        return sorted(set(citations))

    def _detect_uncertainty(self, answer: str, confidence: float) -> bool:
        uncertainty_markers = ["not sure", "uncertain", "might", "possibly", "i don't know"]
        lower_answer = answer.lower()
        return confidence < self.settings.retrieval.high_confidence or any(
            marker in lower_answer for marker in uncertainty_markers
        )
