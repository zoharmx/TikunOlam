import { Globe, Map, GitMerge, Sparkles, Users } from 'lucide-react';
import type { BinahResult } from '../types';
import ProviderBadge from './ProviderBadge';

interface BinahSigmaViewProps {
  binah: BinahResult;
}

function BinahSigmaView({ binah }: BinahSigmaViewProps) {
  const divergenceColor =
    binah.divergence_level === 'high' ? 'text-red-400' :
    binah.divergence_level === 'low'  ? 'text-green-400' :
    'text-yellow-400';

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="p-5 rounded-xl bg-gradient-to-br from-accent/10 to-primary/10 border-2 border-accent/30">
        <div className="flex items-center gap-3 mb-1">
          <GitMerge className="w-5 h-5 text-accent" />
          <h3 className="text-xl font-bold text-accent">BinahSigma Multi-Civilizational Analysis</h3>
        </div>
        <p className="text-slate-400 text-sm">
          Western (VertexAI) vs Eastern (DeepSeek) perspectives — civilizational bias detection
        </p>
      </div>

      {/* Metrics row */}
      <div className="grid grid-cols-3 gap-3">
        <div className="p-4 rounded-xl bg-surface/60 border border-white/8 text-center">
          <p className="text-xs text-slate-400 mb-1">Bias Delta</p>
          <p className={`text-3xl font-bold font-mono ${divergenceColor}`}>{binah.bias_delta}%</p>
        </div>
        <div className="p-4 rounded-xl bg-surface/60 border border-white/8 text-center">
          <p className="text-xs text-slate-400 mb-1">Divergence</p>
          <p className={`text-xl font-bold uppercase ${divergenceColor}`}>{binah.divergence_level}</p>
        </div>
        <div className="p-4 rounded-xl bg-surface/60 border border-white/8 text-center">
          <p className="text-xs text-slate-400 mb-1">Blind Spots</p>
          <p className="text-3xl font-bold font-mono text-accent">{binah.blind_spots_detected || 0}</p>
        </div>
      </div>

      {/* Blind spots comparison */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Western */}
        <div className="p-5 rounded-xl bg-blue-500/5 border border-blue-500/25">
          <div className="flex items-center gap-2 mb-1">
            <Globe className="w-4 h-4 text-primary" />
            <span className="font-semibold text-primary text-sm">Western Perspective</span>
          </div>
          <div className="mb-3">
            <ProviderBadge provider="vertex" label="gemini-2.5-pro" />
          </div>
          <p className="text-xs text-slate-500 mb-3">What Western AI tends to miss:</p>
          <ul className="space-y-2">
            {binah.sigma_synthesis?.west_blind_spots?.map((spot, idx) => (
              <li key={idx} className="flex gap-2 text-sm text-slate-300 leading-relaxed">
                <span className="text-primary flex-shrink-0 mt-0.5">·</span>
                {spot}
              </li>
            ))}
          </ul>
        </div>

        {/* Eastern */}
        <div className="p-5 rounded-xl bg-green-500/5 border border-green-500/25">
          <div className="flex items-center gap-2 mb-1">
            <Map className="w-4 h-4 text-accent" />
            <span className="font-semibold text-accent text-sm">Eastern Perspective</span>
          </div>
          <div className="mb-3">
            <ProviderBadge provider="deepseek" label="deepseek-chat" />
          </div>
          <p className="text-xs text-slate-500 mb-3">What Eastern AI tends to miss:</p>
          <ul className="space-y-2">
            {binah.sigma_synthesis?.east_blind_spots?.map((spot, idx) => (
              <li key={idx} className="flex gap-2 text-sm text-slate-300 leading-relaxed">
                <span className="text-accent flex-shrink-0 mt-0.5">·</span>
                {spot}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Universal convergence */}
      {binah.sigma_synthesis?.universal_convergence && binah.sigma_synthesis.universal_convergence.length > 0 && (
        <div className="p-5 rounded-xl bg-green-500/5 border border-green-500/20">
          <div className="flex items-center gap-2 mb-3">
            <Users className="w-4 h-4 text-green-400" />
            <span className="font-semibold text-green-400 text-sm">Universal Convergence Points</span>
          </div>
          <p className="text-xs text-slate-500 mb-3">Values recognized by both civilizational perspectives:</p>
          <ul className="space-y-2">
            {binah.sigma_synthesis.universal_convergence.map((point, idx) => (
              <li key={idx} className="flex gap-2 text-sm text-slate-300 font-medium leading-relaxed">
                <span className="text-green-500 flex-shrink-0 mt-0.5">·</span>
                {point}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Transcendent synthesis */}
      {binah.sigma_synthesis?.transcendent_synthesis && (
        <div className="p-5 rounded-xl bg-gradient-to-br from-surface to-surface/50 border-2 border-accent/30">
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="w-4 h-4 text-accent" />
            <span className="font-semibold text-accent text-sm">Transcendent Synthesis</span>
            <ProviderBadge provider="vertex" label="gemini-2.5-pro" />
          </div>
          <p className="text-xs text-slate-500 mb-3">A third path that transcends both blind spots:</p>
          <blockquote className="synthesis-quote text-sm">
            {binah.sigma_synthesis.transcendent_synthesis}
          </blockquote>
        </div>
      )}

      {/* Contextual depth footer */}
      <div className="flex items-center justify-between p-4 rounded-xl bg-surface/60 border border-white/8">
        <div>
          <span className="text-sm font-medium text-slate-300">Contextual Depth Score</span>
          <span className="text-xs text-slate-500 ml-2">BinahSigma achieves inherently deep contextual understanding</span>
        </div>
        <span className="text-2xl font-bold text-accent font-mono">{binah.contextual_depth_score}%</span>
      </div>
    </div>
  );
}

export default BinahSigmaView;
