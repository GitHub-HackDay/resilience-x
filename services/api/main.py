"""
FastAPI backend for Resilience-X with polished explanation bullets and source tracing.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging
from .models.response import AskResponse, ExplanationBullet, Source
from .clients.reasoning_client import ReasoningClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Resilience-X API", version="1.0.0")

# CORS middleware for web app integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    """Request model for /ask endpoint."""
    question: str

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Answer questions with polished explanation bullets and source tracing.
    
    Returns structured answer with clear reasoning steps and linked sources.
    """
    try:
        logger.info(f"Processing question: {request.question[:100]}...")
        
        # Initialize reasoning client
        reasoning_client = ReasoningClient()
        
        # Process question with enhanced explainability
        result = await reasoning_client.process_question(request.question)
        
        logger.info(f"Generated {len(result.explanation_bullets)} explanation bullets")
        logger.info(f"Found {len(result.sources)} sources")
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        
        # Return polished fallback with structured explanation
        return AskResponse(
            answer="I'm currently experiencing technical difficulties processing your question.",
            explanation_bullets=[
                ExplanationBullet(
                    step=1,
                    reasoning="System encountered an unexpected error during processing",
                    source_references=[1]
                ),
                ExplanationBullet(
                    step=2, 
                    reasoning="Fallback response activated to maintain service availability",
                    source_references=[1]
                )
            ],
            sources=[
                Source(
                    id=1,
                    title="System Status",
                    content="Technical error occurred during question processing",
                    metadata={"type": "system", "timestamp": "now"}
                )
            ]
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "resilience-x-api"}