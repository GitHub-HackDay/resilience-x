'use client';

import { useState, FormEvent } from 'react';

interface QuestionInputProps {
  onSubmit: (question: string) => void;
  isLoading: boolean;
}

export default function QuestionInput({ onSubmit, isLoading }: QuestionInputProps) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (question.trim() && !isLoading) {
      onSubmit(question.trim());
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-8">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label 
            htmlFor="question-input" 
            className="block text-lg font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Ask about post-disaster recovery:
          </label>
          <div className="relative">
            <input
              id="question-input"
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., Which neighborhoods are facing cleanup delays?"
              className="w-full px-4 py-3 text-lg border border-gray-300 dark:border-gray-600 rounded-lg 
                         bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100
                         focus:ring-2 focus:ring-blue-500 focus:border-transparent
                         disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading}
              required
              minLength={3}
              maxLength={500}
            />
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              {isLoading && (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>
              )}
            </div>
          </div>
        </div>
        <button
          type="submit"
          disabled={!question.trim() || isLoading}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 
                     text-white font-medium rounded-lg transition-colors
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                     disabled:cursor-not-allowed"
        >
          {isLoading ? 'Analyzing...' : 'Ask Question'}
        </button>
      </form>
    </div>
  );
}