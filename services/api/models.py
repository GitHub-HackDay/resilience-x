"""
Pydantic models for the Resilience-X API.
"""
from pydantic import BaseModel, Field
from typing import List


class AskRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str = Field(
        ...,
        description="The natural language question to ask about crisis recovery",
        min_length=1,
        max_length=500
    )


class AskResponse(BaseModel):
    """Response model for the /ask endpoint."""
    answer: str = Field(
        ...,
        description="The generated answer to the question"
    )
    explanation_bullets: List[str] = Field(
        ...,
        description="List of explanation points showing reasoning steps"
    )
    sources: List[str] = Field(
        ...,
        description="List of source references that supported the answer"
    )