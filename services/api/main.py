"""
FastAPI backend for Resilience-X Q&A system.
Provides /ask endpoint that integrates Weaviate retrieval with GraphRAG reasoning.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resilience-X API",
    description="AI-powered Q&A for crisis recovery scenarios",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "Which neighborhoods are facing cleanup delays?"
            }
        }
    }


class AnswerResponse(BaseModel):
    """Response model for the /ask endpoint with answer, explanation, and sources."""
    answer: str
    explanation_bullets: List[str]
    sources: List[str]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "answer": "Cleanup is delayed in King County and Redmond areas.",
                "explanation_bullets": [
                    "Crew shortages reported in King County (Report A)",
                    "Debris overflow affecting multiple sites (Report B)",
                    "Equipment delays due to supply chain issues (Report C)"
                ],
                "sources": [
                    "King County Emergency Report - March 15",
                    "Redmond Cleanup Status - March 16", 
                    "Regional Recovery Assessment - March 17"
                ]
            }
        }
    }


async def query_weaviate(question: str) -> List[str]:
    """
    Query Weaviate for relevant document passages.
    
    Args:
        question: The user's question
        
    Returns:
        List of relevant document passages
    """
    # TODO: Implement actual Weaviate integration
    # For now, return mock sources
    logger.info(f"Querying Weaviate for: {question}")
    
    # Simulate API delay
    await asyncio.sleep(0.1)
    
    # Mock relevant sources based on question keywords
    mock_sources = [
        "King County Emergency Report - March 15",
        "Redmond Cleanup Status - March 16",
        "Regional Recovery Assessment - March 17"
    ]
    
    return mock_sources


async def query_graphrag(question: str, context_passages: List[str]) -> tuple[str, List[str]]:
    """
    Use GraphRAG for multi-hop reasoning to generate answer and explanation.
    
    Args:
        question: The user's question
        context_passages: Relevant passages from Weaviate
        
    Returns:
        Tuple of (answer, explanation_bullets)
    """
    # TODO: Implement actual GraphRAG integration
    logger.info(f"Running GraphRAG reasoning for: {question}")
    
    # Simulate API delay
    await asyncio.sleep(0.2)
    
    # Generate mock answer based on question content
    if "cleanup" in question.lower() or "delay" in question.lower():
        answer = "Cleanup is delayed in King County and Redmond areas."
        explanations = [
            "Crew shortages reported in King County (Report A)",
            "Debris overflow affecting multiple sites (Report B)", 
            "Equipment delays due to supply chain issues (Report C)"
        ]
    elif "road" in question.lower() or "blocked" in question.lower():
        answer = "Several major roads remain blocked, with cleanup prioritized by traffic volume."
        explanations = [
            "Highway 520 blocked by fallen trees (Report A)",
            "I-405 partially closed due to debris removal (Report B)",
            "Local streets cleared first per emergency protocol (Report C)"
        ]
    else:
        answer = "Recovery efforts are ongoing across multiple affected areas."
        explanations = [
            "Emergency response teams deployed to priority zones",
            "Resource allocation based on damage assessments", 
            "Coordination with local and state agencies"
        ]
    
    return answer, explanations


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """
    Main endpoint for answering questions using Weaviate + GraphRAG.
    
    Args:
        request: Question request containing the user's question
        
    Returns:
        AnswerResponse with answer, explanation bullets, and sources
        
    Raises:
        HTTPException: If processing fails or times out
    """
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing question: {question}")
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error validating request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your question"
        )
    
    try:
        # Set timeout for upstream calls
        timeout_seconds = 10
        
        try:
            # Query Weaviate for relevant passages
            sources = await asyncio.wait_for(
                query_weaviate(question), 
                timeout=timeout_seconds
            )
            
            # Use GraphRAG for reasoning
            answer, explanation_bullets = await asyncio.wait_for(
                query_graphrag(question, sources), 
                timeout=timeout_seconds
            )
            
            response = AnswerResponse(
                answer=answer,
                explanation_bullets=explanation_bullets,
                sources=sources
            )
            
            logger.info("Successfully generated response")
            return response
            
        except asyncio.TimeoutError:
            logger.error("Upstream services timed out")
            # Return friendly fallback
            return AnswerResponse(
                answer="I'm sorry, but the system is currently experiencing delays. Please try again in a moment.",
                explanation_bullets=[
                    "The reasoning system is temporarily unavailable",
                    "This may be due to high load or maintenance"
                ],
                sources=["System Status"]
            )
            
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while processing your question"
        )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Resilience-X API is running"}


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "resilience-x-api",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)