"""
Weaviate schema and data loader for crisis documents.
"""

import weaviate
import os
import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class WeaviateBootstrap:
    """Bootstrap Weaviate with schema and sample crisis data."""
    
    def __init__(self):
        """Initialize Weaviate client."""
        self.url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.client = weaviate.Client(url=self.url)
        
    def create_schema(self):
        """Create the schema for crisis documents."""
        schema = {
            "classes": [
                {
                    "class": "CrisisDocument",
                    "description": "A crisis recovery document or report",
                    "properties": [
                        {
                            "name": "content",
                            "dataType": ["text"],
                            "description": "The document content"
                        },
                        {
                            "name": "title",
                            "dataType": ["string"],
                            "description": "Document title"
                        },
                        {
                            "name": "source",
                            "dataType": ["string"],
                            "description": "Document source or author"
                        },
                        {
                            "name": "document_type",
                            "dataType": ["string"],
                            "description": "Type of document (report, assessment, etc.)"
                        }
                    ],
                    "vectorizer": "text2vec-openai"
                }
            ]
        }
        
        try:
            self.client.schema.create(schema)
            logger.info("Schema created successfully")
        except Exception as e:
            logger.warning(f"Schema creation warning: {str(e)}")
            
    def load_sample_data(self):
        """Load sample crisis documents."""
        sample_docs = [
            {
                "content": "Cleanup crews are experiencing severe staffing shortages across King County. Current crew availability is at 60% of normal capacity due to illness and equipment failures. Priority areas include Redmond, Bellevue, and Kirkland neighborhoods.",
                "title": "Emergency Operations Status Report A",
                "source": "King County Emergency Management",
                "document_type": "status_report"
            },
            {
                "content": "Main debris collection sites have reached maximum capacity. Overflow conditions observed at Redmond Collection Center and Bellevue Staging Area. Additional temporary sites needed to prevent further delays in residential cleanup operations.",
                "title": "Field Assessment Report B - Collection Site Capacity",
                "source": "Field Operations Team",
                "document_type": "field_assessment"
            },
            {
                "content": "Heavy rainfall from Nov 15-17 has significantly impacted equipment deployment schedules. Road access to affected neighborhoods limited due to flooding. Estimated 3-day delay in equipment mobilization for debris removal operations.",
                "title": "Weather Impact Assessment C",
                "source": "Operations Planning Division", 
                "document_type": "impact_assessment"
            }
        ]
        
        try:
            for doc in sample_docs:
                self.client.data_object.create(
                    data_object=doc,
                    class_name="CrisisDocument"
                )
            logger.info(f"Loaded {len(sample_docs)} sample documents")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")


if __name__ == "__main__":
    bootstrap = WeaviateBootstrap()
    bootstrap.create_schema()
    bootstrap.load_sample_data()