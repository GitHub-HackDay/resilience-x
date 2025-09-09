"""
Resilience-X API main module
FastAPI application for crisis Q&A with GraphRAG and Weaviate
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resilience-X API",
    description="Crisis Q&A with GraphRAG and Weaviate",
    version="0.1.0",
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    """Request model for the /ask endpoint"""
    question: str

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Which neighborhoods are facing cleanup delays?"
            }
        }


class AskResponse(BaseModel):
    """Response model for the /ask endpoint"""
    answer: str
    explanation_bullets: List[str]
    sources: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Cleanup is delayed in King County.",
                "explanation_bullets": [
                    "Crew shortages identified in Report A",
                    "Debris overflow capacity reached in Report B"
                ],
                "sources": [
                    "Report A: King County Status Update",
                    "Report B: Debris Management Assessment"
                ]
            }
        }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "resilience-x-api"}


@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Main Q&A endpoint that combines Weaviate retrieval with GraphRAG reasoning
    
    Args:
        request: Question to ask about crisis recovery
        
    Returns:
        Answer with explanation bullets and sources
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Processing question: {request.question[:100]}...")
        
        # TODO: Implement Weaviate retrieval
        # passages = await weaviate_client.search(request.question)
        
        # TODO: Implement GraphRAG reasoning  
        # result = await graphrag_client.reason(request.question, passages)
        
        # Fallback response for now
        return AskResponse(
            answer="This is a placeholder response. GraphRAG and Weaviate integration pending.",
            explanation_bullets=[
                "System is processing your question",
                "Full integration with GraphRAG and Weaviate coming soon"
            ],
            sources=[
                "System placeholder response"
            ]
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process question. Please try again."
        )