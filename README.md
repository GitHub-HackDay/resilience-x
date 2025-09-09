# Resilience-X

An AI-powered Q&A demo that connects the dots across messy documents using multi-hop reasoning. Built with GraphRAG for explainability, Weaviate for semantic search, NLWeb for natural language queries, and GitHub Copilot to accelerate development.

## Quick Start (Fallback Mode)

The application includes fallback static examples that work without external services:

### Backend API
```bash
# Install dependencies
cd services/api
pip install fastapi uvicorn pydantic python-dotenv

# Start API server
uvicorn main:app --reload --port 8000
```

### Frontend Web App
```bash
# Install dependencies
cd apps/web
npm ci

# Start development server
npm run dev
```

### Demo Script
```bash
# Test the fallback functionality
bash scripts/demo.sh
```

## API Endpoints

- `POST /ask` - Submit a question and get an explainable answer
- `GET /health` - Health check with fallback mode status

### Example Request
```json
{
  "question": "Which neighborhoods are facing cleanup delays?"
}
```

### Example Response
```json
{
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
```

## Fallback Static Examples

The system includes three categories of static examples:
1. **Cleanup Delays** - Questions about cleanup and recovery delays
2. **Road Blocks** - Questions about blocked roads and infrastructure
3. **Neighborhoods** - Questions about affected areas and communities

These examples ensure the demo works reliably even when external services (Weaviate, GraphRAG) are unavailable.

## Technology Stack

- **Backend**: FastAPI (Python) with Pydantic models
- **Frontend**: Next.js (TypeScript) with accessibility-first design  
- **Vector DB**: Weaviate (when available)
- **Reasoning**: GraphRAG (when available)
- **Development**: GitHub Copilot assisted

## Testing

```bash
# Backend tests
cd services/api
pytest

# Frontend development
cd apps/web
npm run lint
npm run build
```
