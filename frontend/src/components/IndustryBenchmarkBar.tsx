import { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Cell, ReferenceLine, ResponsiveContainer, LabelList,
} from 'recharts';
import { ChevronDown } from 'lucide-react';
import type { SefirotResults } from '../types';
import { BENCHMARK_LIST } from '../data/benchmarks';
import { calculateERI } from '../utils/ethicalRiskIndex';

interface Props {
  sefirotResults: SefirotResults;
  caseName?: string;
}

export function IndustryBenchmarkBar({ sefirotResults, caseName = 'This Scenario' }: Props) {
  const [open, setOpen] = useState(false);
  const scenarioERI = calculateERI(sefirotResults);

  const data = [
    {
      name: caseName.length > 14 ? caseName.slice(0, 12) + '…' : caseName,
      eri: scenarioERI.score,
      isScenario: true,
    },
    ...BENCHMARK_LIST.map((b) => ({
      name: b.label,
      eri: b.riskIndex,
      isScenario: false,
      color: b.color,
    })),
  ];

  const getBarColor = (entry: { isScenario: boolean; color?: string }) =>
    entry.isScenario ? '#a78bfa' : (entry.color ?? '#6b7280');

  return (
    <div className="w-full">
      {/* Legend pill */}
      <div className="flex items-center gap-3 mb-3">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-purple-400" />
          <span className="text-white/50 text-xs">This scenario</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-gray-500" />
          <span className="text-white/50 text-xs">Industry avg ERI</span>
        </div>
        <button
          onClick={() => setOpen(!open)}
          className="ml-auto flex items-center gap-1 text-xs text-white/40 hover:text-white/70 transition-colors"
        >
          What is ERI? <ChevronDown size={12} className={`transition-transform ${open ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {open && (
        <div className="mb-3 p-3 rounded-lg bg-white/5 border border-white/10 text-xs text-white/60 leading-relaxed">
          <strong className="text-white/80">Ethical Risk Index (ERI)</strong> — composite score derived from 5 sefirot:
          Keter alignment (30%), Tiferet harmony (20%), Yesod readiness (20%),
          Chochmah confidence (15%), Chesed opportunity (15%).
          Higher ERI = higher ethical risk. Lower ERI = ethically sound.
        </div>
      )}

      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} margin={{ top: 16, right: 16, bottom: 4, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
          <XAxis
            dataKey="name"
            tick={{ fill: 'rgba(255,255,255,0.6)', fontSize: 10 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 9 }}
            axisLine={false}
            tickLine={false}
            tickCount={5}
          />
          <ReferenceLine y={50} stroke="rgba(255,255,255,0.15)" strokeDasharray="4 2" label={{ value: 'Moderate', fill: 'rgba(255,255,255,0.3)', fontSize: 9 }} />
          <Tooltip
            contentStyle={{
              background: '#1e1b4b',
              border: '1px solid rgba(167,139,250,0.3)',
              borderRadius: 8,
              color: '#e2e8f0',
              fontSize: 12,
            }}
            formatter={(v: number) => [`${v} ERI`, 'Ethical Risk Index']}
          />
          <Bar dataKey="eri" radius={[4, 4, 0, 0]} maxBarSize={52}>
            {data.map((entry, index) => (
              <Cell key={index} fill={getBarColor(entry)} opacity={entry.isScenario ? 1 : 0.6} />
            ))}
            <LabelList
              dataKey="eri"
              position="top"
              style={{ fill: 'rgba(255,255,255,0.5)', fontSize: 10 }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
