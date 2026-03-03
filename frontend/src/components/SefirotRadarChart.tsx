import { useMemo } from 'react';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import type { SefirotResults } from '../types';
import { INDUSTRY_BENCHMARKS, getBenchmarkRadarData } from '../data/benchmarks';

interface Props {
  sefirotResults: SefirotResults;
  benchmarkIndustry?: string;
}

function toNum(v: unknown, fallback = 50): number {
  const n = Number(v);
  return isNaN(n) ? fallback : Math.min(100, Math.max(0, n));
}

export function SefirotRadarChart({ sefirotResults: s, benchmarkIndustry }: Props) {
  const scenarioData = useMemo(() => [
    { subject: 'Keter', value: toNum(s.keter?.alignment_percentage), fullMark: 100 },
    { subject: 'Chochmah', value: toNum(s.chochmah?.confidence_level), fullMark: 100 },
    { subject: 'Binah', value: toNum(s.binah?.contextual_depth_score), fullMark: 100 },
    { subject: 'Chesed', value: toNum(s.chesed?.opportunity_score), fullMark: 100 },
    { subject: 'Gevurah', value: 100 - toNum(s.gevurah?.risk_score), fullMark: 100 },
    { subject: 'Tiferet', value: toNum(s.tiferet?.balance_score), fullMark: 100 },
    { subject: 'Netzach', value: toNum(s.netzach?.strategy_score), fullMark: 100 },
    { subject: 'Hod', value: toNum(s.hod?.communication_score), fullMark: 100 },
    { subject: 'Yesod', value: toNum(s.yesod?.readiness_score), fullMark: 100 },
    { subject: 'Malchut', value: toNum(s.malchut?.confidence_level), fullMark: 100 },
  ], [s]);

  const benchmark = benchmarkIndustry ? INDUSTRY_BENCHMARKS[benchmarkIndustry] : null;
  const benchmarkData = benchmark ? getBenchmarkRadarData(benchmark) : null;

  // Merge scenario + benchmark into single data array for recharts
  const chartData = scenarioData.map((d, i) => ({
    ...d,
    benchmark: benchmarkData ? benchmarkData[i].value : undefined,
  }));

  return (
    <div className="w-full">
      <ResponsiveContainer width="100%" height={320}>
        <RadarChart data={chartData} margin={{ top: 10, right: 20, bottom: 10, left: 20 }}>
          <PolarGrid stroke="rgba(255,255,255,0.1)" />
          <PolarAngleAxis
            dataKey="subject"
            tick={{ fill: 'rgba(255,255,255,0.7)', fontSize: 11 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 9 }}
            tickCount={4}
          />
          <Radar
            name="This Scenario"
            dataKey="value"
            stroke="#a78bfa"
            fill="#a78bfa"
            fillOpacity={0.25}
            strokeWidth={2}
          />
          {benchmarkData && (
            <Radar
              name={`${benchmark!.label} Avg`}
              dataKey="benchmark"
              stroke="#fbbf24"
              fill="#fbbf24"
              fillOpacity={0.08}
              strokeWidth={1.5}
              strokeDasharray="4 2"
            />
          )}
          <Tooltip
            contentStyle={{
              background: '#1e1b4b',
              border: '1px solid rgba(167,139,250,0.3)',
              borderRadius: 8,
              color: '#e2e8f0',
              fontSize: 12,
            }}
            formatter={(value: number, name: string) => [`${value}/100`, name]}
          />
          {benchmarkData && <Legend wrapperStyle={{ fontSize: 11, color: 'rgba(255,255,255,0.6)' }} />}
        </RadarChart>
      </ResponsiveContainer>
      <p className="text-center text-white/30 text-xs mt-1">
        Gevurah shown inverted (higher = lower risk)
      </p>
    </div>
  );
}
