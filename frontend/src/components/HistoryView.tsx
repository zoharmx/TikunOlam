import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Clock, CheckCircle, XCircle, Loader, Eye, Trash2, RefreshCw, Filter } from 'lucide-react';
import api from '../services/api';
import type { JobStatusResponse } from '../types';
import Results from './Results';

const HistoryView = () => {
  const [jobs, setJobs] = useState<JobStatusResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedJob, setSelectedJob] = useState<JobStatusResponse | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [refreshing, setRefreshing] = useState(false);

  const loadJobs = async () => {
    try {
      setRefreshing(true);
      const response = await api.listJobs(50, filterStatus === 'all' ? undefined : filterStatus);
      setJobs(response.jobs);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load history');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadJobs();
  }, [filterStatus]);

  const handleDelete = async (jobId: string) => {
    if (!confirm('Are you sure you want to delete this analysis?')) return;

    try {
      await api.deleteJob(jobId);
      setJobs(jobs.filter(j => (j.job_id ?? (j as any).id) !== jobId));
      if ((selectedJob?.job_id ?? (selectedJob as any)?.id) === jobId) {
        setSelectedJob(null);
      }
    } catch (err: any) {
      alert('Failed to delete job: ' + (err.response?.data?.detail || err.message));
    }
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}m ${remainingSeconds}s`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'processing':
        return <Loader className="w-5 h-5 text-blue-500 animate-spin" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-500" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const colors: Record<string, string> = {
      completed: 'bg-green-500/20 text-green-400 border-green-500/30',
      failed: 'bg-red-500/20 text-red-400 border-red-500/30',
      processing: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
      pending: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    };

    return (
      <span className={`px-2 py-1 rounded text-xs font-medium border ${colors[status] || 'bg-slate-500/20 text-slate-400 border-slate-500/30'}`}>
        {status.toUpperCase()}
      </span>
    );
  };

  if (selectedJob && selectedJob.results) {
    return (
      <div className="space-y-4">
        <button
          onClick={() => setSelectedJob(null)}
          className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-sm transition-colors"
        >
          ← Back to History
        </button>
        <Results results={selectedJob.results} onReset={() => setSelectedJob(null)} />
      </div>
    );
  }

  return (
    <div className="glass-panel p-6 rounded-2xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white">Analysis History</h2>
          <p className="text-slate-400 text-sm mt-1">View and manage previous analyses</p>
        </div>
        <button
          onClick={loadJobs}
          disabled={refreshing}
          className="px-4 py-2 bg-primary/10 hover:bg-primary/20 border border-primary/20 rounded-lg text-sm font-medium text-primary transition-all flex items-center gap-2"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Filter */}
      <div className="flex items-center gap-2 mb-6">
        <Filter className="w-4 h-4 text-slate-400" />
        <span className="text-sm text-slate-400">Filter:</span>
        {['all', 'completed', 'processing', 'failed', 'pending'].map(status => (
          <button
            key={status}
            onClick={() => setFilterStatus(status)}
            className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
              filterStatus === status
                ? 'bg-primary/20 text-primary border border-primary/30'
                : 'bg-white/5 text-slate-400 border border-white/10 hover:bg-white/10'
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-200 mb-6">
          <p className="font-medium">Error loading history</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <Loader className="w-8 h-8 text-primary animate-spin" />
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-20">
          <Clock className="w-16 h-16 text-slate-600 mx-auto mb-4" />
          <p className="text-slate-400 text-lg">No analyses found</p>
          <p className="text-slate-500 text-sm mt-2">
            {filterStatus === 'all'
              ? 'Run your first analysis to see it here'
              : `No ${filterStatus} analyses found`}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <AnimatePresence>
            {jobs.map((job, index) => (
              <motion.div
                key={job.job_id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ delay: index * 0.05 }}
                className="p-4 bg-surface/30 border border-white/10 rounded-xl hover:bg-surface/50 transition-all"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3 flex-1 min-w-0">
                    <div className="mt-1">
                      {getStatusIcon(job.status)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium text-white truncate">
                          {job.case_name || 'Unnamed Analysis'}
                        </h3>
                        {getStatusBadge(job.status)}
                      </div>
                      <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-slate-400 mt-2">
                        <div>
                          <span className="text-slate-500">Created:</span> {formatDate(job.created_at)}
                        </div>
                        {job.completed_at && (
                          <div>
                            <span className="text-slate-500">Completed:</span> {formatDate(job.completed_at)}
                          </div>
                        )}
                        {job.duration_seconds && (
                          <div>
                            <span className="text-slate-500">Duration:</span> {formatDuration(job.duration_seconds)}
                          </div>
                        )}
                        <div>
                          <span className="text-slate-500">Job ID:</span>{' '}
                          <code className="text-slate-300">
                            {(job.job_id ?? (job as any).id ?? 'unknown').substring(0, 8)}...
                          </code>
                        </div>
                      </div>
                      {job.error && (
                        <div className="mt-2 p-2 bg-red-500/10 border border-red-500/20 rounded text-xs text-red-300">
                          <span className="font-medium">Error:</span> {job.error}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {job.status === 'completed' && job.results && (
                      <button
                        onClick={() => setSelectedJob(job)}
                        className="px-3 py-2 bg-primary/10 hover:bg-primary/20 border border-primary/20 rounded-lg text-xs font-medium text-primary transition-all flex items-center gap-1"
                      >
                        <Eye className="w-3 h-3" />
                        View
                      </button>
                    )}
                    <button
                      onClick={() => handleDelete(job.job_id ?? (job as any).id)}
                      className="px-3 py-2 bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 rounded-lg text-xs font-medium text-red-400 transition-all flex items-center gap-1"
                    >
                      <Trash2 className="w-3 h-3" />
                      Delete
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}

      {jobs.length > 0 && (
        <div className="mt-6 text-center text-sm text-slate-500">
          Showing {jobs.length} {jobs.length === 1 ? 'analysis' : 'analyses'}
        </div>
      )}
    </div>
  );
};

export default HistoryView;
