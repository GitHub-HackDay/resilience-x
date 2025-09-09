'use client';

import { useState } from 'react';
import QuestionInput from '@/components/QuestionInput';
import ResultsPanel, { QueryResult } from '@/components/ResultsPanel';

export default function Home() {
  const [result, setResult] = useState<QueryResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>(undefined);

  const handleQuestionSubmit = async (question: string) => {
    setIsLoading(true);
    setError(undefined);
    
    try {
      // For now, we'll simulate an API call with a mock response
      // This will be replaced with actual API call to /ask endpoint
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate network delay
      
      // Mock response for demonstration
      const mockResult: QueryResult = {
        answer: "Cleanup is delayed in several neighborhoods including King County due to multiple factors affecting recovery operations.",
        explanation_bullets: [
          "Crew shortages are limiting the number of cleanup teams available (Report A)",
          "Debris overflow has exceeded storage capacity at temporary sites (Report B)", 
          "Heavy equipment access is blocked by damaged infrastructure in some areas (Report C)"
        ],
        sources: [
          "Report A: Emergency Operations Center Daily Brief - Staffing levels are at 60% capacity due to personnel safety protocols and limited contractor availability.",
          "Report B: Waste Management Status Update - Temporary debris storage sites in King County have reached 85% capacity, requiring establishment of additional locations before cleanup can resume in affected zones.",
          "Report C: Infrastructure Assessment - Road damage on main arterials including Highway 99 and I-405 connector routes is preventing heavy equipment deployment to residential areas."
        ]
      };
      
      setResult(mockResult);
    } catch (err) {
      setError('Failed to get response. Please try again.');
      console.error('Error fetching result:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
              Resilience-X
            </h1>
            <p className="mt-2 text-lg text-gray-600 dark:text-gray-400">
              AI-powered Q&A for post-disaster recovery planning
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          <QuestionInput 
            onSubmit={handleQuestionSubmit}
            isLoading={isLoading}
          />
          
          <ResultsPanel 
            result={result}
            isLoading={isLoading}
            error={error}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500 dark:text-gray-400">
            Built with GitHub Copilot, GraphRAG, NLWeb, and Weaviate
          </p>
        </div>
      </footer>
    </div>
  );
}
