'use client';

import { useState } from 'react';

export interface QueryResult {
  answer: string;
  explanation_bullets: string[];
  sources: string[];
}

interface ResultsPanelProps {
  result: QueryResult | null;
  isLoading: boolean;
  error?: string;
}

export default function ResultsPanel({ result, isLoading, error }: ResultsPanelProps) {
  const [expandedSources, setExpandedSources] = useState<Set<number>>(new Set());

  const toggleSourceExpanded = (index: number) => {
    const newExpanded = new Set(expandedSources);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSources(newExpanded);
  };

  const truncateText = (text: string, maxLength: number = 200) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  if (error) {
    return (
      <div className="w-full max-w-4xl mx-auto">
        <div 
          role="alert" 
          className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"
        >
          <h3 className="text-lg font-medium text-red-800 dark:text-red-300 mb-2">
            Error
          </h3>
          <p className="text-red-700 dark:text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="w-full max-w-4xl mx-auto">
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 dark:bg-gray-600 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-600 rounded w-1/2"></div>
            <div className="h-4 bg-gray-200 dark:bg-gray-600 rounded w-5/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="w-full max-w-4xl mx-auto text-center py-8">
        <p className="text-gray-500 dark:text-gray-400 text-lg">
          Ask a question to get started with your recovery analysis.
        </p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Answer Section */}
      <section 
        aria-labelledby="answer-heading"
        className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6"
      >
        <h2 id="answer-heading" className="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-3">
          Answer
        </h2>
        <p className="text-blue-800 dark:text-blue-200 text-lg leading-relaxed">
          {result.answer}
        </p>
      </section>

      {/* Explanation Section */}
      {result.explanation_bullets && result.explanation_bullets.length > 0 && (
        <section 
          aria-labelledby="explanation-heading"
          className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6"
        >
          <h2 id="explanation-heading" className="text-xl font-semibold text-yellow-900 dark:text-yellow-100 mb-3">
            Why
          </h2>
          <ul className="space-y-2" role="list">
            {result.explanation_bullets.map((bullet, index) => (
              <li 
                key={index}
                className="flex items-start gap-3 text-yellow-800 dark:text-yellow-200"
              >
                <span className="flex-shrink-0 w-2 h-2 bg-yellow-600 dark:bg-yellow-400 rounded-full mt-2"></span>
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Sources Section */}
      {result.sources && result.sources.length > 0 && (
        <section 
          aria-labelledby="sources-heading"
          className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6"
        >
          <h2 id="sources-heading" className="text-xl font-semibold text-green-900 dark:text-green-100 mb-3">
            Sources
          </h2>
          <div className="space-y-3">
            {result.sources.map((source, index) => {
              const isExpanded = expandedSources.has(index);
              const shouldTruncate = source.length > 200;
              
              return (
                <div key={index} className="bg-white dark:bg-gray-800 border border-green-200 dark:border-green-700 rounded p-4">
                  <p className="text-green-800 dark:text-green-200 mb-2">
                    {isExpanded || !shouldTruncate ? source : truncateText(source)}
                  </p>
                  {shouldTruncate && (
                    <button
                      onClick={() => toggleSourceExpanded(index)}
                      className="text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-200 
                                 text-sm font-medium focus:outline-none focus:underline"
                      aria-expanded={isExpanded}
                      aria-controls={`source-${index}`}
                    >
                      {isExpanded ? 'Show less' : 'Show more'}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
}