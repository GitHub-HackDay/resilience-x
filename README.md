# Resilience-X

An AI-powered crisis recovery Q&A system that connects the dots across messy documents using multi-hop reasoning. Built with GraphRAG for explainability, Weaviate for semantic search, Next.js for natural language queries, and GitHub Copilot to accelerate development.

## Quick Start

1. **Start Weaviate**
   ```bash
   docker compose up -d weaviate
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the complete demo**
   ```bash
   bash scripts/demo.sh
   ```

4. **Or run components individually:**

   **Backend API:**
   ```bash
   cd services/api
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   uvicorn main:app --reload --port 8000
   ```

   **Frontend:**
   ```bash
   cd apps/web
   npm ci
   npm run dev
   ```

   **Data Ingestion:**
   ```bash
   bash scripts/ingest.sh
   ```

## Demo

Visit http://localhost:3000 and try asking:
- "Which neighborhoods are facing cleanup delays?"
- "Why is debris collection behind schedule?"
- "What weather impacts are affecting recovery?"

## Architecture

- **Frontend:** Next.js single page with input box and results panel
- **Backend:** FastAPI `/ask` endpoint orchestrating retrieval + reasoning  
- **Vector DB:** Weaviate (localhost:8080) for semantic search
- **Reasoning:** GraphRAG for multi-hop explainable answers
- **Data:** 5-20 sample crisis recovery documents

## Tech Stack

- **AI/ML:** GraphRAG, Weaviate, OpenAI embeddings
- **Backend:** Python, FastAPI, Pydantic  
- **Frontend:** Next.js, TypeScript, React
- **Infrastructure:** Docker, uv (Python), npm
- **Development:** GitHub Copilot assisted

## Project Structure

```
resilience-x/
├── apps/web/                    # Next.js frontend 
├── services/api/                # FastAPI backend
├── rag/
│   ├── data/                    # Sample crisis documents
│   └── graphrag_project/        # GraphRAG configuration
├── vector/weaviate_bootstrap/   # Weaviate setup
├── scripts/                     # Setup and demo scripts
└── docker-compose.yml           # Weaviate service
```

## Development

Built as part of GitHub + Microsoft Research Builders Hack Day, showcasing AI-native development workflows.

## License

MIT
