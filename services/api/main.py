"""
FastAPI main application for Resilience-X.

Provides the /ask endpoint for crisis Q&A with GraphRAG reasoning.
"""

from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging
import asyncio
from contextlib import asynccontextmanager

from .clients.graphrag_client import GraphRAGClient
from .clients.weaviate_client import WeaviateClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global clients
graphrag_client: GraphRAGClient = None
weaviate_client: WeaviateClient = None


class AskRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str = Field(..., description="The question to ask about crisis recovery")


class AskResponse(BaseModel):
    """Response model for the /ask endpoint."""
    answer: str = Field(..., description="The main answer to the question")
    explanation_bullets: List[str] = Field(
        ..., description="Bullet points explaining the reasoning"
    )
    sources: List[str] = Field(..., description="Source documents used")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup clients."""
    global graphrag_client, weaviate_client
    
    logger.info("Initializing clients...")
    try:
        # Initialize GraphRAG client
        graphrag_client = GraphRAGClient()
        await graphrag_client.initialize()
        
        # Initialize Weaviate client
        weaviate_client = WeaviateClient()
        await weaviate_client.initialize()
        
        logger.info("Clients initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize clients: {e}")
        # Continue with limited functionality
    
    yield
    
    # Cleanup
    if graphrag_client:
        await graphrag_client.close()
    if weaviate_client:
        await weaviate_client.close()


app = FastAPI(
    title="Resilience-X API",
    description="Crisis recovery Q&A system with GraphRAG reasoning",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Resilience-X API is running"}


@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """
    Answer a crisis recovery question using GraphRAG reasoning.
    
    This endpoint combines semantic search (Weaviate) with multi-hop reasoning
    (GraphRAG) to provide explainable answers to crisis recovery questions.
    """
    try:
        logger.info(f"Received question: {request.question}")
        
        # Fallback response if clients are not available
        if not graphrag_client or not weaviate_client:
            logger.warning("Clients not available, returning fallback response")
            return AskResponse(
                answer="Service temporarily unavailable. Please try again later.",
                explanation_bullets=[
                    "GraphRAG reasoning service is initializing",
                    "Vector database connection is being established"
                ],
                sources=["System Status"]
            )
        
        # Step 1: Retrieve relevant documents from Weaviate
        logger.info("Retrieving relevant documents from Weaviate...")
        try:
            relevant_passages = await asyncio.wait_for(
                weaviate_client.search_documents(request.question, limit=5),
                timeout=10.0
            )
        except asyncio.TimeoutError:
            logger.warning("Weaviate search timed out")
            relevant_passages = []
        except Exception as e:
            logger.warning(f"Weaviate search failed: {e}")
            relevant_passages = []
        
        # Step 2: Use GraphRAG for multi-hop reasoning
        logger.info("Performing GraphRAG reasoning...")
        try:
            graphrag_result = await asyncio.wait_for(
                graphrag_client.query(
                    question=request.question,
                    context_passages=relevant_passages
                ),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            logger.warning("GraphRAG query timed out")
            return _create_fallback_response(request.question, relevant_passages)
        except Exception as e:
            logger.warning(f"GraphRAG query failed: {e}")
            return _create_fallback_response(request.question, relevant_passages)
        
        # Combine results into response
        response = AskResponse(
            answer=graphrag_result.get("answer", "Unable to generate answer"),
            explanation_bullets=graphrag_result.get("explanation_bullets", [
                "Multi-hop reasoning attempted",
                "Limited context available"
            ]),
            sources=graphrag_result.get("sources", [])
        )
        
        logger.info("Successfully generated response")
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in ask_question: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your question"
        )


def _create_fallback_response(question: str, passages: List[dict]) -> AskResponse:
    """Create a fallback response when GraphRAG is unavailable."""
    # Simple keyword-based fallback
    answer = "I found some relevant information, but detailed reasoning is currently unavailable."
    
    if passages:
        # Try to extract a basic answer from passages
        first_passage = passages[0]
        answer = first_passage.get("text", "")[:200] + "..."
    
    return AskResponse(
        answer=answer,
        explanation_bullets=[
            "Semantic search completed successfully",
            "GraphRAG reasoning temporarily unavailable",
            "Basic information extracted from top-ranked documents"
        ],
        sources=[p.get("source", "Unknown") for p in passages[:3]]
    )