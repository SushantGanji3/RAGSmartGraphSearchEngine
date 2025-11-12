"""Pydantic models for API requests and responses."""
from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    source_link: str
    similarity_score: float
    snippet: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str
    total_results: int

class AskRequest(BaseModel):
    question: str
    top_k: int = 3

class AskResponse(BaseModel):
    answer: str
    supporting_documents: List[str]
    question: str

class StatsResponse(BaseModel):
    total_documents: int
    index_size: int
    average_latency_ms: float
    last_indexed: Optional[str]

