# Resilience-X API Documentation

## Overview

The Resilience-X API provides a single `/ask` endpoint that answers questions about crisis recovery scenarios using semantic search (Weaviate) and multi-hop reasoning (GraphRAG).

## Base URL

```
http://localhost:8000
```

## Endpoints

### POST /ask

Ask a question and get an answer with explanations and sources.

**Request:**
```json
{
  "question": "Which neighborhoods are facing cleanup delays?"
}
```

**Response:**
```json
{
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
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request (empty question)
- `422`: Validation error (malformed JSON)
- `500`: Server error

### GET /

Health check endpoint.

**Response:**
```json
{
  "message": "Resilience-X API is running"
}
```

### GET /health

Detailed health check.

**Response:**
```json
{
  "status": "healthy",
  "service": "resilience-x-api",
  "version": "1.0.0"
}
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Running the Server

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. The API will be available at `http://localhost:8000`

## Example Usage

### Using curl

```bash
# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which roads are blocked near Redmond?"}'

# Health check
curl http://localhost:8000/health
```

### Using Python requests

```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "Which neighborhoods are facing cleanup delays?"}
)

if response.status_code == 200:
    data = response.json()
    print(f"Answer: {data['answer']}")
    print(f"Explanations: {data['explanation_bullets']}")
    print(f"Sources: {data['sources']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Error Handling

The API includes proper error handling and timeouts:

- **Empty questions** return a 400 error
- **Upstream timeouts** (>10 seconds) return a fallback response instead of failing
- **Unexpected errors** are logged and return friendly error messages
- **CORS** is enabled for frontend integration

## Integration Notes

- The API currently uses mock data for Weaviate and GraphRAG integration
- Responses are tailored based on question keywords (cleanup, roads, etc.)
- All endpoints include proper logging for debugging
- The API is designed to be extended with real Weaviate and GraphRAG clients