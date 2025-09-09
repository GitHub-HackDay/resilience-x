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
