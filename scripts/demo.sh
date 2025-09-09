#!/bin/bash

# Demo script for Resilience-X API
# Demonstrates the /ask endpoint with various questions

set -e

API_URL="http://localhost:8000"

echo "🚀 Resilience-X API Demo"
echo "========================="
echo ""

# Check if server is running
echo "📋 Checking API health..."
if curl -s "$API_URL/health" > /dev/null; then
    echo "✅ API is running"
else
    echo "❌ API is not running. Start it with:"
    echo "    uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload"
    exit 1
fi

echo ""

# Function to ask a question and format the response
ask_question() {
    local question="$1"
    echo "🤔 Question: $question"
    echo "---"
    
    response=$(curl -s -X POST "$API_URL/ask" \
        -H "Content-Type: application/json" \
        -d "{\"question\": \"$question\"}")
    
    # Extract and format the response
    answer=$(echo "$response" | python -c "import sys, json; data=json.load(sys.stdin); print(data['answer'])")
    explanations=$(echo "$response" | python -c "import sys, json; data=json.load(sys.stdin); print('\n'.join(['• ' + bullet for bullet in data['explanation_bullets']]))")
    sources=$(echo "$response" | python -c "import sys, json; data=json.load(sys.stdin); print('\n'.join(['📄 ' + source for source in data['sources']]))")
    
    echo "💡 Answer: $answer"
    echo ""
    echo "📝 Explanation:"
    echo "$explanations"
    echo ""
    echo "📚 Sources:"
    echo "$sources"
    echo ""
    echo "================================="
    echo ""
}

# Demo questions
echo "🎯 Demo Questions:"
echo ""

ask_question "Which neighborhoods are facing cleanup delays?"

ask_question "Which roads are blocked near Redmond?"

ask_question "What is the current status of recovery efforts?"

# Test error handling
echo "🚨 Testing error handling:"
echo ""
echo "🤔 Question: (empty)"
echo "---"
error_response=$(curl -s -X POST "$API_URL/ask" \
    -H "Content-Type: application/json" \
    -d '{"question": ""}')

error_detail=$(echo "$error_response" | python -c "import sys, json; data=json.load(sys.stdin); print(data.get('detail', 'Unknown error'))")
echo "❌ Error: $error_detail"
echo ""

echo "✨ Demo completed! Check out the interactive docs at:"
echo "   📖 Swagger UI: $API_URL/docs"
echo "   📖 ReDoc: $API_URL/redoc"