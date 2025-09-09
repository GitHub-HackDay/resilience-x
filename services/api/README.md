# Resilience-X API

FastAPI backend for the Resilience-X crisis Q&A system, integrating Weaviate for semantic search and document retrieval.

## Features

- **POST `/ask`** - Main endpoint for crisis recovery questions
- **Weaviate Integration** - Semantic search across crisis documents  
- **Fallback Handling** - Graceful degradation when services unavailable
- **Comprehensive Testing** - Full test coverage with mocking
- **Docker Support** - Local Weaviate setup via Docker Compose

## Quick Start

### Prerequisites

- Python 3.9+
- Docker (for Weaviate)

### Installation

```bash
# Navigate to API directory
cd services/api

# Install dependencies
pip install fastapi uvicorn weaviate-client pydantic python-multipart httpx

# Or if using uv
uv sync
```

### Running the API

1. **Start Weaviate**:
   ```bash
   # From project root
   docker compose up -d weaviate
   ```

2. **Start the API**:
   ```bash
   # From services/api directory
   uvicorn main:app --reload --port 8000
   ```

3. **Load sample data**:
   ```bash
   # From project root  
   bash scripts/ingest.sh
   ```

4. **Test the API**:
   ```bash
   # From project root
   bash scripts/demo.sh
   ```

## API Endpoints

### POST `/ask`

Ask questions about crisis recovery scenarios.

**Request:**
```json
{
  "question": "Which areas have cleanup delays?"
}
```

**Response:**
```json
{
  "answer": "Based on the available information: Road cleanup in King County is delayed due to crew shortages...",
  "explanation_bullets": [
    "Found 2 relevant documents in the knowledge base",
    "Top match: king_county_report.txt (relevance: 0.85)"
  ],
  "sources": [
    "king_county_report.txt (relevance: 0.85): Road cleanup in King County is delayed due to crew shortages..."
  ]
}
```

### GET `/health`

Health check endpoint showing system status.

### GET `/`

API information and available endpoints.

## Architecture

The API follows a layered architecture:

- **`main.py`** - FastAPI application with endpoints and middleware
- **`models.py`** - Pydantic models for request/response validation  
- **`clients/weaviate_client.py`** - Weaviate integration and document retrieval
- **`tests/`** - Comprehensive test suite

## Weaviate Integration

The `WeaviateClient` class provides:

- **Connection Management** - Automatic connection with retry logic
- **Schema Creation** - Document collection with text vectorization
- **Semantic Search** - Query documents using `near_text` 
- **Error Handling** - Graceful fallbacks and timeout protection

### Document Schema

Documents are stored with:
- `content` - Full document text
- `source` - Source filename/identifier  
- `title` - Document title

## Testing

Run the test suite:

```bash
cd services/api
python -m pytest tests/ -v
```

Test coverage includes:
- API endpoint functionality
- Weaviate client operations
- Error handling and fallbacks
- Edge cases and validation

## Configuration

The API can be configured via environment variables:

- `WEAVIATE_URL` - Weaviate instance URL (default: http://localhost:8080)
- `OPENAI_APIKEY` - OpenAI API key for text vectorization

## Next Steps

This implementation provides the foundation for:

1. **GraphRAG Integration** - Multi-hop reasoning over retrieved documents
2. **Enhanced Answers** - More sophisticated answer generation  
3. **Frontend Integration** - Connect to Next.js UI
4. **Additional Data Sources** - Expand beyond local documents

## Development

### Adding New Features

1. Update models in `models.py` for new request/response formats
2. Extend `WeaviateClient` for new search capabilities
3. Add endpoints in `main.py` following existing patterns
4. Write tests in `tests/` directory

### Error Handling Philosophy

- Always provide fallback responses rather than failing
- Log errors without exposing sensitive information  
- Use structured logging for debugging
- Timeout external calls to prevent blocking