import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

const sefirotStages = [
  { id: 'keter',    name: 'Keter',    label: 'Ethical Validation',   color: '#ffffff', provider: 'Grok-3',       providerColor: '#FF6B35' },
  { id: 'chochmah', name: 'Chochmah', label: 'Wisdom Analysis',      color: '#3a86ff', provider: 'Mistral',      providerColor: '#F72585' },
  { id: 'binah',    name: 'Binah',    label: 'Bias Detection',        color: '#06d6a0', provider: 'Vertex+DeepSeek', providerColor: '#4285F4' },
  { id: 'chesed',   name: 'Chesed',   label: 'Opportunities',         color: '#ffd60a', provider: 'VertexAI',    providerColor: '#4285F4' },
  { id: 'gevurah',  name: 'Gevurah',  label: 'Risk Assessment',       color: '#e63946', provider: 'VertexAI',    providerColor: '#4285F4' },
  { id: 'tiferet',  name: 'Tiferet',  label: 'Synthesis',             color: '#f77f00', provider: 'GPT-4o',      providerColor: '#10A37F' },
  { id: 'netzach',  name: 'Netzach',  label: 'Strategy',              color: '#06ffa5', provider: 'DeepSeek',    providerColor: '#00B4D8' },
  { id: 'hod',      name: 'Hod',      label: 'Communication',         color: '#457b9d', provider: 'VertexAI',    providerColor: '#4285F4' },
  { id: 'yesod',    name: 'Yesod',    label: 'Integration',           color: '#a8dadc', provider: 'Mistral',     providerColor: '#F72585' },
  { id: 'malchut',  name: 'Malchut',  label: 'Final Decision',        color: '#6a4c93', provider: 'Grok-3',      providerColor: '#FF6B35' },
];

function LoadingState() {
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStage((prev) => (prev + 1) % sefirotStages.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-3xl glass-panel p-12 rounded-2xl flex flex-col items-center">
      <div className="relative mb-12">
        <div className="absolute inset-0 bg-primary/20 blur-[50px] rounded-full" />
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          className="w-24 h-24 border-t-2 border-l-2 border-primary rounded-full relative z-10"
        />
        <div className="absolute inset-0 flex items-center justify-center font-mono text-2xl font-bold text-primary">
          {(currentStage + 1) * 10}%
        </div>
      </div>

      <h2 className="text-3xl font-bold mb-2 text-white">Processing Ethics</h2>
      <p className="text-slate-400 mb-3 text-center max-w-md">
        Navigating through 10 Sefirot with 6 AI providers.<br />
        BinahSigma activating for geopolitical content detection...
      </p>
      <p className="text-sm text-slate-500 mb-6 font-mono">
        Estimated time: 8–12 minutes
      </p>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 w-full">
        {sefirotStages.map((stage, idx) => {
          const isActive = idx === currentStage;
          const isPast = idx < currentStage;

          return (
            <motion.div
              key={stage.id}
              animate={{
                scale: isActive ? 1.05 : 1,
                opacity: isActive || isPast ? 1 : 0.3,
                borderColor: isActive ? stage.color : 'rgba(255,255,255,0.1)'
              }}
              className="p-3 rounded-lg border bg-surface/50 backdrop-blur-sm flex flex-col items-center text-center transition-all duration-300 relative overflow-hidden"
            >
              {isActive && (
                <motion.div
                  layoutId="active-glow"
                  className="absolute inset-0 bg-white/5"
                  transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                />
              )}

              <div
                className="w-3 h-3 rounded-full mb-2 shadow-[0_0_10px_currentColor]"
                style={{ backgroundColor: stage.color, color: stage.color }}
              />

              <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
                {stage.name}
              </span>
              <span className="text-[10px] text-slate-500 mt-1 leading-tight">
                {stage.label}
              </span>

              {/* Provider name when active */}
              {isActive && (
                <motion.div
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-1.5 flex items-center gap-1"
                >
                  <span
                    className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                    style={{ backgroundColor: stage.providerColor }}
                  />
                  <span className="text-[9px] font-mono" style={{ color: stage.providerColor }}>
                    {stage.provider}
                  </span>
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export default LoadingState;
