"""
Main FastAPI application for Resilience-X.
"""
import logging
import asyncio
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .models import AskRequest, AskResponse
from .clients.weaviate_client import WeaviateClient  
from .clients.graphrag_client import GraphRAGClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global clients
weaviate_client = None
graphrag_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global weaviate_client, graphrag_client
    
    # Startup
    logger.info("Starting Resilience-X API...")
    weaviate_client = WeaviateClient()
    graphrag_client = GraphRAGClient()
    logger.info("API startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Resilience-X API...")


app = FastAPI(
    title="Resilience-X API",
    description="AI-powered Q&A for crisis recovery scenarios",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "resilience-x-api"}


@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Answer a natural language question about crisis recovery.
    
    This endpoint orchestrates semantic search via Weaviate and 
    multi-hop reasoning via GraphRAG to provide explainable answers.
    
    Args:
        request: Contains the natural language question
        
    Returns:
        Answer with explanation bullets and sources
        
    Raises:
        HTTPException: If the request fails or services are unavailable
    """
    try:
        question = request.question.strip()
        logger.info(f"Processing question: {question[:100]}...")
        
        # Step 1: Retrieve relevant passages using Weaviate
        try:
            passages = await asyncio.wait_for(
                weaviate_client.search(question, top_k=5),
                timeout=5.0
            )
            logger.info(f"Retrieved {len(passages)} relevant passages")
        except asyncio.TimeoutError:
            logger.warning("Weaviate search timed out, using fallback")
            passages = []
        except Exception as e:
            logger.error(f"Weaviate search failed: {str(e)}")
            passages = []
        
        # Step 2: Perform multi-hop reasoning using GraphRAG
        try:
            result = await asyncio.wait_for(
                graphrag_client.reason(question, passages),
                timeout=10.0
            )
            logger.info("GraphRAG reasoning completed successfully")
        except asyncio.TimeoutError:
            logger.warning("GraphRAG reasoning timed out, using fallback")
            result = {
                "answer": "I'm experiencing delays processing your question. Please try again in a moment.",
                "explanation_bullets": ["Service temporarily unavailable - timeout occurred"],
                "sources": []
            }
        except Exception as e:
            logger.error(f"GraphRAG reasoning failed: {str(e)}")
            result = {
                "answer": "I'm having trouble accessing the reasoning service right now.",
                "explanation_bullets": ["Unable to connect to reasoning engine"],
                "sources": []
            }
        
        # Step 3: Return structured response
        response = AskResponse(
            answer=result["answer"],
            explanation_bullets=result["explanation_bullets"],
            sources=result["sources"]
        )
        
        logger.info(f"Question processed successfully: {len(response.answer)} chars answer")
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your question"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)