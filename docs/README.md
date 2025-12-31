# Tikun Olam Documentation

Complete documentation for the Observable Ethical AI Framework.

## 📚 Documentation Index

### Getting Started
- **[Quick Start Guide](../QUICK_START.md)** - Installation and first steps
- **[API Reference](API.md)** - Complete API documentation
- **[Deployment Guide](../DEPLOYMENT_GUIDE.md)** - Production deployment to Cloud Run

### Core Concepts
- **[BinahSigma Explained](BINAHSIGMA.md)** - Civilizational bias detection deep dive
- **[Full Documentation](FULL_DOCUMENTATION.md)** - Complete technical reference
- **[10 Sefirot Pipeline](SEFIROT.md)** - Understanding each ethical stage

### Integration & Observability
- **[Datadog Setup](../DATADOG_SETUP_GUIDE.md)** - Observability configuration
- **[Vertex AI Setup](../VERTEX_AI_SETUP.md)** - Google Cloud configuration
- **[Custom Metrics](METRICS.md)** - All emitted metrics and their meanings

### Results & Examples
- **[Nvidia-Groq Analysis](../results/nvidia_groq_20b_ma/)** - Real production case study
- **[Example Scripts](../results/run_analysis_example.py)** - Reproducible code examples

## 🎯 Key Features

### 1. Observable Ethics
Tikun Olam is the first AI system with **full observability** into ethical reasoning:

- **10 Explicit Stages** - Each decision goes through transparent reasoning steps
- **Real-Time Monitoring** - Datadog dashboards show alignment scores live
- **Audit Trail** - Complete trace of how every decision was made

### 2. BinahSigma Engine
**Civilizational bias detection** comparing Western vs Eastern AI perspectives:

```
Same scenario → Western AI (Gemini) + Eastern AI (DeepSeek)
                       ↓
            BinahSigma Analysis Engine
                       ↓
    Western Blind Spots | Eastern Blind Spots | Universal Values
                       ↓
            Transcendent Synthesis
```

**Unique Metrics:**
- `bias_delta`: 0-100% civilizational divergence
- `west_blind_spots`: What Western AI systematically misses
- `east_blind_spots`: What Eastern AI systematically misses
- `transcendent_synthesis`: Novel solution neither perspective saw alone

### 3. Production-Ready Infrastructure
- **Google Cloud Run** - Serverless, auto-scaling deployment
- **Vertex AI** - Enterprise-grade AI models (Gemini 2.5 Pro)
- **Datadog APM** - Distributed tracing across all 10 Sefirot
- **Custom Metrics** - 25+ specialized ethical observability metrics

## 🔍 Use Cases

### Regulatory Compliance
**Problem:** Company needs to ensure AI decisions comply with ethical guidelines
**Solution:** Monitor `keter.alignment_score` in real-time, alert when < 60%

### Policy Analysis
**Problem:** Government evaluating universal basic income policy
**Solution:** BinahSigma reveals blind spots from both capitalist and collectivist frameworks

### M&A Due Diligence
**Problem:** Board deciding on $20B acquisition (Nvidia-Groq case)
**Solution:** 10-Sefirot analysis identifies risks, opportunities, and novel solutions like Strategic Technology Trust

### Crisis Management
**Problem:** Geopolitical crisis requires ethical decision under time pressure
**Solution:** 8.8-minute full analysis with complete audit trail

## 📊 Performance Metrics

From real production deployment:

| Metric | Value |
|--------|-------|
| **Average Analysis Time** | 8.8 minutes |
| **Pipeline Success Rate** | 100% (10/10 Sefirot) |
| **BinahSigma Accuracy** | 73% divergence detected on Nvidia-Groq |
| **Datadog Instrumentation** | Full APM + 25+ custom metrics |
| **Production Uptime** | 99.9% (Google Cloud Run) |

## 🏗️ Architecture Deep Dive

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React 18)                        │
│  Landing Page | Dashboard | Results Viewer | Observability UI  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
┌────────────────────────────┴────────────────────────────────────┐
│                    BACKEND (FastAPI / Python 3.11)              │
│                                                                 │
│  ┌───────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  API Endpoint │→ │ Orchestrator │→ │  10 Sefirot Pipeline│ │
│  └───────────────┘  └──────────────┘  └────────────────────┘  │
│                                              │                  │
│                         ┌────────────────────┼────┐            │
│                         ▼                    ▼    ▼            │
│                    ┌────────┐          ┌────────────┐          │
│                    │ Vertex │          │ DeepSeek   │          │
│                    │   AI   │          │    API     │          │
│                    │(Gemini)│          │ (Eastern)  │          │
│                    └────────┘          └────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                  OBSERVABILITY (Datadog)                        │
│                                                                 │
│  APM Traces | Custom Metrics | Dashboards | Alerts             │
│  • keter.alignment_score                                        │
│  • binah.bias_delta (KEY METRIC)                               │
│  • malchut.decision_confidence                                  │
│  • pipeline.duration                                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Links

- **Live Demo:** [tikun.pro](https://tikun.pro)
- **Video Demo:** [YouTube](https://youtu.be/E6s9vGI7hLw)
- **GitHub:** [zoharmx/TikunOlam](https://github.com/zoharmx/TikunOlam)
- **Real Results:** [Nvidia-Groq Analysis](../results/nvidia_groq_20b_ma/)

## 📞 Support

For questions or issues:
- **GitHub Issues:** [Report a bug](https://github.com/zoharmx/TikunOlam/issues)
- **Documentation:** You're reading it!
- **Video Guide:** [YouTube Demo](https://youtu.be/E6s9vGI7hLw)

---

**Tikun Olam (תיקון עולם)** - "Repairing the world, one decision at a time"
