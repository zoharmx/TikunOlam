# Cómo Obtener la API Key de Anthropic (Claude)

La API key de Anthropic es **ESENCIAL** para que Tikun Olam funcione correctamente. Claude se usa para análisis avanzado en Chochmah, Tiferet, Yesod y Malchut.

## Paso a Paso (5 minutos)

### 1. Crear Cuenta en Anthropic

Ve a: **https://console.anthropic.com/**

1. Haz clic en "Sign Up" (Registrarse)
2. Usa tu email o cuenta de Google
3. Verifica tu email
4. Completa el perfil

### 2. Agregar Método de Pago

⚠️ **IMPORTANTE**: Anthropic requiere método de pago, pero:
- **NO cobra por adelantado**
- Solo pagas por uso real
- Primer mes incluye **$5 USD en créditos gratis**
- Costo promedio de un análisis Tikun completo: **~$0.50-1.00 USD**

Pasos:
1. En la consola, ve a **Settings → Billing**
2. Agrega tarjeta de crédito o débito
3. Establece límite de gasto mensual (recomendado: $10-20)

### 3. Generar API Key

1. En la consola, ve a **API Keys**
2. Haz clic en "Create Key"
3. Dale un nombre: `Tikun Olam`
4. **COPIA LA KEY INMEDIATAMENTE** (solo se muestra una vez)
5. Guárdala en lugar seguro

La key se ve así:
```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Configurar en Tikun Olam

Edita el archivo `.env`:

```bash
# Reemplaza esta línea:
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Con tu key real:
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Verificar Configuración

Ejecuta este comando:

```bash
python -c "from tikun.config import get_config; c = get_config(); print('✅ Anthropic API key configurada' if c.anthropic_api_key.startswith('sk-ant-') else '❌ Key inválida')"
```

## Costos Esperados

### Por Análisis Tikun Completo:

| Sefirah | Modelo | Tokens Aprox. | Costo Aprox. |
|---------|--------|---------------|--------------|
| Chochmah | Claude Sonnet | 4K input, 2K output | $0.12 |
| Tiferet | Claude Sonnet | 3K input, 1K output | $0.08 |
| Yesod | Claude Sonnet | 8K input, 2K output | $0.20 |
| Malchut | Claude Sonnet | 6K input, 2K output | $0.16 |
| **TOTAL** | | **~21K tokens** | **~$0.50-0.60** |

### Estimaciones:

- **Test RBU ONU**: ~$0.60
- **10 análisis**: ~$6.00
- **20 análisis/mes**: ~$12.00 (dentro de límite conservador)

## Precios de Claude (Diciembre 2025)

- **Claude 3.5 Sonnet**:
  - Input: $3 por millón de tokens
  - Output: $15 por millón de tokens

## Alternativas Temporales

Si no puedes obtener la key ahora:

### Opción 1: Usar solo Gemini (degradado)

Edita `.env`:
```bash
# Configurar todos los sefirot con Gemini
CHOCHMAH_MODEL=gemini-2.0-flash-exp
TIFERET_MODEL=gemini-2.0-flash-exp
YESOD_MODEL=gemini-2.0-flash-exp
MALCHUT_MODEL=gemini-2.0-flash-exp
```

**Desventajas**:
- Menor calidad de razonamiento en síntesis
- Yesod puede ser menos preciso
- Malchut con menos confianza

### Opción 2: Usar Mistral (si tienes API key)

Si tienes Mistral API key, puedes modificar el código para usar:
```
MISTRAL_API_KEY=tu_key_mistral
```

Pero requiere modificar `base.py` para agregar soporte.

## Problemas Comunes

### "Invalid API key"
- Verifica que copiaste la key completa
- Asegúrate de que empiece con `sk-ant-`
- No agregues espacios ni comillas extras

### "Insufficient credits"
- Agrega método de pago en console.anthropic.com
- Verifica límite de gasto mensual

### "Rate limit exceeded"
- Espera 1 minuto entre análisis
- Incrementa `API_TIMEOUT` en .env

## Seguridad

⚠️ **NUNCA COMPARTAS TU API KEY**

- No la subas a GitHub (`.env` está en `.gitignore`)
- No la pegues en Discord/Slack/foros
- No la incluyas en screenshots
- Rótala cada 3 meses

Si la expusiste accidentalmente:
1. Ve a console.anthropic.com → API Keys
2. Revoca la key comprometida
3. Genera una nueva

## Soporte

Si tienes problemas:

1. **Anthropic Support**: support@anthropic.com
2. **Documentación**: https://docs.anthropic.com/
3. **Status**: https://status.anthropic.com/

---

## ¿Listo?

Una vez configurada la key:

```bash
# Ejecuta el test RBU ONU
python test_rbu_onu_COMPATIBLE.py
```

Esto tomará **3-5 minutos** y costará aproximadamente **$0.60 USD**.

---

**Nota**: Anthropic es la empresa detrás de Claude, el AI más avanzado para razonamiento ético. Vale la pena la inversión mínima para obtener análisis de calidad profesional.
