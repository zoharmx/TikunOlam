import type { BinahResult } from '../types';

interface BinahSigmaViewProps {
  binah: BinahResult;
}

function BinahSigmaView({ binah }: BinahSigmaViewProps) {
  const getDivergenceColor = (level?: string) => {
    switch (level?.toLowerCase()) {
      case 'high':
        return 'var(--color-error)';
      case 'medium':
        return 'var(--color-warning)';
      case 'low':
        return 'var(--color-success)';
      default:
        return 'var(--color-text-secondary)';
    }
  };

  return (
    <div>
      <div style={{
        padding: '1.5rem',
        background: 'linear-gradient(135deg, rgba(6, 214, 160, 0.1), rgba(58, 134, 255, 0.1))',
        borderRadius: 'var(--radius-lg)',
        marginBottom: '1.5rem',
        border: '2px solid var(--color-binah)'
      }}>
        <h3 className="text-2xl font-bold mb-2" style={{ color: 'var(--color-binah)' }}>
          🌍 BinahSigma Multi-Civilizational Analysis
        </h3>
        <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.875rem' }}>
          Comparing Western (Gemini) and Eastern (DeepSeek) AI perspectives to detect civilizational biases and blind spots
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-3 mb-3">
        <div style={{
          padding: '1.5rem',
          backgroundColor: 'var(--color-bg-tertiary)',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '0.5rem' }}>
            Bias Delta
          </div>
          <div style={{
            fontSize: '3rem',
            fontWeight: 'bold',
            color: getDivergenceColor(binah.divergence_level)
          }}>
            {binah.bias_delta}%
          </div>
        </div>

        <div style={{
          padding: '1.5rem',
          backgroundColor: 'var(--color-bg-tertiary)',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '0.5rem' }}>
            Divergence Level
          </div>
          <div style={{
            fontSize: '1.5rem',
            fontWeight: 'bold',
            color: getDivergenceColor(binah.divergence_level),
            textTransform: 'uppercase'
          }}>
            {binah.divergence_level}
          </div>
        </div>

        <div style={{
          padding: '1.5rem',
          backgroundColor: 'var(--color-bg-tertiary)',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '0.5rem' }}>
            Blind Spots Detected
          </div>
          <div style={{
            fontSize: '3rem',
            fontWeight: 'bold',
            color: 'var(--color-accent)'
          }}>
            {binah.blind_spots_detected || 0}
          </div>
        </div>
      </div>

      {/* Blind Spots Comparison */}
      <div className="grid grid-cols-2 mb-3">
        {/* Western Blind Spots */}
        <div style={{
          padding: '1.5rem',
          backgroundColor: 'rgba(58, 134, 255, 0.1)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid rgba(58, 134, 255, 0.3)'
        }}>
          <h4 className="text-lg font-bold mb-2" style={{ color: 'var(--color-chochmah)' }}>
            🌐 Western Perspective Blind Spots
          </h4>
          <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>
            What Western AI (Gemini) tends to miss or undervalue
          </p>
          <ul style={{ paddingLeft: '1.5rem' }}>
            {binah.sigma_synthesis?.west_blind_spots?.map((spot, idx) => (
              <li key={idx} style={{
                marginBottom: '0.75rem',
                color: 'var(--color-text-primary)',
                lineHeight: '1.5'
              }}>
                {spot}
              </li>
            ))}
          </ul>
        </div>

        {/* Eastern Blind Spots */}
        <div style={{
          padding: '1.5rem',
          backgroundColor: 'rgba(6, 214, 160, 0.1)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid rgba(6, 214, 160, 0.3)'
        }}>
          <h4 className="text-lg font-bold mb-2" style={{ color: 'var(--color-binah)' }}>
            🌏 Eastern Perspective Blind Spots
          </h4>
          <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>
            What Eastern AI (DeepSeek) tends to miss or undervalue
          </p>
          <ul style={{ paddingLeft: '1.5rem' }}>
            {binah.sigma_synthesis?.east_blind_spots?.map((spot, idx) => (
              <li key={idx} style={{
                marginBottom: '0.75rem',
                color: 'var(--color-text-primary)',
                lineHeight: '1.5'
              }}>
                {spot}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Universal Convergence */}
      {binah.sigma_synthesis?.universal_convergence && binah.sigma_synthesis.universal_convergence.length > 0 && (
        <div style={{
          padding: '1.5rem',
          backgroundColor: 'rgba(63, 185, 80, 0.1)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid rgba(63, 185, 80, 0.3)',
          marginBottom: '1.5rem'
        }}>
          <h4 className="text-lg font-bold mb-2" style={{ color: 'var(--color-success)' }}>
            🤝 Universal Convergence Points
          </h4>
          <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>
            Values and concerns recognized by both civilizational perspectives
          </p>
          <ul style={{ paddingLeft: '1.5rem' }}>
            {binah.sigma_synthesis.universal_convergence.map((point, idx) => (
              <li key={idx} style={{
                marginBottom: '0.75rem',
                color: 'var(--color-text-primary)',
                fontWeight: 500
              }}>
                {point}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Transcendent Synthesis */}
      {binah.sigma_synthesis?.transcendent_synthesis && (
        <div style={{
          padding: '1.5rem',
          background: 'linear-gradient(135deg, var(--color-bg-tertiary), var(--color-bg-secondary))',
          borderRadius: 'var(--radius-md)',
          border: '2px solid var(--color-binah)'
        }}>
          <h4 className="text-lg font-bold mb-2" style={{ color: 'var(--color-binah)' }}>
            🔄 Transcendent Synthesis
          </h4>
          <p style={{ fontSize: '0.875rem', color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>
            A third path that transcends both Western and Eastern blind spots
          </p>
          <div style={{
            padding: '1rem',
            backgroundColor: 'var(--color-bg-tertiary)',
            borderRadius: 'var(--radius-md)',
            lineHeight: '1.8',
            fontSize: '0.95rem'
          }}>
            {binah.sigma_synthesis.transcendent_synthesis}
          </div>
        </div>
      )}

      {/* Contextual Depth Score */}
      <div style={{
        marginTop: '1.5rem',
        padding: '1rem',
        backgroundColor: 'var(--color-bg-tertiary)',
        borderRadius: 'var(--radius-md)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <span style={{ fontWeight: 500 }}>Contextual Depth Score:</span>
          <span style={{ marginLeft: '0.5rem', color: 'var(--color-text-secondary)' }}>
            BinahSigma achieves inherently deep contextual understanding
          </span>
        </div>
        <div style={{
          fontSize: '2rem',
          fontWeight: 'bold',
          color: 'var(--color-binah)'
        }}>
          {binah.contextual_depth_score}%
        </div>
      </div>
    </div>
  );
}

export default BinahSigmaView;
