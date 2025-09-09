#!/bin/bash

# Resilience-X Demo Script
# Complete setup and demo of the Resilience-X system

set -e

echo "🎬 Starting Resilience-X Demo Setup..."

# Check if we're in the project root
if [[ ! -f "docker-compose.yml" ]]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📋 Step 1: Starting Weaviate..."
docker compose up -d weaviate

echo "⏳ Waiting for Weaviate to be ready..."
until curl -s http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo " Ready!"

echo "📋 Step 2: Installing dependencies and ingesting data..."
bash scripts/ingest.sh

echo "📋 Step 3: Starting the API server..."
cd services/api
source .venv/bin/activate
uvicorn main:app --reload --port 8000 &
API_PID=$!
cd ../..

echo "⏳ Waiting for API to be ready..."
until curl -s http://localhost:8000/health > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo " Ready!"

echo "📋 Step 4: Installing frontend dependencies..."
cd apps/web
npm ci
cd ../..

echo "📋 Step 5: Starting the frontend..."
cd apps/web
npm run dev &
WEB_PID=$!
cd ../..

echo ""
echo "🎉 Demo is ready!"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo "   Weaviate: http://localhost:8080"
echo ""
echo "Try asking: 'Which neighborhoods are facing cleanup delays?'"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $API_PID 2>/dev/null || true
    kill $WEB_PID 2>/dev/null || true
    docker compose down
    echo "✅ Cleanup complete"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for user to stop the demo
wait