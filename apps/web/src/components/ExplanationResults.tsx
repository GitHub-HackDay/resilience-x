import { useState } from 'react';
import { AskResponse, AskRequest } from '@/types/api';

/**
 * Component for displaying polished explanation bullets with source tracing
 */
export default function ExplanationResults({ response }: { response: AskResponse }) {
  const [expandedSources, setExpandedSources] = useState<Set<number>>(new Set());

  const toggleSource = (sourceId: number) => {
    const newExpanded = new Set(expandedSources);
    if (newExpanded.has(sourceId)) {
      newExpanded.delete(sourceId);
    } else {
      newExpanded.add(sourceId);
    }
    setExpandedSources(newExpanded);
  };

  const getSourceById = (id: number) => {
    return response.sources.find(source => source.id === id);
  };

  const truncateText = (text: string, maxLength: number = 100) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const getConfidenceColor = (confidence?: number) => {
    if (!confidence) return 'text-gray-600';
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-orange-600';
  };

  const getConfidenceLabel = (confidence?: number) => {
    if (!confidence) return '';
    if (confidence >= 0.8) return 'High confidence';
    if (confidence >= 0.6) return 'Medium confidence';
    return 'Lower confidence';
  };

  return (
    <div className="explanation-results" role="region" aria-label="Question results">
      {/* Answer Section */}
      <div className="answer-section mb-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
        <h2 className="text-xl font-semibold text-blue-900 mb-2">Answer</h2>
        <p className="text-blue-800 text-lg">{response.answer}</p>
      </div>

      {/* Explanation Bullets Section */}
      <div className="explanation-section mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Why - Step by Step Reasoning</h2>
        <ol className="space-y-4" role="list">
          {response.explanation_bullets.map((bullet, index) => (
            <li 
              key={bullet.step} 
              className="explanation-bullet p-4 bg-white rounded-lg border border-gray-200 shadow-sm"
              role="listitem"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center mb-2">
                    <span 
                      className="inline-flex items-center justify-center w-8 h-8 bg-blue-100 text-blue-800 rounded-full font-semibold mr-3"
                      aria-label={`Step ${bullet.step}`}
                    >
                      {bullet.step}
                    </span>
                    {bullet.confidence && (
                      <span 
                        className={`text-sm font-medium ${getConfidenceColor(bullet.confidence)}`}
                        title={`${getConfidenceLabel(bullet.confidence)}: ${Math.round(bullet.confidence * 100)}%`}
                      >
                        {Math.round(bullet.confidence * 100)}% confidence
                      </span>
                    )}
                  </div>
                  <p className="text-gray-800 leading-relaxed ml-11">{bullet.reasoning}</p>
                  
                  {/* Source References */}
                  {bullet.source_references.length > 0 && (
                    <div className="ml-11 mt-3">
                      <p className="text-sm text-gray-600 mb-2">Supported by:</p>
                      <div className="flex flex-wrap gap-2">
                        {bullet.source_references.map(sourceId => {
                          const source = getSourceById(sourceId);
                          return source ? (
                            <button
                              key={sourceId}
                              onClick={() => toggleSource(sourceId)}
                              className="inline-flex items-center px-2 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm text-gray-700 border border-gray-300 transition-colors"
                              aria-expanded={expandedSources.has(sourceId)}
                              aria-controls={`source-${sourceId}`}
                            >
                              <span className="mr-1">📄</span>
                              {source.title}
                            </button>
                          ) : null;
                        })}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ol>
      </div>

      {/* Sources Section */}
      <div className="sources-section">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Sources</h2>
        <div className="space-y-4">
          {response.sources.map(source => (
            <div 
              key={source.id}
              id={`source-${source.id}`}
              className="source p-4 bg-gray-50 rounded-lg border border-gray-200"
              role="article"
              aria-labelledby={`source-title-${source.id}`}
            >
              <div className="flex items-start justify-between mb-2">
                <h3 
                  id={`source-title-${source.id}`}
                  className="font-semibold text-gray-900 flex items-center"
                >
                  <span className="inline-flex items-center justify-center w-6 h-6 bg-gray-600 text-white rounded-full text-sm font-medium mr-2">
                    {source.id}
                  </span>
                  {source.title}
                </h3>
                {source.url && (
                  <a 
                    href={source.url}
                    className="text-blue-600 hover:text-blue-800 text-sm underline"
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`View full document: ${source.title}`}
                  >
                    View Full Document
                  </a>
                )}
              </div>
              
              <div className="source-content">
                {expandedSources.has(source.id) ? (
                  <div>
                    <p className="text-gray-700 leading-relaxed mb-3">{source.content}</p>
                    <button
                      onClick={() => toggleSource(source.id)}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      aria-label="Show less"
                    >
                      Show Less
                    </button>
                  </div>
                ) : (
                  <div>
                    <p className="text-gray-700 leading-relaxed mb-3">
                      {truncateText(source.content)}
                    </p>
                    {source.content.length > 100 && (
                      <button
                        onClick={() => toggleSource(source.id)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                        aria-label="Show more of this source"
                      >
                        Show More
                      </button>
                    )}
                  </div>
                )}
              </div>

              {/* Source Metadata */}
              {Object.keys(source.metadata).length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <p className="text-xs text-gray-500 mb-1">Metadata:</p>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(source.metadata).map(([key, value]) => (
                      <span 
                        key={key}
                        className="inline-block px-2 py-1 bg-white rounded text-xs text-gray-600 border border-gray-300"
                      >
                        <span className="font-medium">{key}:</span> {String(value)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}