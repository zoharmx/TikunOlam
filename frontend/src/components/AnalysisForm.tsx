import { useState } from 'react';
import { Sparkles } from 'lucide-react';

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
    <div className="glass-panel p-8 rounded-2xl">
      <div className="flex items-center gap-3 mb-2">
        <Sparkles className="w-6 h-6 text-primary" />
        <h2 className="text-2xl font-bold text-white">Analyze Ethical Scenario</h2>
      </div>
      <p className="text-slate-400 mb-8">
        Enter a scenario for multi-civilizational ethical analysis through the 10 Sefirot.
        BinahSigma will activate automatically for geopolitical content.
      </p>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="caseName" className="block mb-2 text-sm font-medium text-slate-300">
            Case Name <span className="text-slate-500">(optional)</span>
          </label>
          <input
            type="text"
            id="caseName"
            className="w-full px-4 py-3 bg-surface/50 border border-white/10 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:border-primary/50 transition-colors"
            placeholder="e.g., UBI_Analysis_2024"
            value={caseName}
            onChange={(e) => setCaseName(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="scenario" className="block mb-2 text-sm font-medium text-slate-300">
            Scenario <span className="text-red-400">*</span>
          </label>
          <textarea
            id="scenario"
            className="w-full px-4 py-3 bg-surface/50 border border-white/10 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:border-primary/50 transition-colors resize-none"
            placeholder="Describe the ethical scenario you want to analyze..."
            value={scenario}
            onChange={(e) => setScenario(e.target.value)}
            required
            rows={8}
          />
          <div className="mt-2 text-xs text-slate-500">
            {scenario.length} characters
            {scenario.length > 500 && ' - BinahSigma may activate for geopolitical content'}
          </div>
        </div>

        <div>
          <p className="text-sm font-medium text-slate-300 mb-3">
            Example Scenarios:
          </p>
          <div className="flex gap-3 flex-wrap">
            {exampleScenarios.map((example, idx) => (
              <button
                key={idx}
                type="button"
                className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-lg text-sm text-slate-300 transition-all"
                onClick={() => loadExample(example.text)}
              >
                {example.name}
              </button>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={!scenario.trim()}
          className="w-full py-4 bg-primary hover:bg-primary/90 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-bold rounded-lg transition-all shadow-[0_0_20px_rgba(58,134,255,0.2)] hover:shadow-[0_0_30px_rgba(58,134,255,0.3)]"
        >
          Analyze Scenario
        </button>
      </form>

      <div className="mt-8 p-6 bg-surface/30 border border-white/5 rounded-xl">
        <p className="font-medium text-slate-200 mb-3 text-sm">
          What happens during analysis:
        </p>
        <ul className="space-y-1.5 text-xs text-slate-400">
          <li className="flex items-start gap-2">
            <span className="text-sef-keter">•</span>
            <span>Keter validates ethical alignment</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-chochmah">•</span>
            <span>Chochmah analyzes wisdom and precedents</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-binah">•</span>
            <span>Binah performs multi-civilizational understanding (BinahSigma)</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-chesed">•</span>
            <span>Chesed evaluates opportunities</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-gevurah">•</span>
            <span>Gevurah assesses risks</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-tiferet">•</span>
            <span>Tiferet synthesizes balance</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-netzach">•</span>
            <span>Netzach formulates strategy</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-hod">•</span>
            <span>Hod designs communication</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-yesod">•</span>
            <span>Yesod integrates all insights</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-sef-malchut">•</span>
            <span>Malchut makes final decision</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default AnalysisForm;
