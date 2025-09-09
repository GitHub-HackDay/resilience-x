# Resilience-X Demo Script

This directory contains scripts to orchestrate the complete Resilience-X demo.

## Scripts

### `demo.sh` - Main Demo Orchestration
Complete end-to-end demo script that starts all services and provides demo instructions.

**Usage:**
```bash
# Start full demo
bash scripts/demo.sh

# Check system requirements
bash scripts/demo.sh --check

# Clean up running processes  
bash scripts/demo.sh --clean

# Show help
bash scripts/demo.sh --help
```

**What it does:**
1. ✅ Validates system requirements (Docker, Python, Node.js)
2. 🐳 Starts Weaviate vector database via Docker Compose
3. 📊 Runs data ingestion to populate sample crisis documents
4. 🚀 Starts FastAPI backend API on port 8000
5. 🌐 Starts Next.js frontend on port 3000 (if available)
6. 📋 Displays demo instructions and example queries

### `ingest.sh` - Data Ingestion
Handles ingestion of crisis documents into Weaviate vector database.

**Usage:**
```bash
bash scripts/ingest.sh
```

**What it does:**
1. 📡 Checks Weaviate connection
2. 📁 Creates sample crisis documents if they don't exist
3. 🤖 Sets up vector embedding pipeline using sentence-transformers
4. ⬆️ Ingests documents with semantic embeddings
5. ✅ Verifies successful ingestion

## Demo Flow (90 seconds)

1. **Start Demo**: `bash scripts/demo.sh`
2. **Open Browser**: Navigate to frontend (http://localhost:3000) or API docs (http://localhost:8000/docs)
3. **Ask Questions**:
   - "Which neighborhoods are facing cleanup delays?"
   - "What infrastructure issues need immediate attention?"
   - "Where are the emergency shelters located?"
4. **Show Results**: Answer + explanation bullets + sources
5. **Highlight**: "Built with Copilot, GraphRAG, NLWeb, and Weaviate"

## System Requirements

- **Docker & Docker Compose**: For Weaviate vector database
- **Python 3.8+**: For backend API and data ingestion
- **Node.js 18+**: For frontend (if implemented)
- **Git**: For repository operations

## Ports Used

- **8080**: Weaviate vector database
- **8000**: FastAPI backend API
- **3000**: Next.js frontend UI

## Troubleshooting

**Weaviate won't start:**
```bash
docker compose down
docker compose up -d weaviate
```

**Backend API errors:**
```bash
# Check if port is in use
lsof -i :8000

# View backend logs
docker compose logs -f weaviate
```

**Clean restart:**
```bash
bash scripts/demo.sh --clean
bash scripts/demo.sh
```

## Development Notes

- Demo script includes graceful error handling and cleanup
- Fallback static responses when GraphRAG isn't fully implemented
- Minimal dependencies for quick setup
- Follows the golden path workflow from project documentation