"""
Main FastAPI application for Resilience-X backend.
"""
import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import QuestionRequest, AskResponse
from .clients.weaviate_client import weaviate_client, RetrievedDocument


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    # Startup
    logger.info("Starting Resilience-X API...")
    
    # Connect to Weaviate
    if not weaviate_client.connect():
        logger.warning("Failed to connect to Weaviate - API will use fallback responses")
    else:
        # Ensure schema exists
        weaviate_client.create_schema_if_not_exists()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Resilience-X API...")
    weaviate_client.close()


# Create FastAPI app
app = FastAPI(
    title="Resilience-X API",
    description="AI-powered Q&A system for crisis recovery scenarios",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def generate_fallback_response(question: str) -> AskResponse:
    """Generate a fallback response when external services are unavailable."""
    return AskResponse(
        answer=f"I'm currently unable to access the knowledge base to answer your question about: {question}",
        explanation_bullets=[
            "The vector database (Weaviate) is currently unavailable",
            "This is a fallback response to ensure system reliability",
            "Please try again later or contact system administrator"
        ],
        sources=["System fallback - no sources available"]
    )


def format_sources_from_documents(documents: List[RetrievedDocument]) -> List[str]:
    """Format source information from retrieved documents."""
    sources = []
    for doc in documents:
        source_info = f"{doc.source} (relevance: {doc.score:.2f})"
        if len(doc.content) > 100:
            preview = doc.content[:100] + "..."
        else:
            preview = doc.content
        sources.append(f"{source_info}: {preview}")
    return sources


def generate_explanation_bullets(question: str, documents: List[RetrievedDocument]) -> List[str]:
    """Generate explanation bullets based on retrieved documents."""
    if not documents:
        return [
            "No relevant documents found in the knowledge base",
            "This may indicate the question is outside our current data scope",
            "Consider rephrasing your question or contacting support"
        ]
    
    bullets = [
        f"Found {len(documents)} relevant documents in the knowledge base",
        f"Top match: {documents[0].source} (relevance: {documents[0].score:.2f})"
    ]
    
    if len(documents) > 1:
        bullets.append(f"Additional sources include: {', '.join([doc.source for doc in documents[1:3]])}")
    
    return bullets


@app.post("/ask", response_model=AskResponse)
async def ask_question(request: QuestionRequest) -> AskResponse:
    """
    Main endpoint for asking questions about crisis recovery scenarios.
    
    This endpoint:
    1. Queries Weaviate for semantically similar documents
    2. Generates an answer based on retrieved context
    3. Provides explanation bullets showing reasoning steps
    4. Returns source documents for transparency
    
    Args:
        request: Question request containing the user's question
        
    Returns:
        Structured response with answer, explanations, and sources
        
    Raises:
        HTTPException: If the request is invalid
    """
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    logger.info(f"Processing question: {question[:100]}...")
    
    try:
        # Step 1: Retrieve relevant documents from Weaviate
        documents = weaviate_client.search_documents(question, limit=5)
        
        if not documents:
            logger.warning(f"No documents found for question: {question}")
            # For now, return a basic response - later this will integrate GraphRAG
            return AskResponse(
                answer="I couldn't find specific information to answer your question in the current knowledge base.",
                explanation_bullets=[
                    "Searched the vector database for relevant documents",
                    "No semantically similar content was found",
                    "The knowledge base may not contain information on this topic"
                ],
                sources=["No sources found"]
            )
        
        # Step 2: Generate answer based on retrieved documents
        # For now, we'll create a simple answer from the top document
        # Later this will be enhanced with GraphRAG multi-hop reasoning
        top_doc = documents[0]
        answer = f"Based on the available information: {top_doc.content[:200]}..."
        
        # Step 3: Generate explanation bullets
        explanation_bullets = generate_explanation_bullets(question, documents)
        
        # Step 4: Format sources
        sources = format_sources_from_documents(documents)
        
        response = AskResponse(
            answer=answer,
            explanation_bullets=explanation_bullets,
            sources=sources
        )
        
        logger.info(f"Successfully processed question, returning {len(sources)} sources")
        return response
        
    except Exception as e:
        logger.error(f"Error processing question '{question}': {str(e)}")
        # Return fallback response instead of raising exception
        return generate_fallback_response(question)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "weaviate_connected": weaviate_client._client is not None
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Resilience-X API",
        "description": "AI-powered Q&A system for crisis recovery scenarios",
        "endpoints": {
            "ask": "POST /ask - Ask questions about crisis recovery",
            "health": "GET /health - Health check"
        }
    }