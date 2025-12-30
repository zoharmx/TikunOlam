import React, { useState, useEffect } from 'react'
import { Activity, AlertTriangle, CheckCircle, TrendingUp, BarChart3 } from 'lucide-react'

interface ObservabilityPanelProps {
  dashboardUrl?: string
  scenarioId?: string | null
}

interface Metrics {
  alignment: number | null
  biasDelta: number | null
  pipelineStatus: 'idle' | 'running' | 'completed' | 'failed'
  duration?: number
  decision?: string
  alerts?: Array<{
    name: string
    severity: 'critical' | 'warning' | 'info'
    message: string
  }>
}

const ObservabilityPanel: React.FC<ObservabilityPanelProps> = ({
  dashboardUrl,
  scenarioId
}) => {
  const [metrics, setMetrics] = useState<Metrics>({
    alignment: null,
    biasDelta: null,
    pipelineStatus: 'idle'
  })

  const [showDashboard, setShowDashboard] = useState(false)

  useEffect(() => {
    // Poll metrics from backend when scenario is being analyzed
    if (!scenarioId) {
      setMetrics({
        alignment: null,
        biasDelta: null,
        pipelineStatus: 'idle'
      })
      return
    }

    const pollMetrics = async () => {
      try {
        // TODO: Replace with actual API endpoint
        // const response = await fetch(`/api/metrics/${scenarioId}`)
        // const data = await response.json()
        // setMetrics(data)

        // Mock data for now
        setMetrics({
          alignment: 78,
          biasDelta: 52,
          pipelineStatus: 'completed',
          duration: 12.5,
          decision: 'CONDITIONAL_GO'
        })
      } catch (error) {
        console.error('Failed to fetch metrics:', error)
      }
    }

    // Poll every 2 seconds during analysis
    const interval = setInterval(pollMetrics, 2000)
    pollMetrics() // Initial fetch

    return () => clearInterval(interval)
  }, [scenarioId])

  const getStatusColor = (status: Metrics['pipelineStatus']) => {
    switch (status) {
      case 'running':
        return 'text-blue-600 bg-blue-50'
      case 'completed':
        return 'text-green-600 bg-green-50'
      case 'failed':
        return 'text-red-600 bg-red-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  const getAlignmentColor = (alignment: number | null) => {
    if (alignment === null) return 'text-gray-400'
    if (alignment >= 80) return 'text-green-600'
    if (alignment >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getBiasDeltaColor = (delta: number | null) => {
    if (delta === null) return 'text-gray-400'
    if (delta >= 80) return 'text-red-600'
    if (delta >= 60) return 'text-yellow-600'
    return 'text-green-600'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Activity className="w-6 h-6 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900">
            Pipeline Observability
          </h2>
        </div>

        {dashboardUrl && (
          <button
            onClick={() => setShowDashboard(!showDashboard)}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <BarChart3 className="w-4 h-4" />
            {showDashboard ? 'Hide' : 'Show'} Full Dashboard
          </button>
        )}
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Ethical Alignment */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">
              Ethical Alignment
            </h3>
            <CheckCircle className={`w-5 h-5 ${getAlignmentColor(metrics.alignment)}`} />
          </div>
          <div className={`text-3xl font-bold ${getAlignmentColor(metrics.alignment)}`}>
            {metrics.alignment !== null ? `${metrics.alignment}%` : '--'}
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Keter alignment score
          </p>
        </div>

        {/* BinahSigma Bias Delta */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">
              BinahSigma Bias Δ
            </h3>
            <TrendingUp className={`w-5 h-5 ${getBiasDeltaColor(metrics.biasDelta)}`} />
          </div>
          <div className={`text-3xl font-bold ${getBiasDeltaColor(metrics.biasDelta)}`}>
            {metrics.biasDelta !== null ? `${metrics.biasDelta}%` : '--'}
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Civilizational divergence
          </p>
        </div>

        {/* Pipeline Status */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">
              Pipeline Status
            </h3>
            <Activity className="w-5 h-5 text-blue-600" />
          </div>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(metrics.pipelineStatus)}`}>
              {metrics.pipelineStatus.toUpperCase()}
            </span>
          </div>
          {metrics.duration && (
            <p className="text-xs text-gray-500 mt-2">
              Duration: {metrics.duration}s
            </p>
          )}
        </div>
      </div>

      {/* Decision Badge */}
      {metrics.decision && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="flex-shrink-0">
              <CheckCircle className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-900">Final Decision</h3>
              <p className="text-lg font-bold text-blue-600 mt-1">{metrics.decision}</p>
            </div>
          </div>
        </div>
      )}

      {/* Active Alerts */}
      {metrics.alerts && metrics.alerts.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              Active Alerts
            </h3>
          </div>
          <ul className="space-y-3">
            {metrics.alerts.map((alert, idx) => (
              <li
                key={idx}
                className={`p-3 rounded-lg ${
                  alert.severity === 'critical' ? 'bg-red-50 border-l-4 border-red-500' :
                  alert.severity === 'warning' ? 'bg-yellow-50 border-l-4 border-yellow-500' :
                  'bg-blue-50 border-l-4 border-blue-500'
                }`}
              >
                <div className="flex items-start gap-2">
                  <AlertTriangle className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                    alert.severity === 'critical' ? 'text-red-600' :
                    alert.severity === 'warning' ? 'text-yellow-600' :
                    'text-blue-600'
                  }`} />
                  <div className="flex-1">
                    <strong className="text-sm font-semibold">{alert.name}</strong>
                    <p className="text-xs text-gray-600 mt-1">{alert.message}</p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Embedded Datadog Dashboard */}
      {showDashboard && dashboardUrl && (
        <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              Datadog Dashboard
            </h3>
          </div>
          <div className="relative" style={{ height: '600px' }}>
            <iframe
              src={dashboardUrl}
              width="100%"
              height="100%"
              frameBorder="0"
              title="Datadog Dashboard"
              className="rounded-lg"
            />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Real-time metrics powered by Datadog
          </p>
        </div>
      )}

      {/* Info Message when idle */}
      {metrics.pipelineStatus === 'idle' && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
          <Activity className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <h3 className="text-lg font-semibold text-gray-700 mb-2">
            No Active Analysis
          </h3>
          <p className="text-sm text-gray-600">
            Submit a scenario to see real-time pipeline metrics and observability data
          </p>
        </div>
      )}

      {/* Powered by footer */}
      <div className="text-center pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Powered by <span className="font-semibold">Google Vertex AI</span> +{' '}
          <span className="font-semibold">Datadog</span>
        </p>
      </div>
    </div>
  )
}

export default ObservabilityPanel
