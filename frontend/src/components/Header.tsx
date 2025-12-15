function Header() {
  return (
    <header style={{
      backgroundColor: 'var(--color-bg-secondary)',
      borderBottom: '1px solid var(--color-border)',
      padding: '1.5rem 0',
      boxShadow: 'var(--shadow-md)'
    }}>
      <div className="container">
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem'
        }}>
          <div>
            <h1 style={{
              fontSize: '2rem',
              fontWeight: 'bold',
              background: 'linear-gradient(135deg, var(--color-keter), var(--color-binah))',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              marginBottom: '0.25rem'
            }}>
              תיקון עולם
            </h1>
            <p style={{
              color: 'var(--color-text-secondary)',
              fontSize: '0.875rem'
            }}>
              Ethical AI Reasoning Framework
            </p>
          </div>

          <div style={{
            display: 'flex',
            gap: '1rem',
            alignItems: 'center'
          }}>
            <div className="badge badge-info">
              BinahSigma Active
            </div>
            <div className="badge badge-success">
              10 Sefirot
            </div>
          </div>
        </div>

        <div style={{
          marginTop: '1rem',
          padding: '0.75rem',
          backgroundColor: 'var(--color-bg-tertiary)',
          borderRadius: 'var(--radius-md)',
          fontSize: '0.875rem',
          color: 'var(--color-text-secondary)'
        }}>
          Multi-civilizational AI ethical reasoning based on Kabbalistic Sefirot.
          Detects biases between Western and Eastern perspectives.
        </div>
      </div>
    </header>
  );
}

export default Header;
