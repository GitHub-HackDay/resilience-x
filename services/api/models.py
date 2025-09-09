"""
Pydantic models for the Resilience-X API.
"""
from pydantic import BaseModel, Field
from typing import List


class QuestionRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str = Field(..., description="The question to ask", min_length=1)


class AskResponse(BaseModel):
    """Response model for the /ask endpoint."""
    answer: str = Field(..., description="The generated answer")
    explanation_bullets: List[str] = Field(..., description="Explanation bullets showing reasoning steps")
    sources: List[str] = Field(..., description="Source documents used to generate the answer")