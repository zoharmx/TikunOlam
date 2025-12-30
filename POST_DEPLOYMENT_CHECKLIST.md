# 🚀 POST-DEPLOYMENT CHECKLIST - TIKUN OLAM

**Deployment en progreso:** Cloud Run
**Proyecto:** tikunframework
**Fecha:** 2025-12-28

---

## ✅ YA COMPLETADO

### Configuración Inicial:
- [x] Proyecto GCP configurado: `tikunframework`
- [x] APIs habilitadas (Cloud Run, Cloud Build, Secret Manager, Vertex AI)
- [x] Secrets creados en Secret Manager:
  - [x] GEMINI_API_KEY
  - [x] DEEPSEEK_API_KEY
  - [x] DATADOG_API_KEY
  - [x] DATADOG_APP_KEY
- [x] Permisos de secrets configurados para Cloud Run
- [x] Scripts de deployment actualizados
- [x] Frontend construido exitosamente (8 min build time)

### En Progreso:
- ⏳ Cloud Build construyendo imagen Docker (~10-15 min)

---

## 📋 CHECKLIST INMEDIATAMENTE DESPUÉS DEL DEPLOYMENT

### 1. Obtener URL del Servicio ⭐ CRÍTICO

**Comando:**
```bash
gcloud run services describe tikun-olam --region us-central1 --project=tikunframework --format="value(status.url)"
```

**URL esperada:**
```
https://tikun-olam-495684990330.us-central1.run.app
```

**Acción:** Guardar esta URL para:
- [ ] Devpost submission
- [ ] README.md
- [ ] Video demo (si aplica)

---

### 2. Verificar Health Check ⭐ CRÍTICO

**Comando:**
```bash
curl https://YOUR-SERVICE-URL/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2025-12-28T..."
}
```

**Si falla:**
- [ ] Verificar logs: `gcloud run services logs read tikun-olam --region us-central1 --project=tikunframework`
- [ ] Verificar secrets están disponibles
- [ ] Verificar imagen se construyó correctamente

---

### 3. Probar API Documentation ⭐ IMPORTANTE

**URL:** `https://YOUR-SERVICE-URL/docs`

**Qué verificar:**
- [ ] Swagger UI carga correctamente
- [ ] Endpoints visibles:
  - [ ] POST /analyze (sync)
  - [ ] POST /analyze/async
  - [ ] GET /jobs/{job_id}
  - [ ] GET /health
  - [ ] GET /metrics
- [ ] Schemas de request/response visibles

---

### 4. Probar Frontend ⭐ CRÍTICO

**URL:** `https://YOUR-SERVICE-URL/`

**Qué verificar:**
- [ ] Página principal carga (landing page o dashboard)
- [ ] No hay errores en browser console (F12)
- [ ] CSS/estilos cargan correctamente
- [ ] Botón "Analyze Scenario" visible
- [ ] Datadog RUM inicializado (verificar en console logs)

---

### 5. Probar Análisis Completo ⭐ MUY IMPORTANTE

**Escenario de prueba rápido:**
```
A city council is considering implementing a universal basic income (UBI)
program funded by a 2% tax on automated services. The program would provide
$1000/month to all residents earning less than $50,000/year.
```

**Pasos:**
1. [ ] Abrir frontend: `https://YOUR-SERVICE-URL/`
2. [ ] Pegar escenario en text area
3. [ ] Case name: `test_ubi_deployment`
4. [ ] Click "Analyze Scenario"
5. [ ] Esperar ~8-12 minutos (el pipeline es largo por diseño)
6. [ ] Verificar resultado muestra:
   - [ ] BinahSigma bias_delta (número entre 0-100)
   - [ ] Blind spots detectados
   - [ ] Decisión final (GO/NO_GO/CONDITIONAL_GO)
   - [ ] Confianza (high/medium/low)

**Si falla o toma >15 min:**
- [ ] Revisar logs de Cloud Run
- [ ] Verificar timeout configurado (300s en Cloud Run)
- [ ] Verificar credenciales de Vertex AI (GEMINI_API_KEY, DEEPSEEK_API_KEY)

---

### 6. Verificar Métricas en Datadog ⭐ CRÍTICO PARA HACKATHON

**Dashboard URL:**
```
https://us5.datadoghq.com/dashboard/...
(usar el dashboard_url de tu configuración local)
```

**Qué verificar (después de 5-10 minutos):**
- [ ] Métricas aparecen con tag `env:production`
- [ ] `tikun.binah.bias_delta` tiene valores
- [ ] `tikun.binah.divergence_level` tiene categorías (low/medium/high)
- [ ] `tikun.pipeline.duration` muestra timings
- [ ] `tikun.ethical_alignment.average` tiene valores

**Si no aparecen métricas:**
- [ ] Verificar DATADOG_API_KEY es correcto en Secret Manager
- [ ] Revisar logs: buscar "Datadog initialized successfully"
- [ ] Verificar DATADOG_SITE correcto en env vars: `us5.datadoghq.com`

---

### 7. Verificar Logs de Cloud Run 📊 IMPORTANTE

**Comando:**
```bash
gcloud run services logs read tikun-olam --region us-central1 --project=tikunframework --limit=100
```

**Qué buscar:**
- [ ] "Application startup complete" o similar
- [ ] "Datadog initialized successfully"
- [ ] "Uvicorn running on..." (indica que FastAPI arrancó)
- [ ] No errores de "Secret not found"
- [ ] No errores de "Permission denied"
- [ ] No stack traces de Python

---

## 🔧 TROUBLESHOOTING COMÚN

### Problema: Service URL devuelve 404
**Causa:** Frontend no se sirvió correctamente
**Solución:**
```bash
# Verificar que el Dockerfile copió frontend/dist
# Revisar logs del build
gcloud builds list --project=tikunframework --limit=1
```

### Problema: /health devuelve 502 Bad Gateway
**Causa:** Backend no inició correctamente
**Solución:**
```bash
# Ver logs completos del servicio
gcloud run services logs read tikun-olam --region us-central1 --project=tikunframework --limit=200

# Verificar que uvicorn arrancó en el puerto correcto
# Cloud Run usa PORT env var (8080 por defecto)
```

### Problema: Análisis falla con timeout
**Causa:** Límite de timeout de Cloud Run alcanzado (300s = 5 min)
**Impacto:** Pipeline real toma 8-12 minutos, excede timeout
**Solución temporal:**
```bash
# Aumentar timeout a 900s (15 min) - máximo permitido
gcloud run services update tikun-olam \
  --timeout=900 \
  --region=us-central1 \
  --project=tikunframework
```

### Problema: Métricas no llegan a Datadog
**Causa 1:** API keys incorrectos
**Solución:**
```bash
# Verificar secret
gcloud secrets versions access latest --secret="DATADOG_API_KEY" --project=tikunframework

# Si es incorrecto, actualizar
echo "CORRECT_KEY" | gcloud secrets versions add DATADOG_API_KEY --data-file=- --project=tikunframework
```

**Causa 2:** DATADOG_SITE incorrecto
**Solución:** Verificar que env var `DATADOG_SITE=us5.datadoghq.com` (no `datadoghq.com`)

---

## 📊 MÉTRICAS DE ÉXITO

### Deployment exitoso si:
- [x] Health check returns 200 OK
- [x] Frontend carga sin errores
- [x] API docs accesibles
- [x] Puede completar un análisis (aunque tome tiempo)
- [x] Métricas aparecen en Datadog después de 1 análisis

### Puntos extra si:
- [ ] Análisis completa en <10 minutos
- [ ] Datadog dashboard muestra datos en tiempo real
- [ ] No hay errores 500 en logs
- [ ] RUM de Datadog captura interacciones de frontend

---

## 🎯 NEXT STEPS DESPUÉS DE VERIFICACIÓN

### Si todo funciona:
1. **Actualizar README.md** con:
   - URL de la aplicación desplegada
   - URL de API docs
   - URL de Datadog dashboard (si es público)

2. **Actualizar Devpost submission:**
   - Agregar URL del servicio
   - Mencionar "Deployed on Google Cloud Run"
   - Link a API documentation

3. **Opcional - Configurar dominio personalizado:**
   ```bash
   gcloud run domain-mappings create \
     --service tikun-olam \
     --domain your-domain.com \
     --region us-central1 \
     --project=tikunframework
   ```

4. **Opcional - Configurar HTTPS redirect:**
   - Cloud Run ya incluye HTTPS automático
   - Certificado SSL managed por Google

### Si hay problemas:
1. **Prioridad 1:** Health check y logs
2. **Prioridad 2:** Frontend carga
3. **Prioridad 3:** API funciona (aunque sea con timeout)
4. **Prioridad 4:** Datadog recibe métricas

**Recordar:** Para el hackathon, un deployment funcional con algunos timeouts es mejor que nada. Los jueces evaluarán principalmente:
- ✅ Innovación (BinahSigma civilizational bias detection)
- ✅ Uso de Google Cloud AI (Vertex AI ✅)
- ✅ Integración con Datadog (observabilidad ✅)
- ⚠️ Deployment en producción (nice to have, no crítico)

---

## 📞 RECURSOS ÚTILES

**GCP Console:**
- Cloud Run Services: https://console.cloud.google.com/run?project=tikunframework
- Cloud Build History: https://console.cloud.google.com/cloud-build/builds?project=tikunframework
- Secret Manager: https://console.cloud.google.com/security/secret-manager?project=tikunframework
- Logs Explorer: https://console.cloud.google.com/logs?project=tikunframework

**Datadog:**
- Dashboard: https://us5.datadoghq.com/dashboard/lists
- Metrics Explorer: https://us5.datadoghq.com/metric/explorer
- Infrastructure: https://us5.datadoghq.com/infrastructure

**Comandos rápidos:**
```bash
# Ver servicio
gcloud run services describe tikun-olam --region us-central1 --project=tikunframework

# Ver logs en tiempo real
gcloud run services logs tail tikun-olam --region us-central1 --project=tikunframework

# Ver últimas builds
gcloud builds list --project=tikunframework --limit=5

# Eliminar servicio (si necesitas re-deploy limpio)
gcloud run services delete tikun-olam --region us-central1 --project=tikunframework
```

---

**Creado:** 2025-12-28
**Estado:** Deployment en progreso ⏳
**Tiempo estimado restante:** ~10 minutos

---

✨ **¡Casi listo!** Cuando el deployment termine, sigue este checklist para verificar todo.
