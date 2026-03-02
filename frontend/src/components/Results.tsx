import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle,
  XCircle,
  AlertTriangle,
  TrendingUp,
  Shield,
  Lightbulb,
  Download,
  Share2,
  Printer,
  Clock,
  Cpu
} from 'lucide-react';
import ProviderBadge from './ProviderBadge';
import BinahSigmaView from './BinahSigmaView';
import { PROVIDER_LABELS } from '../types';
import type { ProviderKey } from '../types';

interface ResultsProps {
  results: any;
  onReset: () => void;
}

function Results({ results, onReset }: ResultsProps) {
  console.log('🎨 Results component MOUNTING with data:', results);

  const [activeTab, setActiveTab] = useState<'summary' | 'sefirot' | 'binah'>('summary');

  console.log('✅ Results component state initialized');

  // Safely destructure with fallbacks
  const sefirot_results = results?.sefirot_results || {};
  const metadata = results?.metadata || {};

  console.log('📋 Extracted data:', { sefirot_results, metadata });

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
    window.print();
  };

  const handleShare = () => {
    const shareData = {
      case_name,
      summary,
      timestamp: metadata?.timestamp || new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(shareData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tikun-analysis-${Date.now()}.json`;
    a.click();
  };

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tikun-full-results-${Date.now()}.json`;
    a.click();
  };

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
              {metadata?.total_duration_seconds && (
                <span className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Clock size={11} />
                  {Math.floor(metadata.total_duration_seconds / 60)}m {metadata.total_duration_seconds % 60}s
                </span>
              )}
              {metadata?.models_used && (
                <span className="flex items-center gap-1.5 text-xs text-slate-500">
                  <Cpu size={11} />
                  {new Set(Object.values(metadata.models_used)).size} providers
                </span>
              )}
            </div>
            {/* Provider attribution row */}
            {metadata?.models_used && (
              <div className="flex flex-wrap gap-1.5 mt-3">
                {Array.from(new Set(Object.values(metadata.models_used as Record<string, string>))).map((model) => {
                  const providerKey = PROVIDER_LABELS[model as string] as ProviderKey | undefined;
                  if (!providerKey) return null;
                  return (
                    <ProviderBadge key={model} provider={providerKey} label={model as string} size="sm" />
                  );
                })}
              </div>
            )}
          </div>
          <div className="flex gap-3 items-center flex-wrap">
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
              title="Share Summary"
            >
              <Share2 className="w-5 h-5 text-slate-300" />
            </button>
            <button
              onClick={handleDownload}
              className="p-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
              title="Download Full Results"
            >
              <Download className="w-5 h-5 text-slate-300" />
            </button>
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
            className="space-y-4"
          >
            {Object.entries(sefirot_results || {}).map(([name, data]: [string, any]) => (
              <div
                key={name}
                className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6"
              >
                <h3 className="text-xl font-bold text-white mb-4 capitalize">{name}</h3>
                <pre className="text-sm text-slate-300 overflow-x-auto bg-slate-900/50 rounded-lg p-4">
                  {JSON.stringify(data, null, 2)}
                </pre>
              </div>
            ))}
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
      </AnimatePresence>
    </motion.div>
  );
}

export default Results;