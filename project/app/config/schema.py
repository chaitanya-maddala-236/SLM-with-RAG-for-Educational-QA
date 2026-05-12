from __future__ import annotations

from typing import Dict
from pydantic import BaseModel, Field


class ModelProfile(BaseModel):
    model_name: str
    max_context_docs: int = Field(gt=0)
    safe_context_budget: int = Field(gt=0)


class ModelsConfig(BaseModel):
    default_slm: str
    registry: Dict[str, ModelProfile]


class GenerationConfig(BaseModel):
    temperature: float = 0.05
    max_new_tokens: int = 180
    repetition_penalty: float = 1.15
    top_p: float = 0.9


class RetrievalConfig(BaseModel):
    hyde_enabled: bool = True
    dense_top_k: int = 15
    bm25_top_k: int = 15
    fusion_pool_size: int = 30
    rrf_k: int = 60
    dense_weight: float = 0.6
    bm25_weight: float = 0.4
    mmr_lambda: float = 0.7
    high_confidence: float = 0.60
    low_confidence: float = 0.30
    chunk_size: int = 320
    chunk_overlap: int = 50


class MemoryConfig(BaseModel):
    short_term_limit: int = 8
    summary_trigger_turns: int = 12
    decay_rate: float = 0.25


class EvaluationConfig(BaseModel):
    output_dir: str = "project/experiments/outputs"
    default_k: int = 5


class AppMetaConfig(BaseModel):
    name: str = "EduSLM-RAG"
    environment: str = "development"


class Settings(BaseModel):
    app: AppMetaConfig
    models: ModelsConfig
    generation: GenerationConfig
    retrieval: RetrievalConfig
    memory: MemoryConfig
    evaluation: EvaluationConfig
