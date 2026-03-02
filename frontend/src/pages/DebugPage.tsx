import { useState } from 'react';
import api from '../services/api';

const DebugPage = () => {
  const [jobId, setJobId] = useState('');
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchJob = async () => {
    if (!jobId.trim()) {
      setError('Please enter a job ID');
      return;
    }

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await api.getJobStatus(jobId.trim());
      setData(result);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch job');
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await api.listJobs(20);
      setData(result);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch history');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-8">Tikun Olam - Debug Page</h1>

      <div className="space-y-4 mb-8">
        <div>
          <label className="block mb-2">Job ID:</label>
          <input
            type="text"
            value={jobId}
            onChange={(e) => setJobId(e.target.value)}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded text-white"
            placeholder="Enter job ID (e.g., abad2873-1f25-42a0-9d51-96c2fe31d9c8)"
          />
        </div>

        <div className="flex gap-4">
          <button
            onClick={fetchJob}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Fetch Job'}
          </button>

          <button
            onClick={fetchHistory}
            disabled={loading}
            className="px-6 py-2 bg-green-600 hover:bg-green-700 rounded disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Fetch History (Last 20)'}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-900/50 border border-red-500 rounded mb-4">
          <strong>Error:</strong> {error}
        </div>
      )}

      {data && (
        <div className="bg-gray-800 p-4 rounded overflow-auto">
          <h2 className="text-xl font-bold mb-4">Raw Data:</h2>
          <pre className="text-xs whitespace-pre-wrap">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default DebugPage;
