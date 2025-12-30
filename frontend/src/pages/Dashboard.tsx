import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Play, History, Terminal, LogOut, Activity } from 'lucide-react';
import Header from '../components/Header';
import AnalysisForm from '../components/AnalysisForm';
import LoadingState from '../components/LoadingState';
import Results from '../components/Results';
import ObservabilityPanel from '../components/ObservabilityPanel';
import api from '../services/api';
import type { AnalysisResponse } from '../types';

const Dashboard = () => {
  const [activeView, setActiveView] = useState<'new' | 'history' | 'observability'>('new');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentScenarioId, setCurrentScenarioId] = useState<string | null>(null);

  const handleAnalyze = async (scenario: string, caseName?: string) => {
    setLoading(true);
    setError(null);
    setResults(null);

    // Generate a scenario ID for tracking
    const scenarioId = `scenario_${Date.now()}`
    setCurrentScenarioId(scenarioId)

    try {
      // Use ASYNC analysis to avoid timeouts
      const jobResponse = await api.analyzeAsync({
        scenario,
        case_name: caseName,
        verbose: true,
        auto_export: true,
        include_full_results: true, // CRITICAL: Ensures results are included in job status
      });

      // Poll for results every 3 seconds
      const jobId = jobResponse.job_id;
      const pollInterval = setInterval(async () => {
        try {
          const status = await api.getJobStatus(jobId);

          if (status.status === 'completed' && status.results) {
            clearInterval(pollInterval);
            setResults(status.results);
            setLoading(false);
            // Keep on 'new' view to show results (not observability)
            // setActiveView('observability');
          } else if (status.status === 'failed') {
            clearInterval(pollInterval);
            setError(status.error || 'Analysis failed');
            setLoading(false);
            setCurrentScenarioId(null);
          }
        } catch (pollErr: any) {
          console.error('Polling error:', pollErr);
          // Continue polling even if one request fails
        }
      }, 3000); // Poll every 3 seconds

      // Cleanup on unmount
      return () => clearInterval(pollInterval);

    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Error crítico en el análisis.');
      setCurrentScenarioId(null);
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background text-slate-200 font-sans">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-white/5 flex flex-col z-20">
        <div className="p-6 border-b border-white/5">
          <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-secondary to-primary" />
            TIKUN<span className="text-slate-500">OLAM</span>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <SidebarItem
            icon={<Play size={18} />}
            label="Nuevo Análisis"
            active={activeView === 'new'}
            onClick={() => setActiveView('new')}
          />
          <SidebarItem
            icon={<Activity size={18} />}
            label="Observability"
            active={activeView === 'observability'}
            onClick={() => setActiveView('observability')}
            badge={currentScenarioId ? 'Live' : undefined}
          />
          <SidebarItem
            icon={<History size={18} />}
            label="Historial (Beta)"
            active={activeView === 'history'}
            onClick={() => setActiveView('history')}
          />
          <SidebarItem
            icon={<Terminal size={18} />}
            label="Live Logs"
            active={false}
          />
        </nav>

        <div className="p-4 border-t border-white/5">
          <SidebarItem icon={<LogOut size={18} />} label="Desconectar" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative">
        {/* Background ambient light */}
        <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[100px] pointer-events-none" />

        <div className="max-w-6xl mx-auto p-8">
          <Header />

          <div className="mt-8">
            <AnimatePresence mode="wait">
              {activeView === 'new' && !loading && !results && (
                <motion.div
                  key="form"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  <AnalysisForm onSubmit={handleAnalyze} />
                </motion.div>
              )}

              {activeView === 'observability' && (
                <motion.div
                  key="observability"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  <ObservabilityPanel
                    dashboardUrl={import.meta.env.VITE_DATADOG_DASHBOARD_URL}
                    scenarioId={currentScenarioId}
                  />
                </motion.div>
              )}

              {loading && (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center justify-center py-20"
                >
                  <LoadingState />
                </motion.div>
              )}

              {error && (
                <motion.div
                  key="error"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-6 bg-red-500/10 border border-red-500/20 rounded-xl text-red-200"
                >
                  <h3 className="font-bold text-lg mb-2">Error de Ejecución</h3>
                  <p>{error}</p>
                  <button onClick={handleReset} className="mt-4 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-sm transition-colors">
                    Reintentar
                  </button>
                </motion.div>
              )}

              {results && !loading && activeView === 'new' && (
                <motion.div
                  key="results"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <Results results={results} onReset={handleReset} />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
};

const SidebarItem = ({ icon, label, active = false, onClick, badge }: any) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200
      ${active
        ? 'bg-primary/10 text-primary border border-primary/20 shadow-[0_0_15px_rgba(58,134,255,0.1)]'
        : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
      }`}
  >
    {icon}
    <span className="flex-1 text-left">{label}</span>
    {badge && (
      <span className="px-2 py-0.5 text-xs font-semibold bg-green-500/20 text-green-400 rounded-full animate-pulse">
        {badge}
      </span>
    )}
  </button>
);

export default Dashboard;
