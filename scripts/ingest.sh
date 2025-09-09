#!/bin/bash

# Resilience-X Data Ingestion Script
# Ingests crisis documents into Weaviate vector database

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔄 Starting data ingestion for Resilience-X..."

# Check if Weaviate is running
echo "📡 Checking Weaviate connection..."
if ! curl -s http://localhost:8080/v1/.well-known/ready > /dev/null; then
    echo "❌ Weaviate is not running. Please start it first with:"
    echo "   docker compose up -d weaviate"
    exit 1
fi

echo "✅ Weaviate is running"

# Check if data directory exists
DATA_DIR="$REPO_ROOT/rag/data"
if [ ! -d "$DATA_DIR" ]; then
    echo "📁 Creating sample data directory structure..."
    mkdir -p "$DATA_DIR"
    
    # Create sample crisis documents for demo
    cat > "$DATA_DIR/crisis_report_001.txt" << 'EOF'
Crisis Report #001: King County Infrastructure Assessment
Date: March 15, 2024

Road Conditions:
- Highway 520 bridge: Closed due to structural damage from recent storms
- I-90 eastbound: Single lane closure near Mercer Island
- Local roads in Redmond: Multiple potholes and debris blocking lanes

Cleanup Status:
- Debris removal crews are short-staffed due to illness
- Heavy equipment delayed due to supply chain issues
- Estimated cleanup completion: 5-7 days

Priority Areas:
- Hospital access routes (Highway 520 corridor)
- School zone safety (Redmond elementary districts)
EOF

    cat > "$DATA_DIR/crisis_report_002.txt" << 'EOF'
Crisis Report #002: Utility Infrastructure Status
Date: March 16, 2024

Power Grid:
- 15% of King County still without power
- Priority restoration: Hospitals and emergency services
- Estimated full restoration: 3-4 days

Water Systems:
- Main water line break in Bellevue affects 2,000 residents  
- Temporary water stations established at community centers
- Repair crews working around the clock

Communication:
- Cell tower damage in rural areas causing connectivity issues
- Emergency radio systems operational
- Backup communication systems deployed
EOF

    cat > "$DATA_DIR/crisis_report_003.txt" << 'EOF'
Crisis Report #003: Community Response Update
Date: March 17, 2024

Shelter Operations:
- 3 emergency shelters operational in King County
- 150 displaced residents currently housed
- Adequate supplies for 5 days

Volunteer Coordination:
- 200+ volunteers registered for cleanup efforts  
- Medical volunteers supporting triage centers
- Food distribution coordinated through local churches

Resource Needs:
- Additional cleanup equipment required
- Medical supplies running low at triage centers
- Transportation assistance needed for elderly residents
EOF

    echo "📄 Created sample crisis documents"
fi

# Check if bootstrap script exists
BOOTSTRAP_DIR="$REPO_ROOT/vector/weaviate_bootstrap"
if [ ! -d "$BOOTSTRAP_DIR" ]; then
    echo "📁 Creating Weaviate bootstrap structure..."
    mkdir -p "$BOOTSTRAP_DIR"
    
    # Create basic Python ingestion script
    cat > "$BOOTSTRAP_DIR/ingest_documents.py" << 'EOF'
#!/usr/bin/env python3
"""
Simple document ingestion script for Resilience-X demo.
Loads crisis documents into Weaviate vector database.
"""

import os
import sys
import json
from pathlib import Path
import weaviate
from sentence_transformers import SentenceTransformer

def create_schema(client):
    """Create Weaviate schema for crisis documents."""
    schema = {
        "classes": [
            {
                "class": "CrisisDocument",
                "description": "Crisis and disaster recovery documents",
                "vectorizer": "none",  # We'll provide our own vectors
                "properties": [
                    {
                        "name": "title",
                        "dataType": ["text"],
                        "description": "Document title"
                    },
                    {
                        "name": "content",
                        "dataType": ["text"], 
                        "description": "Full document content"
                    },
                    {
                        "name": "source_file",
                        "dataType": ["text"],
                        "description": "Source filename"
                    },
                    {
                        "name": "date",
                        "dataType": ["text"],
                        "description": "Document date"
                    }
                ]
            }
        ]
    }
    
    # Delete existing schema if it exists
    try:
        client.schema.delete_class("CrisisDocument")
        print("🗑️ Deleted existing schema")
    except:
        pass
    
    client.schema.create(schema)
    print("✅ Created schema")

def ingest_documents(client, data_dir, model):
    """Ingest documents from data directory."""
    data_path = Path(data_dir)
    
    for file_path in data_path.glob("*.txt"):
        print(f"📄 Processing {file_path.name}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from first line or use filename
        lines = content.strip().split('\n')
        title = lines[0] if lines else file_path.stem
        
        # Generate embedding
        embedding = model.encode([content])[0]
        
        # Create document object
        doc_obj = {
            "title": title,
            "content": content,
            "source_file": file_path.name,
            "date": "2024-03-15"  # Default date for demo
        }
        
        # Add to Weaviate with vector
        client.data_object.create(
            data_object=doc_obj,
            class_name="CrisisDocument",
            vector=embedding
        )
        
        print(f"✅ Ingested {file_path.name}")

def main():
    repo_root = Path(__file__).parent.parent.parent
    data_dir = repo_root / "rag" / "data"
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        sys.exit(1)
    
    try:
        # Connect to Weaviate
        client = weaviate.Client("http://localhost:8080")
        
        # Test connection
        if not client.is_ready():
            print("❌ Cannot connect to Weaviate")
            sys.exit(1)
        
        print("✅ Connected to Weaviate")
        
        # Load sentence transformer model
        print("🤖 Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create schema and ingest documents
        create_schema(client)
        ingest_documents(client, data_dir, model)
        
        # Verify ingestion
        result = client.query.aggregate("CrisisDocument").with_meta_count().do()
        count = result['data']['Aggregate']['CrisisDocument'][0]['meta']['count']
        print(f"🎉 Successfully ingested {count} documents")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

    chmod +x "$BOOTSTRAP_DIR/ingest_documents.py"
    echo "📄 Created ingestion script"
fi

# Run the ingestion
echo "🚀 Running document ingestion..."
cd "$BOOTSTRAP_DIR"

# Check if required Python packages are available
python3 -c "import weaviate, sentence_transformers" 2>/dev/null || {
    echo "📦 Installing required Python packages..."
    pip3 install weaviate-client sentence-transformers --user --quiet
}

python3 ingest_documents.py

echo "🎉 Data ingestion completed successfully!"