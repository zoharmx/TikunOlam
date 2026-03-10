import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle,
  XCircle,
  AlertTriangle,
  TrendingUp,
  Shield,
  Lightbulb,
  Share2,
  Printer,
  Clock,
  Cpu,
  FileText,
  Loader2,
  BarChart2,
  Lock,
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import ProviderBadge from './ProviderBadge';
import BinahSigmaView from './BinahSigmaView';

// ─── Admin detection ────────────────────────────────────────────────────────
// Set VITE_ADMIN_EMAIL in your .env.local to enable admin view
const ADMIN_EMAIL = import.meta.env.VITE_ADMIN_EMAIL || '';
import { EthicalRiskGauge } from './EthicalRiskGauge';
import { SefirotRadarChart } from './SefirotRadarChart';
import { IndustryBenchmarkBar } from './IndustryBenchmarkBar';
import { ExecutiveReportTemplate } from './ExecutiveReportTemplate';
import { calculateERI, getERIHex } from '../utils/ethicalRiskIndex';
import { BENCHMARK_LIST } from '../data/benchmarks';
import { PROVIDER_LABELS } from '../types';
import type { ProviderKey } from '../types';

interface ResultsProps {
  results: any;
  onReset: () => void;
}

const SEFIRAH_PRIMARY_KEY: Record<string, string> = {
  keter:    'alignment_percentage',
  chochmah: 'confidence_level',
  binah:    'contextual_depth_score',
  chesed:   'generosity_score',
  gevurah:  'constraint_strength',
  tiferet:  'harmony_score',
  netzach:  'persistence_score',
  hod:      'clarity_score',
  yesod:    'readiness_score',
  malchut:  'manifestation_quality',
};

const SEFIRAH_FALLBACK_KEYS: Record<string, string[]> = {
  chochmah: ['insight_depth_score', 'epistemic_humility_ratio'],
  chesed:   ['expansion_potential'],
  gevurah:  ['risk_score'],
  tiferet:  ['balance_score'],
};

const QUALITY_TO_INT: Record<string, number> = {
  poor: 25, acceptable: 50, good: 75, excellent: 100,
};

function getSefirahScore(name: string, data: any): number | null {
  if (!data) return null;
  const key = name.toLowerCase();
  const keys = [SEFIRAH_PRIMARY_KEY[key], ...(SEFIRAH_FALLBACK_KEYS[key] ?? [])].filter(Boolean);
  for (const field of keys) {
    const val = data[field];
    if (val == null) continue;
    if (typeof val === 'number') return Math.round(val);
    if (typeof val === 'string') {
      const converted = QUALITY_TO_INT[val.toLowerCase()];
      if (converted != null) return converted;
      const parsed = parseFloat(val);
      if (!isNaN(parsed)) return Math.round(parsed);
    }
  }
  return null;
}

function Results({ results, onReset }: ResultsProps) {
  const { user } = useAuth();
  const isAdmin = Boolean(user?.email && ADMIN_EMAIL && user.email === ADMIN_EMAIL);

  const [activeTab, setActiveTab] = useState<'summary' | 'sefirot' | 'binah' | 'executive'>('summary');
  const [selectedIndustry, setSelectedIndustry] = useState<string>('technology');
  const [pdfLoading, setPdfLoading] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  // Safely destructure with fallbacks
  const sefirot_results = results?.sefirot_results || {};
  const metadata = results?.metadata || {};

  // CRITICAL FIX: Generate all required fields from sefirot_results
  // Backend only provides: sefirot_results, metadata, scenario
  // Frontend needs: case_name, summary, sefirot_results, metadata
  
  const malchut = sefirot_results?.malchut || {};
  const keter = sefirot_results?.keter || {};
  const gevurah = sefirot_results?.gevurah || {};
  const chesed = sefirot_results?.chesed || {};
  const binah = sefirot_results?.binah || {};
  const tiferet = sefirot_results?.tiferet || {};

  // Generate summary from sefirot_results (backend doesn't provide it)
  const summary = {
    final_decision: malchut.decision || 'PROCESSING',
    overall_alignment: keter.alignment_percentage || 0,
    key_risks: (gevurah.risks || [])
      .map((r: any) => {
        if (typeof r === 'string') return r;
        if (r.description) return r.description;
        if (r.risk) return r.risk;
        return JSON.stringify(r);
      })
      .filter(Boolean)
      .slice(0, 3),
    key_opportunities: (chesed.opportunities || [])
      .map((o: any) => {
        if (typeof o === 'string') return o;
        if (o.description) return o.description;
        if (o.opportunity) return o.opportunity;
        return JSON.stringify(o);
      })
      .filter(Boolean)
      .slice(0, 3),
    recommendation: malchut.reasoning || tiferet.synthesis || malchut.decision || 'Analysis in progress'
  };

  // Extract case_name from metadata or scenario
  const case_name = metadata?.case_name || metadata?.scenario || results.scenario || 'Tikun Olam Analysis';

  const isBinahSigma = binah?.mode === 'sigma';

  const getDecisionColor = (decision: string) => {
    if (decision.includes('GO') && !decision.includes('NO')) {
      return 'text-green-400';
    } else if (decision.includes('NO_GO')) {
      return 'text-red-400';
    } else {
      return 'text-yellow-400';
    }
  };

  const getDecisionIcon = (decision: string) => {
    if (decision.includes('GO') && !decision.includes('NO')) {
      return <CheckCircle className="w-8 h-8" />;
    } else if (decision.includes('NO_GO')) {
      return <XCircle className="w-8 h-8" />;
    } else {
      return <AlertTriangle className="w-8 h-8" />;
    }
  };

  const handlePrint = () => {
    if (!reportRef.current) { window.print(); return; }
    const printWindow = window.open('', '_blank', 'width=900,height=700');
    if (!printWindow) { window.print(); return; }
    const content = reportRef.current.outerHTML;
    printWindow.document.write(
      `<!DOCTYPE html><html><head><meta charset="utf-8">` +
      `<title>${case_name || 'Tikun Olam Report'}</title>` +
      `<style>*{box-sizing:border-box;}body{background:#fff;margin:0;padding:0;}` +
      `@page{size:A4 portrait;margin:0;}</style></head>` +
      `<body>${content}</body></html>`
    );
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => { printWindow.print(); printWindow.close(); }, 600);
  };

  const handleDownloadPDF = async () => {
    if (!reportRef.current) return;
    setPdfLoading(true);
    try {
      const { default: html2canvas } = await import('html2canvas');
      const { jsPDF } = await import('jspdf');

      // El elemento esta oculto a -9999px. Lo movemos al viewport con z-index alto
      // para que el navegador lo pinte antes de que html2canvas lo capture.
      const wrapper = reportRef.current.parentElement!;
      const origStyle = wrapper.style.cssText;
      wrapper.style.cssText =
        'position:fixed;top:0;left:0;width:794px;pointer-events:none;z-index:99999;opacity:0.01;';
      // Esperar dos frames para que el navegador pinte el elemento
      await new Promise<void>((r) => requestAnimationFrame(() => requestAnimationFrame(() => r())));

      const canvas = await html2canvas(reportRef.current, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        width: 794,
      });

      wrapper.style.cssText = origStyle;

      if (canvas.width === 0 || canvas.height === 0) {
        throw new Error('Canvas tiene dimensiones cero - el elemento no fue renderizado');
      }

      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageW = 210; // mm
      const pageH = 297; // mm
      const pxPerMm = canvas.width / pageW;
      const totalHeightMm = canvas.height / pxPerMm;

      let yMm = 0;
      while (yMm < totalHeightMm) {
        const sliceHeightMm = Math.min(pageH, totalHeightMm - yMm);
        const sourceYPx = Math.round(yMm * pxPerMm);
        const sliceHeightPx = Math.round(sliceHeightMm * pxPerMm);

        const sliceCanvas = document.createElement('canvas');
        sliceCanvas.width = canvas.width;
        sliceCanvas.height = sliceHeightPx;
        const ctx = sliceCanvas.getContext('2d')!;
        ctx.drawImage(canvas, 0, -sourceYPx);

        if (yMm > 0) pdf.addPage();
        pdf.addImage(
          sliceCanvas.toDataURL('image/png'),
          'PNG',
          0, 0,
          pageW,
          sliceHeightMm
        );
        yMm += pageH;
      }

      const safeName = case_name.replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 40);
      pdf.save(`TikunOlam_${safeName}_${new Date().toISOString().slice(0, 10)}.pdf`);
    } catch (err) {
      console.error('[PDF] Generation failed:', err);
      alert('No se pudo generar el PDF. Usa el boton Imprimir y selecciona "Guardar como PDF" desde el navegador.');
    } finally {
      setPdfLoading(false);
    }
  };

  // Sanitized summary export — no pipeline internals
  const handleShare = () => {
    const sefirotScores: Record<string, number | null> = {};
    Object.entries(sefirot_results).forEach(([name, data]: [string, any]) => {
      sefirotScores[name] = getSefirahScore(name, data);
    });
    const sanitized = {
      case_name,
      final_decision: summary.final_decision,
      overall_alignment: summary.overall_alignment,
      key_risks: summary.key_risks,
      key_opportunities: summary.key_opportunities,
      sefirot_scores: sefirotScores,
      analysis_date: metadata?.timestamp
        ? new Date(metadata.timestamp).toLocaleDateString()
        : new Date().toLocaleDateString(),
      framework: 'Tikun Olam — Ethical AI Framework',
      providers: '6 AI Providers',
    };
    const blob = new Blob([JSON.stringify(sanitized, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tikun-summary-${case_name.replace(/\s/g, '_').slice(0, 30)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Admin-only: full pipeline export
  const handleAdminDownload = () => {
    if (!isAdmin) return;
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tikun-FULL-${case_name.replace(/\s/g, '_').slice(0, 30)}-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Rounded duration for public display
  const durationDisplay = metadata?.total_duration_seconds
    ? `~${Math.ceil(metadata.total_duration_seconds / 60)} min`
    : null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h2 className="text-2xl font-bold text-white">Analysis Results</h2>
            <p className="text-slate-400 text-sm">
              {case_name} · {metadata?.timestamp ? new Date(metadata.timestamp).toLocaleString() : new Date().toLocaleString()}
            </p>
            {/* Duration + provider count */}
            <div className="flex items-center gap-3 mt-2 flex-wrap">
              {durationDisplay && (
                <span className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Clock size={11} />
                  {durationDisplay}
                </span>
              )}
              <span className="flex items-center gap-1.5 text-xs text-slate-500">
                <Cpu size={11} />
                6 AI Providers
              </span>
              {isAdmin && (
                <span className="flex items-center gap-1 text-xs text-violet-400 bg-violet-500/10 border border-violet-500/30 px-2 py-0.5 rounded-full">
                  <Lock size={10} /> Admin
                </span>
              )}
            </div>
            {/* Provider attribution — admin sees exact models, users see provider names */}
            {metadata?.models_used && (
              <div className="flex flex-wrap gap-1.5 mt-3">
                {isAdmin
                  ? Array.from(new Set(Object.values(metadata.models_used as Record<string, string>))).map((model) => {
                      const providerKey = PROVIDER_LABELS[model as string] as ProviderKey | undefined;
                      if (!providerKey) return null;
                      return <ProviderBadge key={model} provider={providerKey} label={model as string} size="sm" />;
                    })
                  : Array.from(new Set(Object.values(metadata.models_used as Record<string, string>))).map((model) => {
                      const providerKey = PROVIDER_LABELS[model as string] as ProviderKey | undefined;
                      if (!providerKey) return null;
                      return <ProviderBadge key={model} provider={providerKey} label={providerKey} size="sm" />;
                    })
                }
              </div>
            )}
          </div>
          <div className="flex gap-3 items-center flex-wrap">
            {/* ERI badge */}
            {sefirot_results && (() => {
              const eri = calculateERI(sefirot_results as any);
              return (
                <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5">
                  <BarChart2 size={13} style={{ color: getERIHex(eri.score) }} />
                  <span className="text-xs font-bold" style={{ color: getERIHex(eri.score) }}>ERI {eri.score}</span>
                  <span className="text-white/40 text-xs">{eri.label}</span>
                </div>
              );
            })()}
            <button
              onClick={handleDownloadPDF}
              disabled={pdfLoading}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg font-medium text-sm transition-all disabled:opacity-50"
              style={{ background: 'linear-gradient(135deg, #7c3aed88, #a78bfa88)' }}
              title="Download Board-ready PDF"
            >
              {pdfLoading ? <Loader2 size={14} className="animate-spin" /> : <FileText size={14} />}
              PDF Report
            </button>
            <button
              onClick={handlePrint}
              className="p-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
              title="Print"
            >
              <Printer className="w-5 h-5 text-slate-300" />
            </button>
            <button
              onClick={handleShare}
              className="p-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
              title="Export Summary JSON"
            >
              <Share2 className="w-5 h-5 text-slate-300" />
            </button>
            {/* Admin-only: full pipeline export */}
            {isAdmin && (
              <button
                onClick={handleAdminDownload}
                className="p-2 bg-violet-900/40 hover:bg-violet-800/60 border border-violet-500/30 rounded-lg transition-colors"
                title="[Admin] Download Full Pipeline JSON"
              >
                <Lock className="w-4 h-4 text-violet-400" />
              </button>
            )}
            <button
              onClick={onReset}
              className="px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 rounded-lg font-medium transition-all"
            >
              New Analysis
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-700">
        <button
          onClick={() => setActiveTab('summary')}
          className={`px-6 py-3 font-medium transition-all ${
            activeTab === 'summary'
              ? 'text-white border-b-2 border-purple-500'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          Summary
        </button>
        <button
          onClick={() => setActiveTab('sefirot')}
          className={`px-6 py-3 font-medium transition-all ${
            activeTab === 'sefirot'
              ? 'text-white border-b-2 border-purple-500'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          10 Sefirot
        </button>
        {isBinahSigma && (
          <button
            onClick={() => setActiveTab('binah')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'binah'
                ? 'text-white border-b-2 border-purple-500'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            BinahSigma Analysis
          </button>
        )}
        <button
          onClick={() => setActiveTab('executive')}
          className={`px-6 py-3 font-medium transition-all flex items-center gap-1.5 ${
            activeTab === 'executive'
              ? 'text-white border-b-2 border-purple-500'
              : 'text-slate-400 hover:text-white'
          }`}
        >
          <BarChart2 size={14} />
          Executive
        </button>
      </div>

      {/* Content */}
      <AnimatePresence mode="wait">
        {activeTab === 'summary' && (
          <motion.div
            key="summary"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            {/* Decision Card */}
            <div className={`backdrop-blur-sm border rounded-xl p-8 ${
              summary.final_decision.includes('NO_GO') && !summary.final_decision.includes('CONDITIONAL')
                ? 'bg-gradient-to-br from-red-950/40 to-slate-900/50 border-red-500/20'
                : summary.final_decision === 'GO'
                ? 'bg-gradient-to-br from-green-950/40 to-slate-900/50 border-green-500/20'
                : 'bg-gradient-to-br from-yellow-950/30 to-slate-900/50 border-yellow-500/20'
            }`}>
              <div className="flex items-center gap-4 mb-6">
                <div className={getDecisionColor(summary.final_decision)}>
                  {getDecisionIcon(summary.final_decision)}
                </div>
                <div>
                  <h3 className="text-sm font-medium text-slate-400">Final Decision</h3>
                  <p className={`text-3xl font-bold ${getDecisionColor(summary.final_decision)}`}>
                    {summary.final_decision}
                  </p>
                </div>
              </div>
              
              <div className="mb-6">
                <h4 className="text-sm font-medium text-slate-400 mb-2">Overall Alignment</h4>
                <div className="flex items-center gap-4">
                  <div className="flex-1 bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-full rounded-full transition-all ${
                        summary.overall_alignment >= 70
                          ? 'bg-green-500'
                          : summary.overall_alignment >= 40
                          ? 'bg-yellow-500'
                          : 'bg-red-500'
                      }`}
                      style={{ width: `${summary.overall_alignment}%` }}
                    />
                  </div>
                  <span className="text-2xl font-bold text-white">
                    {summary.overall_alignment}%
                  </span>
                </div>
              </div>

              <div className="bg-slate-800/50 rounded-lg p-4">
                <h4 className="text-sm font-medium text-slate-400 mb-2">Recommendation</h4>
                <p className="text-white leading-relaxed">{summary.recommendation}</p>
              </div>
            </div>

            {/* Risks and Opportunities Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Key Risks */}
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <Shield className="w-6 h-6 text-red-400" />
                  <h3 className="text-xl font-bold text-white">Key Risks</h3>
                </div>
                <div className="space-y-3">
                  {summary.key_risks && summary.key_risks.length > 0 ? (
                    summary.key_risks.map((risk: string, idx: number) => (
                      <div key={idx} className="flex items-start gap-3 bg-slate-900/50 rounded-lg p-3">
                        <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        <p className="text-slate-300 text-sm">{risk}</p>
                      </div>
                    ))
                  ) : (
                    <p className="text-slate-500 text-sm italic">No significant risks identified</p>
                  )}
                </div>
              </div>

              {/* Key Opportunities */}
              <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <Lightbulb className="w-6 h-6 text-green-400" />
                  <h3 className="text-xl font-bold text-white">Key Opportunities</h3>
                </div>
                <div className="space-y-3">
                  {summary.key_opportunities && summary.key_opportunities.length > 0 ? (
                    summary.key_opportunities.map((opp: string, idx: number) => (
                      <div key={idx} className="flex items-start gap-3 bg-slate-900/50 rounded-lg p-3">
                        <TrendingUp className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                        <p className="text-slate-300 text-sm">{opp}</p>
                      </div>
                    ))
                  ) : (
                    <p className="text-slate-500 text-sm italic">No specific opportunities identified</p>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'sefirot' && (
          <motion.div
            key="sefirot"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-3"
          >
            <div className="grid sm:grid-cols-2 gap-3">
              {Object.entries(sefirot_results || {}).map(([name, data]: [string, any]) => {
                const score = getSefirahScore(name, data);
                const decision = data?.decision || null;
                const scoreColor = score == null ? '#64748b' : score >= 70 ? '#22c55e' : score >= 40 ? '#eab308' : '#ef4444';
                return (
                  <div key={name} className="bg-slate-800/50 border border-slate-700 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-white capitalize">{name}</h3>
                      {score != null && (
                        <span className="text-lg font-bold font-mono" style={{ color: scoreColor }}>{score}</span>
                      )}
                    </div>
                    {decision && (
                      <span className="text-xs text-slate-400 bg-slate-700/50 px-2 py-0.5 rounded">{decision}</span>
                    )}
                    {score != null && (
                      <div className="mt-2 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all" style={{ width: `${score}%`, backgroundColor: scoreColor }} />
                      </div>
                    )}
                    {/* Admin: raw data */}
                    {isAdmin && (
                      <details className="mt-3">
                        <summary className="text-xs text-violet-400 cursor-pointer flex items-center gap-1">
                          <Lock size={10} /> Raw pipeline data
                        </summary>
                        <pre className="mt-2 text-xs text-slate-400 overflow-x-auto bg-slate-900/50 rounded p-3 max-h-48">
                          {JSON.stringify(data, null, 2)}
                        </pre>
                      </details>
                    )}
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}

        {activeTab === 'binah' && isBinahSigma && (
          <motion.div
            key="binah"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <BinahSigmaView binah={binah} />
          </motion.div>
        )}

        {activeTab === 'executive' && (
          <motion.div
            key="executive"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            {/* Industry selector + download */}
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div className="flex items-center gap-3">
                <span className="text-white/50 text-sm">Compare vs industry:</span>
                <select
                  value={selectedIndustry}
                  onChange={(e) => setSelectedIndustry(e.target.value)}
                  className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-purple-500/50"
                >
                  {BENCHMARK_LIST.map((b) => (
                    <option key={b.id} value={b.id} style={{ background: '#1e1b4b' }}>{b.label}</option>
                  ))}
                </select>
              </div>
              <button
                onClick={handleDownloadPDF}
                disabled={pdfLoading}
                className="flex items-center gap-2 px-5 py-2 rounded-xl font-semibold text-sm transition-all disabled:opacity-50"
                style={{ background: 'linear-gradient(135deg, #7c3aed, #a78bfa)' }}
              >
                {pdfLoading ? <Loader2 size={14} className="animate-spin" /> : <FileText size={14} />}
                Download Board PDF
              </button>
            </div>

            {/* ERI + Radar row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div className="lg:col-span-1">
                <EthicalRiskGauge sefirotResults={sefirot_results as any} />
              </div>
              <div className="lg:col-span-2 bg-slate-800/50 border border-slate-700 rounded-xl p-5">
                <h3 className="text-white/70 text-sm font-semibold mb-2 flex items-center gap-2">
                  <BarChart2 size={14} /> Sefirot Radar — Scenario vs {BENCHMARK_LIST.find(b => b.id === selectedIndustry)?.label} avg
                </h3>
                <SefirotRadarChart sefirotResults={sefirot_results as any} benchmarkIndustry={selectedIndustry} />
              </div>
            </div>

            {/* Industry Benchmark Bar */}
            <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-5">
              <h3 className="text-white/70 text-sm font-semibold mb-4">Ethical Risk Index vs Industry Benchmarks</h3>
              <IndustryBenchmarkBar sefirotResults={sefirot_results as any} caseName={case_name} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Hidden PDF template */}
      <div style={{ position: 'absolute', left: '-9999px', top: 0, zIndex: -1 }}>
        <ExecutiveReportTemplate
          ref={reportRef}
          analysis={{ sefirot_results, summary, metadata, case_name, status: 'completed', timestamp: metadata?.timestamp || '' } as any}
          industry={selectedIndustry}
        />
      </div>
    </motion.div>
  );
}

export default Results;