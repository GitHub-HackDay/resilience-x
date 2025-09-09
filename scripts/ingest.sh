#!/bin/bash

# Crisis Document Ingestion Script
# Ingests crisis recovery documents into Weaviate for the Resilience-X Q&A system

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting Resilience-X Document Ingestion Pipeline"
echo "======================================================"

# Check if Weaviate is running
echo "🔍 Checking Weaviate connection..."
if ! curl -sf http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo "❌ Weaviate is not running at localhost:8080"
    echo "💡 Start Weaviate with: docker compose up -d weaviate"
    exit 1
fi
echo "✅ Weaviate is running"

# Check Python environment
echo "🐍 Checking Python environment..."
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first."
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing Python dependencies..."
cd "$PROJECT_ROOT"
uv sync --quiet

# Set environment variables
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Run ingestion
echo "📚 Processing and ingesting crisis documents..."
uv run python -c "
import sys
import os
sys.path.insert(0, '$PROJECT_ROOT')

import logging
from vector.weaviate_bootstrap import ingest_crisis_documents

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Run ingestion
data_dir = '$PROJECT_ROOT/rag/data'
success = ingest_crisis_documents(data_dir)

if success:
    print('✅ Document ingestion completed successfully!')
    print('🔍 You can now query the documents through the Weaviate API')
    sys.exit(0)
else:
    print('❌ Document ingestion failed!')
    sys.exit(1)
"

# Verify ingestion
echo "🔍 Verifying ingestion..."
DOCUMENT_COUNT=$(curl -s -X POST http://localhost:8080/v1/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ Aggregate { CrisisDocument { meta { count } } } }"}' | \
  python -c "import sys, json; data=json.load(sys.stdin); print(data['data']['Aggregate']['CrisisDocument'][0]['meta']['count'])" 2>/dev/null || echo "0")

if [ "$DOCUMENT_COUNT" -gt 0 ]; then
    echo "✅ Ingestion verified: $DOCUMENT_COUNT documents in Weaviate"
    echo ""
    echo "🎉 Ingestion pipeline completed successfully!"
    echo "📊 Next steps:"
    echo "   - Run the API server: uv run uvicorn services.api.main:app --reload --port 8000"
    echo "   - Start the frontend: npm run dev --prefix apps/web"
    echo "   - Test queries through the /ask endpoint"
else
    echo "❌ Verification failed: No documents found in Weaviate"
    exit 1
fi