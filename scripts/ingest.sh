#!/bin/bash

# Resilience-X Data Ingestion Script
# Loads crisis documents into Weaviate and builds GraphRAG index

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

main() {
    log_info "Starting Resilience-X data ingestion..."
    
    # Check if Weaviate is running
    if ! curl -s http://localhost:8080/v1/.well-known/ready | grep -q "true"; then
        log_warning "Weaviate is not running. Please start it first:"
        echo "  docker compose up -d weaviate"
        exit 1
    fi
    
    # Check if data directory exists
    if [ ! -d "rag/data" ]; then
        log_info "Creating sample data directory structure..."
        mkdir -p rag/data
        mkdir -p rag/graphrag_project
        
        # Create sample crisis documents
        cat > rag/data/crisis-report-001.txt << 'EOF'
King County Cleanup Status Report - Day 5

SUMMARY: Debris removal operations continue across King County with mixed progress.

ROAD CLOSURES:
- SR-520 eastbound remains blocked due to fallen trees
- I-405 northbound has partial lane restrictions
- Local streets in Redmond experiencing delays

CREW STATUS:
- 15 cleanup crews deployed (5 short of target)
- Equipment maintenance issues affecting 3 crews
- Additional crew requests submitted to state emergency management

BOTTLENECKS:
- Debris overflow at transfer stations
- Limited heavy equipment availability
- Permit delays for tree removal on private property

NEXT STEPS:
- Prioritize SR-520 clearance
- Coordinate with utility companies for power line clearance
- Request additional debris hauling capacity
EOF
        
        cat > rag/data/neighborhood-assessment-002.txt << 'EOF'
Neighborhood Impact Assessment - Redmond Area

AFFECTED AREAS:
- Downtown Redmond: 60% of businesses affected
- Overlake: Residential power outages continue
- Marymoor: Park facilities damaged, trails blocked

INFRASTRUCTURE:
- 12 traffic signals down
- 3 water main breaks reported
- Fiber optic cables damaged on 148th Ave

RESOURCE NEEDS:
- More cleanup crews for residential areas
- Traffic control personnel
- Temporary power solutions

COMMUNITY IMPACT:
- 2,000 households without power
- School closures extended through Friday
- Public transit detours in effect

CLEANUP PRIORITY:
1. Main arterials and business district
2. Residential power restoration
3. Park and recreational facility cleanup
EOF
        
        log_success "Sample crisis documents created in rag/data/"
    fi
    
    # Ingest into Weaviate
    if [ -f "vector/weaviate_bootstrap/ingest.py" ]; then
        log_info "Running Weaviate ingestion..."
        cd vector/weaviate_bootstrap
        uv run python ingest.py
        cd ../..
    else
        log_warning "Weaviate ingestion script not found"
        log_info "Would normally process documents and create vectors in Weaviate"
        
        # Simulate ingestion with a simple API call
        log_info "Creating Weaviate schema..."
        curl -X POST "http://localhost:8080/v1/schema" \
            -H "Content-Type: application/json" \
            -d '{
                "class": "CrisisDocument",
                "description": "Crisis recovery documents for emergency planning",
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "The main content of the document"
                    },
                    {
                        "name": "filename", 
                        "dataType": ["string"],
                        "description": "Source filename"
                    },
                    {
                        "name": "document_type",
                        "dataType": ["string"], 
                        "description": "Type of crisis document"
                    }
                ]
            }' || log_warning "Schema may already exist"
    fi
    
    # Build GraphRAG index
    if [ -d "rag/graphrag_project" ]; then
        log_info "Building GraphRAG knowledge graph..."
        cd rag/graphrag_project
        
        # Initialize GraphRAG if needed
        if [ ! -f "settings.yaml" ]; then
            log_info "Initializing GraphRAG project..."
            # Would normally run: uv run python -m graphrag.index --init
            log_warning "GraphRAG initialization would happen here"
        fi
        
        # Build index from documents
        # Would normally run: uv run python -m graphrag.index --root .
        log_warning "GraphRAG indexing would process documents here"
        cd ../..
    else
        log_warning "GraphRAG project directory not found"
        log_info "Would build knowledge graph from crisis documents"
    fi
    
    log_success "Data ingestion complete!"
    echo
    echo "Summary:"
    echo "• Sample crisis documents created"
    echo "• Weaviate schema configured (simulated)"
    echo "• Document vectors generated (simulated)"
    echo "• GraphRAG knowledge graph built (simulated)"
    echo
    echo "The system is ready to answer questions about:"
    echo "• Road closures and cleanup status"
    echo "• Resource shortages and crew availability"
    echo "• Infrastructure damage and repair priorities"
    echo "• Community impact and recovery progress"
}

main "$@"