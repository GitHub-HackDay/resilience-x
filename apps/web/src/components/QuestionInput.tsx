import { useState } from 'react';
import { AskRequest } from '@/types/api';

interface QuestionInputProps {
  onSubmit: (question: string) => void;
  loading: boolean;
}

/**
 * Accessible input component for asking questions
 */
export default function QuestionInput({ onSubmit, loading }: QuestionInputProps) {
  const [question, setQuestion] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }
    
    if (question.trim().length < 5) {
      setError('Please enter a more detailed question');
      return;
    }

    setError('');
    onSubmit(question.trim());
  };

  const sampleQuestions = [
    "Which neighborhoods are facing cleanup delays?",
    "What roads are still blocked near Redmond?",
    "Why is debris removal taking longer than expected?",
    "What crew shortage issues are affecting operations?"
  ];

  const handleSampleClick = (sampleQuestion: string) => {
    setQuestion(sampleQuestion);
    setError('');
  };

  return (
    <div className="question-input-section mb-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-2">
          Resilience-X Crisis Recovery Q&A
        </h1>
        <p className="text-gray-600 text-center mb-8">
          Ask questions about post-disaster recovery and get explained answers with sources
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label 
              htmlFor="question-input"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Your Question
            </label>
            <textarea
              id="question-input"
              value={question}
              onChange={(e) => {
                setQuestion(e.target.value);
                if (error) setError('');
              }}
              placeholder="e.g., Which areas are experiencing cleanup delays and why?"
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              rows={3}
              disabled={loading}
              aria-describedby={error ? "question-error" : "question-help"}
            />
            <p id="question-help" className="mt-1 text-sm text-gray-500">
              Ask about recovery operations, delays, resource issues, or infrastructure status
            </p>
            {error && (
              <p id="question-error" className="mt-1 text-sm text-red-600" role="alert">
                {error}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                Analyzing Question...
              </div>
            ) : (
              'Get Explained Answer'
            )}
          </button>
        </form>

        {/* Sample Questions */}
        <div className="mt-8">
          <p className="text-sm font-medium text-gray-700 mb-3">Try these sample questions:</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {sampleQuestions.map((sampleQuestion, index) => (
              <button
                key={index}
                onClick={() => handleSampleClick(sampleQuestion)}
                className="text-left p-3 text-sm text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 border border-blue-200 transition-colors"
                disabled={loading}
              >
                "{sampleQuestion}"
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}