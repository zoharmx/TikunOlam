# 📸 GUÍA DE SCREENSHOTS PARA DEVPOST SUBMISSION

**Proyecto:** Tikun Olam
**Para:** Google Cloud AI Partner Catalyst - Datadog Challenge
**URL:** https://tikun-olam-hzz2wlra6a-uc.a.run.app/

---

## 🎯 SCREENSHOTS REQUERIDOS

### 1. Landing Page - Hero Section ✨
**URL:** `https://tikun-olam-hzz2wlra6a-uc.a.run.app/`

**Elementos a capturar:**
- ✅ Título: "Ethical Reasoning Architecture for AI" (ahora en inglés)
- ✅ Subtitle: "Don't just optimize for utility. Optimize for repair."
- ✅ Botones: "Access Console" + "Watch UBI/UN Demo"
- ✅ Logo "תיקון עולם" en hebreo + "TikunOlam"
- ✅ Badges: "BinahSigma Active" + "10 Sefirot"

**Tamaño recomendado:** 1920x1080 (full screen)
**Vista:** Desktop (responsive también funciona)

**Tip para captura:**
```
Herramientas:
- Windows: Win + Shift + S (Snipping Tool)
- Chrome DevTools: Ctrl+Shift+P → "Capture full size screenshot"
- Online: https://www.screenshotmachine.com
```

---

### 2. Landing Page - Features Grid 🎨
**URL:** `https://tikun-olam-hzz2wlra6a-uc.a.run.app/`
**Scroll:** Hacia abajo para ver las 3 feature cards

**Elementos a capturar:**
- ✅ Card 1: "10 Sefirot Pipeline" (ahora en inglés)
  - Icon: BrainCircuit
  - Desc: "Breaks down complex decisions into 10 functional stages..."

- ✅ Card 2: "BinahSigma Engine"
  - Icon: Globe
  - Desc: "Detects and quantifies civilizational biases..."

- ✅ Card 3: "Full Auditability"
  - Icon: ShieldCheck
  - Desc: "Every decision generates an immutable reasoning trail..."

**Tamaño:** 1920x1080
**Highlight:** Las 3 cards side-by-side

---

### 3. Dashboard - Analysis Form 📝
**URL:** `https://tikun-olam-hzz2wlra6a-uc.a.run.app/app`

**Elementos a capturar:**
- ✅ Header: "תיקון עולם" + "Ethical AI Reasoning Framework"
- ✅ Form title: "Analyze Ethical Scenario"
- ✅ Example scenario buttons: "Universal Basic Income" + "AI Governance Framework"
- ✅ Sefirot pipeline explanation (10 bullet points con colores)
- ✅ "Analyze Scenario" button (azul con glow effect)

**Tamaño:** 1920x1080
**Estado:** Form vacío o con uno de los ejemplos cargados

**Bonus:** Mostrar el contador de caracteres activo

---

### 4. Analysis Results - Complete Pipeline 🎯
**Cómo obtener:** Ejecutar un análisis completo

**Pasos:**
1. Ir a `/app`
2. Click en "Universal Basic Income (UBI)" para cargar ejemplo
3. Click "Analyze Scenario"
4. Esperar ~7-8 minutos
5. Capturar resultados completos

**Elementos a capturar:**

#### Screenshot 4A: Keter Results
- ✅ Alignment Percentage: 70%
- ✅ Corruption Severity: medium
- ✅ Dimensional Scores: Justice, Compassion, Wisdom, etc.
- ✅ Corruptions Detected: Inequity + Irreversibility

#### Screenshot 4B: Chochmah Wisdom
- ✅ Confidence Level: 85%
- ✅ Patterns Identified (5 patterns):
  - The Pacing Problem
  - Technological Solutionism
  - The Ratchet Effect
  - etc.
- ✅ Historical Precedents (3):
  - COPPA (1998)
  - US Prohibition
  - Hays Code
- ✅ Hidden Insights (4)
- ✅ Paradoxes (3)

#### Screenshot 4C: BinahSigma (CRÍTICO - CORE DIFFERENTIATOR)
- ✅ Contextual Depth Score: 95/100
- ✅ Stakeholder Analysis:
  - Beneficiaries
  - Harmed
  - Ignored/Invisible
- ✅ Ethical Tensions (4)
- ✅ Contextual Factors (Historical, Cultural, Economic, Political)

**Nota:** Si BinahSigma está en "simple mode", mostrar que igual hace análisis profundo contextual

#### Screenshot 4D: Malchut Final Decision
- ✅ Decision: CONDITIONAL_GO / GO / NO_GO
- ✅ Confidence: high / medium / low
- ✅ Key Recommendations
- ✅ Implementation Roadmap

---

### 5. API Documentation 📚
**URL:** `https://tikun-olam-hzz2wlra6a-uc.a.run.app/docs`

**Elementos a capturar:**
- ✅ FastAPI Swagger UI
- ✅ Endpoints visibles:
  - POST /analyze
  - POST /analyze/async
  - GET /jobs/{job_id}
  - GET /health
- ✅ Modelo de datos: AnalysisRequest, AnalysisResponse
- ✅ Schemas expandidos mostrando la estructura

**Tamaño:** 1920x1080 (puede requerir scroll largo)
**Highlight:** La complejidad del pipeline evidenciada en los schemas

---

### 6. Datadog Dashboard (Opcional pero Recomendado) 📊
**URL:** `https://us5.datadoghq.com`

**Si hay datos disponibles, capturar:**

#### Dashboard Custom (si lo creaste):
- ✅ Total Analyses (count)
- ✅ Success Rate (%)
- ✅ Average Duration per Sefira (bar chart)
- ✅ BinahSigma Activation Rate
- ✅ Bias Delta Distribution

#### Logs Explorer:
- ✅ Logs de un análisis completo
- ✅ Filtro: `service:tikun-olam @case_name:*`
- ✅ Mostrar structured logging (JSON)

#### APM (si está habilitado):
- ✅ Service map
- ✅ Traces de /analyze endpoint
- ✅ Latencia por operación

**Nota:** Si no hay suficientes datos aún, esto puede omitirse o generarse después de más tests

---

### 7. Cloud Run Console 🚀
**URL:** `https://console.cloud.google.com/run`

**Elementos a capturar:**
- ✅ Service: tikun-olam
- ✅ Region: us-central1
- ✅ Status: ✅ Healthy
- ✅ Metrics tab:
  - Request count
  - Request latency
  - Instance count
  - Memory utilization
- ✅ Revisions tab:
  - Latest revision: tikun-olam-00007-xxx (o actual)
  - Traffic: 100%
  - Status: Active

---

### 8. Architecture Diagram (Bonus) 🏗️
**Crear manualmente o usar:**
- Draw.io
- Excalidraw
- Lucidchart

**Elementos a mostrar:**
```
┌─────────────┐
│   Frontend  │ (React + Vite)
│  Cloud Run  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Backend    │ (FastAPI)
│  Cloud Run  │
└──────┬──────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌────────────┐  ┌────────────┐
│ Vertex AI  │  │ Datadog    │
│  Gemini    │  │  Metrics   │
└────────────┘  └────────────┘
       │
       ▼
┌────────────┐
│ Anthropic  │
│  Claude    │
└────────────┘
       │
       ▼
┌────────────┐
│ DeepSeek   │
│   Chat     │
└────────────┘
```

**Mostrar:**
- 10 Sefirot Pipeline flow
- BinahSigma adversarial comparison (West vs East)
- Data flow desde user input hasta final decision

---

## 📋 CHECKLIST DE SCREENSHOTS

Antes de submit a Devpost, verificar que tienes:

- [ ] **Screenshot 1:** Landing Page Hero (inglés) ✅
- [ ] **Screenshot 2:** Features Grid (3 cards)
- [ ] **Screenshot 3:** Analysis Form (dashboard)
- [ ] **Screenshot 4A:** Keter Results
- [ ] **Screenshot 4B:** Chochmah Wisdom
- [ ] **Screenshot 4C:** BinahSigma Analysis ⭐ (CORE DIFFERENTIATOR)
- [ ] **Screenshot 4D:** Malchut Final Decision
- [ ] **Screenshot 5:** API Docs (Swagger UI)
- [ ] **Screenshot 6:** Datadog Dashboard (opcional)
- [ ] **Screenshot 7:** Cloud Run Console
- [ ] **Screenshot 8:** Architecture Diagram (bonus)

**Mínimo requerido:** Screenshots 1-5
**Recomendado:** Screenshots 1-7
**Impresionante:** Todo incluyendo 8

---

## 🎨 TIPS PARA MEJORES SCREENSHOTS

### 1. Resolución
- Usar **1920x1080** para desktop
- Usar **1440x900** si es laptop
- Evitar 4K (demasiado grande para web)

### 2. Browser
- **Chrome DevTools:** Mejores herramientas de screenshot
- **Firefox:** Captura nativa de página completa
- Sin extensiones visibles en la barra

### 3. Zoom
- **100%** (no zoom in/out)
- **Full screen** (F11) para capturas limpias
- Ocultar bookmarks bar

### 4. Timing
- Esperar a que **todas las animaciones** terminen
- Esperar carga completa de **todos los assets**
- Para Framer Motion animations, esperar ~2 segundos

### 5. Edición Post-Captura
- Agregar **flechas/highlights** para puntos clave
- **Anotar** features importantes
- **Crop** para enfocarse en lo relevante
- Mantener **aspect ratio** consistente

### 6. Formato
- Guardar como **PNG** (no JPG)
- Comprimir si >2MB (TinyPNG.com)
- Nombrar descriptivamente:
  - `tikun_landing_hero.png`
  - `tikun_binah_sigma_analysis.png`
  - `tikun_api_docs.png`

---

## 🚀 CÓMO EJECUTAR UN ANÁLISIS PARA SCREENSHOTS

### Opción 1: Via Frontend (Recomendado para screenshots)
```
1. Ir a https://tikun-olam-hzz2wlra6a-uc.a.run.app/app
2. Click "Universal Basic Income (UBI)"
3. Click "Analyze Scenario"
4. Esperar ~7-8 minutos
5. Tomar screenshots mientras los resultados aparecen
```

### Opción 2: Via curl (Para testing rápido)
```bash
curl -X POST "https://tikun-olam-hzz2wlra6a-uc.a.run.app/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "A government is considering mandatory AI ethics certification for all autonomous systems deployed in public spaces.",
    "case_name": "screenshot_test",
    "include_full_results": true
  }' \
  --max-time 1800 > results.json

# Ver resultados formateados
cat results.json | jq '.'
```

---

## 📝 CAPTIONS SUGERIDOS PARA DEVPOST

### Screenshot 1 (Landing):
```
Tikun Olam: Ethical Reasoning Architecture for AI
Multi-civilizational ethical analysis with civilizational bias detection (BinahSigma)
```

### Screenshot 2 (Features):
```
Core Features: 10 Sefirot Pipeline, BinahSigma Engine for bias detection,
and full auditability trail
```

### Screenshot 3 (Form):
```
Analysis Dashboard: Submit ethical scenarios for comprehensive 10-stage reasoning
Example: Universal Basic Income funded by 1% of military spending
```

### Screenshot 4C (BinahSigma - MÁS IMPORTANTE):
```
BinahSigma in Action: Detecting civilizational biases by comparing
Western (Gemini) vs Eastern (DeepSeek) perspectives on the same scenario.
Contextual depth score: 95/100
```

### Screenshot 5 (API):
```
Production API: FastAPI with comprehensive schema validation,
async job processing, and structured reasoning output
```

---

## 🎯 KEY MESSAGING PARA DEVPOST

**En tus captions/descriptions, enfatizar:**

1. **Innovation:** "First framework to detect civilizational bias in AI reasoning (BinahSigma)"

2. **Technical Depth:** "10-stage pipeline based on Kabbalistic Sefirot, integrating 3 AI providers"

3. **Production Ready:** "Deployed on Google Cloud Run with Datadog observability"

4. **Real Impact:** "Transforms AI from optimization machines to ethical reasoning systems"

5. **Unique Value:** "Don't just optimize for utility. Optimize for repair (Tikun Olam)"

---

## ✅ READY TO SCREENSHOT

**Una vez que el deployment complete (~2 minutos más), todo estará listo:**
- ✅ Frontend en inglés
- ✅ Sistema 100% funcional
- ✅ Todos los endpoints activos
- ✅ API docs accesibles
- ✅ Listo para ejecutar análisis

**Próximo paso:** Esperar deployment → Tomar screenshots → Submit a Devpost!

---

**Creado:** 2025-12-30
**URL de Producción:** https://tikun-olam-hzz2wlra6a-uc.a.run.app/
**Status:** Listo para screenshots
