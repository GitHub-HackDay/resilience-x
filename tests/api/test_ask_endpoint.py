"""
Test API endpoint for polished explanation bullets and source tracing.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from services.api.main import app
from services.api.models.response import AskResponse, ExplanationBullet, Source

client = TestClient(app)

class TestAskEndpoint:
    """Test /ask endpoint returns polished explanations."""

    def test_ask_endpoint_happy_path(self):
        """Test successful request returns well-formatted explanation."""
        request_data = {"question": "Why are cleanup operations delayed?"}
        
        response = client.post("/ask", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure matches AskResponse model
        assert "answer" in data
        assert "explanation_bullets" in data  
        assert "sources" in data
        
        # Validate explanation bullets structure
        bullets = data["explanation_bullets"]
        assert len(bullets) > 0
        
        for bullet in bullets:
            assert "step" in bullet
            assert "reasoning" in bullet
            assert "source_references" in bullet
            assert isinstance(bullet["source_references"], list)
            assert len(bullet["source_references"]) > 0
            
        # Validate sources structure
        sources = data["sources"]
        assert len(sources) > 0
        
        for source in sources:
            assert "id" in source
            assert "title" in source
            assert "content" in source
            assert "metadata" in source

    def test_ask_endpoint_source_reference_integrity(self):
        """Test that source references in bullets point to valid sources."""
        request_data = {"question": "Which roads are blocked?"}
        
        response = client.post("/ask", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Collect all source IDs
        source_ids = {source["id"] for source in data["sources"]}
        
        # Check all bullet references are valid
        for bullet in data["explanation_bullets"]:
            for ref_id in bullet["source_references"]:
                assert ref_id in source_ids, f"Bullet references non-existent source {ref_id}"

    def test_ask_endpoint_confidence_scores(self):
        """Test that confidence scores are properly included and valid."""
        request_data = {"question": "What crew shortages exist?"}
        
        response = client.post("/ask", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check confidence scores where present
        for bullet in data["explanation_bullets"]:
            if "confidence" in bullet and bullet["confidence"] is not None:
                confidence = bullet["confidence"]
                assert 0.0 <= confidence <= 1.0, f"Invalid confidence score: {confidence}"

    def test_ask_endpoint_empty_question(self):
        """Test handling of empty question."""
        request_data = {"question": ""}
        
        response = client.post("/ask", json=request_data)
        
        # Should still return valid structure
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "explanation_bullets" in data
        assert "sources" in data

    def test_ask_endpoint_malformed_request(self):
        """Test handling of malformed requests.""" 
        # Missing question field
        response = client.post("/ask", json={})
        assert response.status_code == 422  # Validation error
        
        # Invalid JSON
        response = client.post("/ask", data="invalid json")
        assert response.status_code == 422

    @patch('services.api.clients.reasoning_client.ReasoningClient.process_question')
    def test_ask_endpoint_error_handling(self, mock_process):
        """Test graceful error handling with structured fallback."""
        # Mock an exception during processing
        mock_process.side_effect = Exception("Simulated error")
        
        request_data = {"question": "Test question"}
        response = client.post("/ask", json=request_data)
        
        assert response.status_code == 200  # Should not fail completely
        data = response.json()
        
        # Should return structured fallback response
        assert "answer" in data
        assert "explanation_bullets" in data
        assert "sources" in data
        assert len(data["explanation_bullets"]) > 0
        assert len(data["sources"]) > 0
        
        # Fallback explanation should mention the error
        assert "technical difficulties" in data["answer"].lower() or "error" in data["answer"].lower()

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data