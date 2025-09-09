'use client';

import { useState } from 'react';
import { QueryForm } from '@/components/query-form';
import { ResultsSection } from '@/components/results-section';

interface QueryResult {
  answer: string;
  explanation_bullets: string[];
  sources: string[];
}

export default function Home() {
  const [result, setResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleQuery = async (question: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const data: QueryResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Resilience-X
          </h1>
          <p className="text-lg text-gray-600">
            AI-powered Q&A with multi-hop reasoning for crisis recovery
          </p>
        </header>

        <div className="space-y-8">
          <QueryForm 
            onSubmit={handleQuery} 
            loading={loading}
            disabled={loading}
          />
          
          <ResultsSection 
            result={result}
            loading={loading}
            error={error}
          />
        </div>
      </div>
    </main>
  );
}
