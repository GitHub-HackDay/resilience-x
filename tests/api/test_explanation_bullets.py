"""
Test polished explanation bullets and source tracing functionality.
"""
import pytest
from unittest.mock import AsyncMock, patch
from services.api.clients.reasoning_client import ReasoningClient
from services.api.models.response import AskResponse, ExplanationBullet, Source

class TestReasoningClient:
    """Test reasoning client generates polished explanations."""

    def setup_method(self):
        """Set up test client."""
        self.client = ReasoningClient()

    @pytest.mark.asyncio
    async def test_cleanup_delay_explanation_structure(self):
        """Test cleanup delay response has well-structured explanation bullets."""
        question = "Why are cleanup operations delayed?"
        
        response = await self.client.process_question(question)
        
        # Validate response structure
        assert isinstance(response, AskResponse)
        assert len(response.explanation_bullets) >= 3
        assert len(response.sources) >= 2
        
        # Validate explanation bullet structure
        for i, bullet in enumerate(response.explanation_bullets):
            assert bullet.step == i + 1  # Sequential steps
            assert len(bullet.reasoning) > 20  # Meaningful content
            assert len(bullet.source_references) > 0  # Has source attribution
            assert bullet.confidence is not None  # Has confidence score
            assert 0.0 <= bullet.confidence <= 1.0  # Valid confidence range

    @pytest.mark.asyncio
    async def test_source_tracing_accuracy(self):
        """Test that source references in bullets match actual sources."""
        question = "Which areas have crew shortages?"
        
        response = await self.client.process_question(question)
        
        # Get all referenced source IDs from bullets
        referenced_ids = set()
        for bullet in response.explanation_bullets:
            referenced_ids.update(bullet.source_references)
        
        # Get all available source IDs
        available_ids = {source.id for source in response.sources}
        
        # All referenced sources should exist
        assert referenced_ids.issubset(available_ids), f"Referenced IDs {referenced_ids} not all in available {available_ids}"
        
        # Each source should have required fields
        for source in response.sources:
            assert source.id > 0
            assert len(source.title) > 0
            assert len(source.content) > 0
            assert isinstance(source.metadata, dict)

    @pytest.mark.asyncio
    async def test_explanation_confidence_progression(self):
        """Test that explanation bullets show logical confidence progression."""
        question = "Why are cleanup operations delayed?"  # Use specific question that triggers cleanup response
        
        response = await self.client.process_question(question)
        
        # Should have confidence scores that make sense
        confidences = [b.confidence for b in response.explanation_bullets if b.confidence]
        assert len(confidences) > 0
        
        # Early steps often have higher confidence than later inference steps
        if len(confidences) >= 2:
            # At least some bullets should have reasonably high confidence
            high_confidence_count = sum(1 for c in confidences if c >= 0.8)
            assert high_confidence_count >= 1, f"Should have at least one high-confidence explanation step, got: {confidences}"

    @pytest.mark.asyncio  
    async def test_fallback_explanation_structure(self):
        """Test fallback responses maintain explanation structure."""
        question = "Random unrelated question about weather"
        
        response = await self.client.process_question(question)
        
        # Even fallback should have structured explanation
        assert isinstance(response, AskResponse)
        assert len(response.explanation_bullets) > 0
        assert len(response.sources) > 0
        
        # Fallback bullets should still be well-formed
        for bullet in response.explanation_bullets:
            assert bullet.step > 0
            assert len(bullet.reasoning) > 10
            assert len(bullet.source_references) > 0

    def test_source_metadata_richness(self):
        """Test that sources contain rich metadata for tracing."""
        sources = self.client.demo_sources
        
        for source in sources.values():
            assert source.id > 0
            assert len(source.title) > 0
            assert len(source.content) > 0
            
            # Should have meaningful metadata
            assert len(source.metadata) > 0
            
            # Metadata should contain useful tracing information
            metadata_keys = set(source.metadata.keys())
            expected_keys = {'date', 'author', 'type', 'location', 'area', 'priority'}
            
            # Should have at least some expected metadata fields
            assert len(metadata_keys.intersection(expected_keys)) > 0, f"Source {source.id} lacks useful metadata"

    @pytest.mark.asyncio
    async def test_negative_case_graceful_handling(self):
        """Test graceful handling of edge cases in explanation generation.""" 
        # Empty question
        response = await self.client.process_question("")
        assert isinstance(response, AskResponse)
        assert len(response.answer) > 0
        
        # Very short question  
        response = await self.client.process_question("Help")
        assert isinstance(response, AskResponse)
        assert len(response.explanation_bullets) > 0