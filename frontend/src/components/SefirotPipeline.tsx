import { motion } from 'framer-motion';
import ProviderBadge from './ProviderBadge';
import type { ProviderKey } from '../types';

interface SefirahNode {
  id: string;
  name: string;
  hebrew: string;
  role: string;
  provider: string;
  providerKey: ProviderKey;
  color: string;
  side: 'left' | 'right' | 'center';
}

const SEFIROT: SefirahNode[] = [
  { id: 'keter',    name: 'Keter',    hebrew: 'כתר',  role: 'Ethical Alignment',    provider: 'Grok-3',               providerKey: 'grok',    color: '#ffffff', side: 'center' },
  { id: 'chochmah', name: 'Chochmah', hebrew: 'חכמה', role: 'Wisdom & Precedents',  provider: 'Mistral Large',         providerKey: 'mistral', color: '#3a86ff', side: 'right'  },
  { id: 'binah',    name: 'Binah',    hebrew: 'בינה', role: 'Bias Detection',        provider: 'Vertex + DeepSeek',     providerKey: 'vertex',  color: '#06d6a0', side: 'left'   },
  { id: 'chesed',   name: 'Chesed',   hebrew: 'חסד',  role: 'Opportunity Analysis',  provider: 'VertexAI',              providerKey: 'vertex',  color: '#ffd60a', side: 'right'  },
  { id: 'gevurah',  name: 'Gevurah',  hebrew: 'גבורה', role: 'Risk Assessment',       provider: 'VertexAI',              providerKey: 'vertex',  color: '#e63946', side: 'left'   },
  { id: 'tiferet',  name: 'Tiferet',  hebrew: 'תפארת', role: 'Synthesis & Balance',   provider: 'GPT-4o',                providerKey: 'openai',  color: '#f77f00', side: 'center' },
  { id: 'netzach',  name: 'Netzach',  hebrew: 'נצח',  role: 'Strategy Formulation',  provider: 'DeepSeek',              providerKey: 'deepseek', color: '#06ffa5', side: 'right' },
  { id: 'hod',      name: 'Hod',      hebrew: 'הוד',  role: 'Communication Design',  provider: 'VertexAI',              providerKey: 'vertex',  color: '#457b9d', side: 'left'   },
  { id: 'yesod',    name: 'Yesod',    hebrew: 'יסוד', role: 'Integration & GO/NO-GO', provider: 'Mistral Large',        providerKey: 'mistral', color: '#a8dadc', side: 'center' },
  { id: 'malchut',  name: 'Malchut',  hebrew: 'מלכות', role: 'Final Decision',        provider: 'Grok-3',               providerKey: 'grok',    color: '#9d4edd', side: 'center' },
];

function SefirotPipeline() {
  return (
    <div className="relative max-w-3xl mx-auto py-8">
      {/* Center spine */}
      <div className="absolute left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-white/20 via-primary/20 to-transparent pointer-events-none" />

      <div className="space-y-6">
        {SEFIROT.map((sefirah, idx) => {
          const isLeft = sefirah.side === 'left' || (sefirah.side === 'center' && idx % 2 === 0);
          const isCenter = sefirah.side === 'center';

          return (
            <motion.div
              key={sefirah.id}
              initial={{ opacity: 0, x: isLeft ? -30 : 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ delay: idx * 0.07, duration: 0.5, ease: 'easeOut' }}
              className={`flex items-center gap-4 ${isCenter ? 'justify-center' : isLeft ? 'justify-start pr-[52%]' : 'justify-end pl-[52%]'}`}
            >
              <div
                className={`relative glass-card rounded-xl p-4 flex-1 max-w-xs ${isLeft ? 'text-left' : !isCenter ? 'text-right' : 'text-center'}`}
                style={{ borderColor: `${sefirah.color}30` }}
              >
                {/* Glow */}
                <div
                  className="absolute inset-0 rounded-xl opacity-10 pointer-events-none"
                  style={{ background: `radial-gradient(circle at center, ${sefirah.color}, transparent 70%)` }}
                />

                <div className={`flex items-center gap-2 mb-2 ${isCenter ? 'justify-center' : !isLeft ? 'flex-row-reverse' : ''}`}>
                  <div
                    className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                    style={{ backgroundColor: sefirah.color, boxShadow: `0 0 8px ${sefirah.color}` }}
                  />
                  <span className="font-bold text-white text-sm">{sefirah.name}</span>
                  <span className="text-slate-500 text-sm font-mono">{sefirah.hebrew}</span>
                </div>

                <p className="text-xs text-slate-400 mb-2">{sefirah.role}</p>

                <div className={`flex ${isCenter ? 'justify-center' : !isLeft ? 'justify-end' : ''}`}>
                  <ProviderBadge provider={sefirah.providerKey} label={sefirah.provider} size="sm" />
                </div>

                {/* Index number */}
                <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-surface border border-white/10 flex items-center justify-center text-[10px] text-slate-500 font-mono">
                  {idx + 1}
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export default SefirotPipeline;
