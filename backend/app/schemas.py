from typing import Any, Literal
from pydantic import BaseModel, Field


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    section_title: str
    text: str
    document_type: str = "product_doc"
    service: str = "platform"
    version: str = ""
    updated_at: str = ""
    environment: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    publisher: str = ""
    source_url: str = ""


class RankedChunk(BaseModel):
    chunk: Chunk
    score: float = 0
    rank: int = 0
    dense_rank: int | None = None
    bm25_rank: int | None = None
    rrf_rank: int | None = None
    reranker_score: float | None = None
    final_rank: int | None = None


class QueryEntities(BaseModel):
    services: list[str] = Field(default_factory=list)
    versions: list[str] = Field(default_factory=list)
    error_codes: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    environment: list[str] = Field(default_factory=list)


class QueryAnalysis(BaseModel):
    original_query: str
    intent: str
    rewritten_query: str
    entities: QueryEntities
    filters: dict[str, Any] = Field(default_factory=dict)
    subqueries: list[str] = Field(default_factory=list)


class Citation(BaseModel):
    document_id: str
    title: str
    section: str


class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=6000)


class QueryRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)
    debug: bool = True
    conversation_id: str | None = None
    history: list[ConversationTurn] = Field(default_factory=list, max_length=12)


class QueryResponse(BaseModel):
    response_id: str
    conversation_id: str
    answer: str
    citations: list[Citation]
    sources: list[RankedChunk]
    evidence_support: Literal["High evidence support", "Moderate evidence support", "General diagnostic guidance", "Insufficient evidence"]
    evidence_explanation: str
    citation_validity: float
    source_coverage: float
    latency_ms: float
    answer_mode: Literal["AI synthesis", "Guided fallback"] = "Guided fallback"
    retrieval_debug: dict[str, Any] | None = None


class FeedbackRequest(BaseModel):
    response_id: str = Field(min_length=8, max_length=80)
    conversation_id: str = Field(min_length=8, max_length=80)
    helpful: bool
    comment: str = Field(default="", max_length=1000)


class FeedbackResponse(BaseModel):
    status: Literal["saved"] = "saved"


class AIStatus(BaseModel):
    provider: str
    model: str
    connected: bool
    message: str


class DocumentSummary(BaseModel):
    document_id: str
    title: str
    document_type: str
    service: str
    version: str = ""
    updated_at: str = ""
    environment: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    chunk_count: int = 0
    publisher: str = ""
    source_url: str = ""


class DocumentDetail(DocumentSummary):
    content: str


class HealthResponse(BaseModel):
    status: str
    corpus_loaded: bool
    document_count: int
    chunk_count: int
    vector_backend: str
    llm_provider: str
