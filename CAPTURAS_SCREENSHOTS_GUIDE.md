# 📸 GUÍA DE CAPTURAS - Resultados Nvidia-Groq

**Archivo a usar**: `C:\Users\jesus\TikunOlam\results\tikun_Nvidia_Groq_20251226_182512.json`

## ✅ DATOS CONFIRMADOS

- **BinahSigma Divergencia**: **75%** ⭐
- **Nivel**: HIGH (Alto)
- **Puntos Ciegos**: **16 totales** (8 Western + 8 Eastern)
- **Decisión Final**: **CONDITIONAL_GO**
- **Confianza**: HIGH (Alta)
- **Duración**: 646.6 segundos = **10.8 minutos**
- **Timestamp**: 2025-12-26 18:14:26

---

## 🎯 PASO 1: Abrir el Archivo

```bash
# Abre VS Code con el archivo:
code "C:\Users\jesus\TikunOlam\results\tikun_Nvidia_Groq_20251226_182512.json"
```

**Preparación en VS Code:**
1. Presiona `Ctrl+Shift+P`
2. Escribe: `Format Document`
3. Enter (formatea el JSON)
4. Presiona `Ctrl+G` para ir a línea específica
5. Zoom: `Ctrl +` hasta 130-150%

---

## 📷 CAPTURAS OBLIGATORIAS (6 Total)

### CAPTURA 1: BinahSigma - Divergencia 75% ⭐⭐⭐ CRÍTICA

**Cómo llegar:**
- Presiona `Ctrl+G` → Escribe `24` → Enter
- O busca: `Ctrl+F` → `"bias_delta"`

**Qué capturar (líneas 23-40):**
```json
"binah": {
  "bias_delta": 75,                    ← RESALTA ESTA LÍNEA
  "blind_spots_detected": 16,          ← Y ESTA
  "contextual_depth_score": 90,
  "contextual_factors": [
    "Multi-civilizational value divergence",
    "Geopolitical tension present",
    "Cultural assumptions embedded"
  ],
  "convergence_points": 5,
  "divergence_level": "high",          ← TAMBIÉN IMPORTANTE
  "mode": "sigma",                     ← SIGMA ACTIVADO
```

**Checklist:**
- [ ] `bias_delta: 75` visible y resaltado
- [ ] `blind_spots_detected: 16` visible
- [ ] `mode: "sigma"` visible
- [ ] `divergence_level: "high"` visible
- [ ] Pestaña del archivo visible arriba
- [ ] Zoom 150%

---

### CAPTURA 2: Decisión Final - CONDITIONAL_GO ⭐⭐⭐ CRÍTICA

**Cómo llegar:**
- Presiona `Ctrl+F`
- Busca: `"malchut"`
- Baja hasta ver `"decision"`

**Qué capturar:**
```json
"malchut": {
  "conditions": [
    "depth investigation into the Nvidia-Groq transaction...",
    ...
  ],
  "confidence": "high",                ← CONFIANZA ALTA
  "decision": "CONDITIONAL_GO",        ← DECISIÓN FINAL
```

**Checklist:**
- [ ] `"decision": "CONDITIONAL_GO"` muy visible
- [ ] `"confidence": "high"` visible
- [ ] Nombre de la sección `"malchut"` visible

---

### CAPTURA 3: Puntos Ciegos Occidentales ⭐⭐

**Cómo llegar:**
- Presiona `Ctrl+F`
- Busca: `west_blind_spots`

**Qué capturar (líneas 58-63):**
```json
"west_blind_spots": [
  "**Underestimation of National Strategic Imperatives:** The focus on abstract principles...",
  "**Idealization of a \"Level Playing Field\":\" The Western lens can sometimes romanticize...",
  "**Process-Oriented Slowness:** The commitment to due process, investigation...",
  "**Potential for Regulatory Capture/Error:** The framework assumes regulators are benevolent..."
]
```

**Checklist:**
- [ ] Los 4 puntos ciegos visibles
- [ ] Texto legible (puede estar truncado, está bien)
- [ ] Título `west_blind_spots` visible

---

### CAPTURA 4: Puntos Ciegos Orientales ⭐⭐

**Cómo llegar:**
- Presiona `Ctrl+F`
- Busca: `east_blind_spots`

**Qué capturar (líneas 42-49):**
```json
"east_blind_spots": [
  "**The Generative Power of Disruptive, \"Selfish\" Competition:** This perspective may undervalue...",
  "**Efficiency Gains from Consolidation:** The potential for significant short-to-medium term...",
  "**The Role of the Exceptional Individual (Founder):** The Eastern lens, emphasizing the collective...",
  "**Regulatory Overreach Stifling a National Champion:** In a global tech race..."
]
```

**Checklist:**
- [ ] Al menos 4 puntos ciegos visibles
- [ ] Contraste con Western visible (si están juntos en pantalla)
- [ ] Título `east_blind_spots` visible

---

### CAPTURA 5: Síntesis Trascendente ⭐⭐

**Cómo llegar:**
- Presiona `Ctrl+F`
- Busca: `transcendent_synthesis`

**Qué capturar (línea 50):**
```json
"transcendent_synthesis": "A transcendent synthesis moves beyond the binary of blocking (Western process-focus) versus approving (Eastern strategic-focus). The FTC should impose a 'Competitive Dividend' as a condition of approval.\n\nThis approach permits the deal's core—the talent acquisition and non-exclusive license—addressing the need for speed and strategic resource pooling. However, it mandates that a substantial portion of the $20B premium (e.g., $10B) be placed into an independently administered 'AI Hardware Innovation Fund.'\n\nThis fund provides non-dilutive capital to the next generation of competing US-based chip startups..."
```

**Checklist:**
- [ ] Frase "Competitive Dividend" visible
- [ ] Concepto de "$10B into Innovation Fund" visible
- [ ] Muestra síntesis entre Western y Eastern

---

### CAPTURA 6: Metadata - Timing y Modelos ⭐

**Cómo llegar:**
- Presiona `Ctrl+Home` (va al inicio)
- O `Ctrl+G` → Línea `2`

**Qué capturar (líneas 2-20):**
```json
"metadata": {
  "case_name": "Nvidia_Groq",
  "models_used": {
    "binah": "gemini-2.5-pro + deepseek-chat",  ← DUAL MODEL
    "chesed": "gemini-2.5-pro",
    "chochmah": "gemini-2.5-pro",
    "gevurah": "gemini-2.5-pro",
    "keter": "gemini-2.5-pro",
    "malchut": "gemini-2.5-pro"
  },
  "scenario_length": 5377,
  "timestamp": "2025-12-26T18:14:26.364201",
  "total_duration_seconds": 646.6,               ← 10.8 MINUTOS
  "version": "1.0.0"
}
```

**Checklist:**
- [ ] `total_duration_seconds: 646.6` visible
- [ ] `binah: "gemini-2.5-pro + deepseek-chat"` visible (muestra dual-model)
- [ ] Timestamp visible
- [ ] Case name visible

---

## 🖥️ ALTERNATIVA: Capturas desde Terminal

Si prefieres mostrar datos "en vivo" desde el API:

### Terminal Captura 1: BinahSigma Metrics
```bash
curl -s http://127.0.0.1:8000/jobs/260d39d4-8171-40e2-a78e-cfde4ccb225c | jq '.results.sefirot_results.binah | {mode, bias_delta, divergence_level, blind_spots_detected}'
```

**Salida esperada:**
```json
{
  "mode": "sigma",
  "bias_delta": 75,
  "divergence_level": "high",
  "blind_spots_detected": 16
}
```

### Terminal Captura 2: Decisión Final
```bash
curl -s http://127.0.0.1:8000/jobs/260d39d4-8171-40e2-a78e-cfde4ccb225c | jq '.results.sefirot_results.malchut | {decision, confidence}'
```

**Salida esperada:**
```json
{
  "decision": "CONDITIONAL_GO",
  "confidence": "high"
}
```

### Terminal Captura 3: Metadata
```bash
curl -s http://127.0.0.1:8000/jobs/260d39d4-8171-40e2-a78e-cfde4ccb225c | jq '.results.metadata | {case_name, total_duration_seconds, timestamp}'
```

---

## 📊 LISTA DE VERIFICACIÓN FINAL

Antes de grabar el video, confirma que tienes:

### Capturas de JSON (VS Code):
- [ ] ⭐⭐⭐ BinahSigma (bias_delta: 75, blind_spots: 16)
- [ ] ⭐⭐⭐ Malchut Decision (CONDITIONAL_GO, high confidence)
- [ ] ⭐⭐ Western blind spots (4 items)
- [ ] ⭐⭐ Eastern blind spots (4+ items)
- [ ] ⭐⭐ Transcendent synthesis (Competitive Dividend)
- [ ] ⭐ Metadata (timing: 646.6s, dual models)

### Capturas de Terminal (Opcional):
- [ ] BinahSigma extract (curl + jq)
- [ ] Decision extract (curl + jq)
- [ ] Metadata extract (curl + jq)
- [ ] Health check (API running)

---

## 🎬 GUIÓN DE VOZ (Para usar con estas capturas)

**Para Captura 1 (BinahSigma):**
```
"Aquí vemos el núcleo del análisis: BinahSigma detectó
una divergencia civilizacional del 75% entre las perspectivas
occidental y oriental sobre monopolios tecnológicos.
Se identificaron 16 puntos ciegos distintos."
```

**Para Captura 2 (Decisión):**
```
"La decisión final: CONDITIONAL_GO—aprobación condicional.
No es un simple sí o no. Es una síntesis que reconoce
la complejidad del caso y propone supervisión activa."
```

**Para Capturas 3-4 (Blind Spots):**
```
"La perspectiva occidental no ve los imperativos estratégicos nacionales.
La perspectiva oriental no ve el poder de la competencia disruptiva.
Cada civilización tiene sus ángulos muertos."
```

**Para Captura 5 (Síntesis):**
```
"La síntesis trascendente propone algo que ninguna perspectiva
imaginó sola: un 'Dividendo Competitivo'—usar 10 mil millones
del precio de compra para financiar a la próxima generación
de competidores. Convierte la consolidación en catalizador
de innovación futura."
```

**Para Captura 6 (Metadata):**
```
"Todo esto se generó en 10.8 minutos usando una arquitectura
multi-modelo: Gemini representando el pensamiento occidental,
DeepSeek el oriental, en debate adversarial directo."
```

---

## 🚀 PRÓXIMOS PASOS

Una vez completadas estas 6 capturas:

1. **Guardar screenshots** en carpeta `screenshots/` con nombres descriptivos:
   - `01_binah_sigma_75_divergence.png`
   - `02_malchut_conditional_go.png`
   - `03_west_blind_spots.png`
   - `04_east_blind_spots.png`
   - `05_transcendent_synthesis.png`
   - `06_metadata_timing.png`

2. **Capturas de Datadog** (5 min):
   - Abrir `monitoring/datadog_config.py`
   - Ver: `DATADOG_HACKATHON_SOLUTION.md`

3. **Crear gráficos** (30 min):
   - Medidor de divergencia 75%
   - Diagrama de flujo de decisión
   - Árbol de Sefirot con tiempos

4. **Actualizar VIDEO_DEMO_SCRIPT.md**:
   - Cambiar todos los "95%" → "75%"
   - Cambiar "14 blind spots" → "16 blind spots"
   - Actualizar timing "8.9 min" → "10.8 min"

---

## 💡 TIPS PARA MEJORES CAPTURAS

**Configuración de VS Code:**
- Tema oscuro: `Ctrl+K Ctrl+T` → "Dark+"
- Quitar minimap: `Ctrl+Shift+P` → "Toggle Minimap"
- Fullscreen: `F11`
- Quitar barra lateral: `Ctrl+B`

**Herramientas de captura:**
- Windows: `Win+Shift+S` (Snipping Tool)
- ShareX (gratis, más profesional)
- OBS Studio (para grabación de pantalla)

**Calidad:**
- Resolución: Mínimo 1920x1080
- Formato: PNG (sin compresión)
- Contraste: Alto (texto blanco sobre fondo oscuro)
- Zoom: 130-150% para legibilidad en video

---

## ✅ VERIFICACIÓN PRE-VIDEO

Antes de grabar, revisa cada screenshot:
- [ ] Texto completamente legible
- [ ] Sin información sensible visible (API keys, etc.)
- [ ] Nombre de archivo visible en pestaña
- [ ] Números clave resaltados o claramente visibles
- [ ] Sin distracciones en pantalla (notificaciones, etc.)

---

**¡LISTO! Con estas 6 capturas tienes todo el material visual para demostrar BinahSigma en acción.**
