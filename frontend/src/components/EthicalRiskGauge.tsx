import { useMemo } from 'react';
import { motion } from 'framer-motion';
import type { SefirotResults } from '../types';
import { calculateERI, getERIBgClass } from '../utils/ethicalRiskIndex';

interface Props {
  sefirotResults: SefirotResults;
  compact?: boolean;
}

export function EthicalRiskGauge({ sefirotResults, compact = false }: Props) {
  const eri = useMemo(() => calculateERI(sefirotResults), [sefirotResults]);

  // SVG arc parameters
  const radius = compact ? 48 : 72;
  const strokeWidth = compact ? 8 : 12;
  const circumference = Math.PI * radius; // half-circle
  const progress = (eri.score / 100) * circumference;

  // Arc goes from 180° to 0° (left to right, bottom half)
  const cx = compact ? 60 : 90;
  const cy = compact ? 56 : 84;
  const svgW = cx * 2;
  const svgH = compact ? 70 : 100;

  // Gradient stops
  const gradientId = 'eri-gradient';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`rounded-xl border p-4 ${getERIBgClass(eri.score)} ${compact ? '' : 'p-6'}`}
    >
      {/* SVG Arc Gauge */}
      <div className="flex flex-col items-center">
        <svg width={svgW} height={svgH} viewBox={`0 0 ${svgW} ${svgH}`}>
          <defs>
            <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#34d399" />
              <stop offset="40%" stopColor="#facc15" />
              <stop offset="70%" stopColor="#fb923c" />
              <stop offset="100%" stopColor="#ef4444" />
            </linearGradient>
          </defs>
          {/* Background arc */}
          <path
            d={`M ${strokeWidth / 2} ${cy} A ${radius} ${radius} 0 0 1 ${svgW - strokeWidth / 2} ${cy}`}
            fill="none"
            stroke="rgba(255,255,255,0.1)"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />
          {/* Progress arc */}
          <path
            d={`M ${strokeWidth / 2} ${cy} A ${radius} ${radius} 0 0 1 ${svgW - strokeWidth / 2} ${cy}`}
            fill="none"
            stroke={`url(#${gradientId})`}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={`${progress} ${circumference}`}
          />
          {/* Score text */}
          <text
            x={cx}
            y={cy - 4}
            textAnchor="middle"
            fill={eri.hexColor}
            fontSize={compact ? 20 : 28}
            fontWeight="bold"
            fontFamily="monospace"
          >
            {eri.score}
          </text>
          <text
            x={cx}
            y={cy + (compact ? 10 : 14)}
            textAnchor="middle"
            fill="rgba(255,255,255,0.6)"
            fontSize={compact ? 8 : 10}
            fontFamily="sans-serif"
          >
            / 100
          </text>
        </svg>

        <div className="text-center -mt-1">
          <p className={`font-bold ${compact ? 'text-sm' : 'text-base'}`} style={{ color: eri.hexColor }}>
            {eri.label}
          </p>
          {!compact && (
            <p className="text-white/50 text-xs mt-0.5">Ethical Risk Index</p>
          )}
        </div>
      </div>

      {/* Component breakdown */}
      {!compact && (
        <div className="mt-4 space-y-2">
          <p className="text-white/50 text-xs uppercase tracking-wider">Score components</p>
          {eri.components.map((c) => (
            <div key={c.sefirah} className="flex items-center gap-2">
              <span className="text-white/60 text-xs w-32 truncate">{c.name}</span>
              <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{ width: `${c.rawScore}%`, backgroundColor: eri.hexColor, opacity: 0.7 }}
                />
              </div>
              <span className="text-white/60 text-xs w-8 text-right">{c.rawScore}</span>
              <span className="text-white/30 text-xs w-8 text-right">{Math.round(c.weight * 100)}%</span>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
