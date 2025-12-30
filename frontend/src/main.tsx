import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Initialize Datadog RUM (Real User Monitoring)
import { datadogRum } from '@datadog/browser-rum'

// Only initialize if Datadog credentials are provided
const datadogAppId = import.meta.env.VITE_DATADOG_APP_ID
const datadogClientToken = import.meta.env.VITE_DATADOG_CLIENT_TOKEN

if (datadogAppId && datadogClientToken && datadogAppId !== 'your-app-id') {
  datadogRum.init({
    applicationId: datadogAppId,
    clientToken: datadogClientToken,
    site: import.meta.env.VITE_DATADOG_SITE || 'datadoghq.com',
    service: 'tikun-olam-frontend',
    env: import.meta.env.VITE_DATADOG_ENV || 'development',
    version: '2.0.0',
    sessionSampleRate: 100,
    sessionReplaySampleRate: 20,
    trackUserInteractions: true,
    trackResources: true,
    trackLongTasks: true,
    defaultPrivacyLevel: 'mask-user-input'
  })

  datadogRum.startSessionReplayRecording()

  console.log('✅ Datadog RUM initialized')
} else {
  console.log('ℹ️ Datadog RUM not configured (credentials missing)')
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
