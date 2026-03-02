import type { ProviderKey } from '../types';
import { PROVIDER_COLORS } from '../types';

interface ProviderBadgeProps {
  provider: ProviderKey;
  label: string;
  size?: 'sm' | 'md';
}

const PROVIDER_DISPLAY: Record<ProviderKey, string> = {
  grok: 'Grok',
  mistral: 'Mistral',
  openai: 'OpenAI',
  deepseek: 'DeepSeek',
  vertex: 'VertexAI',
};

function ProviderBadge({ provider, label, size = 'sm' }: ProviderBadgeProps) {
  const color = PROVIDER_COLORS[provider];
  const displayName = PROVIDER_DISPLAY[provider];

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/5 font-mono ${
        size === 'md' ? 'px-3 py-1.5 text-xs' : 'px-2.5 py-1 text-[11px]'
      }`}
    >
      <span
        className="rounded-full flex-shrink-0"
        style={{ width: 6, height: 6, backgroundColor: color, boxShadow: `0 0 6px ${color}` }}
      />
      <span className="text-slate-300">
        {displayName}
        <span className="text-slate-500 ml-1">· {label}</span>
      </span>
    </span>
  );
}

export default ProviderBadge;
