#!/bin/bash

# Demo script for Resilience-X fallback static example
# This script demonstrates the fallback functionality without requiring external services

echo "🚀 Starting Resilience-X Demo (Fallback Mode)"
echo "============================================="

echo ""
echo "📋 This demo shows static fallback examples for crisis recovery Q&A"
echo "🔧 No external services (Weaviate, GraphRAG) required"
echo ""

# Check if we're in the right directory
if [[ ! -f "services/api/main.py" ]]; then
    echo "❌ Error: Please run this script from the repository root"
    exit 1
fi

# Install Python dependencies if needed
if [[ ! -d "services/api/.venv" ]] && command -v uv >/dev/null 2>&1; then
    echo "📦 Installing Python dependencies..."
    cd services/api
    uv sync
    cd ../..
elif command -v pip >/dev/null 2>&1; then
    echo "📦 Installing Python dependencies with pip..."
    cd services/api
    pip install fastapi uvicorn pydantic python-dotenv
    cd ../..
fi

# Start the backend API in background
echo "🔧 Starting backend API (port 8000)..."
cd services/api
if command -v uv >/dev/null 2>&1; then
    uv run uvicorn main:app --reload --port 8000 &
else
    python -m uvicorn main:app --reload --port 8000 &
fi
API_PID=$!
cd ../..

# Wait for API to start
echo "⏳ Waiting for API to start..."
sleep 3

# Test the API with example questions
echo ""
echo "🧪 Testing fallback examples:"
echo "==============================="

echo ""
echo "1️⃣ Testing cleanup delays question..."
response1=$(curl -s -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Which areas have cleanup delays?"}')
if [[ $? -eq 0 ]]; then
    echo "✅ Success! Response:"
    echo "$response1" | python -m json.tool
else
    echo "❌ Failed to get response"
fi

echo ""
echo "2️⃣ Testing road blocks question..."
response2=$(curl -s -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Which roads are blocked near Redmond?"}')
if [[ $? -eq 0 ]]; then
    echo "✅ Success! Response:"
    echo "$response2" | python -m json.tool
else
    echo "❌ Failed to get response"
fi

echo ""
echo "3️⃣ Testing health check..."
health=$(curl -s "http://localhost:8000/health")
if [[ $? -eq 0 ]]; then
    echo "✅ Health check passed:"
    echo "$health" | python -m json.tool
else
    echo "❌ Health check failed"
fi

echo ""
echo "🎯 Demo completed successfully!"
echo ""
echo "💡 Next steps:"
echo "  1. Install frontend dependencies: npm ci --prefix apps/web"
echo "  2. Start frontend: npm run dev --prefix apps/web"
echo "  3. Visit http://localhost:3000 to try the web interface"
echo ""
echo "🛑 Stopping backend API..."
kill $API_PID 2>/dev/null
wait $API_PID 2>/dev/null

echo "✨ Demo finished!"