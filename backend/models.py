from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]

class DocumentInfo(BaseModel):
    id: str
    filename: str
    pages: int
