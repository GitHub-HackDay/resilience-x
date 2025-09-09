"""
Resilience-X FastAPI Main Application

Provides a single /ask endpoint that orchestrates Weaviate retrieval
and GraphRAG reasoning to answer crisis recovery questions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resilience-X API",
    description="Crisis recovery Q&A system with explainable multi-hop reasoning",
    version="0.1.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str


class AnswerResponse(BaseModel):
    """Response model with answer, explanation, and sources."""
    answer: str
    explanation_bullets: List[str]
    sources: List[str]


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "resilience-x-api"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """
    Answer a crisis recovery question using Weaviate + GraphRAG.
    
    Args:
        request: Question request containing the user's question
        
    Returns:
        AnswerResponse with answer, explanation bullets, and sources
    """
    try:
        logger.info(f"Received question: {request.question}")
        
        # TODO: Implement Weaviate retrieval
        # TODO: Implement GraphRAG reasoning
        # TODO: Combine results for explainable answer
        
        # Fallback static example for now
        return AnswerResponse(
            answer="Cleanup is delayed in King County and Redmond neighborhoods.",
            explanation_bullets=[
                "Crew shortages reported in multiple districts (Source: Emergency Report A)",
                "Debris overflow at main collection sites causing bottlenecks (Source: Field Report B)", 
                "Heavy rain last week slowed equipment deployment (Source: Weather Impact C)"
            ],
            sources=[
                "Emergency Operations Report A - King County Status",
                "Field Assessment Report B - Collection Site Capacity",
                "Weather Impact Assessment C - Equipment Delays"
            ]
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000))
    )