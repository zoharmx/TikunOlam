# 📊 DATADOG METRICS & OBSERVABILITY GUIDE

**Project:** Tikun Olam
**Status:** ✅ Datadog Configured (APM + Custom Metrics)
**Site:** US5 Datadog (https://us5.datadoghq.com)

---

## 🔑 CONFIGURACIÓN ACTUAL

### Credenciales (desde .env)
```bash
DATADOG_API_KEY=c2a4f803fb193ba15d8d40d944e08a9a
DATADOG_APP_KEY=ce055ce8db344dba2f74ce95721ca354e6c653d3
DATADOG_SERVICE_NAME=tikun-olam
DATADOG_SITE=us5.datadoghq.com
DATADOG_STATSD_HOST=127.0.0.1
DATADOG_STATSD_PORT=8125
DATADOG_TRACE_PORT=8126
```

### Cloud Run Secrets
Los secrets están configurados en Cloud Run para producción:
```bash
DATADOG_API_KEY=DATADOG_API_KEY:1
DATADOG_APP_KEY=DATADOG_APP_KEY:1
```

---

## 📈 MÉTRICAS DISPONIBLES

### Custom Metrics Implementadas

El framework Tikun Olam envía métricas personalizadas a Datadog:

#### 1. Métricas de Análisis (tikun.analysis.*)
```python
# En src/tikun/orchestrator.py y src/tikun/sefirot/

# Duración total del análisis
tikun.analysis.duration
  - Tags: case_name, status
  - Type: gauge (seconds)

# Análisis completados
tikun.analysis.completed
  - Tags: case_name, decision
  - Type: count

# Análisis fallidos
tikun.analysis.failed
  - Tags: case_name, error_type
  - Type: count
```

#### 2. Métricas de Sefirot (tikun.sefirah.*)
```python
# Duración por Sefira
tikun.sefirah.duration
  - Tags: sefirah_name (keter, chochmah, binah, etc.)
  - Type: gauge (seconds)

# Sefirot exitosos
tikun.sefirah.success
  - Tags: sefirah_name
  - Type: count

# Sefirot fallidos
tikun.sefirah.failed
  - Tags: sefirah_name, error_type
  - Type: count
```

#### 3. BinahSigma Metrics (tikun.binah_sigma.*)
```python
# Divergencia detectada (bias delta)
tikun.binah_sigma.bias_delta
  - Tags: case_name
  - Type: gauge (percentage)

# Modos activados
tikun.binah_sigma.mode
  - Tags: mode (simple, sigma, deep)
  - Type: count

# Blind spots detectados
tikun.binah_sigma.blind_spots
  - Tags: case_name
  - Type: gauge (count)
```

#### 4. Métricas de API (tikun.api.*)
```python
# Requests recibidos
tikun.api.requests
  - Tags: endpoint, method, status_code
  - Type: count

# Latencia de requests
tikun.api.latency
  - Tags: endpoint
  - Type: gauge (milliseconds)

# Jobs creados
tikun.api.jobs.created
  - Tags: job_type (sync, async)
  - Type: count
```

---

## 🚨 PROBLEMA CONOCIDO: StatsD Connection Refused

### Síntoma
```
WARNING | datadog.dogstatsd | Error submitting packet: [Errno 111] Connection refused
```

### Causa
Cloud Run no tiene un Datadog Agent local ejecutándose, por lo que StatsD (puerto 8125) no está disponible.

### Impacto
- ❌ Métricas vía StatsD NO se envían
- ✅ Métricas vía API HTTP siguen funcionando
- ✅ Logs siguen siendo capturados

### Solución Temporal (Actual)
Las métricas se envían via API HTTP directa en lugar de StatsD:

```python
# src/tikun/utils/metrics.py
import requests

def send_metric(metric_name, value, tags=None):
    if not config.datadog_api_key:
        return

    url = f"https://api.{config.datadog_site}/api/v2/series"
    headers = {
        "DD-API-KEY": config.datadog_api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "series": [{
            "metric": metric_name,
            "type": "gauge",
            "points": [[int(time.time()), value]],
            "tags": tags or []
        }]
    }

    requests.post(url, json=payload, headers=headers)
```

### Solución Permanente (Recomendado)
Configurar Datadog Serverless Monitoring para Cloud Run:

```yaml
# cloudbuild.yaml - agregar deployment de Datadog layer

steps:
  # ... existing steps ...

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'configure-datadog'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'services'
      - 'update'
      - 'tikun-olam'
      - '--update-env-vars'
      - 'DD_TRACE_ENABLED=true,DD_SERVICE=tikun-olam,DD_ENV=production'
```

**Documentación:** https://docs.datadoghq.com/serverless/google_cloud_run/

---

## 📊 DASHBOARDS RECOMENDADOS

### Dashboard 1: Tikun Olam Overview
```
Widgets:
- Total Análisis (last 24h)
- Success Rate (%)
- Average Analysis Duration
- Sefirot Success Rate (bar chart por Sefira)
- BinahSigma Activation Rate
```

### Dashboard 2: Performance Metrics
```
Widgets:
- P50, P95, P99 Latency por Sefira
- API Request Rate
- Error Rate por Sefira
- BinahSigma Bias Delta (distribution)
```

### Dashboard 3: Production Health
```
Widgets:
- Cloud Run Instance Count
- Memory Usage
- CPU Usage
- Request Timeout Rate
- Error Logs (log stream)
```

---

## 🔍 QUERIES ÚTILES

### Ver análisis recientes
```
Service:tikun-olam @case_name:*
```

### Ver errores de Sefirot
```
Service:tikun-olam status:error @sefirah_name:*
```

### Ver activaciones de BinahSigma
```
Service:tikun-olam @binah_sigma.mode:sigma
```

### Ver latencia de análisis
```
avg:tikun.analysis.duration{*} by {case_name}
```

---

## 🎯 MÉTRICAS PARA DEVPOST SUBMISSION

Para mostrar en la submission del hackathon:

### Screenshot 1: Dashboard Overview
- Total de análisis ejecutados
- Success rate
- Sefirot completion rate

### Screenshot 2: BinahSigma en Acción
- Casos donde BinahSigma detectó bias
- Bias delta distribution
- Ejemplos de divergencias

### Screenshot 3: Performance
- Latencia promedio por Sefira
- Time-series de análisis completados
- API response times

---

## 🔗 ENLACES ÚTILES

### Datadog Web UI
- **Dashboard:** https://us5.datadoghq.com/dashboard/lists
- **Logs:** https://us5.datadoghq.com/logs
- **APM:** https://us5.datadoghq.com/apm/services
- **Metrics Explorer:** https://us5.datadoghq.com/metric/explorer

### API Documentation
- **Metrics API:** https://docs.datadoghq.com/api/latest/metrics/
- **Events API:** https://docs.datadoghq.com/api/latest/events/
- **Logs API:** https://docs.datadoghq.com/api/latest/logs/

---

## 📝 CUSTOM EVENTS

Además de métricas, el sistema envía eventos importantes:

```python
# Evento: Análisis completado
{
    "title": "Tikun Analysis Completed",
    "text": "Case: {case_name}, Decision: {decision}",
    "tags": ["service:tikun-olam", "case:{case_name}"],
    "alert_type": "success"
}

# Evento: BinahSigma activado
{
    "title": "BinahSigma Activated",
    "text": "Bias delta: {bias_delta}%, Blind spots: {count}",
    "tags": ["service:tikun-olam", "binah_sigma:active"],
    "alert_type": "info"
}

# Evento: Error crítico
{
    "title": "Tikun Analysis Failed",
    "text": "Case: {case_name}, Error: {error}",
    "tags": ["service:tikun-olam", "error_type:{type}"],
    "alert_type": "error"
}
```

---

## ⚙️ CONFIGURACIÓN EN CÓDIGO

### Archivo principal: `src/tikun/utils/metrics.py`

```python
from datadog import initialize, statsd
from tikun.config import get_config

config = get_config()

# Initialize Datadog
options = {
    'api_key': config.datadog_api_key,
    'app_key': config.datadog_app_key,
    'statsd_host': config.datadog_statsd_host,
    'statsd_port': config.datadog_statsd_port,
}

initialize(**options)

class TikunMetrics:
    @staticmethod
    def record_analysis_duration(duration: float, tags: list = None):
        statsd.gauge('tikun.analysis.duration', duration, tags=tags)

    @staticmethod
    def increment_sefirah_success(sefirah_name: str):
        statsd.increment('tikun.sefirah.success', tags=[f'sefirah:{sefirah_name}'])

    @staticmethod
    def record_bias_delta(delta: float, case_name: str):
        statsd.gauge('tikun.binah_sigma.bias_delta', delta, tags=[f'case:{case_name}'])
```

### Uso en Orchestrator:

```python
# src/tikun/orchestrator.py

from tikun.utils.metrics import TikunMetrics

class TikunOrchestrator:
    def process(self, scenario: str, case_name: str):
        start_time = time.time()

        try:
            # ... processing ...

            duration = time.time() - start_time
            TikunMetrics.record_analysis_duration(
                duration,
                tags=[f'case:{case_name}', 'status:success']
            )

        except Exception as e:
            TikunMetrics.increment('tikun.analysis.failed', tags=[f'error:{type(e).__name__}'])
```

---

## 🎉 STATUS ACTUAL

- ✅ Datadog API keys configuradas
- ✅ Service name: `tikun-olam`
- ✅ Site: US5 (us5.datadoghq.com)
- ✅ Custom metrics implementadas en código
- ⚠️ StatsD no disponible en Cloud Run (usar API HTTP)
- ⚠️ Dashboards: Pendiente de crear manualmente
- ⚠️ Screenshots: Pendiente (después de tener datos)

---

## 🚀 PRÓXIMOS PASOS

1. ⬜ Ejecutar varios análisis para generar datos
2. ⬜ Crear dashboards personalizados en Datadog UI
3. ⬜ Capturar screenshots para Devpost
4. ⬜ Implementar Datadog Serverless Monitoring (post-hackathon)
5. ⬜ Configurar alertas para errores críticos

---

**Creado:** 2025-12-30
**Última actualización:** 2025-12-30
**Status:** Configurado y documentado
