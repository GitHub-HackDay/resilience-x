#!/bin/bash
# demo.sh - Run the Resilience-X API server for demonstration

set -e

echo "🎬 Starting Resilience-X Demo..."

# Check if we're in the right directory
if [ ! -f "services/api/pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the repository root"
    exit 1
fi

# Check if Weaviate is running
echo "📡 Checking Weaviate connection..."
if ! curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; then
    echo "⚠️  Weaviate not available. The API will use mock data."
fi

# Start the API server
echo "🚀 Starting FastAPI server..."
cd services/api

if command -v uv &> /dev/null; then
    echo "📦 Using uv to run the server..."
    uv run uvicorn main:app --reload --port 8000 --host 0.0.0.0
else
    echo "📦 Using pip installation to run the server..."
    uvicorn main:app --reload --port 8000 --host 0.0.0.0
fi