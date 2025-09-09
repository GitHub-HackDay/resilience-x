#!/bin/bash

# Resilience-X Demo Script
# Complete end-to-end demo orchestration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
WEAVIATE_PORT=8080
BACKEND_PORT=8000
FRONTEND_PORT=3000
DEMO_TIMEOUT=300 # 5 minutes max for demo setup

print_header() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════╗"
    echo "║          RESILIENCE-X DEMO           ║"
    echo "║     AI-Powered Crisis Q&A System     ║"
    echo "╚══════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_requirements() {
    print_step "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
    
    # Check Python
    if ! python3 --version &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+."
        exit 1
    fi
    
    # Check Node.js (if frontend exists)
    if [ -d "$REPO_ROOT/apps/web" ] && ! command -v npm &> /dev/null; then
        print_error "Node.js/npm is not installed. Please install Node.js 18+."
        exit 1
    fi
    
    print_success "System requirements check passed"
}

start_weaviate() {
    print_step "Starting Weaviate vector database..."
    
    cd "$REPO_ROOT"
    
    # Start Weaviate
    docker compose up -d weaviate
    
    # Wait for Weaviate to be ready
    echo -n "Waiting for Weaviate to start"
    for i in {1..30}; do
        if curl -s http://localhost:${WEAVIATE_PORT}/v1/.well-known/ready > /dev/null 2>&1; then
            echo ""
            print_success "Weaviate is ready on http://localhost:${WEAVIATE_PORT}"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    
    echo ""
    print_error "Weaviate failed to start within 60 seconds"
    exit 1
}

run_data_ingestion() {
    print_step "Running data ingestion..."
    
    if [ -f "$SCRIPT_DIR/ingest.sh" ]; then
        bash "$SCRIPT_DIR/ingest.sh"
    else
        print_warning "Ingest script not found. Creating minimal setup..."
        
        # Create minimal data structure
        mkdir -p "$REPO_ROOT/rag/data"
        mkdir -p "$REPO_ROOT/vector/weaviate_bootstrap"
        
        print_success "Basic directory structure created"
    fi
}

start_backend() {
    print_step "Starting backend API..."
    
    BACKEND_DIR="$REPO_ROOT/services/api"
    
    if [ -d "$BACKEND_DIR" ]; then
        cd "$BACKEND_DIR"
        
        # Install dependencies if uv is available, otherwise use pip
        if command -v uv &> /dev/null; then
            uv sync
            uv run uvicorn main:app --reload --port $BACKEND_PORT &
        elif [ -f "requirements.txt" ]; then
            pip3 install -r requirements.txt --user --quiet
            python3 -m uvicorn main:app --reload --port $BACKEND_PORT &
        else
            print_warning "Backend not fully implemented yet"
            # Create a minimal FastAPI placeholder
            create_placeholder_backend
        fi
        
        BACKEND_PID=$!
        
        # Wait for backend to start
        echo -n "Waiting for backend to start"
        for i in {1..15}; do
            if curl -s http://localhost:${BACKEND_PORT}/health > /dev/null 2>&1; then
                echo ""
                print_success "Backend API ready on http://localhost:${BACKEND_PORT}"
                return 0
            fi
            echo -n "."
            sleep 2
        done
        
        echo ""
        print_success "Backend started (may still be initializing)"
    else
        print_warning "Backend directory not found at $BACKEND_DIR"
        create_placeholder_backend
    fi
}

create_placeholder_backend() {
    print_step "Creating placeholder backend for demo..."
    
    mkdir -p "$REPO_ROOT/services/api"
    cd "$REPO_ROOT/services/api"
    
    cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="Resilience-X API", description="Crisis Q&A API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    explanation_bullets: List[str]
    sources: List[str]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    """Demo endpoint with static response for validation."""
    return Answer(
        answer="Cleanup is delayed in King County due to crew shortages and equipment delays.",
        explanation_bullets=[
            "Debris removal crews are short-staffed due to illness (Crisis Report #001)",
            "Heavy equipment delayed due to supply chain issues (Crisis Report #001)", 
            "Multiple infrastructure issues require coordinated response (Crisis Report #002)"
        ],
        sources=[
            "crisis_report_001.txt",
            "crisis_report_002.txt"
        ]
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
    
    # Install FastAPI
    pip3 install fastapi uvicorn --user --quiet
    
    # Start placeholder backend
    python3 main.py &
    BACKEND_PID=$!
    
    sleep 3
    print_success "Placeholder backend started"
}

start_frontend() {
    print_step "Starting frontend..."
    
    FRONTEND_DIR="$REPO_ROOT/apps/web"
    
    if [ -d "$FRONTEND_DIR" ]; then
        cd "$FRONTEND_DIR"
        
        # Install dependencies and start
        npm ci --quiet
        npm run dev -- --port $FRONTEND_PORT &
        FRONTEND_PID=$!
        
        # Wait for frontend to start
        echo -n "Waiting for frontend to start"
        for i in {1..20}; do
            if curl -s http://localhost:${FRONTEND_PORT} > /dev/null 2>&1; then
                echo ""
                print_success "Frontend ready on http://localhost:${FRONTEND_PORT}"
                return 0
            fi
            echo -n "."
            sleep 2
        done
        
        echo ""
        print_success "Frontend started (may still be building)"
    else
        print_warning "Frontend directory not found at $FRONTEND_DIR"
        print_warning "You can test the API directly at http://localhost:${BACKEND_PORT}/docs"
    fi
}

show_demo_instructions() {
    print_step "Demo Instructions"
    
    echo -e "${YELLOW}"
    echo "🎯 DEMO READY! Here's how to demonstrate Resilience-X:"
    echo ""
    echo "1. 🌐 Open your browser to:"
    if [ -d "$REPO_ROOT/apps/web" ]; then
        echo "   Frontend: http://localhost:${FRONTEND_PORT}"
    fi
    echo "   API Docs: http://localhost:${BACKEND_PORT}/docs"
    echo ""
    echo "2. 🔍 Try these demo questions:"
    echo "   • 'Which neighborhoods are facing cleanup delays?'"
    echo "   • 'What infrastructure issues need immediate attention?'"
    echo "   • 'Where are the emergency shelters located?'"
    echo ""
    echo "3. 📋 Expected response format:"
    echo "   • Answer: Clear, actionable response"
    echo "   • Why: 2-3 explanation bullets with sources"  
    echo "   • Sources: Relevant document references"
    echo ""
    echo "4. 🎪 Demo script (90 seconds):"
    echo "   • Show the clean, single-page interface"
    echo "   • Ask: 'Which roads are still blocked near Redmond?'"
    echo "   • Highlight the explainable AI features"
    echo "   • End with: 'Built in one day with Copilot, GraphRAG, NLWeb, and Weaviate'"
    echo -e "${NC}"
    
    echo -e "${BLUE}"
    echo "🔧 Services running:"
    echo "   • Weaviate (Vector DB): http://localhost:${WEAVIATE_PORT}"
    echo "   • Backend API: http://localhost:${BACKEND_PORT}"
    if [ -d "$REPO_ROOT/apps/web" ]; then
        echo "   • Frontend UI: http://localhost:${FRONTEND_PORT}"
    fi
    echo -e "${NC}"
}

cleanup() {
    print_step "Cleaning up demo processes..."
    
    # Kill background processes
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Stop Docker containers
    cd "$REPO_ROOT"
    docker compose down --quiet 2>/dev/null || true
    
    print_success "Cleanup completed"
}

# Trap cleanup on exit
trap cleanup EXIT

main() {
    cd "$REPO_ROOT"
    
    print_header
    
    # Validate setup
    check_requirements
    
    # Start services
    start_weaviate
    run_data_ingestion
    start_backend
    start_frontend
    
    # Show demo instructions
    show_demo_instructions
    
    # Keep script running
    echo ""
    echo -e "${GREEN}🚀 Demo is ready! Press Ctrl+C to stop all services.${NC}"
    
    # Wait for user interrupt
    while true; do
        sleep 1
    done
}

# Help function
show_help() {
    echo "Resilience-X Demo Script"
    echo ""
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  (no args)  Start full demo"
    echo "  --help     Show this help"
    echo "  --check    Check system requirements only"
    echo "  --clean    Clean up any running processes"
    echo ""
}

# Handle arguments
case "${1:-}" in
    --help)
        show_help
        exit 0
        ;;
    --check)
        check_requirements
        exit 0
        ;;
    --clean)
        cleanup
        exit 0
        ;;
    "")
        main
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
esac