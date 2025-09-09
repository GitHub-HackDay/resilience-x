"""
Response models for structured explanation bullets and source tracing.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ExplanationBullet(BaseModel):
    """
    A single explanation step with clear reasoning and source references.
    Designed for maximum clarity and traceability.
    """
    step: int = Field(..., description="Sequential step number for logical flow")
    reasoning: str = Field(..., description="Clear, concise explanation of this reasoning step")
    source_references: List[int] = Field(..., description="IDs of sources supporting this step")
    confidence: Optional[float] = Field(None, description="Confidence score 0-1 for this step")

class Source(BaseModel):
    """
    Source document with metadata for proper attribution and tracing.
    """
    id: int = Field(..., description="Unique identifier for source reference")
    title: str = Field(..., description="Human-readable title of the source")
    content: str = Field(..., description="Relevant content excerpt from source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional source metadata")
    url: Optional[str] = Field(None, description="Link to full source document")

class AskResponse(BaseModel):
    """
    Structured response with polished explanation bullets and source tracing.
    """
    answer: str = Field(..., description="Direct answer to the user's question")
    explanation_bullets: List[ExplanationBullet] = Field(..., description="Step-by-step reasoning explanation")
    sources: List[Source] = Field(..., description="All sources referenced in explanation")
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "Cleanup is delayed in King County due to crew shortages and debris overflow.",
                "explanation_bullets": [
                    {
                        "step": 1,
                        "reasoning": "Initial assessment shows King County has ongoing cleanup operations",
                        "source_references": [1, 2],
                        "confidence": 0.9
                    },
                    {
                        "step": 2,
                        "reasoning": "Crew shortage reported due to staff reassignments to other emergency zones", 
                        "source_references": [1],
                        "confidence": 0.85
                    },
                    {
                        "step": 3,
                        "reasoning": "Debris overflow at collection sites is creating additional delays",
                        "source_references": [2, 3],
                        "confidence": 0.8
                    }
                ],
                "sources": [
                    {
                        "id": 1,
                        "title": "Emergency Operations Report - Day 3",
                        "content": "King County cleanup crews have been reduced by 40% due to reassignments...",
                        "metadata": {"date": "2024-01-15", "author": "Emergency Coordination Center"},
                        "url": "/docs/emergency-ops-day3.pdf"
                    }
                ]
            }
        }