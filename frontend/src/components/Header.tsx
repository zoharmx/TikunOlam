function Header() {
  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-4xl font-bold text-gradient mb-2">
            תיקון עולם
          </h1>
          <p className="text-slate-400 text-sm">
            Ethical AI Reasoning Framework
          </p>
        </div>

        <div className="flex gap-3">
          <div className="px-4 py-2 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-medium">
            BinahSigma Active
          </div>
          <div className="px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-medium">
            10 Sefirot
          </div>
        </div>
      </div>

      <div className="glass-panel p-4 rounded-xl text-sm text-slate-300">
        Multi-civilizational AI ethical reasoning based on Kabbalistic Sefirot.
        Detects biases between Western and Eastern perspectives.
      </div>
    </div>
  );
}

export default Header;
