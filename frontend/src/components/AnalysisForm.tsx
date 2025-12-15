import { useState } from 'react';

interface AnalysisFormProps {
  onSubmit: (scenario: string, caseName?: string) => void;
}

function AnalysisForm({ onSubmit }: AnalysisFormProps) {
  const [scenario, setScenario] = useState('');
  const [caseName, setCaseName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (scenario.trim()) {
      onSubmit(scenario, caseName || undefined);
    }
  };

  const exampleScenarios = [
    {
      name: 'Universal Basic Income (UBI)',
      text: `Proposal: Implement a global Universal Basic Income funded by redirecting 1% of worldwide military spending.

Context:
- Global military spending: ~$2.7 trillion annually
- 1% = $27 billion/year
- Target: 700 million people in extreme poverty (<$2.15/day)
- Monthly UBI: ~$38.50 per person ($462/year)

This represents an 18% income increase for those in extreme poverty while maintaining 99% of current military budgets.

The proposal includes:
- UN administration and distribution
- Transparent blockchain tracking
- Phased rollout over 5 years
- Annual review and adjustment

Geopolitical considerations:
- Requires cooperation from NATO, BRICS, China, Russia, USA
- Potential sovereignty concerns
- Defense budget implications
- Economic impact on recipient nations`
    },
    {
      name: 'AI Governance Framework',
      text: `Proposal: Create an international AI governance body similar to the IAEA for nuclear energy.

Key provisions:
- Mandatory safety testing for frontier AI models
- Global registry of advanced AI systems
- Incident reporting requirements
- Enforcement mechanisms with sanctions

The framework would address:
- Existential risk from AGI
- AI arms race dynamics
- Economic disruption and job displacement
- Democratic governance of transformative technology
- Equitable access to AI benefits

Critical questions:
- Who sets the standards?
- How to balance innovation with safety?
- Enforcement across sovereign nations
- Corporate vs. public control`
    }
  ];

  const loadExample = (text: string) => {
    setScenario(text);
  };

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-3">Analyze Ethical Scenario</h2>
      <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem' }}>
        Enter a scenario for multi-civilizational ethical analysis through the 10 Sefirot.
        BinahSigma will activate automatically for geopolitical content.
      </p>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label
            htmlFor="caseName"
            style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: 500
            }}
          >
            Case Name (optional)
          </label>
          <input
            type="text"
            id="caseName"
            className="input"
            placeholder="e.g., UBI_Analysis_2024"
            value={caseName}
            onChange={(e) => setCaseName(e.target.value)}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label
            htmlFor="scenario"
            style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: 500
            }}
          >
            Scenario <span style={{ color: 'var(--color-error)' }}>*</span>
          </label>
          <textarea
            id="scenario"
            className="input textarea"
            placeholder="Describe the ethical scenario you want to analyze..."
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            required
            style={{ minHeight: '200px' }}
          />
          <div style={{
            marginTop: '0.5rem',
            fontSize: '0.875rem',
            color: 'var(--color-text-secondary)'
          }}>
            {scenario.length} characters
            {scenario.length > 500 && ' - BinahSigma may activate for geopolitical content'}
          </div>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <p style={{
            fontSize: '0.875rem',
            fontWeight: 500,
            marginBottom: '0.5rem'
          }}>
            Example Scenarios:
          </p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {exampleScenarios.map((example, idx) => (
              <button
                key={idx}
                type="button"
                className="button button-secondary"
                onClick={() => loadExample(example.text)}
                style={{ fontSize: '0.875rem' }}
              >
                {example.name}
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          className="button button-primary"
          disabled={!scenario.trim()}
          style={{ width: '100%', padding: '0.75rem' }}
        >
          Analyze Scenario
        </button>
      </form>

      <div style={{
        marginTop: '1.5rem',
        padding: '1rem',
        backgroundColor: 'var(--color-bg-tertiary)',
        borderRadius: 'var(--radius-md)',
        fontSize: '0.875rem'
      }}>
        <p style={{ fontWeight: 500, marginBottom: '0.5rem' }}>
          What happens during analysis:
        </p>
        <ul style={{ paddingLeft: '1.5rem', color: 'var(--color-text-secondary)' }}>
          <li>Keter validates ethical alignment</li>
          <li>Chochmah analyzes wisdom and precedents</li>
          <li>Binah performs multi-civilizational understanding (BinahSigma)</li>
          <li>Chesed evaluates opportunities</li>
          <li>Gevurah assesses risks</li>
          <li>Tiferet synthesizes balance</li>
          <li>Netzach formulates strategy</li>
          <li>Hod designs communication</li>
          <li>Yesod integrates all insights</li>
          <li>Malchut makes final decision</li>
        </ul>
      </div>
    </div>
  );
}

export default AnalysisForm;
