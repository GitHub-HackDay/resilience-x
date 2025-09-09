# Resilience-X

> **AI-powered crisis recovery Q&A system that turns messy documents into actionable, explainable answers**

An intelligent demo application that helps emergency operations planners quickly answer critical questions like *"Which neighborhoods are facing cleanup delays and why?"* by combining semantic search, graph reasoning, and natural language processing.

Built for GitHub + Microsoft Research Builders Hack Day, showcasing how AI-native tools (GitHub Copilot, GraphRAG, NLWeb, Weaviate) can accelerate startup-style product building.

## 🎯 Quick Demo (90 seconds)

1. **Ask a natural language question:** "Which roads are still blocked near Redmond, and why is cleanup delayed?"
2. **Get comprehensive answers:**
   - **Answer:** "Cleanup is delayed in King County neighborhoods..."
   - **Why:** Step-by-step explanation with reasoning
   - **Sources:** Links to original documents and evidence

3. **See the magic:** Multi-hop reasoning across documents with full explainability

## 🏗️ Architecture

```
Frontend (Next.js/NLWeb) → API (FastAPI) → Vector Search (Weaviate) + Graph Reasoning (GraphRAG)
```

- **Frontend:** Single-page Next.js app with natural language input and structured results
- **Backend:** FastAPI service with `/ask` endpoint orchestrating retrieval and reasoning  
- **Vector DB:** Weaviate for semantic search across crisis documents
- **Reasoning:** GraphRAG for multi-hop explanations and source attribution

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+ with npm

### Setup & Run

1. **Clone and setup:**
```bash
git clone https://github.com/GitHub-HackDay/resilience-x
cd resilience-x
```

2. **Start Weaviate:**
```bash
docker compose up -d weaviate
```

3. **Setup backend:**
```bash
uv sync
```

4. **Setup frontend:**
```bash
npm ci --prefix apps/web
```

5. **Ingest demo data:**
```bash
bash scripts/ingest.sh
```

6. **Start services:**
```bash
# Backend (Terminal 1)
uv run uvicorn services.api.main:app --reload --port 8000

# Frontend (Terminal 2)  
npm run dev --prefix apps/web
```

7. **Open demo:** http://localhost:3000

### One-Click Demo
```bash
bash scripts/demo.sh
```

## 📁 Project Structure

```
resilience-x/
├── apps/web/                 # Next.js frontend (NLWeb UI)
├── services/api/             # FastAPI backend with /ask endpoint
├── rag/
│   ├── graphrag_project/     # GraphRAG configuration and pipeline
│   └── data/                 # Crisis documents (5-20 demo docs)
├── vector/weaviate_bootstrap/# Weaviate schema and data loader
├── scripts/                  # Setup and demo automation
│   ├── ingest.sh            # Data ingestion pipeline
│   └── demo.sh              # Full demo runner
└── .github/                  # Copilot instructions and workflows
```

## 🔧 Development

### Backend Development
```bash
# Run with hot reload
uv run uvicorn services.api.main:app --reload --port 8000

# Run tests
uv run pytest -q

# Type checking
uv run mypy services/
```

### Frontend Development
```bash
# Development server
npm run dev --prefix apps/web

# Build for production
npm run build --prefix apps/web

# Run tests
npm run test --prefix apps/web
```

### Testing
```bash
# All tests
uv run pytest -q && npm run test --prefix apps/web

# Backend only
uv run pytest services/api/tests/

# Frontend only (Playwright)
npm run test --prefix apps/web
```

## 🤖 AI-Native Development

This project showcases AI-accelerated development:

- **GitHub Copilot:** Code generation and completion throughout
- **GraphRAG:** Multi-hop reasoning with explainability
- **NLWeb:** Natural language interface for web interactions
- **Weaviate:** Semantic vector search with AI embeddings

## 📊 Demo Data

The system works with a curated set of 5-20 short crisis recovery documents covering:
- Road closures and infrastructure damage
- Resource shortages and crew availability  
- Cleanup progress and delays
- Community impact assessments

## 🎯 Use Cases

Perfect for emergency operations planners who need to:
- **Quickly assess** recovery status across multiple areas
- **Understand root causes** of delays and bottlenecks
- **Get explainable answers** with source attribution
- **Navigate complex** multi-document information

## 🔍 API Reference

### POST `/ask`
**Request:**
```json
{
  "question": "Which neighborhoods are facing cleanup delays?"
}
```

**Response:**
```json
{
  "answer": "Cleanup is delayed in King County neighborhoods...",
  "explanation_bullets": [
    "Crew shortages identified in Report A",
    "Debris overflow reported in Report B",
    "Equipment maintenance issues in Report C"
  ],
  "sources": [
    "crisis-report-001.pdf",
    "status-update-kingcounty.txt"
  ]
}
```

## 🛠️ Troubleshooting

### Weaviate Issues
```bash
# Check Weaviate status
docker compose ps weaviate

# Reset Weaviate data
docker compose down weaviate
docker volume rm resilience-x_weaviate_data
docker compose up -d weaviate
```

### GraphRAG Issues
```bash
# Rebuild GraphRAG index
cd rag/graphrag_project
python -m graphrag.index --init
python -m graphrag.index --root .
```

### General Issues
- Ensure all ports (3000, 8000, 8080) are available
- Check Docker has sufficient memory (4GB+ recommended)
- Verify environment variables in `.env` files

## 🤝 Contributing

1. Follow existing code patterns and type hints
2. Add tests for new functionality  
3. Update documentation for user-facing changes
4. Use GitHub Copilot for code generation assistance

### Code Style
- **Python:** Type hints, docstrings, pytest for tests
- **TypeScript:** Strict mode, accessible UI components
- **Documentation:** Clear, concise, example-driven

## 📋 Roadmap

- [x] Core MVP with semantic search + graph reasoning
- [x] Single-page frontend with explainable results  
- [x] Docker-based local development setup
- [ ] Enhanced visualization of reasoning paths
- [ ] Additional crisis management domains
- [ ] Production deployment templates

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built in one day with AI-native tools** 🚀  
*GitHub Copilot + GraphRAG + NLWeb + Weaviate*
