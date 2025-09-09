#!/bin/bash
# Demo script for Resilience-X
# Shows the complete end-to-end functionality

set -e

echo "🎯 Resilience-X Demo Script"
echo "=========================="

# Check if services are running
echo "⚡ Checking service status..."

# Check Weaviate
if ! curl -s http://localhost:8080/v1/meta > /dev/null; then
    echo "❌ Weaviate not running. Start with: docker compose up -d weaviate"
    exit 1
fi
echo "✅ Weaviate is running"

# Check API
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "⚠️  API not running. Starting API server..."
    cd services/api
    echo "🚀 Starting API server in background..."
    uv run uvicorn main:app --reload --port 8000 &
    API_PID=$!
    cd ../..
    
    # Wait for API to start
    echo "⏳ Waiting for API to start..."
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            break
        fi
        sleep 2
    done
    
    if ! curl -s http://localhost:8000/health > /dev/null; then
        echo "❌ API failed to start"
        exit 1
    fi
fi
echo "✅ API is running"

echo ""
echo "🎬 Running Demo Queries"
echo "======================"

# Demo query 1
echo "📝 Query 1: Which areas have cleanup delays?"
curl -s -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Which areas have cleanup delays?"}' | \
     python -m json.tool

echo ""
echo "---"
echo ""

# Demo query 2  
echo "📝 Query 2: What are the power outage numbers?"
curl -s -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the current power outage numbers?"}' | \
     python -m json.tool

echo ""
echo "---"
echo ""

# Demo query 3
echo "📝 Query 3: Where are the debris overflow issues?"
curl -s -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Where are the debris overflow issues occurring?"}' | \
     python -m json.tool

echo ""
echo "🎉 Demo completed!"
echo ""
echo "💡 Next steps:"
echo "  • Open http://localhost:8000/docs for API documentation"
echo "  • Start frontend with: npm run dev --prefix apps/web"
echo "  • Try your own questions by posting to /ask endpoint"

# Cleanup API if we started it
if [ ! -z "$API_PID" ]; then
    echo "🧹 Stopping API server..."
    kill $API_PID 2>/dev/null || true
fi