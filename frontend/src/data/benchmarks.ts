export interface IndustryBenchmark {
  id: string;
  label: string;
  color: string;
  alignment: number;   // avg keter alignment (0-100)
  harmony: number;     // avg tiferet harmony (0-100)
  readiness: number;   // avg yesod readiness (0-100)
  confidence: number;  // avg chochmah confidence (0-100)
  expansion: number;   // avg chesed expansion (0-100)
  riskIndex: number;   // avg ERI (0-100, computed)
  description: string;
}

export const INDUSTRY_BENCHMARKS: Record<string, IndustryBenchmark> = {
  technology: {
    id: 'technology',
    label: 'Technology',
    color: '#6366f1',
    alignment: 72,
    harmony: 65,
    readiness: 78,
    confidence: 74,
    expansion: 82,
    riskIndex: 29,
    description: 'Software, AI, SaaS, hardware companies',
  },
  pharmaceutical: {
    id: 'pharmaceutical',
    label: 'Pharmaceutical',
    color: '#10b981',
    alignment: 68,
    harmony: 70,
    readiness: 62,
    confidence: 80,
    expansion: 60,
    riskIndex: 32,
    description: 'Drug development, clinical trials, biotech',
  },
  finance: {
    id: 'finance',
    label: 'Finance',
    color: '#f59e0b',
    alignment: 60,
    harmony: 58,
    readiness: 71,
    confidence: 70,
    expansion: 65,
    riskIndex: 41,
    description: 'Banking, investment, insurance, fintech',
  },
  defense: {
    id: 'defense',
    label: 'Defense',
    color: '#ef4444',
    alignment: 48,
    harmony: 45,
    readiness: 68,
    confidence: 62,
    expansion: 40,
    riskIndex: 58,
    description: 'Military, weapons, surveillance, security',
  },
  energy: {
    id: 'energy',
    label: 'Energy',
    color: '#f97316',
    alignment: 55,
    harmony: 52,
    readiness: 65,
    confidence: 65,
    expansion: 58,
    riskIndex: 48,
    description: 'Oil, gas, renewable energy, utilities',
  },
  healthcare: {
    id: 'healthcare',
    label: 'Healthcare',
    color: '#3b82f6',
    alignment: 75,
    harmony: 72,
    readiness: 66,
    confidence: 78,
    expansion: 68,
    riskIndex: 27,
    description: 'Hospitals, medical devices, public health',
  },
};

export const BENCHMARK_LIST = Object.values(INDUSTRY_BENCHMARKS);

export function getBenchmarkRadarData(benchmark: IndustryBenchmark) {
  return [
    { subject: 'Keter', value: benchmark.alignment, fullMark: 100 },
    { subject: 'Chochmah', value: benchmark.confidence, fullMark: 100 },
    { subject: 'Binah', value: 70, fullMark: 100 },
    { subject: 'Chesed', value: benchmark.expansion, fullMark: 100 },
    { subject: 'Gevurah', value: 100 - benchmark.riskIndex, fullMark: 100 },
    { subject: 'Tiferet', value: benchmark.harmony, fullMark: 100 },
    { subject: 'Netzach', value: 65, fullMark: 100 },
    { subject: 'Hod', value: 68, fullMark: 100 },
    { subject: 'Yesod', value: benchmark.readiness, fullMark: 100 },
    { subject: 'Malchut', value: 70, fullMark: 100 },
  ];
}
