import { useState } from 'react';
import type { AnalysisResponse } from '../types';
import BinahSigmaView from './BinahSigmaView';
import SefirahCard from './SefirahCard';

interface ResultsProps {
  results: AnalysisResponse;
  onReset: () => void;
}

function Results({ results, onReset }: ResultsProps) {
  const [activeTab, setActiveTab] = useState<'summary' | 'sefirot' | 'binah'>('summary');

  const { sefirot_results, summary, metadata } = results;
  const isBinahSigma = sefirot_results.binah.mode === 'sigma';

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'low':
        return 'var(--color-success)';
      case 'medium':
        return 'var(--color-warning)';
      case 'high':
      case 'critical':
        return 'var(--color-error)';
      default:
        return 'var(--color-text-secondary)';
    }
  };

  const getDecisionColor = (decision: string) => {
    if (decision.includes('GO') && !decision.includes('NO')) {
      return 'var(--color-success)';
    } else if (decision.includes('CONDITIONAL')) {
      return 'var(--color-warning)';
    } else {
      return 'var(--color-error)';
    }
  };

  return (
    <div>
      <div className="card mb-3">
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem'
        }}>
          <div>
            <h2 className="text-2xl font-bold">Analysis Results</h2>
            <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.875rem' }}>
              {results.case_name} • {new Date(metadata.timestamp).toLocaleString()}
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            {isBinahSigma && (
              <div className="badge badge-info">BinahSigma Active</div>
            )}
            <button
              className="button button-secondary"
              onClick={onReset}
            >
              New Analysis
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="card mb-3">
        <div style={{
          display: 'flex',
          gap: '0.5rem',
          borderBottom: '1px solid var(--color-border)',
          marginBottom: '1rem'
        }}>
          <button
            onClick={() => setActiveTab('summary')}
            style={{
              padding: '0.75rem 1.5rem',
              border: 'none',
              background: 'transparent',
              color: activeTab === 'summary' ? 'var(--color-accent)' : 'var(--color-text-secondary)',
              borderBottom: `2px solid ${activeTab === 'summary' ? 'var(--color-accent)' : 'transparent'}`,
              cursor: 'pointer',
              fontWeight: 500,
              transition: 'all 0.2s'
            }}
          >
            Summary
          </button>
          <button
            onClick={() => setActiveTab('sefirot')}
            style={{
              padding: '0.75rem 1.5rem',
              border: 'none',
              background: 'transparent',
              color: activeTab === 'sefirot' ? 'var(--color-accent)' : 'var(--color-text-secondary)',
              borderBottom: `2px solid ${activeTab === 'sefirot' ? 'var(--color-accent)' : 'transparent'}`,
              cursor: 'pointer',
              fontWeight: 500,
              transition: 'all 0.2s'
            }}
          >
            10 Sefirot
          </button>
          {isBinahSigma && (
            <button
              onClick={() => setActiveTab('binah')}
              style={{
                padding: '0.75rem 1.5rem',
                border: 'none',
                background: 'transparent',
                color: activeTab === 'binah' ? 'var(--color-accent)' : 'var(--color-text-secondary)',
                borderBottom: `2px solid ${activeTab === 'binah' ? 'var(--color-accent)' : 'transparent'}`,
                cursor: 'pointer',
                fontWeight: 500,
                transition: 'all 0.2s'
              }}
            >
              BinahSigma 🌍
            </button>
          )}
        </div>

        {/* Summary Tab */}
        {activeTab === 'summary' && (
          <div>
            <div style={{
              padding: '1.5rem',
              backgroundColor: 'var(--color-bg-tertiary)',
              borderRadius: 'var(--radius-md)',
              marginBottom: '1.5rem'
            }}>
              <h3 className="text-xl font-bold mb-2">Final Decision</h3>
              <div style={{
                fontSize: '2rem',
                fontWeight: 'bold',
                color: getDecisionColor(summary.final_decision),
                marginBottom: '0.5rem'
              }}>
                {summary.final_decision}
              </div>
              <p style={{ color: 'var(--color-text-secondary)' }}>
                {summary.recommendation}
              </p>
            </div>

            <div className="grid grid-cols-2 mb-3">
              <div>
                <h4 className="font-semibold mb-2">Overall Alignment</h4>
                <div style={{
                  fontSize: '2.5rem',
                  fontWeight: 'bold',
                  color: summary.overall_alignment >= 70 ? 'var(--color-success)' :
                    summary.overall_alignment >= 50 ? 'var(--color-warning)' : 'var(--color-error)'
                }}>
                  {summary.overall_alignment}%
                </div>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Analysis Duration</h4>
                <div style={{
                  fontSize: '2.5rem',
                  fontWeight: 'bold',
                  color: 'var(--color-accent)'
                }}>
                  {Math.round(metadata.total_duration_seconds)}s
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 mb-3">
              <div>
                <h4 className="font-semibold mb-2">Key Opportunities ({summary.key_opportunities.length})</h4>
                <ul style={{ paddingLeft: '1.5rem', color: 'var(--color-text-secondary)' }}>
                  {summary.key_opportunities.slice(0, 3).map((opp, idx) => (
                    <li key={idx} style={{ marginBottom: '0.5rem' }}>{opp}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Key Risks ({summary.key_risks.length})</h4>
                <ul style={{ paddingLeft: '1.5rem', color: 'var(--color-text-secondary)' }}>
                  {summary.key_risks.slice(0, 3).map((risk, idx) => (
                    <li key={idx} style={{ marginBottom: '0.5rem' }}>{risk}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div style={{
              padding: '1rem',
              backgroundColor: 'var(--color-bg-tertiary)',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.875rem'
            }}>
              <h4 className="font-semibold mb-2">Models Used</h4>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                gap: '0.5rem',
                color: 'var(--color-text-secondary)'
              }}>
                {Object.entries(metadata.models_used).map(([sefirah, model]) => (
                  <div key={sefirah}>
                    <strong>{sefirah}:</strong> {model}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Sefirot Tab */}
        {activeTab === 'sefirot' && (
          <div className="grid grid-cols-1" style={{ gap: '1rem' }}>
            <SefirahCard
              name="Keter"
              subtitle="Crown - Ethical Validation"
              color="var(--color-keter)"
              data={sefirot_results.keter}
            />
            <SefirahCard
              name="Chochmah"
              subtitle="Wisdom - Pattern Analysis"
              color="var(--color-chochmah)"
              data={sefirot_results.chochmah}
            />
            <SefirahCard
              name="Binah"
              subtitle="Understanding - Multi-civilizational"
              color="var(--color-binah)"
              data={sefirot_results.binah}
            />
            <SefirahCard
              name="Chesed"
              subtitle="Kindness - Opportunities"
              color="var(--color-chesed)"
              data={sefirot_results.chesed}
            />
            <SefirahCard
              name="Gevurah"
              subtitle="Severity - Risks"
              color="var(--color-gevurah)"
              data={sefirot_results.gevurah}
            />
            <SefirahCard
              name="Tiferet"
              subtitle="Beauty - Synthesis"
              color="var(--color-tiferet)"
              data={sefirot_results.tiferet}
            />
            <SefirahCard
              name="Netzach"
              subtitle="Victory - Strategy"
              color="var(--color-netzach)"
              data={sefirot_results.netzach}
            />
            <SefirahCard
              name="Hod"
              subtitle="Glory - Communication"
              color="var(--color-hod)"
              data={sefirot_results.hod}
            />
            <SefirahCard
              name="Yesod"
              subtitle="Foundation - Integration"
              color="var(--color-yesod)"
              data={sefirot_results.yesod}
            />
            <SefirahCard
              name="Malchut"
              subtitle="Kingdom - Final Decision"
              color="var(--color-malchut)"
              data={sefirot_results.malchut}
            />
          </div>
        )}

        {/* BinahSigma Tab */}
        {activeTab === 'binah' && isBinahSigma && (
          <BinahSigmaView binah={sefirot_results.binah} />
        )}
      </div>
    </div>
  );
}

export default Results;
