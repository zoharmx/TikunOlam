# ⚠️ JOB PERSISTENCE ISSUE - Cloud Run Multi-Instance Problem

**Fecha:** 2025-12-29
**Status:** 🔴 **CRITICAL - Afecta async endpoints**
**Severidad:** HIGH (bloquea `/analyze/async` endpoint)

---

## 🔍 PROBLEMA IDENTIFICADO

### Síntoma
```bash
POST /analyze/async → {"job_id": "abc123", "status": "pending"}
GET /jobs/abc123 → 404 Not Found
```

### Causa Raíz

**Cloud Run multi-instance + in-memory job storage**

```python
# src/tikun/api/main.py:35
jobs: Dict[str, Dict[str, Any]] = {}  # ❌ EN MEMORIA
```

#### ¿Qué sucede?

1. **Request 1 (POST /analyze/async)** → llega a **Instance A**
   - Instance A crea job en `jobs` dictionary
   - Retorna `{"job_id": "abc123"}`

2. **Request 2 (GET /jobs/abc123)** → llega a **Instance B**
   - Instance B no tiene el job (su `jobs = {}` está vacío)
   - Retorna **404 Not Found**

3. **Cloud Run Restart/Scale**
   - Instance A se destruye
   - Jobs se pierden permanentemente

---

## 📊 EVIDENCIA (Logs de Cloud Run)

```
2025-12-30 02:19:54 | INFO | Background analysis completed  ✅
2025-12-30 02:20:03 | INFO | GET /jobs/5c0256eb-... HTTP/1.1" 200 OK  ✅
2025-12-30 02:20:03 | INFO | GET /jobs/5c0256eb-... HTTP/1.1" 404 Not Found  ❌
```

**Interpretación:**
- Mismo job ID
- 200 OK cuando hit la instancia correcta
- 404 cuando hit otra instancia

---

## ✅ WORKAROUND ACTUAL (Para Testing)

### Usar endpoint síncrono `/analyze` (no `/analyze/async`)

**Ventaja:** Todo sucede en una sola request-response (misma instancia)

```bash
curl -X POST "https://tikun-olam-hzz2wlra6a-uc.a.run.app/analyze" \
  -H "Content-Type: application/json" \
  -d '{"scenario":"...", "case_name":"test"}' \
  --max-time 1800  # 30 min timeout
```

**Desventaja:**
- Request bloqueante (20-30 minutos)
- No hay progreso tracking
- No hay UI responsiveness

---

## 🔧 SOLUCIONES PROPUESTAS

### 🔥 Opción A: Firestore (Recomendado para GCP)

**Pros:**
- ✅ Nativo de GCP
- ✅ Serverless (no infra management)
- ✅ Free tier generoso
- ✅ Queries rápidas

**Implementación:**

```python
from google.cloud import firestore

class FirestoreJobStore:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection('tikun_jobs')

    def create_job(self, job_id: str, job_data: dict):
        self.collection.document(job_id).set({
            **job_data,
            'created_at': firestore.SERVER_TIMESTAMP
        })

    def get_job(self, job_id: str) -> dict:
        doc = self.collection.document(job_id).get()
        if not doc.exists:
            raise HTTPException(404, "Job not found")
        return doc.to_dict()

    def update_job(self, job_id: str, updates: dict):
        self.collection.document(job_id).update(updates)

# En main.py
job_store = FirestoreJobStore()
```

**Setup:**
```bash
# Habilitar Firestore API
gcloud services enable firestore.googleapis.com --project=tikunframework

# Crear database (console o CLI)
gcloud firestore databases create --location=us-central1 --project=tikunframework
```

---

### 🚀 Opción B: Redis (Memorystore)

**Pros:**
- ✅ Más rápido que Firestore
- ✅ TTL automático
- ✅ Pub/Sub para real-time updates

**Contras:**
- ⚠️ Requiere infra (Memorystore instance)
- ⚠️ Costo mínimo ~$50/mes

**Implementación:**

```python
import redis
import json
import os

r = redis.from_url(os.getenv('REDIS_URL'))

def create_job(job_id: str, job_data: dict):
    r.setex(
        f"job:{job_id}",
        3600,  # TTL 1 hora
        json.dumps(job_data)
    )

def get_job(job_id: str) -> dict:
    data = r.get(f"job:{job_id}")
    if not data:
        raise HTTPException(404, "Job not found")
    return json.loads(data)
```

---

### 🛠️ Opción C: Cloud SQL (PostgreSQL)

**Pros:**
- ✅ Persistencia completa
- ✅ Queries complejas
- ✅ Backup automático

**Contras:**
- ⚠️ Más complejo
- ⚠️ Overhead de setup
- ⚠️ Costo

---

## 📝 FRONTEND FIXES (Inmediato)

### Fix 1: Manejo de 404 + Stop Polling

```typescript
// frontend/src/components/AnalysisForm.tsx

const pollJobStatus = async (jobId: string) => {
  const MAX_RETRIES = 100;
  const POLL_INTERVAL = 3000; // 3 segundos
  let retries = 0;

  const interval = setInterval(async () => {
    try {
      const status = await api.getJobStatus(jobId);

      if (status.status === 'completed') {
        clearInterval(interval);
        setResults(status.results);
      } else if (status.status === 'failed') {
        clearInterval(interval);
        setError(status.error);
      }

      retries = 0; // Reset en éxito

    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 404) {
          retries++;

          if (retries >= 3) {
            // 3 404s consecutivos = job perdido
            clearInterval(interval);
            setError(
              "Job not found. The Cloud Run instance may have restarted. " +
              "Please try again or use the synchronous endpoint."
            );
          }
        } else {
          // Otro error
          clearInterval(interval);
          setError(`Error: ${error.message}`);
        }
      }
    }

    if (++retries >= MAX_RETRIES) {
      clearInterval(interval);
      setError("Analysis timeout after 5 minutes");
    }
  }, POLL_INTERVAL);
};
```

### Fix 2: Timeout Visual

```typescript
const [timeElapsed, setTimeElapsed] = useState(0);

useEffect(() => {
  const timer = setInterval(() => {
    setTimeElapsed(prev => prev + 1);
  }, 1000);

  return () => clearInterval(timer);
}, []);

// En UI
<p>Time elapsed: {Math.floor(timeElapsed / 60)}:{timeElapsed % 60}</p>
```

---

## 🎯 PLAN DE ACCIÓN

### Para el Hackathon (HOY):
1. ✅ **Usar endpoint síncrono** para demos y testing
2. ✅ **Agregar frontend 404 handling** (5 minutos de código)
3. ✅ **Documentar limitación** en README/Devpost

### Post-Hackathon (Semana 1):
4. ⬜ **Implementar Firestore job storage**
5. ⬜ **Migrar async endpoint** a usar Firestore
6. ⬜ **Testing multi-instance**

---

## 📌 NOTAS IMPORTANTES

### ¿Por qué no pasó en pruebas locales?

**Desarrollo local:**
```bash
uvicorn tikun.api.main:app --reload
```
- ✅ Una sola instancia siempre
- ✅ Jobs persisten en memoria mientras el proceso corre
- ✅ No hay auto-scaling

**Producción (Cloud Run):**
```
Request 1 → Instance A (new)
Request 2 → Instance B (new)  # Diferentes instancias
Request 3 → Instance A (reused)
```
- ❌ Múltiples instancias concurrentes
- ❌ Cold starts reinician memoria
- ❌ Auto-scale to zero destruye instancias

### ¿Por qué un job SÍ completó?

En los logs vimos:
```
2025-12-30 02:19:54 | Background analysis completed
2025-12-30 02:20:03 | GET /jobs/... 200 OK
```

**Hipótesis:**
- User hizo polling consistente
- Algunos requests **hit la instancia correcta** por suerte
- Ese 200 OK confirma que el job SÍ existía en esa instancia

Pero luego:
```
2025-12-30 02:20:03 | GET /jobs/... 404 Not Found  # Siguiente request hit otra instancia
```

---

## 🔗 REFERENCIAS

- **Issue en GitHub:** [Cloud Run multi-instance job persistence](https://github.com/tikun-olam/issues/xxx)
- **GCP Docs:** [Firestore Quickstart](https://cloud.google.com/firestore/docs/quickstart-servers)
- **Alternativa:** [Redis + Cloud Run](https://cloud.google.com/memorystore/docs/redis)

---

**Creado:** 2025-12-30 02:30 UTC
**Última actualización:** 2025-12-30 02:30 UTC
**Status:** Documentado, workaround activo, fix permanente pendiente
