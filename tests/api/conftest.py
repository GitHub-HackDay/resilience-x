"""
Test configuration and fixtures for API tests.
"""
import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

@pytest.fixture
def sample_ask_response():
    """Sample AskResponse for testing."""
    from services.api.models.response import AskResponse, ExplanationBullet, Source
    
    return AskResponse(
        answer="Sample answer for testing",
        explanation_bullets=[
            ExplanationBullet(
                step=1,
                reasoning="First reasoning step",
                source_references=[1],
                confidence=0.9
            ),
            ExplanationBullet(
                step=2,
                reasoning="Second reasoning step",
                source_references=[1, 2],
                confidence=0.8
            )
        ],
        sources=[
            Source(
                id=1,
                title="Test Source 1",
                content="Content of test source 1",
                metadata={"type": "test", "date": "2024-01-01"}
            ),
            Source(
                id=2,
                title="Test Source 2", 
                content="Content of test source 2",
                metadata={"type": "test", "date": "2024-01-02"}
            )
        ]
    )