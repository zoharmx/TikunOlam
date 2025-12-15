import { useState } from 'react';

interface SefirahCardProps {
  name: string;
  subtitle: string;
  color: string;
  data: any;
}

function SefirahCard({ name, subtitle, color, data }: SefirahCardProps) {
  const [expanded, setExpanded] = useState(false);

  const renderContent = () => {
    switch (name) {
      case 'Keter':
        return (
          <div>
            <div className="grid grid-cols-2" style={{ gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>
                  Alignment
                </div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color }}>
                  {data.alignment_percentage}%
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>
                  Corruption Severity
                </div>
                <div style={{
                  fontSize: '1.25rem',
                  fontWeight: 'bold',
                  textTransform: 'uppercase',
                  color: data.corruption_severity === 'low' ? 'var(--color-success)' :
                    data.corruption_severity === 'medium' ? 'var(--color-warning)' : 'var(--color-error)'
                }}>
                  {data.corruption_severity}
                </div>
              </div>
            </div>

            {data.scores && (
              <div style={{ marginBottom: '1rem' }}>
                <h5 style={{ fontWeight: 600, marginBottom: '0.5rem' }}>Dimension Scores:</h5>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '0.5rem' }}>
                  {Object.entries(data.scores).map(([dim, score]: [string, any]) => (
                    <div key={dim} style={{
                      padding: '0.5rem',
                      backgroundColor: 'var(--color-bg-tertiary)',
                      borderRadius: 'var(--radius-sm)'
                    }}>
                      <div style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)' }}>{dim}</div>
                      <div style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>{score}/10</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {data.corruptions && data.corruptions.length > 0 && (
              <div>
                <h5 style={{ fontWeight: 600, marginBottom: '0.5rem' }}>
                  Corruptions Detected ({data.corruptions.length}):
                </h5>
                {data.corruptions.map((corr: any, idx: number) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    backgroundColor: 'var(--color-bg-tertiary)',
                    borderRadius: 'var(--radius-md)',
                    marginBottom: '0.5rem'
                  }}>
                    <div style={{ fontWeight: 500, marginBottom: '0.25rem' }}>
                      {corr.type} <span className={`badge badge-${corr.severity === 'low' ? 'success' : corr.severity === 'medium' ? 'warning' : 'error'}`}>{corr.severity}</span>
                    </div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>
                      {corr.description}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );

      case 'Chochmah':
        return (
          <div>
            <div className="grid grid-cols-3" style={{ gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>Confidence</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color }}>{data.confidence_level}%</div>
              </div>
              <div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>Humility</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color }}>{data.epistemic_humility_ratio}%</div>
              </div>
              <div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>Insight Depth</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color }}>{data.insight_depth_score}%</div>
              </div>
            </div>

            {data.patterns_identified && (
              <div style={{ marginBottom: '1rem' }}>
                <h5 style={{ fontWeight: 600, marginBottom: '0.5rem' }}>
                  Patterns Identified ({data.patterns_identified.length}):
                </h5>
                <ul style={{ paddingLeft: '1.5rem', fontSize: '0.875rem' }}>
                  {data.patterns_identified.slice(0, 3).map((pattern: string, idx: number) => (
                    <li key={idx} style={{ marginBottom: '0.5rem' }}>{pattern}</li>
                  ))}
                </ul>
              </div>
            )}

            {data.precedents && data.precedents.length > 0 && (
              <div>
                <h5 style={{ fontWeight: 600, marginBottom: '0.5rem' }}>
                  Historical Precedents ({data.precedents.length}):
                </h5>
                {data.precedents.slice(0, 2).map((prec: any, idx: number) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    backgroundColor: 'var(--color-bg-tertiary)',
                    borderRadius: 'var(--radius-md)',
                    marginBottom: '0.5rem',
                    fontSize: '0.875rem'
                  }}>
                    <div style={{ fontWeight: 500 }}>{prec.name} {prec.year && `(${prec.year})`}</div>
                    <div style={{ color: 'var(--color-text-secondary)', marginTop: '0.25rem' }}>
                      {prec.relevance}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );

      case 'Binah':
        return (
          <div>
            <div style={{ marginBottom: '1rem' }}>
              <span className={`badge badge-${data.mode === 'sigma' ? 'info' : 'success'}`}>
                Mode: {data.mode.toUpperCase()}
              </span>
              {data.mode === 'sigma' && (
                <span className="badge badge-warning" style={{ marginLeft: '0.5rem' }}>
                  Bias Delta: {data.bias_delta}%
                </span>
              )}
            </div>
            <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>
              Contextual Depth: <strong style={{ color }}>{data.contextual_depth_score}%</strong>
            </div>
            {data.mode === 'sigma' && (
              <div style={{
                marginTop: '1rem',
                padding: '1rem',
                backgroundColor: 'rgba(6, 214, 160, 0.1)',
                borderRadius: 'var(--radius-md)'
              }}>
                BinahSigma detected {data.blind_spots_detected} blind spots across civilizational perspectives.
                See BinahSigma tab for full analysis.
              </div>
            )}
          </div>
        );

      case 'Gevurah':
        return (
          <div>
            <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>
              Risk Score: <strong style={{ fontSize: '1.5rem', color }}>{data.risk_score}%</strong>
            </div>
            {data.risks && data.risks.length > 0 && (
              <div>
                <h5 style={{ fontWeight: 600, marginBottom: '0.5rem' }}>Top Risks:</h5>
                {data.risks.slice(0, 3).map((risk: any, idx: number) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    backgroundColor: 'var(--color-bg-tertiary)',
                    borderRadius: 'var(--radius-md)',
                    marginBottom: '0.5rem',
                    fontSize: '0.875rem'
                  }}>
                    <div style={{ fontWeight: 500 }}>
                      {risk.category} <span className={`badge badge-${risk.severity === 'high' ? 'error' : 'warning'}`}>{risk.severity}</span>
                    </div>
                    <div style={{ color: 'var(--color-text-secondary)', marginTop: '0.25rem' }}>
                      {risk.description}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );

      case 'Yesod':
        return (
          <div>
            <div className="grid grid-cols-2" style={{ gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>Readiness</div>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color }}>{data.readiness_score}%</div>
              </div>
              <div>
                <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>Quality</div>
                <div style={{ fontSize: '1.25rem', fontWeight: 'bold', textTransform: 'uppercase' }}>
                  {data.integration_quality}
                </div>
              </div>
            </div>
            <div style={{
              padding: '1rem',
              backgroundColor: 'var(--color-bg-tertiary)',
              borderRadius: 'var(--radius-md)'
            }}>
              <strong>Recommendation:</strong> {data.recommendation}
            </div>
          </div>
        );

      case 'Malchut':
        return (
          <div>
            <div style={{
              padding: '1rem',
              backgroundColor: 'var(--color-bg-tertiary)',
              borderRadius: 'var(--radius-md)',
              marginBottom: '1rem'
            }}>
              <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>Decision</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color }}>{data.decision}</div>
              <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginTop: '0.5rem' }}>
                Confidence: {data.confidence_level}%
              </div>
            </div>
            {data.action_items && data.action_items.length > 0 && (
              <div>
                <h5 style={{ fontWeight: 600, marginBottom: '0.5rem' }}>Action Items:</h5>
                <ul style={{ paddingLeft: '1.5rem', fontSize: '0.875rem' }}>
                  {data.action_items.map((item: string, idx: number) => (
                    <li key={idx} style={{ marginBottom: '0.5rem' }}>{item}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        );

      default:
        return (
          <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>
            {JSON.stringify(data, null, 2).slice(0, 200)}...
          </div>
        );
    }
  };

  return (
    <div style={{
      backgroundColor: 'var(--color-bg-secondary)',
      border: `2px solid ${color}`,
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden'
    }}>
      <div
        style={{
          padding: '1rem 1.5rem',
          backgroundColor: `${color}15`,
          borderBottom: `1px solid ${color}`,
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <div>
          <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color, marginBottom: '0.25rem' }}>
            {name}
          </h3>
          <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)' }}>
            {subtitle}
          </p>
        </div>
        <div style={{
          fontSize: '1.5rem',
          color,
          transform: expanded ? 'rotate(180deg)' : 'rotate(0)',
          transition: 'transform 0.3s'
        }}>
          ▼
        </div>
      </div>

      {expanded && (
        <div style={{ padding: '1.5rem' }}>
          {renderContent()}
        </div>
      )}
    </div>
  );
}

export default SefirahCard;
