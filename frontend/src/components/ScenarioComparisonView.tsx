import { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer,
} from 'recharts';
import { Download, RotateCcw, Loader2 } from 'lucide-react';
import type { AnalysisResponse } from '../types';
import { calculateERI, getERILabel, getERIHex } from '../utils/ethicalRiskIndex';

interface ScenarioResult {
  label: string;
  caseName: string;
  analysis: AnalysisResponse;
}

interface Props {
  scenarios: ScenarioResult[];
  onReset: () => void;
}

const COLORS = ['#a78bfa', '#34d399', '#fb923c'];
const LABELS_BG = ['bg-purple-500/20 text-purple-300', 'bg-emerald-500/20 text-emerald-300', 'bg-orange-500/20 text-orange-300'];

const DECISION_BADGE: Record<string, string> = {
  GO: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
  NO_GO: 'bg-red-500/20 text-red-300 border-red-500/30',
  CONDITIONAL_GO: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
};

function toNum(v: unknown, fb = 0): number {
  const n = Number(v);
  return isNaN(n) ? fb : n;
}

export function ScenarioComparisonView({ scenarios, onReset }: Props) {
  const reportRef = useRef<HTMLDivElement>(null);
  const [downloading, setDownloading] = useState(false);

  const eris = scenarios.map((s) => calculateERI(s.analysis.sefirot_results));

  const metricsRows = [
    { label: 'Ethical Risk Index', values: eris.map((e) => e.score), lowerBetter: true },
    { label: 'Keter — Alignment %', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.keter?.alignment_percentage)), lowerBetter: false },
    { label: 'Tiferet — Harmony', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.tiferet?.balance_score)), lowerBetter: false },
    { label: 'Yesod — Readiness', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.yesod?.readiness_score)), lowerBetter: false },
    { label: 'Chochmah — Confidence', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.chochmah?.confidence_level)), lowerBetter: false },
    { label: 'Chesed — Opportunity', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.chesed?.opportunity_score)), lowerBetter: false },
    { label: 'Gevurah — Risk Score', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.gevurah?.risk_score)), lowerBetter: true },
    { label: 'Netzach — Strategy', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.netzach?.strategy_score)), lowerBetter: false },
    { label: 'Hod — Communication', values: scenarios.map((s) => toNum(s.analysis.sefirot_results.hod?.communication_score)), lowerBetter: false },
  ];

  // Recharts grouped bar data
  const sefirotChartData = [
    { name: 'Keter', ...Object.fromEntries(scenarios.map((s) => [s.label, toNum(s.analysis.sefirot_results.keter?.alignment_percentage)])) },
    { name: 'Chochmah', ...Object.fromEntries(scenarios.map((s) => [s.label, toNum(s.analysis.sefirot_results.chochmah?.confidence_level)])) },
    { name: 'Tiferet', ...Object.fromEntries(scenarios.map((s) => [s.label, toNum(s.analysis.sefirot_results.tiferet?.balance_score)])) },
    { name: 'Yesod', ...Object.fromEntries(scenarios.map((s) => [s.label, toNum(s.analysis.sefirot_results.yesod?.readiness_score)])) },
    { name: 'Chesed', ...Object.fromEntries(scenarios.map((s) => [s.label, toNum(s.analysis.sefirot_results.chesed?.opportunity_score)])) },
    { name: 'Netzach', ...Object.fromEntries(scenarios.map((s) => [s.label, toNum(s.analysis.sefirot_results.netzach?.strategy_score)])) },
    { name: 'Hod', ...Object.fromEntries(scenarios.map((s) => [s.label, toNum(s.analysis.sefirot_results.hod?.communication_score)])) },
  ];

  const handleDownload = async () => {
    if (!reportRef.current) return;
    setDownloading(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { jsPDF } = await import('jspdf');
      const canvas = await html2canvas(reportRef.current, { scale: 1.5, useCORS: true, backgroundColor: '#0f0e1a' });
      const pdf = new jsPDF('l', 'mm', 'a4');
      const imgData = canvas.toDataURL('image/png');
      const pageW = 297;
      const pageH = (canvas.height / canvas.width) * pageW;
      pdf.addImage(imgData, 'PNG', 0, 0, pageW, Math.min(pageH, 210));
      pdf.save(`TikunOlam_Comparison_${new Date().toISOString().slice(0, 10)}.pdf`);
    } finally {
      setDownloading(false);
    }
  };

  const getBest = (values: number[], lowerBetter: boolean) => {
    if (lowerBetter) return Math.min(...values);
    return Math.max(...values);
  };

  return (
    <div className="space-y-6">
      {/* Action bar */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Comparison Results</h2>
        <div className="flex gap-2">
          <button
            onClick={onReset}
            className="flex items-center gap-2 px-4 py-2 rounded-lg border border-white/10 text-white/50 hover:text-white/80 text-sm"
          >
            <RotateCcw size={14} /> New Comparison
          </button>
          <button
            onClick={handleDownload}
            disabled={downloading}
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold disabled:opacity-50"
            style={{ background: 'linear-gradient(135deg, #7c3aed, #a78bfa)' }}
          >
            {downloading ? <Loader2 size={14} className="animate-spin" /> : <Download size={14} />}
            Export PDF
          </button>
        </div>
      </div>

      <div ref={reportRef} className="space-y-6">
        {/* Decision header cards */}
        <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${scenarios.length}, 1fr)` }}>
          {scenarios.map((s, i) => {
            const decision = s.analysis.sefirot_results.malchut?.decision || s.analysis.summary?.final_decision || 'PENDING';
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="rounded-xl border border-white/10 bg-white/5 p-5"
                style={{ borderTopColor: COLORS[i], borderTopWidth: 3 }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${LABELS_BG[i]}`}>{s.label}</span>
                  <span className="text-white/60 text-sm truncate">{s.caseName}</span>
                </div>
                <div className={`inline-block px-3 py-1 rounded-full text-xs font-bold border ${DECISION_BADGE[decision] ?? 'bg-white/10 text-white/60 border-white/10'}`}>
                  {decision.replace('_', ' ')}
                </div>
                <div className="mt-3 flex items-center gap-2">
                  <span className="text-white/40 text-xs">ERI</span>
                  <span className="text-lg font-bold" style={{ color: getERIHex(eris[i].score) }}>
                    {eris[i].score}
                  </span>
                  <span className="text-xs" style={{ color: getERIHex(eris[i].score) }}>{getERILabel(eris[i].score)}</span>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Metrics comparison table */}
        <div className="rounded-xl border border-white/10 bg-white/5 overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 bg-white/5">
                <th className="text-left px-4 py-3 text-white/50 font-medium">Metric</th>
                {scenarios.map((s, i) => (
                  <th key={i} className="text-center px-4 py-3 font-semibold" style={{ color: COLORS[i] }}>
                    Scenario {s.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {metricsRows.map((row, ri) => {
                const best = getBest(row.values, row.lowerBetter);
                return (
                  <tr key={ri} className={`border-b border-white/5 ${ri % 2 === 0 ? 'bg-white/[0.02]' : ''}`}>
                    <td className="px-4 py-2.5 text-white/60">{row.label}</td>
                    {row.values.map((v, vi) => (
                      <td key={vi} className="text-center px-4 py-2.5">
                        <span
                          className={`font-bold ${v === best ? 'text-white' : 'text-white/40'}`}
                        >
                          {v}
                          {v === best && (
                            <span className="ml-1 text-xs" style={{ color: COLORS[vi] }}>★</span>
                          )}
                        </span>
                      </td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
          <p className="px-4 py-2 text-white/30 text-xs">★ Best value per row</p>
        </div>

        {/* Grouped bar chart */}
        <div className="rounded-xl border border-white/10 bg-white/5 p-5">
          <h3 className="text-white/70 text-sm font-semibold mb-4">Sefirot Score Comparison</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={sefirotChartData} margin={{ top: 4, right: 8, bottom: 4, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
              <XAxis dataKey="name" tick={{ fill: 'rgba(255,255,255,0.5)', fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis domain={[0, 100]} tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 9 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: '#1e1b4b', border: '1px solid rgba(167,139,250,0.3)', borderRadius: 8, color: '#e2e8f0', fontSize: 12 }}
              />
              <Legend wrapperStyle={{ fontSize: 11, color: 'rgba(255,255,255,0.6)' }} />
              {scenarios.map((s, i) => (
                <Bar key={i} dataKey={s.label} name={`Scenario ${s.label}`} fill={COLORS[i]} radius={[3, 3, 0, 0]} maxBarSize={32} fillOpacity={0.8} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
