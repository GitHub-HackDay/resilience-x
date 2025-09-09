#!/bin/bash
# Demo script for Resilience-X

echo "Starting Resilience-X Demo..."

# Start API server in background
echo "Starting API server..."
cd services/api
uvicorn main:app --reload --port 8000 &
API_PID=$!
cd ../..

# Wait for API to start
sleep 3

echo "Testing API with sample questions..."

# Test 1: Cleanup delays
echo "Question: Why are cleanup operations delayed?"
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Why are cleanup operations delayed?"}' \
  | python -m json.tool

echo -e "\n\nQuestion: Which roads are blocked?"
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Which roads are blocked?"}' \
  | python -m json.tool

echo -e "\n\nAPI Demo complete. Starting frontend..."
echo "Install frontend dependencies with: npm ci --prefix apps/web"
echo "Start frontend with: npm run dev --prefix apps/web"
echo "Then visit: http://localhost:3000"

# Keep API running
echo "API server running at http://localhost:8000"
echo "Press Ctrl+C to stop"
wait $API_PID