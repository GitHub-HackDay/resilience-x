'use client';

import { useState, FormEvent } from 'react';

interface QueryFormProps {
  onSubmit: (question: string) => void;
  loading: boolean;
  disabled: boolean;
}

export function QueryForm({ onSubmit, loading, disabled }: QueryFormProps) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (question.trim() && !disabled) {
      onSubmit(question.trim());
    }
  };

  return (
    <section className="bg-white rounded-lg shadow-md p-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label 
            htmlFor="question-input" 
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Ask a question about crisis recovery:
          </label>
          <textarea
            id="question-input"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., What are the key steps for business continuity after a disaster?"
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-32"
            disabled={disabled}
            aria-describedby="question-help"
          />
          <p id="question-help" className="mt-2 text-sm text-gray-500">
            Enter your question and we&apos;ll provide an answer with explanations and sources.
          </p>
        </div>
        
        <button
          type="submit"
          disabled={disabled || !question.trim()}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-6 rounded-lg transition-colors focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          aria-describedby="submit-status"
        >
          {loading ? 'Searching...' : 'Ask Question'}
        </button>
        
        {loading && (
          <div 
            id="submit-status" 
            className="text-sm text-gray-600 text-center"
            role="status" 
            aria-live="polite"
          >
            Processing your question...
          </div>
        )}
      </form>
    </section>
  );
}