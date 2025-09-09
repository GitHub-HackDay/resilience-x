"""
Reasoning client that generates polished explanation bullets with source tracing.
"""
import asyncio
from typing import List, Dict, Any
import logging
from ..models.response import AskResponse, ExplanationBullet, Source

logger = logging.getLogger(__name__)

class ReasoningClient:
    """
    Client for generating structured reasoning with explanation bullets and source tracing.
    Focuses on clear, step-by-step explanations with proper source attribution.
    """
    
    def __init__(self):
        self.demo_sources = self._load_demo_sources()
    
    def _load_demo_sources(self) -> Dict[int, Source]:
        """Load demo sources for explanation and testing."""
        return {
            1: Source(
                id=1,
                title="Emergency Operations Report - Day 3",
                content="King County cleanup crews have been reduced by 40% due to reassignments to higher priority zones. Current staffing levels insufficient for planned debris removal timeline.",
                metadata={
                    "date": "2024-01-15",
                    "author": "Emergency Coordination Center",
                    "report_type": "operational_status",
                    "priority": "high"
                },
                url="/docs/emergency-ops-day3.pdf"
            ),
            2: Source(
                id=2,
                title="Debris Collection Status Update",
                content="Collection sites in King County have reached 85% capacity. Overflow conditions expected within 24-48 hours without additional disposal coordination.",
                metadata={
                    "date": "2024-01-15",
                    "author": "Waste Management Division",
                    "location": "King County",
                    "capacity_status": "critical"
                },
                url="/docs/debris-status-update.pdf"
            ),
            3: Source(
                id=3,
                title="Infrastructure Assessment - Roads",
                content="Secondary roads in Redmond area still blocked by fallen trees. Priority given to main arterials, secondary cleanup scheduled for later phases.",
                metadata={
                    "date": "2024-01-14",
                    "author": "Transportation Department",
                    "area": "Redmond",
                    "road_type": "secondary"
                },
                url="/docs/road-assessment.pdf"
            )
        }
    
    async def process_question(self, question: str) -> AskResponse:
        """
        Process question and generate polished explanation with source tracing.
        
        Args:
            question: User's question about recovery/crisis situation
            
        Returns:
            AskResponse with structured explanation bullets and sources
        """
        logger.info(f"Processing question for explanation generation")
        
        # Simulate processing delay for realistic behavior
        await asyncio.sleep(0.5)
        
        # Analyze question to determine response strategy
        question_lower = question.lower()
        
        if "cleanup" in question_lower and "delay" in question_lower:
            return self._generate_cleanup_delay_response()
        elif "road" in question_lower and "block" in question_lower:
            return self._generate_road_blockage_response()
        elif "crew" in question_lower or "staff" in question_lower:
            return self._generate_staffing_response()
        else:
            return self._generate_general_response(question)
    
    def _generate_cleanup_delay_response(self) -> AskResponse:
        """Generate response about cleanup delays with polished explanation bullets."""
        return AskResponse(
            answer="Cleanup is delayed in King County due to crew shortages and debris collection capacity issues.",
            explanation_bullets=[
                ExplanationBullet(
                    step=1,
                    reasoning="King County is currently experiencing active cleanup operations with identified bottlenecks",
                    source_references=[1, 2],
                    confidence=0.95
                ),
                ExplanationBullet(
                    step=2,
                    reasoning="Crew availability has been significantly reduced by 40% due to staff reassignments to higher priority emergency zones",
                    source_references=[1],
                    confidence=0.9
                ),
                ExplanationBullet(
                    step=3,
                    reasoning="Debris collection sites are approaching maximum capacity at 85%, creating additional processing delays",
                    source_references=[2],
                    confidence=0.85
                ),
                ExplanationBullet(
                    step=4,
                    reasoning="Combined impact of reduced staffing and limited collection capacity is extending cleanup timeline beyond original estimates",
                    source_references=[1, 2],
                    confidence=0.8
                )
            ],
            sources=[self.demo_sources[1], self.demo_sources[2]]
        )
    
    def _generate_road_blockage_response(self) -> AskResponse:
        """Generate response about road blockages with clear source tracing."""
        return AskResponse(
            answer="Secondary roads in Redmond remain blocked while priority is given to main arterials.",
            explanation_bullets=[
                ExplanationBullet(
                    step=1,
                    reasoning="Infrastructure assessment identified multiple road blockages in Redmond area requiring clearance",
                    source_references=[3],
                    confidence=0.9
                ),
                ExplanationBullet(
                    step=2,
                    reasoning="Transportation department has prioritized main arterial roads for immediate clearing to restore critical traffic flow",
                    source_references=[3],
                    confidence=0.85
                ),
                ExplanationBullet(
                    step=3,
                    reasoning="Secondary roads are scheduled for later cleanup phases due to resource constraints and priority allocation",
                    source_references=[3],
                    confidence=0.8
                )
            ],
            sources=[self.demo_sources[3]]
        )
    
    def _generate_staffing_response(self) -> AskResponse:
        """Generate response about staffing issues with detailed explanation."""
        return AskResponse(
            answer="Staff shortages are impacting operations due to reassignments to higher priority zones.",
            explanation_bullets=[
                ExplanationBullet(
                    step=1,
                    reasoning="Current staffing levels have been assessed as insufficient for planned operational timeline",
                    source_references=[1],
                    confidence=0.9
                ),
                ExplanationBullet(
                    step=2,
                    reasoning="40% reduction in cleanup crews resulted from strategic reassignments to address more critical emergency situations",
                    source_references=[1],
                    confidence=0.85
                )
            ],
            sources=[self.demo_sources[1]]
        )
    
    def _generate_general_response(self, question: str) -> AskResponse:
        """Generate general response with fallback explanation."""
        return AskResponse(
            answer=f"Based on available recovery data, multiple factors are affecting the situation you asked about.",
            explanation_bullets=[
                ExplanationBullet(
                    step=1,
                    reasoning="Analysis of current operational reports shows ongoing recovery efforts across multiple areas",
                    source_references=[1, 2, 3],
                    confidence=0.7
                ),
                ExplanationBullet(
                    step=2,
                    reasoning="Resource allocation and priority management are key factors influencing recovery timeline and effectiveness",
                    source_references=[1, 3],
                    confidence=0.6
                )
            ],
            sources=list(self.demo_sources.values())
        )