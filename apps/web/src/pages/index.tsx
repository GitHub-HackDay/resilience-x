import { useState } from 'react';
import Head from 'next/head';
import QuestionInput from '@/components/QuestionInput';
import ExplanationResults from '@/components/ExplanationResults';
import { AskResponse, AskRequest } from '@/types/api';

/**
 * Main page for Resilience-X with polished explanation display
 */
export default function HomePage() {
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAskQuestion = async (question: string) => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const requestBody: AskRequest = { question };
      
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!res.ok) {
        throw new Error(`Failed to get answer: ${res.status} ${res.statusText}`);
      }

      const data: AskResponse = await res.json();
      setResponse(data);
    } catch (err) {
      console.error('Error asking question:', err);
      setError(err instanceof Error ? err.message : 'Failed to process question');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Resilience-X - Crisis Recovery Q&A</title>
        <meta name="description" content="AI-powered Q&A for post-disaster recovery with explained answers and source tracing" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gray-100 py-8 px-4">
        <div className="max-w-4xl mx-auto">
          <QuestionInput 
            onSubmit={handleAskQuestion}
            loading={loading}
          />

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg" role="alert">
              <h3 className="text-red-800 font-semibold mb-1">Error</h3>
              <p className="text-red-700">{error}</p>
              <p className="text-red-600 text-sm mt-2">
                Make sure the API server is running at http://localhost:8000
              </p>
            </div>
          )}

          {loading && (
            <div className="mb-6 p-6 bg-white rounded-lg border border-gray-200 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent mx-auto mb-4"></div>
              <p className="text-gray-600">Processing your question and generating explanation...</p>
            </div>
          )}

          {response && !loading && (
            <ExplanationResults response={response} />
          )}

          {!response && !loading && !error && (
            <div className="text-center py-12">
              <div className="mx-auto w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center mb-4">
                <span className="text-4xl">🤔</span>
              </div>
              <p className="text-gray-600 text-lg">
                Ask a question about recovery operations to see explained answers with sources
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}