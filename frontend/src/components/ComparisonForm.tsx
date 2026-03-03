import { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Minus, GitCompare, Loader2 } from 'lucide-react';

export interface ComparisonScenario {
  label: string;
  scenario: string;
  case_name: string;
}

interface Props {
  onSubmit: (scenarios: ComparisonScenario[]) => void;
  isLoading?: boolean;
}

const COLORS = ['#a78bfa', '#34d399', '#fb923c'];
const LABELS = ['A', 'B', 'C'];

const DEFAULT_SCENARIOS: ComparisonScenario[] = [
  { label: 'A', scenario: '', case_name: 'scenario_a' },
  { label: 'B', scenario: '', case_name: 'scenario_b' },
];

export function ComparisonForm({ onSubmit, isLoading = false }: Props) {
  const [scenarios, setScenarios] = useState<ComparisonScenario[]>(DEFAULT_SCENARIOS);

  const updateScenario = (i: number, field: keyof ComparisonScenario, val: string) => {
    setScenarios((prev) => prev.map((s, idx) => idx === i ? { ...s, [field]: val } : s));
  };

  const addScenario = () => {
    if (scenarios.length >= 3) return;
    const idx = scenarios.length;
    setScenarios((prev) => [...prev, { label: LABELS[idx], scenario: '', case_name: `scenario_${LABELS[idx].toLowerCase()}` }]);
  };

  const removeScenario = (i: number) => {
    if (scenarios.length <= 2) return;
    setScenarios((prev) => prev.filter((_, idx) => idx !== i));
  };

  const canSubmit = !isLoading && scenarios.every((s) => s.scenario.trim().length >= 20);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-3xl mx-auto"
    >
      <div className="flex items-center gap-3 mb-6">
        <GitCompare size={22} className="text-purple-400" />
        <div>
          <h2 className="text-xl font-bold text-white">Scenario Comparison</h2>
          <p className="text-white/50 text-sm">Submit 2–3 scenario variants to compare their ethical profiles side by side.</p>
        </div>
      </div>

      <div className="space-y-4">
        {scenarios.map((s, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="rounded-xl border border-white/10 bg-white/5 p-5"
            style={{ borderLeftColor: COLORS[i], borderLeftWidth: 3 }}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span
                  className="w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold"
                  style={{ background: COLORS[i] + '33', color: COLORS[i] }}
                >
                  {s.label}
                </span>
                <span className="text-white/70 text-sm">Scenario {s.label}</span>
              </div>
              {i >= 2 && (
                <button
                  onClick={() => removeScenario(i)}
                  className="text-white/30 hover:text-red-400 transition-colors"
                >
                  <Minus size={16} />
                </button>
              )}
            </div>

            <input
              type="text"
              placeholder={`Case name for scenario ${s.label}`}
              value={s.case_name}
              onChange={(e) => updateScenario(i, 'case_name', e.target.value)}
              className="w-full mb-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-white/80 text-sm placeholder-white/30 focus:outline-none focus:border-purple-500/50"
            />
            <textarea
              placeholder={`Describe scenario ${s.label} in detail (min. 20 characters)…`}
              value={s.scenario}
              onChange={(e) => updateScenario(i, 'scenario', e.target.value)}
              rows={4}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white/80 text-sm placeholder-white/30 focus:outline-none focus:border-purple-500/50 resize-none"
            />
            <p className="text-white/30 text-xs mt-1">{s.scenario.length} chars</p>
          </motion.div>
        ))}
      </div>

      <div className="flex items-center gap-3 mt-4">
        {scenarios.length < 3 && (
          <button
            onClick={addScenario}
            className="flex items-center gap-2 px-4 py-2 rounded-lg border border-white/10 text-white/50 hover:text-white/80 hover:border-white/20 transition-all text-sm"
          >
            <Plus size={14} />
            Add Scenario C
          </button>
        )}
        <button
          disabled={!canSubmit}
          onClick={() => onSubmit(scenarios)}
          className="ml-auto flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold text-sm transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          style={{ background: canSubmit ? 'linear-gradient(135deg, #7c3aed, #a78bfa)' : undefined }}
        >
          {isLoading ? (
            <><Loader2 size={15} className="animate-spin" /> Running {scenarios.length} analyses…</>
          ) : (
            <><GitCompare size={15} /> Compare {scenarios.length} Scenarios</>
          )}
        </button>
      </div>
    </motion.div>
  );
}
