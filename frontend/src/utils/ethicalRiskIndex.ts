import type { SefirotResults } from '../types';

export interface ERIResult {
  score: number;           // 0-100 (higher = more risk)
  label: string;           // "Low Risk", "Moderate Risk", etc.
  color: string;           // Tailwind color class
  hexColor: string;        // Hex for inline styles
  components: ERIComponent[];
}

export interface ERIComponent {
  name: string;
  sefirah: string;
  weight: number;
  rawScore: number;        // Original 0-100 value from sefirah
  contribution: number;   // Weighted contribution to the positive sum
}

/**
 * Ethical Risk Index (ERI)
 *
 * ERI = 100 - WeightedAverage(positive_sefirot_scores)
 *
 * Higher ERI = more ethical risk
 * Lower ERI  = ethically sound / low risk
 */
export function calculateERI(sefirot: SefirotResults): ERIResult {
  const keterScore = Number(sefirot.keter?.alignment_percentage ?? 50);
  const tiferetScore = Number(sefirot.tiferet?.balance_score ?? 50);
  const yesodScore = Number(sefirot.yesod?.readiness_score ?? 50);
  const chochmahScore = Number(sefirot.chochmah?.confidence_level ?? 50);
  const chesedScore = Number(sefirot.chesed?.opportunity_score ?? 50);

  const components: ERIComponent[] = [
    { name: 'Ethical Alignment', sefirah: 'Keter', weight: 0.30, rawScore: keterScore, contribution: keterScore * 0.30 },
    { name: 'Harmony & Balance', sefirah: 'Tiferet', weight: 0.20, rawScore: tiferetScore, contribution: tiferetScore * 0.20 },
    { name: 'Readiness', sefirah: 'Yesod', weight: 0.20, rawScore: yesodScore, contribution: yesodScore * 0.20 },
    { name: 'Confidence', sefirah: 'Chochmah', weight: 0.15, rawScore: chochmahScore, contribution: chochmahScore * 0.15 },
    { name: 'Opportunity Potential', sefirah: 'Chesed', weight: 0.15, rawScore: chesedScore, contribution: chesedScore * 0.15 },
  ];

  const weightedSum = components.reduce((acc, c) => acc + c.contribution, 0);
  const score = Math.round(100 - weightedSum);

  return {
    score,
    label: getERILabel(score),
    color: getERIColorClass(score),
    hexColor: getERIHex(score),
    components,
  };
}

export function getERILabel(score: number): string {
  if (score <= 25) return 'Low Risk';
  if (score <= 50) return 'Moderate Risk';
  if (score <= 75) return 'High Risk';
  return 'Critical Risk';
}

export function getERIColorClass(score: number): string {
  if (score <= 25) return 'text-emerald-400';
  if (score <= 50) return 'text-yellow-400';
  if (score <= 75) return 'text-orange-400';
  return 'text-red-500';
}

export function getERIHex(score: number): string {
  if (score <= 25) return '#34d399';
  if (score <= 50) return '#facc15';
  if (score <= 75) return '#fb923c';
  return '#ef4444';
}

export function getERIBgClass(score: number): string {
  if (score <= 25) return 'bg-emerald-500/10 border-emerald-500/30';
  if (score <= 50) return 'bg-yellow-500/10 border-yellow-500/30';
  if (score <= 75) return 'bg-orange-500/10 border-orange-500/30';
  return 'bg-red-500/10 border-red-500/30';
}
