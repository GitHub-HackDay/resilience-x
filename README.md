# Resilience-X

An AI-powered Q&A demo that connects the dots across messy documents using multi-hop reasoning. Built with GraphRAG for explainability, Weaviate for semantic search, NLWeb for natural language queries, and GitHub Copilot to accelerate development.

## 🎯 Project Overview

Resilience-X helps answer "what/why/where" recovery questions from a tiny crisis corpus with explainability. This hackday project demonstrates how AI-native tools can accelerate startup-style product building.

### Tech Stack
- **Backend:** Python (FastAPI) - Orchestrates Weaviate retrieval + GraphRAG reasoning
- **Frontend:** Next.js (NLWeb) - Single page with input box and results panel  
- **Vector DB:** Weaviate (localhost:8080) - Semantic search and document storage
- **Reasoning:** GraphRAG - Multi-hop reasoning with explainability

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Node.js 18+ (for frontend)

### Backend Setup
```bash
# 1. Start Weaviate
docker compose up -d weaviate

# 2. Install API dependencies
cd services/api
pip install fastapi uvicorn weaviate-client pydantic python-multipart httpx

# 3. Start the API
uvicorn main:app --reload --port 8000

# 4. In another terminal, load sample data
bash scripts/ingest.sh

# 5. Test with demo queries
bash scripts/demo.sh
```

### Frontend Setup (Coming Soon)
```bash
cd apps/web
npm install
npm run dev
```

## 📁 Project Structure

```
resilience-x/
├── services/api/          # FastAPI backend with Weaviate integration
│   ├── main.py           # Main FastAPI app with /ask endpoint
│   ├── models.py         # Pydantic models for requests/responses
│   ├── clients/          # External service integrations
│   │   └── weaviate_client.py  # Weaviate semantic search client
│   └── tests/            # Comprehensive test suite
├── apps/web/             # Next.js frontend (NLWeb UI) - Coming Soon
├── rag/                  # GraphRAG project and sample data
│   └── data/             # Sample crisis documents
├── scripts/              # Setup and demo scripts
│   ├── ingest.sh        # Load sample data into Weaviate
│   └── demo.sh          # End-to-end demo queries
└── docker-compose.yml   # Local Weaviate setup
```

## 🔄 API Usage

### POST /ask
Ask questions about crisis recovery scenarios:

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Which areas have cleanup delays?"}'
```

**Response:**
```json
{
  "answer": "Based on the available information: Road cleanup in King County is delayed due to crew shortages and equipment issues.",
  "explanation_bullets": [
    "Found 2 relevant documents in the knowledge base",
    "Top match: king_county_report.txt (relevance: 0.85)"
  ],
  "sources": [
    "king_county_report.txt (relevance: 0.85): Road cleanup in King County is delayed..."
  ]
}
```

## 🧪 Testing

```bash
# Run API tests
cd services/api
python -m pytest tests/ -v

# Validate implementation without external dependencies
python validate_implementation.py
```

## 🛠️ Development Status

### ✅ Completed (Sprint 1: Backend & Data)
- [x] **Weaviate Integration** - Semantic search with fallback handling
- [x] **FastAPI Backend** - `/ask` endpoint with proper error handling  
- [x] **Sample Data** - Crisis recovery documents and ingestion script
- [x] **Testing** - Comprehensive test coverage with mocking
- [x] **Docker Setup** - Local Weaviate environment
- [x] **Demo Scripts** - End-to-end functionality demonstration

### 🚧 In Progress (Sprint 2: Frontend & Integration)
- [ ] **GraphRAG Integration** - Multi-hop reasoning over retrieved documents
- [ ] **Next.js Frontend** - NLWeb UI with accessibility focus
- [ ] **End-to-End Integration** - Connect frontend to backend API
- [ ] **Enhanced Answers** - More sophisticated response generation

## 🎪 Demo Script (90 seconds)

1. **Show the API in action**: `bash scripts/demo.sh`
2. **Ask sample questions**:
   - "Which areas have cleanup delays?" 
   - "What are the power outage numbers?"
   - "Where are debris overflow issues?"
3. **Show explainable results** with sources and reasoning bullets
4. **Highlight the tech stack**: "Built with Copilot, GraphRAG, NLWeb, and Weaviate"

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:
- `WEAVIATE_URL` - Weaviate instance URL
- `OPENAI_APIKEY` - For text vectorization (optional for demo)

## 📚 Documentation

- [API Documentation](services/api/README.md) - Detailed backend setup and usage
- [Frontend Documentation](apps/web/README.md) - UI setup and components (Coming Soon)

## 🤝 Contributing

This is a hackday project built with GitHub Copilot to demonstrate rapid AI-assisted development. The focus is on clean, minimal code that showcases the integration of multiple AI technologies.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.
