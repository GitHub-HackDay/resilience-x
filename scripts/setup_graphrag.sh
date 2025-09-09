#!/bin/bash
# GraphRAG Setup and Build Script for Resilience-X
# This script sets up the GraphRAG environment and builds the knowledge graph

set -e  # Exit on any error

echo "🚀 Starting Resilience-X GraphRAG Setup..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GRAPHRAG_DIR="$PROJECT_ROOT/rag/graphrag_project"

# Check if we're in the right directory
if [ ! -f "$GRAPHRAG_DIR/settings.yaml" ]; then
    echo "❌ Error: GraphRAG settings.yaml not found at $GRAPHRAG_DIR/settings.yaml"
    echo "   Please run this script from the project root directory"
    exit 1
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY environment variable not set"
    echo "   You'll need to set this before running the graph builder:"
    echo "   export OPENAI_API_KEY=your_api_key_here"
    echo ""
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

echo "📦 Installing GraphRAG dependencies..."
cd "$GRAPHRAG_DIR"

# Install dependencies (in a real scenario, you'd want to use a virtual environment)
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️  Warning: requirements.txt not found, skipping dependency installation"
fi

# Check if data files exist
DATA_DIR="$PROJECT_ROOT/rag/data"
if [ ! -d "$DATA_DIR" ] || [ -z "$(ls -A "$DATA_DIR"/*.txt 2>/dev/null)" ]; then
    echo "❌ Error: No .txt files found in $DATA_DIR"
    echo "   Please add crisis recovery documents to the data directory"
    exit 1
fi

echo "📄 Found crisis recovery documents:"
ls -1 "$DATA_DIR"/*.txt | while read file; do
    echo "   - $(basename "$file")"
done

# Create output directories
mkdir -p "$GRAPHRAG_DIR/output"
mkdir -p "$GRAPHRAG_DIR/cache"
mkdir -p "$GRAPHRAG_DIR/reports"

echo "🔨 Building GraphRAG knowledge graph..."

# Run the graph builder
if [ -n "$OPENAI_API_KEY" ]; then
    python3 "$GRAPHRAG_DIR/build_graph.py"
    
    if [ $? -eq 0 ]; then
        echo "✅ GraphRAG knowledge graph created successfully!"
        echo "🎯 The graph is ready for use with the /ask endpoint"
        echo ""
        echo "📊 Output files:"
        find "$GRAPHRAG_DIR/output" -name "*.parquet" | while read file; do
            echo "   - $(basename "$file")"
        done
    else
        echo "❌ GraphRAG graph creation failed"
        exit 1
    fi
else
    echo "⏭️  Skipping graph creation (OPENAI_API_KEY not set)"
    echo "   Run 'export OPENAI_API_KEY=your_key' and then:"
    echo "   python3 $GRAPHRAG_DIR/build_graph.py"
fi

echo ""
echo "🎉 GraphRAG setup complete!"
echo "📍 Project location: $GRAPHRAG_DIR"
echo "📚 Data location: $DATA_DIR"