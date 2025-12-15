import { useEffect, useState } from 'react';

const sefirotStages = [
  { name: 'Keter', label: 'Crown - Ethical Validation', color: 'var(--color-keter)' },
  { name: 'Chochmah', label: 'Wisdom - Pattern Analysis', color: 'var(--color-chochmah)' },
  { name: 'Binah', label: 'Understanding - Multi-civilizational', color: 'var(--color-binah)' },
  { name: 'Chesed', label: 'Kindness - Opportunities', color: 'var(--color-chesed)' },
  { name: 'Gevurah', label: 'Severity - Risks', color: 'var(--color-gevurah)' },
  { name: 'Tiferet', label: 'Beauty - Synthesis', color: 'var(--color-tiferet)' },
  { name: 'Netzach', label: 'Victory - Strategy', color: 'var(--color-netzach)' },
  { name: 'Hod', label: 'Glory - Communication', color: 'var(--color-hod)' },
  { name: 'Yesod', label: 'Foundation - Integration', color: 'var(--color-yesod)' },
  { name: 'Malchut', label: 'Kingdom - Decision', color: 'var(--color-malchut)' },
];

function LoadingState() {
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStage((prev) => (prev + 1) % sefirotStages.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card" style={{ textAlign: 'center' }}>
      <h2 className="text-2xl font-bold mb-3">Analyzing Scenario...</h2>
      <p style={{ color: 'var(--color-text-secondary)', marginBottom: '2rem' }}>
        Processing through the 10 Sefirot ethical reasoning pipeline
      </p>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
        marginBottom: '2rem'
      }}>
        <div className="spinner"></div>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem'
      }}>
        {sefirotStages.map((stage, idx) => (
          <div
            key={stage.name}
            style={{
              padding: '1rem',
              borderRadius: 'var(--radius-md)',
              backgroundColor: idx === currentStage
                ? 'var(--color-bg-tertiary)'
                : 'transparent',
              border: `2px solid ${idx <= currentStage ? stage.color : 'var(--color-border)'}`,
              opacity: idx <= currentStage ? 1 : 0.3,
              transition: 'all 0.3s ease',
              transform: idx === currentStage ? 'scale(1.05)' : 'scale(1)'
            }}
          >
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              backgroundColor: stage.color,
              margin: '0 auto 0.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 'bold',
              fontSize: '1.2rem'
            }}>
              {idx + 1}
            </div>
            <div style={{
              fontWeight: 600,
              marginBottom: '0.25rem',
              fontSize: '0.9rem'
            }}>
              {stage.name}
            </div>
            <div style={{
              fontSize: '0.75rem',
              color: 'var(--color-text-secondary)'
            }}>
              {stage.label}
            </div>
          </div>
        ))}
      </div>

      <div style={{
        padding: '1rem',
        backgroundColor: 'rgba(88, 166, 255, 0.1)',
        borderRadius: 'var(--radius-md)',
        fontSize: '0.875rem',
        color: 'var(--color-text-secondary)'
      }}>
        <p style={{ marginBottom: '0.5rem' }}>
          <strong>Current Stage:</strong> {sefirotStages[currentStage].name}
        </p>
        <p>
          {sefirotStages[currentStage].label}
        </p>
      </div>

      <p style={{
        marginTop: '1.5rem',
        fontSize: '0.875rem',
        color: 'var(--color-text-secondary)'
      }}>
        This may take 2-3 minutes depending on scenario complexity
      </p>
    </div>
  );
}

export default LoadingState;
