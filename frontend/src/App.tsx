import { useState } from 'react';
import Header from './components/Header';
import AnalysisForm from './components/AnalysisForm';
import Results from './components/Results';
import LoadingState from './components/LoadingState';
import api from './services/api';
import type { AnalysisResponse } from './types';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async (scenario: string, caseName?: string) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await api.analyzeSync({
        scenario,
        case_name: caseName,
        verbose: true,
        auto_export: true,
      });

      setResults(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <Header />

      <main className="container" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
        {!loading && !results && (
          <AnalysisForm onSubmit={handleAnalyze} />
        )}

        {loading && <LoadingState />}

        {error && (
          <div className="card" style={{
            backgroundColor: 'rgba(248, 81, 73, 0.1)',
            borderColor: 'var(--color-error)'
          }}>
            <h2 style={{ color: 'var(--color-error)', marginBottom: '1rem' }}>
              Analysis Error
            </h2>
            <p style={{ color: 'var(--color-text-secondary)' }}>{error}</p>
            <button
              className="button button-secondary mt-2"
              onClick={handleReset}
            >
              Try Again
            </button>
          </div>
        )}

        {results && !loading && (
          <Results results={results} onReset={handleReset} />
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '2rem 1rem',
        marginTop: 'auto',
        borderTop: `1px solid var(--color-border)`,
        color: 'var(--color-text-secondary)',
        fontSize: '0.875rem'
      }}>
        <p>תיקון עולם - Tikun Olam v1.0.0</p>
        <p style={{ marginTop: '0.5rem' }}>
          Ethical AI Reasoning Framework | Multi-civilizational Analysis
        </p>
      </footer>
    </div>
  );
}

export default App;
