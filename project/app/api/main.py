from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from project.app.models.schemas import UserInput
from project.app.rag.pipeline import EduSLMRAGPipeline
from project.app.utils.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="EduSLM-RAG API", version="1.0.0")
pipeline = EduSLMRAGPipeline()


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    chat_history: list[dict[str, str]] = Field(default_factory=list)
    metadata_filters: dict[str, str] = Field(default_factory=dict)


class AskResponse(BaseModel):
    answer: str
    context: str
    diagnostics: dict[str, Any]
    citations: list[str]


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(payload: AskRequest) -> AskResponse:
    result = await pipeline.run(
        user_input=UserInput(
            question=payload.question,
            chat_history=payload.chat_history,
            metadata_filters=payload.metadata_filters,
        )
    )
    return AskResponse(
        answer=result.answer,
        context=result.context,
        diagnostics={
            "retrieval_confidence": result.diagnostics.retrieval_confidence,
            "fallback_level": result.diagnostics.fallback_level,
            "ambiguity_detected": result.diagnostics.ambiguity_detected,
        },
        citations=result.diagnostics.citations,
    )
