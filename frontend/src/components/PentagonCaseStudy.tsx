import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, Globe, Map, GitMerge, Sparkles, CheckCircle, Shield, Clock } from 'lucide-react';
import ProviderBadge from './ProviderBadge';
import { PENTAGON_CASE } from '../data/pentagonCase';

type Panel = 'overview' | 'keter' | 'binah' | 'strategies' | 'decision';

const PANELS: { id: Panel; label: string; icon: React.ReactNode }[] = [
  { id: 'overview',   label: 'Overview',       icon: <Shield size={15} /> },
  { id: 'keter',      label: 'Keter (Grok)',    icon: <AlertTriangle size={15} /> },
  { id: 'binah',      label: 'BinahSigma',      icon: <Globe size={15} /> },
  { id: 'strategies', label: 'Strategies',      icon: <Sparkles size={15} /> },
  { id: 'decision',   label: 'Decision',        icon: <CheckCircle size={15} /> },
];

const SEVERITY_COLORS: Record<string, string> = {
  critical: 'text-red-400 border-red-500/30 bg-red-500/10',
  high:     'text-orange-400 border-orange-500/30 bg-orange-500/10',
  medium:   'text-yellow-400 border-yellow-500/30 bg-yellow-500/10',
  low:      'text-green-400 border-green-500/30 bg-green-500/10',
};

function PentagonCaseStudy() {
  const [activePanel, setActivePanel] = useState<Panel>('overview');
  const [prevPanel, setPrevPanel] = useState<Panel>('overview');

  const handlePanelChange = (panel: Panel) => {
    setPrevPanel(activePanel);
    setActivePanel(panel);
  };

  const panelIndex = (p: Panel) => PANELS.findIndex(x => x.id === p);
  const direction = panelIndex(activePanel) > panelIndex(prevPanel) ? 1 : -1;

  const duration = PENTAGON_CASE.metadata.total_duration_seconds;
  const durationStr = `${Math.floor(duration / 60)}m ${duration % 60}s`;

  return (
    <div className="glass-panel rounded-2xl overflow-hidden">
      {/* Case header */}
      <div className="bg-gradient-to-r from-red-950/40 via-slate-900/80 to-yellow-950/30 border-b border-white/5 p-5 sm:p-6">
        <div className="flex flex-wrap items-start gap-4 justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-yellow-500/20 border border-yellow-500/30 text-yellow-400 uppercase tracking-wider">
                Live Case Study
              </span>
              <span className="text-slate-500 text-xs font-mono">Feb 15, 2026</span>
            </div>
            <h3 className="text-xl sm:text-2xl font-bold text-white">Anthropic vs. The Pentagon</h3>
            <p className="text-slate-400 text-sm mt-1">
              $2.4B contract — autonomous weapons targeting — should Anthropic accept?
            </p>
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <div className="flex items-center gap-1.5 text-xs text-slate-400">
              <Clock size={12} />
              <span className="font-mono">{durationStr}</span>
            </div>
            <span className="verdict-conditional px-3 py-1.5 rounded-full text-sm font-bold border">
              CONDITIONAL_GO
            </span>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row">
        {/* Nav */}
        <nav className="sm:w-44 border-b sm:border-b-0 sm:border-r border-white/5 p-3 sm:p-4 flex sm:flex-col gap-1 overflow-x-auto sm:overflow-visible">
          {PANELS.map(panel => (
            <button
              key={panel.id}
              onClick={() => handlePanelChange(panel.id)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium whitespace-nowrap transition-all duration-200 ${
                activePanel === panel.id
                  ? 'bg-primary/15 text-primary border border-primary/25'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              {panel.icon}
              {panel.label}
            </button>
          ))}
        </nav>

        {/* Content */}
        <div className="flex-1 min-w-0 p-5 sm:p-6">
          <AnimatePresence mode="wait" custom={direction}>
            <motion.div
              key={activePanel}
              custom={direction}
              initial={{ opacity: 0, x: direction * 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: direction * -20 }}
              transition={{ duration: 0.22, ease: 'easeOut' }}
            >
              {activePanel === 'overview' && <OverviewPanel />}
              {activePanel === 'keter' && <KeterPanel />}
              {activePanel === 'binah' && <BinahPanel />}
              {activePanel === 'strategies' && <StrategiesPanel />}
              {activePanel === 'decision' && <DecisionPanel />}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

function OverviewPanel() {
  const metrics = [
    { label: 'Keter Alignment', value: '42%', sub: 'Threshold: 70%', color: 'text-red-400', bg: 'bg-red-500/10 border-red-500/20' },
    { label: 'Bias Delta (East/West)', value: '0%', sub: 'Both agreed', color: 'text-green-400', bg: 'bg-green-500/10 border-green-500/20' },
    { label: 'Blind Spots Found', value: '6', sub: '3 West · 3 East', color: 'text-yellow-400', bg: 'bg-yellow-500/10 border-yellow-500/20' },
    { label: 'Integration Readiness', value: '88%', sub: 'Yesod (Mistral)', color: 'text-green-400', bg: 'bg-green-500/10 border-green-500/20' },
  ];

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-2 gap-3">
        {metrics.map(m => (
          <div key={m.label} className={`p-4 rounded-xl border ${m.bg}`}>
            <p className="text-[11px] text-slate-400 mb-1">{m.label}</p>
            <p className={`text-2xl font-bold font-mono ${m.color}`}>{m.value}</p>
            <p className="text-[10px] text-slate-500 mt-1">{m.sub}</p>
          </div>
        ))}
      </div>

      <div className="p-4 rounded-xl bg-white/3 border border-white/8">
        <p className="text-xs text-slate-400 mb-3 font-medium uppercase tracking-wider">Provider Distribution</p>
        <div className="flex flex-wrap gap-2">
          <ProviderBadge provider="grok" label="Keter, Malchut" />
          <ProviderBadge provider="mistral" label="Chochmah, Yesod" />
          <ProviderBadge provider="openai" label="Tiferet" />
          <ProviderBadge provider="deepseek" label="Binah-East, Netzach" />
          <ProviderBadge provider="vertex" label="Binah-West, Chesed, Gevurah, Hod" />
        </div>
      </div>

      <div className="p-4 rounded-xl bg-yellow-500/5 border border-yellow-500/20">
        <p className="text-xs font-semibold text-yellow-400 mb-1">Verdict</p>
        <p className="text-sm text-slate-300 leading-relaxed">
          CONDITIONAL_GO — Anthropic may engage only under 3 non-negotiable conditions.
          Remove any one and the answer becomes <span className="text-red-400 font-semibold">NO_GO</span>.
        </p>
      </div>
    </div>
  );
}

function KeterPanel() {
  const { keter } = PENTAGON_CASE;

  return (
    <div className="space-y-4">
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-slate-400">Ethical Alignment Score</span>
          <span className="text-sm font-bold font-mono text-red-400">{keter.alignment_percentage}% / 70% threshold</span>
        </div>
        <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            className="h-full rounded-full bg-gradient-to-r from-red-600 to-red-400"
            initial={{ width: 0 }}
            animate={{ width: `${keter.alignment_percentage}%` }}
            transition={{ duration: 1.2, ease: 'easeOut', delay: 0.2 }}
          />
        </div>
        <div className="flex justify-between mt-1">
          <span className="text-[10px] text-slate-600">0%</span>
          <div className="w-px h-3 bg-yellow-500/60 relative">
            <span className="absolute -top-4 left-1/2 -translate-x-1/2 text-[10px] text-yellow-500 whitespace-nowrap">70% min</span>
          </div>
          <span className="text-[10px] text-slate-600">100%</span>
        </div>
      </div>

      <p className="text-xs text-slate-400">
        <ProviderBadge provider="grok" label="grok-3" size="sm" /> analyzed and detected <strong className="text-red-400">5 corruptions</strong>:
      </p>

      <div className="space-y-2">
        {keter.corruptions.map((c, idx) => (
          <div key={idx} className={`p-3 rounded-lg border text-xs ${SEVERITY_COLORS[c.severity] || SEVERITY_COLORS.medium}`}>
            <div className="flex items-start gap-2">
              <span className="uppercase text-[9px] font-bold tracking-wider px-1.5 py-0.5 rounded bg-current/10 flex-shrink-0 mt-0.5">
                {c.severity}
              </span>
              <div>
                <p className="font-semibold">{c.type}</p>
                <p className="text-slate-400 mt-0.5 leading-relaxed">{c.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function BinahPanel() {
  const { binah } = PENTAGON_CASE;
  const sigma = binah.sigma_synthesis!;

  return (
    <div className="space-y-4">
      <div className="flex gap-3 flex-wrap">
        <div className="flex items-center gap-1.5 text-xs">
          <span className="w-2 h-2 rounded-full bg-green-400 shadow-[0_0_6px_#4ade80]" />
          <span className="text-slate-400">Bias Delta: </span>
          <span className="text-green-400 font-bold font-mono">{binah.bias_delta}%</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs">
          <span className="w-2 h-2 rounded-full bg-green-400 shadow-[0_0_6px_#4ade80]" />
          <span className="text-slate-400">Divergence: </span>
          <span className="text-green-400 font-bold uppercase">{binah.divergence_level}</span>
        </div>
        <div className="flex items-center gap-1.5 text-xs">
          <span className="w-2 h-2 rounded-full bg-yellow-400 shadow-[0_0_6px_#facc15]" />
          <span className="text-slate-400">Blind Spots: </span>
          <span className="text-yellow-400 font-bold font-mono">{binah.blind_spots_detected}</span>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-3">
        <div className="p-4 rounded-xl bg-blue-500/5 border border-blue-500/20">
          <div className="flex items-center gap-2 mb-3">
            <Globe size={14} className="text-blue-400" />
            <span className="text-xs font-semibold text-blue-400">Western Perspective</span>
            <ProviderBadge provider="vertex" label="gemini-2.5-pro" />
          </div>
          <p className="text-[10px] text-slate-500 mb-2">Blind spots (what it misses):</p>
          <ul className="space-y-2">
            {sigma.west_blind_spots.map((s, i) => (
              <li key={i} className="text-xs text-slate-300 flex gap-2">
                <span className="text-blue-500 flex-shrink-0 mt-0.5">·</span>
                {s}
              </li>
            ))}
          </ul>
        </div>

        <div className="p-4 rounded-xl bg-green-500/5 border border-green-500/20">
          <div className="flex items-center gap-2 mb-3">
            <Map size={14} className="text-green-400" />
            <span className="text-xs font-semibold text-green-400">Eastern Perspective</span>
            <ProviderBadge provider="deepseek" label="deepseek-chat" />
          </div>
          <p className="text-[10px] text-slate-500 mb-2">Blind spots (what it misses):</p>
          <ul className="space-y-2">
            {sigma.east_blind_spots.map((s, i) => (
              <li key={i} className="text-xs text-slate-300 flex gap-2">
                <span className="text-green-500 flex-shrink-0 mt-0.5">·</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="p-4 rounded-xl bg-accent/5 border border-accent/20">
        <div className="flex items-center gap-2 mb-2">
          <GitMerge size={14} className="text-accent" />
          <span className="text-xs font-semibold text-accent">Transcendent Synthesis</span>
          <ProviderBadge provider="vertex" label="gemini-2.5-pro" />
        </div>
        <blockquote className="synthesis-quote text-xs">
          {sigma.transcendent_synthesis}
        </blockquote>
      </div>
    </div>
  );
}

function StrategiesPanel() {
  const { netzach } = PENTAGON_CASE;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 mb-1">
        <ProviderBadge provider="deepseek" label="deepseek-chat · Netzach" />
        <span className="text-xs text-slate-500">formulated {netzach.strategies.length} strategies</span>
      </div>

      {netzach.strategies.map((strategy, idx) => (
        <motion.div
          key={idx}
          initial={{ opacity: 0, x: -15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.1 }}
          className="flex gap-3 p-4 rounded-xl glass-card"
        >
          <div
            className="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-background"
            style={{ backgroundColor: '#00B4D8' }}
          >
            {idx + 1}
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">{strategy}</p>
        </motion.div>
      ))}
    </div>
  );
}

function DecisionPanel() {
  const { malchut, yesod } = PENTAGON_CASE;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <CheckCircle size={28} className="text-yellow-400" />
        <div>
          <p className="text-xs text-slate-500">Final Decision</p>
          <p className="text-2xl font-bold text-yellow-400 font-mono">CONDITIONAL_GO</p>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap text-xs text-slate-400">
        <ProviderBadge provider="grok" label="Malchut · grok-3" />
        <ProviderBadge provider="mistral" label="Yesod · mistral-large" />
      </div>

      <div>
        <p className="text-xs font-semibold text-slate-300 mb-2 uppercase tracking-wider">Non-Negotiable Conditions</p>
        <div className="space-y-2">
          {malchut.conditions.map((cond, idx) => (
            <div key={idx} className="flex gap-3 p-3 rounded-lg bg-yellow-500/5 border border-yellow-500/20">
              <span className="flex-shrink-0 w-5 h-5 rounded-full border border-yellow-500/50 flex items-center justify-center text-[10px] font-bold text-yellow-400">
                {idx + 1}
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">{cond}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 rounded-xl bg-white/3 border border-white/8">
        <p className="text-xs text-slate-500 mb-2">Yesod Integration Readiness</p>
        <div className="flex items-center gap-3">
          <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-accent to-primary"
              initial={{ width: 0 }}
              animate={{ width: `${yesod.readiness_score}%` }}
              transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
            />
          </div>
          <span className="text-sm font-bold text-accent font-mono">{yesod.readiness_score}%</span>
        </div>
        <p className="text-xs text-slate-400 mt-2 leading-relaxed">{malchut.final_summary}</p>
      </div>
    </div>
  );
}

export default PentagonCaseStudy;
