/**
 * Main page component for Resilience-X Q&A interface
 */

import { useState } from 'react'
import Head from 'next/head'

interface AnswerResponse {
  answer: string
  explanation_bullets: string[]
  sources: string[]
}

export default function Home() {
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState<AnswerResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })

      if (!res.ok) throw new Error('Failed to get answer')

      const data: AnswerResponse = await res.json()
      setResponse(data)
    } catch (error) {
      console.error('Error asking question:', error)
      // TODO: Show error message to user
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Resilience-X - Crisis Recovery Q&A</title>
        <meta name="description" content="AI-powered crisis recovery Q&A system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      
      <main style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
        <h1>Resilience-X</h1>
        <p>Ask questions about crisis recovery and get explainable answers.</p>

        <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
          <label htmlFor="question" style={{ display: 'block', marginBottom: '0.5rem' }}>
            Your Question:
          </label>
          <input
            id="question"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Which neighborhoods are facing cleanup delays?"
            style={{
              width: '100%',
              padding: '0.75rem',
              fontSize: '1rem',
              border: '1px solid #ccc',
              borderRadius: '4px',
              marginBottom: '1rem'
            }}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            style={{
              padding: '0.75rem 1.5rem',
              fontSize: '1rem',
              backgroundColor: '#0070f3',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Thinking...' : 'Ask Question'}
          </button>
        </form>

        {response && (
          <div style={{ border: '1px solid #ddd', padding: '1.5rem', borderRadius: '4px' }}>
            <h2>Answer</h2>
            <p style={{ fontSize: '1.1rem', lineHeight: '1.5' }}>{response.answer}</p>

            <h3>Why (Explanation)</h3>
            <ul>
              {response.explanation_bullets.map((bullet, index) => (
                <li key={index} style={{ marginBottom: '0.5rem' }}>{bullet}</li>
              ))}
            </ul>

            <h3>Sources</h3>
            <ul>
              {response.sources.map((source, index) => (
                <li key={index} style={{ marginBottom: '0.25rem' }}>{source}</li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </>
  )
}