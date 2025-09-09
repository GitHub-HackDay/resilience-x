"""
Resilience-X FastAPI backend with fallback static example.
Provides crisis recovery Q&A with explainable answers.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resilience-X API",
    description="Crisis recovery Q&A with GraphRAG reasoning and fallback examples",
    version="0.1.0"
)

class QuestionRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str

class AnswerResponse(BaseModel):
    """Response model with answer, explanation, and sources."""
    answer: str
    explanation_bullets: List[str]
    sources: List[str]

# Static fallback example data for crisis recovery scenarios
FALLBACK_EXAMPLES = {
    "cleanup delays": {
        "answer": "Cleanup is delayed in King County due to crew shortages and debris overflow.",
        "explanation_bullets": [
            "Emergency crews are operating at 60% capacity due to staff shortages",
            "Debris collection sites are at maximum capacity, slowing removal operations",
            "Priority routes are being cleared first, causing delays in residential areas"
        ],
        "sources": [
            "King County Emergency Operations Report - Day 5",
            "Public Works Status Update - Debris Management",
            "Regional Coordination Center Briefing - Staffing Issues"
        ]
    },
    "road blocks": {
        "answer": "Several major roads near Redmond remain blocked, with SR-520 bridge partially closed.",
        "explanation_bullets": [
            "SR-520 bridge has structural damage requiring inspection before full reopening",
            "Debris from storm damaged sections of 148th Ave NE and NE 40th St",
            "Utility work is ongoing on Redmond Way, preventing full traffic restoration"
        ],
        "sources": [
            "WSDOT Bridge Inspection Report - SR-520",
            "Redmond Public Works Daily Update",
            "Puget Sound Energy Infrastructure Status"
        ]
    },
    "neighborhoods": {
        "answer": "Cleanup delays are affecting neighborhoods in King County, particularly Redmond and Bellevue areas.",
        "explanation_bullets": [
            "Residential areas in Redmond are experiencing 2-3 day delays due to debris volume",
            "Bellevue neighborhoods near damaged infrastructure have priority scheduling conflicts",
            "Limited access routes are causing bottlenecks in cleanup crew deployment"
        ],
        "sources": [
            "King County Emergency Management - Neighborhood Status",
            "City of Redmond Recovery Coordination",
            "Bellevue Emergency Services Daily Brief"
        ]
    }
}

def get_fallback_response(question: str) -> AnswerResponse:
    """
    Return a static fallback response based on question keywords.
    
    Args:
        question: The user's question string
        
    Returns:
        AnswerResponse with static example data
    """
    question_lower = question.lower()
    
    # Simple keyword matching for demo purposes
    if any(keyword in question_lower for keyword in ["cleanup", "delay", "clean up"]):
        return AnswerResponse(**FALLBACK_EXAMPLES["cleanup delays"])
    elif any(keyword in question_lower for keyword in ["road", "block", "route", "bridge"]):
        return AnswerResponse(**FALLBACK_EXAMPLES["road blocks"])
    elif any(keyword in question_lower for keyword in ["neighborhood", "area", "community"]):
        return AnswerResponse(**FALLBACK_EXAMPLES["neighborhoods"])
    else:
        # Default fallback
        return AnswerResponse(**FALLBACK_EXAMPLES["cleanup delays"])

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """
    Process a crisis recovery question and return an explainable answer.
    
    Currently returns static fallback examples. In full implementation,
    this would query Weaviate and GraphRAG services with timeout handling.
    
    Args:
        request: QuestionRequest with the user's question
        
    Returns:
        AnswerResponse with answer, explanation bullets, and sources
        
    Raises:
        HTTPException: If the question is empty or invalid
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    logger.info(f"Processing question: {request.question}")
    
    # TODO: In full implementation, this would:
    # 1. Try to query Weaviate for semantic search
    # 2. Try to run GraphRAG reasoning with timeout
    # 3. Fall back to static example if services unavailable
    
    # For now, always return fallback static example
    response = get_fallback_response(request.question)
    
    logger.info(f"Returning fallback response for question: {request.question}")
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "fallback_mode": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)