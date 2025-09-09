#!/bin/bash
# ingest.sh - Ingest crisis documents into Weaviate and create GraphRAG project

set -e

echo "🚀 Starting Resilience-X data ingestion..."

# Check if we're in the right directory
if [ ! -f "services/api/pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the repository root"
    exit 1
fi

# Check if Weaviate is running
echo "📡 Checking Weaviate connection..."
if ! curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo "⚠️  Weaviate not running. Starting with Docker Compose..."
    if [ -f "docker-compose.yml" ]; then
        docker compose up -d weaviate
        echo "⏳ Waiting for Weaviate to be ready..."
        sleep 10
    else
        echo "❌ No docker-compose.yml found. Please ensure Weaviate is running at http://localhost:8080"
        exit 1
    fi
fi

# Install dependencies if needed
echo "📦 Installing API dependencies..."
cd services/api
if command -v uv &> /dev/null; then
    uv sync
else
    pip install -e .
fi
cd ../..

# Create GraphRAG project structure
echo "🧠 Setting up GraphRAG project..."
mkdir -p rag/graphrag_project/input

# Copy sample documents to GraphRAG input
cp rag/data/*.txt rag/graphrag_project/input/

# Create basic GraphRAG settings if not exists
if [ ! -f "rag/graphrag_project/settings.yaml" ]; then
    cat > rag/graphrag_project/settings.yaml << EOF
llm:
  api_key: \${OPENAI_API_KEY}
  type: openai_chat
  model: gpt-3.5-turbo
  max_tokens: 4000

embeddings:
  api_key: \${OPENAI_API_KEY}
  type: openai_embedding
  model: text-embedding-ada-002

storage:
  type: memory

input:
  type: file
  file_type: text
  base_dir: "./input"

reporting:
  type: file
  base_dir: "./output"
EOF
    echo "✅ Created GraphRAG settings file"
fi

echo "✅ Data ingestion setup complete!"
echo ""
echo "Next steps:"
echo "1. Set your OPENAI_API_KEY environment variable"
echo "2. Run 'bash scripts/demo.sh' to start the API server"
echo "3. The API will be available at http://localhost:8000"