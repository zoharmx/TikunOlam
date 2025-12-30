import { useState } from 'react';
import { RotateCcw } from 'lucide-react';
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

  const getDecisionColor = (decision: string) => {
    if (decision.includes('GO') && !decision.includes('NO')) {
      return 'text-green-400';
    } else if (decision.includes('CONDITIONAL')) {
      return 'text-yellow-400';
    } else {
      return 'text-red-400';
    }
  };

  const getAlignmentColor = (score: number) => {
    if (score >= 70) return 'text-green-400';
    if (score >= 50) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div>
      {/* Header */}
      <div className="glass-panel p-6 rounded-2xl mb-6">
        <div className="flex justify-between items-center flex-wrap gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white">Analysis Results</h2>
            <p className="text-slate-400 text-sm">
              {results.case_name} • {new Date(metadata.timestamp).toLocaleString()}
            </p>
          </div>
          <div className="flex gap-3 items-center">
            {isBinahSigma && (
              <div className="px-4 py-2 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-medium">
                BinahSigma Active
              </div>
            )}
            <button
              className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-lg text-sm text-slate-300 transition-all"
              onClick={onReset}
            >
              <RotateCcw className="w-4 h-4" />
              New Analysis
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="glass-panel p-6 rounded-2xl">
        <div className="flex gap-2 border-b border-white/10 mb-6">
          <button
            onClick={() => setActiveTab('summary')}
            className={`px-6 py-3 font-medium transition-all border-b-2 ${
              activeTab === 'summary'
                ? 'text-primary border-primary'
                : 'text-slate-400 border-transparent hover:text-slate-300'
            }`}
          >
            Summary
          </button>
          <button
            onClick={() => setActiveTab('sefirot')}
            className={`px-6 py-3 font-medium transition-all border-b-2 ${
              activeTab === 'sefirot'
                ? 'text-primary border-primary'
                : 'text-slate-400 border-transparent hover:text-slate-300'
            }`}
          >
            10 Sefirot
          </button>
          {isBinahSigma && (
            <button
              onClick={() => setActiveTab('binah')}
              className={`px-6 py-3 font-medium transition-all border-b-2 ${
                activeTab === 'binah'
                  ? 'text-primary border-primary'
                  : 'text-slate-400 border-transparent hover:text-slate-300'
              }`}
            >
              BinahSigma 🌍
            </button>
          )}
        </div>

        {/* Summary Tab */}
        {activeTab === 'summary' && (
          <div className="space-y-6">
            {/* Final Decision */}
            <div className="p-6 bg-surface/50 rounded-xl border border-white/10">
              <h3 className="text-xl font-bold text-white mb-3">Final Decision</h3>
              <div className={`text-3xl font-bold mb-2 ${getDecisionColor(summary.final_decision)}`}>
                {summary.final_decision}
              </div>
              <p className="text-slate-400">{summary.recommendation}</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-6 bg-surface/30 rounded-xl border border-white/5">
                <h4 className="font-semibold text-slate-300 mb-2">Overall Alignment</h4>
                <div className={`text-4xl font-bold ${getAlignmentColor(summary.overall_alignment)}`}>
                  {summary.overall_alignment}%
                </div>
              </div>
              <div className="p-6 bg-surface/30 rounded-xl border border-white/5">
                <h4 className="font-semibold text-slate-300 mb-2">Analysis Duration</h4>
                <div className="text-4xl font-bold text-primary">
                  {Math.round(metadata.total_duration_seconds)}s
                </div>
              </div>
            </div>

            {/* Opportunities and Risks */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-6 bg-surface/30 rounded-xl border border-white/5">
                <h4 className="font-semibold text-slate-200 mb-3">
                  Key Opportunities ({summary.key_opportunities.length})
                </h4>
                <ul className="space-y-2 text-sm text-slate-400">
                  {summary.key_opportunities.slice(0, 3).map((opp, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-green-400">•</span>
                      <span>{opp}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="p-6 bg-surface/30 rounded-xl border border-white/5">
                <h4 className="font-semibold text-slate-200 mb-3">
                  Key Risks ({summary.key_risks.length})
                </h4>
                <ul className="space-y-2 text-sm text-slate-400">
                  {summary.key_risks.slice(0, 3).map((risk, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-red-400">•</span>
                      <span>{risk}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Models Used */}
            <div className="p-6 bg-surface/30 rounded-xl border border-white/5">
              <h4 className="font-semibold text-slate-200 mb-3">Models Used</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-sm">
                {Object.entries(metadata.models_used).map(([sefirah, model]) => (
                  <div key={sefirah} className="text-slate-400">
                    <span className="font-medium text-slate-300">{sefirah}:</span> {model}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Sefirot Tab */}
        {activeTab === 'sefirot' && (
          <div className="space-y-4">
            <SefirahCard
              name="Keter"
              subtitle="Crown - Ethical Validation"
              color="#9d4edd"
              data={sefirot_results.keter}
            />
            <SefirahCard
              name="Chochmah"
              subtitle="Wisdom - Pattern Analysis"
              color="#3a86ff"
              data={sefirot_results.chochmah}
            />
            <SefirahCard
              name="Binah"
              subtitle="Understanding - Multi-civilizational"
              color="#06d6a0"
              data={sefirot_results.binah}
            />
            <SefirahCard
              name="Chesed"
              subtitle="Kindness - Opportunities"
              color="#ffd60a"
              data={sefirot_results.chesed}
            />
            <SefirahCard
              name="Gevurah"
              subtitle="Severity - Risks"
              color="#e63946"
              data={sefirot_results.gevurah}
            />
            <SefirahCard
              name="Tiferet"
              subtitle="Beauty - Synthesis"
              color="#f77f00"
              data={sefirot_results.tiferet}
            />
            <SefirahCard
              name="Netzach"
              subtitle="Victory - Strategy"
              color="#06ffa5"
              data={sefirot_results.netzach}
            />
            <SefirahCard
              name="Hod"
              subtitle="Glory - Communication"
              color="#457b9d"
              data={sefirot_results.hod}
            />
            <SefirahCard
              name="Yesod"
              subtitle="Foundation - Integration"
              color="#a8dadc"
              data={sefirot_results.yesod}
            />
            <SefirahCard
              name="Malchut"
              subtitle="Kingdom - Final Decision"
              color="#6a4c93"
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
