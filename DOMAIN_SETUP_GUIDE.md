# 🌐 GUÍA DE CONFIGURACIÓN: Dominio Personalizado tikun.pro

**Objetivo:** Configurar https://tikun.pro para apuntar a Cloud Run service
**Status:** Requiere acciones manuales en Google Search Console + DNS provider

---

## 📋 PREREQUISITOS

1. ✅ Servicio Cloud Run desplegado: `tikun-olam`
2. ✅ URL actual: `https://tikun-olam-hzz2wlra6a-uc.a.run.app/`
3. ⚠️ **Dominio tikun.pro:** ¿Ya está registrado? ¿Dónde?
4. ⚠️ **Acceso a DNS:** Necesitas poder agregar registros DNS

---

## 🚀 PASO 1: VERIFICAR PROPIEDAD DEL DOMINIO

### Opción A: Google Search Console (Recomendado)

1. **Ir a Google Search Console:**
   ```
   https://search.google.com/search-console
   ```

2. **Agregar propiedad:**
   - Click "Add property"
   - Seleccionar "Domain" (no URL prefix)
   - Ingresar: `tikun.pro`

3. **Verificar vía DNS (TXT record):**
   Google te dará un código TXT como:
   ```
   google-site-verification=abc123xyz456...
   ```

4. **Agregar en tu DNS provider:**
   ```
   Type: TXT
   Name: @ (or tikun.pro)
   Value: google-site-verification=abc123xyz456...
   TTL: 3600
   ```

5. **Click "Verify" en Search Console**
   - Puede tomar hasta 24 horas
   - Una vez verificado, Google sabe que eres dueño del dominio

### Opción B: Google Cloud Domain Verification (Alternativa)

1. **Verificar dominio directamente con gcloud:**
   ```bash
   gcloud domains verify tikun.pro --project=tikunframework
   ```

2. **Seguir las instrucciones** que te proporcione el comando

---

## 🚀 PASO 2: CREAR DOMAIN MAPPING EN CLOUD RUN

Una vez que el dominio esté verificado:

```bash
gcloud beta run domain-mappings create \
  --service=tikun-olam \
  --domain=tikun.pro \
  --region=us-central1 \
  --project=tikunframework
```

**Output esperado:**
```
✓ Creating domain mapping...
  Domain: tikun.pro
  Service: tikun-olam

DNS records to configure:
  Type: A
  Name: tikun.pro
  Value: 216.239.32.21

  Type: A
  Name: tikun.pro
  Value: 216.239.34.21

  Type: A
  Name: tikun.pro
  Value: 216.239.36.21

  Type: A
  Name: tikun.pro
  Value: 216.239.38.21

  Type: AAAA
  Name: tikun.pro
  Value: 2001:4860:4802:32::15

  Type: AAAA
  Name: tikun.pro
  Value: 2001:4860:4802:34::15

  Type: AAAA
  Name: tikun.pro
  Value: 2001:4860:4802:36::15

  Type: AAAA
  Name: tikun.pro
  Value: 2001:4860:4802:38::15
```

Google te dará las IPs específicas para tu mapping.

---

## 🚀 PASO 3: CONFIGURAR DNS RECORDS

### Registros DNS a Agregar:

**Opción 1: Root domain (tikun.pro)**

Si quieres que `tikun.pro` (sin www) apunte a Cloud Run:

```dns
# A Records (IPv4)
Type: A
Name: @ (or tikun.pro)
Value: 216.239.32.21
TTL: 3600

Type: A
Name: @ (or tikun.pro)
Value: 216.239.34.21
TTL: 3600

Type: A
Name: @ (or tikun.pro)
Value: 216.239.36.21
TTL: 3600

Type: A
Name: @ (or tikun.pro)
Value: 216.239.38.21
TTL: 3600

# AAAA Records (IPv6) - Opcional pero recomendado
Type: AAAA
Name: @ (or tikun.pro)
Value: 2001:4860:4802:32::15
TTL: 3600

Type: AAAA
Name: @ (or tikun.pro)
Value: 2001:4860:4802:34::15
TTL: 3600

Type: AAAA
Name: @ (or tikun.pro)
Value: 2001:4860:4802:36::15
TTL: 3600

Type: AAAA
Name: @ (or tikun.pro)
Value: 2001:4860:4802:38::15
TTL: 3600
```

**Opción 2: Con subdomain (www.tikun.pro)**

Si prefieres `www.tikun.pro`:

```dns
Type: CNAME
Name: www
Value: ghs.googlehosted.com.
TTL: 3600
```

Y luego redirigir `tikun.pro` → `www.tikun.pro`

---

## 🚀 PASO 4: ESPERAR PROPAGACIÓN DNS

**Tiempo típico:** 15 minutos a 48 horas (usualmente 1-2 horas)

**Verificar propagación:**
```bash
# Check DNS propagation
nslookup tikun.pro

# Check A records
dig tikun.pro A

# Check AAAA records
dig tikun.pro AAAA
```

**Online tools:**
- https://dnschecker.org
- https://www.whatsmydns.net

---

## 🚀 PASO 5: HABILITAR HTTPS (Automático)

Cloud Run provee **SSL certificates automáticos** via Let's Encrypt/Google-managed.

**Una vez que DNS propague:**
1. Google detectará el domain mapping
2. Automáticamente provisionará certificado SSL
3. HTTPS estará disponible en ~15 minutos

**Verificar status:**
```bash
gcloud beta run domain-mappings describe tikun.pro \
  --region=us-central1 \
  --project=tikunframework
```

**Look for:**
```yaml
status:
  conditions:
  - type: Ready
    status: "True"
  - type: CertificateProvisioned
    status: "True"  # ✅ SSL certificate ready
```

---

## 🚀 PASO 6: FORZAR HTTPS (Opcional pero Recomendado)

Cloud Run automáticamente redirige HTTP → HTTPS, pero puedes agregar headers de seguridad en FastAPI:

```python
# src/tikun/api/main.py

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Force HTTPS in production
if config.tikun_env == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["tikun.pro", "www.tikun.pro", "*.tikun.pro"]
    )
```

---

## 📊 DÓNDE ESTÁ REGISTRADO TIKUN.PRO?

**Necesitas confirmar:**

1. **¿Ya está registrado el dominio?**
   - Verificar en: https://whois.domaintools.com/tikun.pro

2. **¿Dónde está el DNS configurado?**
   - GoDaddy?
   - Namecheap?
   - Cloudflare?
   - Google Domains?
   - Otro registrar?

3. **¿Tienes acceso al panel de DNS?**
   - Necesitarás login para agregar los registros A/AAAA

---

## 🔧 TROUBLESHOOTING

### Error: "Domain not verified"
**Solución:** Completar Paso 1 (verificación en Google Search Console)

### Error: "DNS records not found"
**Solución:**
1. Verificar que agregaste los registros A/AAAA correctos
2. Esperar propagación DNS (1-2 horas)
3. Usar `dig tikun.pro A` para verificar

### Error: "Certificate provisioning failed"
**Solución:**
1. Verificar que DNS apunta correctamente a Cloud Run IPs
2. Esperar 15-30 minutos después de propagación DNS
3. Revisar con: `gcloud beta run domain-mappings describe tikun.pro --region=us-central1`

### HTTPS no funciona
**Solución:**
1. Esperar hasta que `CertificateProvisioned: True`
2. Verificar que el dominio resuelve correctamente
3. Probar con `curl -I https://tikun.pro`

---

## 🎯 COMANDOS ÚTILES

### Check domain mapping status
```bash
gcloud beta run domain-mappings list --project=tikunframework
gcloud beta run domain-mappings describe tikun.pro --region=us-central1 --project=tikunframework
```

### Delete domain mapping (if needed)
```bash
gcloud beta run domain-mappings delete tikun.pro --region=us-central1 --project=tikunframework
```

### Check DNS resolution
```bash
nslookup tikun.pro
dig tikun.pro A
dig tikun.pro AAAA
```

### Test HTTPS
```bash
curl -I https://tikun.pro
curl -I https://tikun.pro/health
```

---

## 📝 RESUMEN DE PASOS

1. ✅ **Verificar dominio** en Google Search Console
2. ✅ **Crear domain mapping** con gcloud
3. ✅ **Agregar DNS records** (A + AAAA) en tu DNS provider
4. ⏳ **Esperar propagación** (1-2 horas)
5. ⏳ **Esperar SSL provisioning** (15-30 min después de propagación)
6. ✅ **Verificar** que https://tikun.pro funciona
7. ✅ **Update frontend** para usar nuevo dominio en producción

---

## 🔗 REFERENCIAS

- **Cloud Run Custom Domains:** https://cloud.google.com/run/docs/mapping-custom-domains
- **Google Search Console:** https://search.google.com/search-console
- **DNS Checker:** https://dnschecker.org
- **Let's Encrypt:** https://letsencrypt.org

---

**Creado:** 2025-12-30
**Status:** Pendiente - Requiere acciones manuales
**Próximo paso:** Verificar si tikun.pro está registrado y obtener acceso a DNS
