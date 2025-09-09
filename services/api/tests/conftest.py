"""
Test configuration and fixtures for Resilience-X API tests.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app
from clients.weaviate_client import RetrievedDocument


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
        RetrievedDocument(
            content="Road cleanup in King County is delayed due to crew shortages and equipment issues.",
            source="Report_A_20241201.pdf",
            score=0.85,
            metadata={"title": "King County Status Update", "date": "2024-12-01"}
        ),
        RetrievedDocument(
            content="Debris overflow reported in multiple neighborhoods requiring additional resources.",
            source="Report_B_20241202.pdf", 
            score=0.72,
            metadata={"title": "Debris Management Report", "date": "2024-12-02"}
        )
    ]


@pytest.fixture
def mock_weaviate_client():
    """Mock Weaviate client for testing."""
    with patch('main.weaviate_client') as mock_client:
        mock_client._client = Mock()
        yield mock_client