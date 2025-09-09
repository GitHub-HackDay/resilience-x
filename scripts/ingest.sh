#!/bin/bash
# Ingestion script for Resilience-X demo data
# This script sets up sample crisis recovery documents in Weaviate

set -e

echo "🚀 Starting Resilience-X ingestion process..."

# Check if Weaviate is running
echo "⏳ Checking Weaviate availability..."
if ! curl -s http://localhost:8080/v1/meta > /dev/null; then
    echo "❌ Weaviate is not running at localhost:8080"
    echo "💡 Start it with: docker compose up -d weaviate"
    exit 1
fi

echo "✅ Weaviate is running"

# Install dependencies if needed
echo "📦 Installing dependencies..."
cd services/api
if command -v uv >/dev/null 2>&1; then
    uv sync
else
    pip install -e .
fi

# Create sample data if it doesn't exist
echo "📄 Creating sample crisis documents..."
mkdir -p ../../rag/data

cat > ../../rag/data/king_county_report.txt << 'EOF'
KING COUNTY EMERGENCY OPERATIONS STATUS REPORT
Date: December 1, 2024

SITUATION OVERVIEW:
Road cleanup operations in King County are experiencing significant delays due to crew shortages and equipment maintenance issues. Primary affected areas include Interstate 405 corridor and State Route 520.

RESOURCE STATUS:
- Cleanup crews: 40% below normal staffing
- Heavy machinery: 3 excavators offline for repairs
- Estimated completion: 5-7 additional days

PRIORITIES:
1. Restore I-405 northbound lanes (highest priority)
2. Clear debris from residential access roads
3. Coordinate with utility companies for power restoration
EOF

cat > ../../rag/data/debris_management_report.txt << 'EOF'
DEBRIS MANAGEMENT SITUATION REPORT
Date: December 2, 2024

OVERFLOW CONDITIONS:
Multiple neighborhoods in King County are reporting debris overflow at collection points. The situation requires immediate attention and additional resources.

AFFECTED AREAS:
- Redmond: Marymoor Park staging area at 95% capacity
- Bellevue: Crossroads Community Center staging full
- Kirkland: Juanita Beach Park collection point overwhelmed

RESOURCE NEEDS:
- Additional dump trucks (minimum 6 units)
- Extended collection hours (16-hour shifts)
- Temporary staging locations for overflow

ACTION ITEMS:
1. Deploy emergency debris removal contractors
2. Establish overflow staging at King County Fairgrounds
3. Coordinate with neighboring counties for disposal capacity
EOF

cat > ../../rag/data/utility_restoration_update.txt << 'EOF'
UTILITY RESTORATION STATUS UPDATE
Date: December 3, 2024

POWER OUTAGES:
Approximately 12,000 customers remain without power across King County. Priority restoration efforts are focused on critical infrastructure and residential areas with vulnerable populations.

AFFECTED ZONES:
- Zone A (Redmond/Kirkland): 4,500 customers
- Zone B (Bellevue/Mercer Island): 3,200 customers  
- Zone C (Rural King County): 4,300 customers

RESTORATION TIMELINE:
- Critical facilities: 48 hours (hospitals, emergency services)
- Residential areas: 72-96 hours
- Rural/remote areas: 96-120 hours

COORDINATION:
Working closely with road cleanup teams to ensure safe access for utility crews. Some restoration work dependent on debris removal completion.
EOF

echo "📚 Sample documents created in rag/data/"

# Simple Python script to ingest documents into Weaviate
cat > ingest_data.py << 'EOF'
"""Simple script to ingest sample documents into Weaviate."""
import os
import sys
sys.path.append('.')

from clients.weaviate_client import weaviate_client

def ingest_documents():
    """Ingest sample documents into Weaviate."""
    print("🔗 Connecting to Weaviate...")
    if not weaviate_client.connect():
        print("❌ Failed to connect to Weaviate")
        return False
    
    # Create schema
    print("🏗️  Creating schema...")
    weaviate_client.create_schema_if_not_exists()
    
    # Load and ingest documents
    data_dir = "../../rag/data"
    documents_collection = weaviate_client._client.collections.get("Document")
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_dir, filename)
            print(f"📄 Processing {filename}...")
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Extract title from first line or use filename
            lines = content.split('\n')
            title = lines[0] if lines else filename
            
            # Insert document
            documents_collection.data.insert({
                "content": content,
                "source": filename,
                "title": title
            })
            print(f"✅ Ingested {filename}")
    
    print("🎉 Ingestion complete!")
    weaviate_client.close()
    return True

if __name__ == "__main__":
    ingest_documents()
EOF

echo "🔄 Running ingestion..."
python ingest_data.py

echo "✅ Ingestion completed successfully!"
echo "💡 You can now test queries with: bash scripts/demo.sh"

# Cleanup temporary script
rm ingest_data.py