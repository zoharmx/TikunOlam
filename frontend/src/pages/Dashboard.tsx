import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Play, History, Terminal, LogOut, Activity, Menu, X, GitCompare } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import AnalysisForm from '../components/AnalysisForm';
import LoadingState from '../components/LoadingState';
import Results from '../components/Results';
import ObservabilityPanel from '../components/ObservabilityPanel';
import HistoryView from '../components/HistoryView';
import ErrorBoundary from '../components/ErrorBoundary';
import { ComparisonForm } from '../components/ComparisonForm';
import { ScenarioComparisonView } from '../components/ScenarioComparisonView';
import api from '../services/api';
import type { AnalysisResponse } from '../types';
import type { ComparisonScenario } from '../components/ComparisonForm';
import { PENTAGON_SCENARIO } from '../data/pentagonCase';

const Dashboard = () => {
  const { user, signOut } = useAuth();
  const [activeView, setActiveView] = useState<'new' | 'history' | 'observability' | 'compare'>('new');
  const [comparisonLoading, setComparisonLoading] = useState(false);
  const [comparisonResults, setComparisonResults] = useState<{ label: string; caseName: string; analysis: AnalysisResponse }[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentScenarioId, setCurrentScenarioId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Debug effect to track results state changes
  useEffect(() => {
    console.log('🔍 STATE DEBUG:', {
      hasResults: !!results,
      isLoading: loading,
      activeView,
      shouldShowResults: !!results && !loading && activeView === 'new'
    });
    if (results) {
      console.log('📊 Results data:', {
        hasSefirotResults: !!results.sefirot_results,
        hasMetadata: !!results.metadata,
        caseName: results.case_name || (results.metadata as any)?.case_name || 'NO CASE NAME'
      });
    }
  }, [results, loading, activeView]);

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

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

      // Set job ID to trigger polling via useEffect
      setCurrentJobId(jobResponse.job_id);

    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Error crítico en el análisis.');
      setCurrentScenarioId(null);
      setLoading(false);
    }
  };

  // Effect to handle polling with proper cleanup
  useEffect(() => {
    if (!currentJobId) return;

    // Clear any existing interval
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }

    const startTime = Date.now();
    const TIMEOUT_MS = 15 * 60 * 1000; // 15 minutes
    let consecutiveErrors = 0;
    const MAX_CONSECUTIVE_ERRORS = 5; // Stop after 5 consecutive failures (~15s)

    const stopPolling = () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };

    pollIntervalRef.current = setInterval(async () => {
      try {
        const elapsed = Date.now() - startTime;

        if (elapsed > TIMEOUT_MS) {
          stopPolling();
          setError('Analysis timeout — took longer than 15 minutes. Please try again.');
          setLoading(false);
          setCurrentJobId(null);
          return;
        }

        const status = await api.getJobStatus(currentJobId);
        consecutiveErrors = 0; // Reset on success

        console.log('[Poll]', { jobId: currentJobId, status: status.status, hasResults: !!status.results });

        if (status.status === 'completed' && status.results) {
          stopPolling();

          const transformedResults = {
            ...status.results,
            case_name: status.results.case_name || status.results.metadata?.case_name || status.case_name || 'Unknown',
            timestamp: status.results.metadata?.timestamp || new Date().toISOString()
          };

          setActiveView('new');
          setCurrentJobId(null);
          setLoading(false);
          setResults(transformedResults as any);

        } else if (status.status === 'failed') {
          stopPolling();
          setError(status.error || 'Analysis failed in backend. Check logs.');
          setLoading(false);
          setCurrentScenarioId(null);
          setCurrentJobId(null);
        }

      } catch (pollErr: any) {
        consecutiveErrors += 1;
        const errStatus = pollErr?.response?.status;
        const errMsg = pollErr?.response?.data?.detail || pollErr?.message || 'Network error';

        console.error('[Poll error]', {
          attempt: consecutiveErrors,
          httpStatus: errStatus,
          message: errMsg,
          code: pollErr?.code,
        });

        if (consecutiveErrors >= MAX_CONSECUTIVE_ERRORS) {
          stopPolling();
          setCurrentJobId(null);
          setLoading(false);

          if (errStatus === 404) {
            setError(`Job not found (${currentJobId.slice(0, 8)}…). The backend may have restarted. Try again.`);
          } else if (errStatus === 403 || errStatus === 401) {
            setError('Backend authentication error (403). Check Cloud Run IAM settings.');
          } else if (errStatus >= 500) {
            setError(`Backend error ${errStatus}: ${errMsg}. Check Cloud Run logs.`);
          } else {
            setError(`Cannot reach backend after ${MAX_CONSECUTIVE_ERRORS} attempts: ${errMsg}`);
          }
        }
      }
    }, 3000); // Poll every 3 seconds

    // Cleanup on unmount or when jobId changes
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    };
  }, [currentJobId]);

  const handleReset = () => {
    // Clear polling if active
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
    setResults(null);
    setError(null);
    setLoading(false);
    setCurrentJobId(null);
    setCurrentScenarioId(null);
  };

  const handleCompare = async (scenarios: ComparisonScenario[]) => {
    setComparisonLoading(true);
    setComparisonResults(null);
    try {
      const jobResponses = await api.analyzeMultiple(
        scenarios.map((s) => ({ scenario: s.scenario, case_name: s.case_name }))
      );
      const jobIds = jobResponses.map((r) => r.job_id);

      // Poll all jobs until done
      const resolved = await Promise.all(
        jobIds.map(async (jobId, i) => {
          for (let attempt = 0; attempt < 60; attempt++) {
            await new Promise((res) => setTimeout(res, 10000));
            const status = await api.getJobStatus(jobId);
            if (status.status === 'completed' && status.results) {
              const r = status.results as any;
              return {
                label: scenarios[i].label,
                caseName: scenarios[i].case_name,
                analysis: {
                  sefirot_results: r.sefirot_results || r,
                  summary: r.summary || {},
                  metadata: r.metadata || {},
                  case_name: scenarios[i].case_name,
                  status: 'completed',
                  timestamp: r.metadata?.timestamp || '',
                } as AnalysisResponse,
              };
            }
            if (status.status === 'failed') throw new Error(`Scenario ${scenarios[i].label} failed`);
          }
          throw new Error(`Scenario ${scenarios[i].label} timed out`);
        })
      );
      setComparisonResults(resolved);
    } catch (err: any) {
      alert(`Comparison error: ${err.message}`);
    } finally {
      setComparisonLoading(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background text-slate-200 font-sans">
      {/* Mobile menu button */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="fixed top-4 left-4 z-50 lg:hidden p-2 rounded-lg glass-panel border border-white/10"
      >
        {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        w-64 glass-panel border-r border-white/5 flex flex-col z-40
        fixed lg:relative h-screen
        transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="p-6 border-b border-white/5">
          <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-secondary to-primary" />
            TIKUN<span className="text-slate-500">OLAM</span>
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <SidebarItem
            icon={<Play size={18} />}
            label="New Analysis"
            active={activeView === 'new'}
            onClick={() => { setActiveView('new'); setSidebarOpen(false); }}
          />
          <SidebarItem
            icon={<Activity size={18} />}
            label="Observability"
            active={activeView === 'observability'}
            onClick={() => { setActiveView('observability'); setSidebarOpen(false); }}
            badge={currentScenarioId ? 'Live' : undefined}
          />
          <SidebarItem
            icon={<History size={18} />}
            label="History"
            active={activeView === 'history'}
            onClick={() => { setActiveView('history'); setSidebarOpen(false); }}
          />
          <SidebarItem
            icon={<GitCompare size={18} />}
            label="Compare"
            active={activeView === 'compare'}
            onClick={() => { setActiveView('compare'); setSidebarOpen(false); }}
          />
          <SidebarItem
            icon={<Terminal size={18} />}
            label="Live Logs"
            active={false}
          />
        </nav>

        <div className="p-4 border-t border-white/5 space-y-3">
          {/* User info */}
          {user && (
            <div className="flex items-center gap-3 px-3 py-2">
              <img
                src={user.photoURL || 'https://via.placeholder.com/40'}
                alt={user.displayName || 'User'}
                className="w-8 h-8 rounded-full border border-white/20"
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {user.displayName || 'User'}
                </p>
                <p className="text-xs text-slate-400 truncate">
                  {user.email}
                </p>
              </div>
            </div>
          )}
          {/* Logout button */}
          <SidebarItem icon={<LogOut size={18} />} label="Sign Out" onClick={handleSignOut} />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative w-full lg:w-auto">
        {/* Background ambient light */}
        <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[100px] pointer-events-none" />

        <div className="max-w-6xl mx-auto p-4 sm:p-6 lg:p-8 pt-16 lg:pt-8">
          <Header isAnalyzing={loading} />

          <div className="mt-8">
            {/* NEW VIEW - Analysis Form, Loading, Results, or Error */}
            {activeView === 'new' && (
              <>
                {/* Show form when no results and not loading */}
                {!loading && !results && !error && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="space-y-4"
                  >
                    {/* Featured Pentagon banner */}
                    <div className="p-4 rounded-xl bg-gradient-to-r from-yellow-950/40 to-slate-900/60 border border-yellow-500/20 flex items-center justify-between gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-yellow-500/20 border border-yellow-500/30 text-yellow-400 uppercase tracking-wider">Flagship</span>
                          <span className="text-xs text-slate-400">Anthropic vs. The Pentagon</span>
                        </div>
                        <p className="text-sm text-slate-300">Load our flagship case study — $2.4B Pentagon contract for autonomous weapons AI.</p>
                      </div>
                      <button
                        onClick={() => handleAnalyze(PENTAGON_SCENARIO, 'Anthropic_Pentagon_Ultimatum')}
                        className="flex-shrink-0 px-4 py-2 rounded-lg bg-yellow-500/15 hover:bg-yellow-500/25 border border-yellow-500/30 text-yellow-400 text-sm font-medium transition-all"
                      >
                        Run Analysis
                      </button>
                    </div>
                    <AnalysisForm onSubmit={handleAnalyze} />
                  </motion.div>
                )}

                {/* Show loading state */}
                {loading && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex flex-col items-center justify-center py-20"
                  >
                    <LoadingState />
                  </motion.div>
                )}

                {/* Show error */}
                {error && !results && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="p-6 bg-red-500/10 border border-red-500/20 rounded-xl text-red-200"
                  >
                    <h3 className="font-bold text-lg mb-2">Analysis Error</h3>
                    <p>{error}</p>
                    <button onClick={handleReset} className="mt-4 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg text-sm transition-colors">
                      Try Again
                    </button>
                  </motion.div>
                )}

                {/* Show results - SIMPLIFIED WITHOUT AnimatePresence mode="wait" */}
                {results && !loading && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                  >
                    <ErrorBoundary>
                      <Results results={results} onReset={handleReset} />
                    </ErrorBoundary>
                  </motion.div>
                )}
              </>
            )}

            {/* COMPARE VIEW */}
            {activeView === 'compare' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                {!comparisonResults ? (
                  <ComparisonForm onSubmit={handleCompare} isLoading={comparisonLoading} />
                ) : (
                  <ScenarioComparisonView
                    scenarios={comparisonResults}
                    onReset={() => setComparisonResults(null)}
                  />
                )}
              </motion.div>
            )}

            {/* HISTORY VIEW */}
            {activeView === 'history' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <HistoryView />
              </motion.div>
            )}

            {/* OBSERVABILITY VIEW */}
            {activeView === 'observability' && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <ObservabilityPanel
                  dashboardUrl={import.meta.env.VITE_DATADOG_DASHBOARD_URL}
                  scenarioId={currentScenarioId}
                />
              </motion.div>
            )}
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
