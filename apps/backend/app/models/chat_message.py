from pydantic import BaseModel, Field

from app.core.config import get_settings


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    k: int = Field(default_factory=lambda: get_settings().top_k, ge=1, le=20)


class SourceChunk(BaseModel):
    doc_id: str
    doc_name: str
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]


class SearchRequest(BaseModel):
    question: str = Field(min_length=1)
    k: int = Field(default_factory=lambda: get_settings().top_k, ge=1, le=20)


class SearchResponse(BaseModel):
    sources: list[SourceChunk]


class DocumentInfo(BaseModel):
    id: str
    name: str
    chunks: int
    added_at: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentInfo]
