#!/bin/bash

# Resilience-X Data Ingestion Script
# Ingests crisis documents and creates vectors in Weaviate

set -e

echo "🚀 Starting data ingestion for Resilience-X..."

# Check if Weaviate is running
if ! curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo "❌ Weaviate is not running. Please start it first:"
    echo "   docker compose up -d weaviate"
    exit 1
fi

echo "✅ Weaviate is running"

# Check if we're in the project root
if [[ ! -f "docker-compose.yml" ]]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Install/check Python dependencies
echo "📦 Checking Python dependencies..."
cd services/api
if [[ ! -f ".venv/pyvenv.cfg" ]]; then
    echo "Creating Python virtual environment..."
    python -m venv .venv
fi

source .venv/bin/activate
pip install -e .

echo "📄 Loading documents to Weaviate..."
python -m vector.weaviate_bootstrap.loader

echo "🕸️  Building GraphRAG project graph..."
cd ../../rag/graphrag_project
python -m graphrag.index --root .

echo "✅ Data ingestion complete!"
echo "💡 Ready to run queries via the API"