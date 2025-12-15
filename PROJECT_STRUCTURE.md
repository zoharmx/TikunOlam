# Estructura Completa del Proyecto TikunOlam

```
TikunOlam/
│
├── 📱 FRONTEND (React + TypeScript)                    ← NUEVO ✨
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx                    # Barra superior con logo
│   │   │   ├── AnalysisForm.tsx              # Formulario de entrada
│   │   │   ├── LoadingState.tsx              # Animación de carga (10 Sefirot)
│   │   │   ├── Results.tsx                   # Vista principal de resultados
│   │   │   ├── BinahSigmaView.tsx            # Dashboard BinahSigma
│   │   │   └── SefirahCard.tsx               # Card individual por Sefirah
│   │   ├── services/
│   │   │   └── api.ts                        # Cliente API (Axios)
│   │   ├── types/
│   │   │   └── index.ts                      # TypeScript interfaces
│   │   ├── App.tsx                           # Componente raíz
│   │   ├── main.tsx                          # Entry point
│   │   └── index.css                         # Estilos globales
│   ├── index.html                            # HTML template
│   ├── vite.config.ts                        # Configuración Vite
│   ├── tsconfig.json                         # TypeScript config
│   ├── package.json                          # Dependencias npm
│   ├── Dockerfile                            # Multi-stage build
│   ├── nginx.conf                            # Nginx config
│   ├── .gitignore
│   ├── .dockerignore
│   └── README.md                             # Docs del frontend
│
├── 🐍 BACKEND (Python FastAPI)
│   ├── src/tikun/
│   │   ├── sefirot/                          # 10 Sefirot
│   │   │   ├── base.py                       # Clase base
│   │   │   ├── keter.py                      # Validación ética
│   │   │   ├── chochmah.py                   # Sabiduría
│   │   │   ├── binah.py                      # BinahSigma ⭐
│   │   │   ├── chesed.py                     # Oportunidades
│   │   │   ├── gevurah.py                    # Riesgos
│   │   │   ├── tiferet.py                    # Síntesis
│   │   │   ├── netzach.py                    # Estrategia
│   │   │   ├── hod.py                        # Comunicación
│   │   │   ├── yesod.py                      # Integración
│   │   │   ├── malchut.py                    # Decisión final
│   │   │   └── __init__.py
│   │   ├── api/
│   │   │   ├── main.py                       # FastAPI app
│   │   │   ├── routes.py                     # Endpoints
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── schemas.py                    # Pydantic models
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── logging.py                    # Structured logging
│   │   │   ├── validation.py                 # Validaciones
│   │   │   ├── export.py                     # Export JSON/TXT
│   │   │   └── __init__.py
│   │   ├── orchestrator.py                   # Pipeline principal
│   │   ├── config.py                         # Configuración
│   │   └── __init__.py
│   ├── tests/                                # Suite de tests
│   │   ├── test_keter.py
│   │   ├── test_binah.py
│   │   └── ...
│   ├── requirements.txt                      # Dependencias Python
│   ├── setup.py                              # Instalación del paquete
│   └── Dockerfile                            # Backend container
│
├── 🐳 DOCKER & DEPLOYMENT
│   ├── docker-compose.yml                    # Full stack (frontend + backend + monitoring)
│   ├── .dockerignore
│   └── monitoring/
│       ├── prometheus.yml
│       └── grafana/
│
├── 📊 RESULTS & LOGS
│   ├── results/                              # JSON/TXT exports
│   │   └── tikun_RBU_ONU_*.json
│   └── logs/                                 # Application logs
│
├── 📚 DOCUMENTATION
│   ├── README.md                             # Main README
│   ├── QUICKSTART.md                         # Quick start guide
│   ├── README_USAGE.md                       # Usage manual
│   ├── PHILOSOPHY.md                         # Philosophy document
│   ├── INVESTOR_PITCH.md                     # Business pitch
│   ├── SISTEMA_LISTO.md                      # System ready (Spanish)
│   ├── ANTHROPIC_ALTERNATIVES.md             # Claude alternatives
│   ├── GET_ANTHROPIC_KEY.md                  # Anthropic setup
│   ├── FRONTEND_SETUP.md                     # Frontend setup ← NUEVO
│   ├── FRONTEND_COMPLETADO.md                # Frontend done ← NUEVO
│   └── PROJECT_STRUCTURE.md                  # Este archivo ← NUEVO
│
├── 🚀 SCRIPTS
│   ├── start.sh                              # Start all (Bash) ← NUEVO
│   ├── start.ps1                             # Start all (PowerShell) ← NUEVO
│   └── test_rbu_onu_COMPATIBLE.py            # Test script
│
├── ⚙️ CONFIGURATION
│   ├── .env                                  # Environment variables
│   ├── .env.no-claude                        # Gemini-only config
│   ├── .gitignore
│   └── pyproject.toml                        # Python project config
│
└── 📄 PROJECT FILES
    ├── LICENSE
    └── VERSION
```

---

## 🎯 Navegación Rápida

### Para Desarrolladores

**Frontend:**
```
cd frontend/
npm install
npm run dev
```

**Backend:**
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
uvicorn tikun.api.main:app --reload
```

**Full Stack:**
```
docker-compose up --build
```

### Para Usuarios

**Usar el sistema:**
1. Abrir http://localhost:3000
2. Ingresar escenario
3. Analizar
4. Ver resultados

**Leer documentación:**
1. `QUICKSTART.md` - Inicio rápido
2. `FRONTEND_SETUP.md` - Frontend setup
3. `README_USAGE.md` - Manual completo

---

## 📊 Estadísticas del Proyecto

### Backend
- **Sefirot**: 10 clases implementadas
- **API Endpoints**: 8+ endpoints
- **Tests**: Suite completa
- **Líneas de código**: ~5,000+

### Frontend
- **Componentes**: 7 componentes React
- **TypeScript Interfaces**: 15+
- **Líneas de código**: ~2,000+
- **Bundle size**: ~150KB (gzipped)

### Total
- **Archivos Python**: 40+
- **Archivos TypeScript/JavaScript**: 15+
- **Archivos de configuración**: 20+
- **Documentación**: 15+ archivos

---

## 🌟 Características Principales

### Backend (Python)
✅ 10 Sefirot (Kabbalistic reasoning)
✅ BinahSigma (multi-civilizational analysis)
✅ FastAPI REST API
✅ Pydantic validation
✅ Structured logging
✅ Docker containerization
✅ Export to JSON/TXT
✅ Comprehensive tests

### Frontend (React)
✅ Modern UI with dark theme
✅ BinahSigma dashboard
✅ 10 Sefirot visualization
✅ Real-time analysis
✅ Loading animations
✅ Responsive design
✅ TypeScript type safety
✅ Docker + Nginx

### DevOps
✅ Docker Compose
✅ Multi-stage builds
✅ Health checks
✅ Prometheus monitoring
✅ Grafana dashboards
✅ CI/CD ready

---

## 🔥 Archivos Clave

### Must-Read
1. `QUICKSTART.md` - Inicio rápido
2. `FRONTEND_SETUP.md` - Setup del frontend
3. `README_USAGE.md` - Manual de uso completo

### For Developers
1. `src/tikun/orchestrator.py` - Pipeline principal
2. `src/tikun/sefirot/binah.py` - BinahSigma implementation
3. `frontend/src/App.tsx` - Frontend principal
4. `frontend/src/components/BinahSigmaView.tsx` - BinahSigma UI

### Configuration
1. `.env` - Environment variables
2. `docker-compose.yml` - Full stack config
3. `frontend/vite.config.ts` - Vite config
4. `frontend/nginx.conf` - Nginx config

---

## 💡 Casos de Uso

### 1. Análisis Ético
```
Input: Escenario ético
↓
Backend: 10 Sefirot pipeline
↓
Frontend: Visualización de resultados
```

### 2. BinahSigma
```
Input: Escenario geopolítico
↓
Binah: Gemini (West) vs DeepSeek (East)
↓
Frontend: Comparación civilizacional
```

### 3. Exportación
```
Análisis completo
↓
Backend: Export to JSON/TXT
↓
results/ directory
```

---

## 🎓 Tecnologías Utilizadas

### Backend
- Python 3.8+
- FastAPI
- Pydantic
- Anthropic (Claude)
- Google Gemini
- DeepSeek
- OpenAI
- Tenacity (retry logic)
- Structlog (logging)

### Frontend
- React 18
- TypeScript 5
- Vite 5
- Axios
- CSS Variables
- Nginx (production)

### DevOps
- Docker
- Docker Compose
- Prometheus
- Grafana
- GitHub Actions (CI/CD ready)

---

## 📈 Roadmap

### Completado ✅
- [x] Backend con 10 Sefirot
- [x] BinahSigma implementation
- [x] FastAPI REST API
- [x] Frontend React
- [x] BinahSigma dashboard
- [x] Docker containers
- [x] Documentación completa

### Próximos Pasos 🚀
- [ ] Tests E2E (Playwright)
- [ ] PWA support
- [ ] Export to PDF
- [ ] History de análisis
- [ ] User authentication
- [ ] Multi-language

---

**תיקון עולם - Reparando el mundo, un commit a la vez** 🌍✨
