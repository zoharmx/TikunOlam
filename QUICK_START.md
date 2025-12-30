# Quick Start - Tikun Olam con Vertex AI

## Instalación Rápida (2 minutos)

### 1. Instalar Dependencias Backend

```powershell
# En PowerShell (como administrador si es necesario)
pip install -r requirements.txt
```

**Dependencias principales que se instalarán:**
- `google-cloud-aiplatform` - Vertex AI SDK
- `ddtrace`, `datadog-api-client`, `datadog` - Observabilidad
- Y todas las demás dependencias existentes

### 2. Verificar Instalación

```powershell
python test_vertex_migration.py
```

## Solución de Problemas

### Error: "No module named 'vertexai'"

**Solución:**
```powershell
pip install google-cloud-aiplatform
```

### Error: "Could not automatically determine credentials"

**Opción 1 - Usando gcloud (Recomendado para desarrollo local):**
```powershell
gcloud auth application-default login
```

**Opción 2 - Usando Service Account:**
```powershell
# Descargar JSON key de GCP Console
# Configurar variable de entorno:
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\ruta\hacia\vertex-ai-key.json"

# O en CMD:
set GOOGLE_APPLICATION_CREDENTIALS=C:\ruta\hacia\vertex-ai-key.json
```

### Error: "GCP_PROJECT_ID not configured"

Verificar que `.env` tenga:
```
GCP_PROJECT_ID=algebraic-craft-453221-g1
GCP_LOCATION=us-central1
```

✅ **YA CONFIGURADO** - Tu .env ya tiene el project ID correcto!

### Error: "Permission denied" o "API not enabled"

1. Habilitar Vertex AI API:
   ```powershell
   gcloud services enable aiplatform.googleapis.com --project=algebraic-craft-453221-g1
   ```

2. O manualmente:
   - Ve a: https://console.cloud.google.com/apis/library/aiplatform.googleapis.com
   - Selecciona proyecto: `algebraic-craft-453221-g1`
   - Click "Enable"

## Ejecutar Test

```powershell
# Test de migración Vertex AI
python test_vertex_migration.py
```

**Resultado esperado:**
```
🚀 TIKUN OLAM - VERTEX AI MIGRATION TEST

================================================================================
TEST 1: Vertex AI Initialization
================================================================================
✅ GCP Project ID: algebraic-craft-453221-g1
✅ GCP Location: us-central1
✅ Keter Model: gemini-1.5-pro

================================================================================
TEST 2: Keter Vertex AI Integration
================================================================================
✅ Keter initialized successfully
✅ Vertex AI call successful!
✅ Response structure validated

🎉 ALL CRITICAL TESTS PASSED!
```

## Ejecutar Pipeline Completo

```powershell
# 1. Iniciar backend
uvicorn src.tikun.api.main:app --reload --port 8000

# 2. En otra terminal, iniciar frontend
cd frontend
npm install  # Solo primera vez
npm run dev
```

## Estado de tu Configuración

✅ **GCP_PROJECT_ID** configurado: `algebraic-craft-453221-g1`
✅ **GCP_LOCATION** configurado: `us-central1`
✅ **GEMINI_API_KEY** configurado
✅ **DEEPSEEK_API_KEY** configurado

⏳ **Pendiente:**
- Instalar dependencias: `pip install -r requirements.txt`
- Configurar credenciales GCP: `gcloud auth application-default login`
- Habilitar Vertex AI API en GCP Console

## Credenciales GCP - Opciones

### Opción A: gcloud CLI (Más fácil para desarrollo)

```powershell
# Instalar gcloud CLI si no lo tienes:
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Configurar proyecto
gcloud config set project algebraic-craft-453221-g1

# Configurar credenciales para aplicaciones
gcloud auth application-default login
```

### Opción B: Service Account JSON (Para producción)

1. Ir a: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Seleccionar proyecto: `algebraic-craft-453221-g1`
3. Crear Service Account con rol: "Vertex AI User"
4. Descargar JSON key
5. Configurar variable de entorno (en cada sesión de PowerShell):
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\ruta\hacia\service-account-key.json"
   ```

## Siguiente Paso

Una vez que ejecutes exitosamente `python test_vertex_migration.py`, podrás:

1. ✅ Ejecutar análisis completos con Vertex AI
2. ✅ Ver métricas en Datadog (cuando configures las API keys)
3. ✅ Usar el frontend con observabilidad en tiempo real

---

**¿Necesitas ayuda?** Revisa `VERTEX_AI_SETUP.md` para más detalles.
