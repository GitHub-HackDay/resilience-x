'use client';

import { useState } from 'react';

interface QueryResult {
  answer: string;
  explanation_bullets: string[];
  sources: string[];
}

interface ResultsSectionProps {
  result: QueryResult | null;
  loading: boolean;
  error: string | null;
}

export function ResultsSection({ result, loading, error }: ResultsSectionProps) {
  if (loading) {
    return (
      <section 
        className="bg-white rounded-lg shadow-md p-6"
        role="status"
        aria-live="polite"
      >
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <p className="text-sm text-gray-600 mt-4">Loading results...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section 
        className="bg-red-50 border border-red-200 rounded-lg p-6"
        role="alert"
      >
        <h2 className="text-lg font-semibold text-red-800 mb-2">Error</h2>
        <p className="text-red-700">{error}</p>
        <p className="text-sm text-red-600 mt-2">
          Please check that the backend service is running and try again.
        </p>
      </section>
    );
  }

  if (!result) {
    return (
      <section className="bg-gray-50 rounded-lg p-8 text-center">
        <p className="text-gray-600">
          Ask a question above to get started with AI-powered crisis recovery insights.
        </p>
      </section>
    );
  }

  return (
    <section className="space-y-6" role="region" aria-label="Query results">
      {/* Answer Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Answer</h2>
        <div className="prose max-w-none">
          <p className="text-gray-800 leading-relaxed">{result.answer}</p>
        </div>
      </div>

      {/* Explanation Section */}
      {result.explanation_bullets.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Why</h2>
          <ul 
            className="space-y-2" 
            role="list"
            aria-label="Explanation steps"
          >
            {result.explanation_bullets.map((bullet, index) => (
              <li 
                key={index}
                className="flex items-start space-x-2"
              >
                <span 
                  className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"
                  aria-hidden="true"
                />
                <span className="text-gray-700">{bullet}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Sources Section */}
      {result.sources.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Sources</h2>
          <SourcesList sources={result.sources} />
        </div>
      )}
    </section>
  );
}

interface SourcesListProps {
  sources: string[];
}

function SourcesList({ sources }: SourcesListProps) {
  const [expandedSources, setExpandedSources] = useState<Set<number>>(new Set());

  const toggleSource = (index: number) => {
    const newExpanded = new Set(expandedSources);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSources(newExpanded);
  };

  return (
    <div className="space-y-3" role="list" aria-label="Source documents">
      {sources.map((source, index) => {
        const isExpanded = expandedSources.has(index);
        const shouldTruncate = source.length > 200;
        const displayText = shouldTruncate && !isExpanded 
          ? source.substring(0, 200) + '...' 
          : source;

        return (
          <div 
            key={index} 
            className="border border-gray-200 rounded-lg p-4"
            role="listitem"
          >
            <div className="flex items-start justify-between">
              <span className="text-sm font-medium text-gray-500 mb-2 block">
                Source {index + 1}
              </span>
            </div>
            
            <p className="text-gray-700 text-sm leading-relaxed mb-2">
              {displayText}
            </p>

            {shouldTruncate && (
              <button
                onClick={() => toggleSource(index)}
                className="text-blue-600 hover:text-blue-800 text-sm font-medium focus:outline-none focus:underline"
                aria-expanded={isExpanded}
                aria-controls={`source-${index}-content`}
              >
                {isExpanded ? 'Show less' : 'Show more'}
              </button>
            )}
          </div>
        );
      })}
    </div>
  );
}