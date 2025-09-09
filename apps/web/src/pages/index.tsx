/**
 * Main page for Resilience-X crisis Q&A interface.
 * Provides input box and results panel for querying crisis recovery information.
 */
import { useState } from 'react'
import type { NextPage } from 'next'
import Head from 'next/head'

interface AnswerResponse {
  answer: string
  explanation_bullets: string[]
  sources: string[]
}

const Home: NextPage = () => {
  const [question, setQuestion] = useState<string>('')
  const [response, setResponse] = useState<AnswerResponse | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!question.trim()) {
      setError('Please enter a question')
      return
    }

    setLoading(true)
    setError('')
    setResponse(null)

    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      })

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      }

      const data: AnswerResponse = await res.json()
      setResponse(data)
    } catch (err) {
      console.error('API Error:', err)
      setError('Unable to process your question. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleTryExample = (exampleQuestion: string) => {
    setQuestion(exampleQuestion)
  }

  return (
    <>
      <Head>
        <title>Resilience-X - Crisis Recovery Q&A</title>
        <meta name="description" content="AI-powered crisis recovery question answering with explainable responses" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
        <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1>Resilience-X</h1>
          <p>Crisis Recovery Q&A with Explainable AI</p>
        </header>

        <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="question-input" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Ask a question about crisis recovery:
            </label>
            <textarea
              id="question-input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., Which neighborhoods are facing cleanup delays?"
              rows={3}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '1rem',
                resize: 'vertical'
              }}
              disabled={loading}
            />
          </div>
          
          <button
            type="submit"
            disabled={loading || !question.trim()}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: loading ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '1rem',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Processing...' : 'Ask Question'}
          </button>
        </form>

        {/* Example questions */}
        <div style={{ marginBottom: '2rem', padding: '1rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
          <h3>Try these example questions:</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <button
              type="button"
              onClick={() => handleTryExample('Which neighborhoods are facing cleanup delays?')}
              style={{ textAlign: 'left', background: 'none', border: '1px solid #ddd', padding: '0.5rem', borderRadius: '4px', cursor: 'pointer' }}
            >
              Which neighborhoods are facing cleanup delays?
            </button>
            <button
              type="button"
              onClick={() => handleTryExample('Which roads are blocked near Redmond?')}
              style={{ textAlign: 'left', background: 'none', border: '1px solid #ddd', padding: '0.5rem', borderRadius: '4px', cursor: 'pointer' }}
            >
              Which roads are blocked near Redmond?
            </button>
            <button
              type="button"
              onClick={() => handleTryExample('What is causing cleanup delays in King County?')}
              style={{ textAlign: 'left', background: 'none', border: '1px solid #ddd', padding: '0.5rem', borderRadius: '4px', cursor: 'pointer' }}
            >
              What is causing cleanup delays in King County?
            </button>
          </div>
        </div>

        {error && (
          <div style={{ padding: '1rem', backgroundColor: '#f8d7da', color: '#721c24', border: '1px solid #f5c6cb', borderRadius: '4px', marginBottom: '1rem' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {response && (
          <div style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '1.5rem', backgroundColor: '#fff' }}>
            <section style={{ marginBottom: '1.5rem' }}>
              <h2>Answer</h2>
              <p style={{ fontSize: '1.1rem', lineHeight: '1.6' }}>{response.answer}</p>
            </section>

            <section style={{ marginBottom: '1.5rem' }}>
              <h3>Why (Explanation)</h3>
              <ul style={{ paddingLeft: '1.5rem' }}>
                {response.explanation_bullets.map((bullet, index) => (
                  <li key={index} style={{ marginBottom: '0.5rem', lineHeight: '1.5' }}>
                    {bullet}
                  </li>
                ))}
              </ul>
            </section>

            <section>
              <h3>Sources</h3>
              <ul style={{ paddingLeft: '1.5rem', listStyleType: 'none' }}>
                {response.sources.map((source, index) => (
                  <li key={index} style={{ marginBottom: '0.5rem', padding: '0.5rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                    📄 {source}
                  </li>
                ))}
              </ul>
            </section>
          </div>
        )}

        <footer style={{ marginTop: '3rem', textAlign: 'center', color: '#666', fontSize: '0.9rem' }}>
          <p>Resilience-X Demo - Built with GitHub Copilot, GraphRAG, NLWeb, and Weaviate</p>
          <p><em>Currently running in fallback mode with static examples</em></p>
        </footer>
      </main>
    </>
  )
}

export default Home