/**
 * Resilience-X Main Page Component
 * Single page application for crisis Q&A with accessibility-first design
 */
'use client';

import { useState, useRef } from 'react';

interface ApiResponse {
  answer: string;
  explanation_bullets: string[];
  sources: string[];
}

interface ErrorState {
  message: string;
  type: 'network' | 'server' | 'validation';
}

export default function Home(): JSX.Element {
  const [question, setQuestion] = useState<string>('');
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<ErrorState | null>(null);
  const [expandedSources, setExpandedSources] = useState<Set<number>>(new Set());
  
  const questionInputRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError({
        message: 'Please enter a question.',
        type: 'validation'
      });
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data: ApiResponse = await res.json();
      setResponse(data);
    } catch (err) {
      console.error('Error asking question:', err);
      
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError({
          message: 'Unable to connect to the service. Please check if the API is running.',
          type: 'network'
        });
      } else {
        setError({
          message: 'An error occurred while processing your question. Please try again.',
          type: 'server'
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const toggleSourceExpansion = (index: number): void => {
    const newExpanded = new Set(expandedSources);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSources(newExpanded);
  };

  const truncateText = (text: string, limit: number = 100): string => {
    return text.length > limit ? text.substring(0, limit) + '...' : text;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Resilience-X
          </h1>
          <p className="text-lg text-gray-600">
            AI-powered crisis recovery Q&A with explainable reasoning
          </p>
        </div>

        {/* Question Input Form */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="mb-4">
            <label 
              htmlFor="question-input" 
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Ask a question about crisis recovery:
            </label>
            <textarea
              id="question-input"
              ref={questionInputRef}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., Which neighborhoods are facing cleanup delays?"
              className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical min-h-[100px]"
              rows={3}
              disabled={loading}
              aria-describedby="question-help"
            />
            <div id="question-help" className="mt-1 text-sm text-gray-500">
              Ask about recovery status, bottlenecks, resource allocation, or timeline concerns.
            </div>
          </div>
          
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : (
              'Ask Question'
            )}
          </button>
        </form>

        {/* Error Display */}
        {error && (
          <div 
            role="alert" 
            className="mb-6 p-4 border border-red-300 rounded-md bg-red-50"
            aria-live="polite"
          >
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error.message}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {response && (
          <div className="bg-white rounded-lg shadow-md p-6">
            {/* Answer Section */}
            <section className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-3">Answer</h2>
              <div 
                className="text-gray-700 leading-relaxed"
                role="region"
                aria-label="Answer to your question"
              >
                {response.answer}
              </div>
            </section>

            {/* Explanation Section */}
            {response.explanation_bullets.length > 0 && (
              <section className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-3">Why</h2>
                <ul 
                  className="space-y-2"
                  role="list"
                  aria-label="Explanation steps"
                >
                  {response.explanation_bullets.map((bullet, index) => (
                    <li key={index} className="flex items-start">
                      <span className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3"></span>
                      <span className="text-gray-700">{bullet}</span>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {/* Sources Section */}
            {response.sources.length > 0 && (
              <section>
                <h2 className="text-xl font-semibold text-gray-900 mb-3">Sources</h2>
                <div 
                  className="space-y-2"
                  role="region"
                  aria-label="Source documents"
                >
                  {response.sources.map((source, index) => (
                    <div key={index} className="border border-gray-200 rounded p-3">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <p className="text-gray-700">
                            {expandedSources.has(index) 
                              ? source 
                              : truncateText(source)
                            }
                          </p>
                        </div>
                        {source.length > 100 && (
                          <button
                            onClick={() => toggleSourceExpansion(index)}
                            className="ml-2 text-blue-600 hover:text-blue-800 text-sm font-medium focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded"
                            aria-expanded={expandedSources.has(index)}
                            aria-label={
                              expandedSources.has(index) 
                                ? `Collapse source ${index + 1}` 
                                : `Expand source ${index + 1}`
                            }
                          >
                            {expandedSources.has(index) ? 'Show less' : 'Show more'}
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </div>
        )}
      </main>
    </div>
  );
}