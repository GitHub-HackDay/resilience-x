import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ExplanationResults from '@/components/ExplanationResults';
import { AskResponse } from '@/types/api';

const mockResponse: AskResponse = {
  answer: "Cleanup is delayed in King County due to crew shortages and debris overflow.",
  explanation_bullets: [
    {
      step: 1,
      reasoning: "King County is currently experiencing active cleanup operations with identified bottlenecks",
      source_references: [1, 2],
      confidence: 0.95
    },
    {
      step: 2,
      reasoning: "Crew availability has been significantly reduced by 40% due to staff reassignments",
      source_references: [1],
      confidence: 0.9
    }
  ],
  sources: [
    {
      id: 1,
      title: "Emergency Operations Report - Day 3",
      content: "King County cleanup crews have been reduced by 40% due to reassignments to higher priority zones. Current staffing levels insufficient for planned debris removal timeline.",
      metadata: {
        date: "2024-01-15",
        author: "Emergency Coordination Center"
      },
      url: "/docs/emergency-ops-day3.pdf"
    },
    {
      id: 2,
      title: "Debris Collection Status Update",
      content: "Collection sites in King County have reached 85% capacity. Overflow conditions expected within 24-48 hours without additional disposal coordination.",
      metadata: {
        date: "2024-01-15",
        author: "Waste Management Division"
      }
    }
  ]
};

describe('ExplanationResults', () => {
  test('displays answer section with correct content', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    expect(screen.getByRole('region', { name: 'Question results' })).toBeInTheDocument();
    expect(screen.getByText('Answer')).toBeInTheDocument();
    expect(screen.getByText(mockResponse.answer)).toBeInTheDocument();
  });

  test('displays explanation bullets with step numbers and reasoning', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    expect(screen.getByText('Why - Step by Step Reasoning')).toBeInTheDocument();
    
    // Check step numbers are displayed
    expect(screen.getByLabelText('Step 1')).toBeInTheDocument();
    expect(screen.getByLabelText('Step 2')).toBeInTheDocument();
    
    // Check reasoning content
    expect(screen.getByText(/King County is currently experiencing active cleanup/)).toBeInTheDocument();
    expect(screen.getByText(/Crew availability has been significantly reduced/)).toBeInTheDocument();
  });

  test('displays confidence scores for explanation bullets', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    expect(screen.getByText('95% confidence')).toBeInTheDocument();
    expect(screen.getByText('90% confidence')).toBeInTheDocument();
  });

  test('displays source references for each bullet', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    // First bullet should reference both sources
    const firstBullet = screen.getByText(/King County is currently experiencing/).closest('.explanation-bullet');
    expect(firstBullet).toContainElement(screen.getByText('Emergency Operations Report - Day 3'));
    expect(firstBullet).toContainElement(screen.getByText('Debris Collection Status Update'));
  });

  test('displays sources section with all source information', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    expect(screen.getByText('Sources')).toBeInTheDocument();
    
    // Check source titles and metadata
    expect(screen.getByText('Emergency Operations Report - Day 3')).toBeInTheDocument();
    expect(screen.getByText('Debris Collection Status Update')).toBeInTheDocument();
    
    // Check metadata display
    expect(screen.getByText(/date:/)).toBeInTheDocument();
    expect(screen.getByText(/author:/)).toBeInTheDocument();
  });

  test('truncates long source content with show more button', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    // Should show truncated content initially
    const showMoreButtons = screen.getAllByText('Show More');
    expect(showMoreButtons.length).toBeGreaterThan(0);
    
    // Click show more to expand
    fireEvent.click(showMoreButtons[0]);
    
    // Should now show "Show Less" button
    expect(screen.getByText('Show Less')).toBeInTheDocument();
  });

  test('toggles source expansion correctly', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    const showMoreButton = screen.getAllByText('Show More')[0];
    fireEvent.click(showMoreButton);
    
    // Should show full content
    expect(screen.getByText(/King County cleanup crews have been reduced by 40%/)).toBeInTheDocument();
    
    // Click show less
    const showLessButton = screen.getByText('Show Less');
    fireEvent.click(showLessButton);
    
    // Should truncate again
    expect(screen.getByText('Show More')).toBeInTheDocument();
  });

  test('displays external source links when available', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    const externalLink = screen.getByText('View Full Document');
    expect(externalLink).toBeInTheDocument();
    expect(externalLink).toHaveAttribute('href', '/docs/emergency-ops-day3.pdf');
    expect(externalLink).toHaveAttribute('target', '_blank');
  });

  test('has proper accessibility attributes', () => {
    render(<ExplanationResults response={mockResponse} />);
    
    // Check ARIA labels and roles
    expect(screen.getByRole('region', { name: 'Question results' })).toBeInTheDocument();
    expect(screen.getByRole('list')).toBeInTheDocument();
    
    // Check list items
    const listItems = screen.getAllByRole('listitem');
    expect(listItems).toHaveLength(mockResponse.explanation_bullets.length);
    
    // Check articles for sources
    const articles = screen.getAllByRole('article');
    expect(articles).toHaveLength(mockResponse.sources.length);
  });

  test('handles empty response gracefully', () => {
    const emptyResponse: AskResponse = {
      answer: "No information available",
      explanation_bullets: [],
      sources: []
    };
    
    render(<ExplanationResults response={emptyResponse} />);
    
    expect(screen.getByText('No information available')).toBeInTheDocument();
    expect(screen.getByText('Why - Step by Step Reasoning')).toBeInTheDocument();
    expect(screen.getByText('Sources')).toBeInTheDocument();
  });
});