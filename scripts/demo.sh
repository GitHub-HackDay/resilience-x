#!/bin/bash

# Resilience-X Demo Script
# Comprehensive demo runner for hackday presentations

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is required but not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is required but not installed"
        exit 1
    fi
    
    # Check uv (Python package manager)
    if ! command -v uv &> /dev/null; then
        log_error "uv is required but not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        log_error "npm is required but not installed"
        exit 1
    fi
    
    log_success "All prerequisites are installed"
}

# Start Weaviate
start_weaviate() {
    log_info "Starting Weaviate vector database..."
    
    # Check if Weaviate is already running
    if docker ps | grep -q "resilience-x-weaviate"; then
        log_warning "Weaviate is already running"
    else
        docker compose up -d weaviate
        
        # Wait for Weaviate to be ready
        log_info "Waiting for Weaviate to be ready..."
        timeout=60
        while [ $timeout -gt 0 ]; do
            if curl -s http://localhost:8080/v1/.well-known/ready | grep -q "true"; then
                break
            fi
            sleep 2
            timeout=$((timeout - 2))
        done
        
        if [ $timeout -eq 0 ]; then
            log_error "Weaviate failed to start within 60 seconds"
            exit 1
        fi
    fi
    
    log_success "Weaviate is ready at http://localhost:8080"
}

# Install dependencies
install_dependencies() {
    log_info "Installing backend dependencies..."
    uv sync
    
    # Check if frontend directory exists
    if [ -d "apps/web" ]; then
        log_info "Installing frontend dependencies..."
        npm ci --prefix apps/web
    else
        log_warning "Frontend directory (apps/web) not found, skipping frontend setup"
    fi
    
    log_success "Dependencies installed"
}

# Ingest demo data
ingest_data() {
    log_info "Setting up demo data..."
    
    if [ -f "scripts/ingest.sh" ]; then
        log_info "Running data ingestion script..."
        bash scripts/ingest.sh
    else
        log_warning "Ingest script not found, skipping data ingestion"
        log_info "You may need to set up demo data manually"
    fi
    
    log_success "Demo data setup complete"
}

# Start backend service
start_backend() {
    log_info "Starting backend service..."
    
    if [ -d "services/api" ]; then
        log_info "Backend found, starting FastAPI server..."
        log_info "Backend will be available at http://localhost:8000"
        log_info "API documentation at http://localhost:8000/docs"
        
        # Start in background
        uv run uvicorn services.api.main:app --reload --port 8000 &
        BACKEND_PID=$!
        
        # Wait for backend to be ready
        log_info "Waiting for backend to start..."
        timeout=30
        while [ $timeout -gt 0 ]; do
            if curl -s http://localhost:8000/health &> /dev/null || curl -s http://localhost:8000/docs &> /dev/null; then
                break
            fi
            sleep 2
            timeout=$((timeout - 2))
        done
        
        if [ $timeout -gt 0 ]; then
            log_success "Backend is ready at http://localhost:8000"
        else
            log_warning "Backend may still be starting up"
        fi
    else
        log_warning "Backend directory (services/api) not found"
        log_info "Skipping backend startup"
    fi
}

# Start frontend service
start_frontend() {
    log_info "Starting frontend service..."
    
    if [ -d "apps/web" ]; then
        log_info "Frontend found, starting Next.js development server..."
        log_info "Frontend will be available at http://localhost:3000"
        
        # Start in background
        npm run dev --prefix apps/web &
        FRONTEND_PID=$!
        
        # Wait for frontend to be ready
        log_info "Waiting for frontend to start..."
        timeout=60
        while [ $timeout -gt 0 ]; do
            if curl -s http://localhost:3000 &> /dev/null; then
                break
            fi
            sleep 2
            timeout=$((timeout - 2))
        done
        
        if [ $timeout -gt 0 ]; then
            log_success "Frontend is ready at http://localhost:3000"
        else
            log_warning "Frontend may still be starting up"
        fi
    else
        log_warning "Frontend directory (apps/web) not found"
        log_info "Skipping frontend startup"
    fi
}

# Demo instructions
show_demo_instructions() {
    echo
    echo "🎯 Resilience-X Demo Ready!"
    echo "=========================="
    echo
    echo "Demo Script (90 seconds):"
    echo "1. Open http://localhost:3000 in your browser"
    echo "2. Ask: 'Which neighborhoods are facing cleanup delays?'"
    echo "3. Observe the structured response:"
    echo "   • Answer: Direct response to the question"
    echo "   • Why: Step-by-step explanation bullets"
    echo "   • Sources: Links to original documents"
    echo
    echo "Example Questions to Try:"
    echo "• Which roads are still blocked near Redmond?"
    echo "• What are the main causes of cleanup delays?"
    echo "• Where do we need more cleanup crews?"
    echo "• Why is debris removal taking so long?"
    echo
    echo "Services Running:"
    echo "• Frontend: http://localhost:3000 (Main Demo Interface)"
    echo "• Backend API: http://localhost:8000 (FastAPI)"
    echo "• API Docs: http://localhost:8000/docs (Interactive API docs)"
    echo "• Weaviate: http://localhost:8080 (Vector Database)"
    echo
    echo "Press Ctrl+C to stop all services"
    echo
}

# Cleanup function
cleanup() {
    log_info "Shutting down services..."
    
    # Kill background processes
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Stop Docker containers
    docker compose down weaviate 2>/dev/null || true
    
    log_success "All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "🚀 Resilience-X Demo Setup"
    echo "========================="
    echo
    
    check_prerequisites
    start_weaviate
    install_dependencies
    ingest_data
    start_backend
    start_frontend
    show_demo_instructions
    
    # Keep script running
    wait
}

# Run main function
main "$@"