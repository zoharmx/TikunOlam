/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string
  readonly VITE_DATADOG_APP_ID?: string
  readonly VITE_DATADOG_CLIENT_TOKEN?: string
  readonly VITE_DATADOG_SITE?: string
  readonly VITE_DATADOG_ENV?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
