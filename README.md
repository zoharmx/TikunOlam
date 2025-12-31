<p align="center">
  <img src="docs/images/tikun-banner.png" alt="Tikun Olam - Observable Ethical AI" width="800"/>
</p>

<p align="center">
  <strong>The first AI system that makes ethical reasoning visible, auditable, and monitorable in production.</strong>
</p>

<p align="center">
  <a href="https://tikun.pro">🌐 Live Demo</a> •
  <a href="https://youtu.be/E6s9vGI7hLw">📹 Video Demo</a> •
  <a href="https://github.com/zoharmx/TikunOlam">📦 GitHub</a> •
  <a href="results/">📊 Real Results</a>
</p>

<p align="center">
  <a href="https://cloud.google.com/vertex-ai"><img src="https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-4285F4?logo=google-cloud" alt="Google Cloud"/></a>
  <a href="https://www.datadoghq.com/"><img src="https://img.shields.io/badge/Datadog-Observability-632CA6?logo=datadog" alt="Datadog"/></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python" alt="Python"/></a>
  <a href="https://react.dev"><img src="https://img.shields.io/badge/React-18+-61DAFB?logo=react" alt="React"/></a>
  <a href="results/nvidia_groq_20b_ma/"><img src="https://img.shields.io/badge/Results-Verified-success" alt="Real Results"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"/></a>
</p>

---

## 🎯 The Problem

Current AI systems make life-changing decisions as **black boxes**:
- No visibility into ethical reasoning
- Hidden civilizational biases
- No monitoring for alignment violations
- Impossible to audit or debug moral failures

## ✨ The Solution

**Tikun Olam** provides the first **observable ethical AI pipeline** with:

- **10-Stage Sefirot Pipeline** - Explicit ethical reasoning stages (not a black box)
- **BinahSigma Engine** - Detects civilizational bias by comparing Western vs Eastern AI perspectives
- **Full Datadog Observability** - Real-time monitoring of ethical alignment, bias deltas, and decision quality
- **Production-Ready** - Deployed on Google Cloud Run with 8.8 min analysis time

## 📊 Key Results: Nvidia-Groq $20B Acquisition Analysis

Real production analysis from December 26, 2025:

| Metric | Value |
|--------|-------|
| **BinahSigma Bias Delta** | **73%** (HIGH civilizational divergence) |
| **Ethical Alignment** | 15% (complex ethical tensions) |
| **Final Decision** | CONDITIONAL_GO |
| **Blind Spots Detected** | 14 (Western + Eastern) |
| **Analysis Duration** | 8.8 minutes |

**Key Finding:** Western AI recommended blocking the deal (antitrust concerns), Eastern AI recommended conditional approval (collective stability). BinahSigma synthesized a novel "Strategic Technology Trust" solution neither perspective envisioned.

👉 **[View Full Analysis Results](results/nvidia_groq_20b_ma/)**

## 🏗️ Architecture

```
User Input → FastAPI Backend → 10 Sefirot Pipeline → Final Decision
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
            Vertex AI (Gemini)  DeepSeek (East)  Datadog (Observe)
```

**10 Sefirot Stages:**
1. **Keter** - Ethical Alignment Validation
2. **Chochmah** - Historical Wisdom & Precedents
3. **Binah** - Understanding + **BinahSigma** (bias detection)
4. **Chesed** - Opportunity Identification
5. **Gevurah** - Risk Assessment
6. **Tiferet** - Balanced Synthesis
7. **Netzach** - Strategic Planning
8. **Hod** - Stakeholder Communication
9. **Yesod** - Integration & Coherence
10. **Malchut** - Final Decision & Action

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/zoharmx/TikunOlam.git
cd TikunOlam

# 2. Configure environment
cp .env.example .env
# Add your API keys: GEMINI_API_KEY, DEEPSEEK_API_KEY, DATADOG_API_KEY

# 3. Install dependencies
pip install -r requirements.txt
cd frontend && npm install

# 4. Run locally
uvicorn src.tikun.api.main:app --reload --port 8000
cd frontend && npm run dev
```

Open http://localhost:5173

## 💻 Quick Demo

Try the Nvidia-Groq analysis yourself:

```python
from tikun.orchestrator import TikunOrchestrator

scenario = """
Nvidia announced a $20B deal to acquire Groq's technology and team.
Should the FTC approve, block, or conditionally approve this deal?
"""

result = await TikunOrchestrator().process(
    scenario=scenario,
    case_name="nvidia_groq_test"
)

print(f"BinahSigma Delta: {result['binah']['bias_delta']}%")
print(f"Decision: {result['malchut']['decision']}")
```

## 📚 Documentation

- **[Full Documentation](docs/FULL_DOCUMENTATION.md)** - Complete technical guide
- **[BinahSigma Explained](docs/BINAHSIGMA.md)** - How civilizational bias detection works
- **[API Reference](docs/API.md)** - API endpoints and examples
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Cloud Run deployment
- **[Datadog Setup](DATADOG_SETUP_GUIDE.md)** - Observability configuration

## 🏆 Hackathon: Google Cloud AI + Datadog Challenge

Built for the 2025 Google Cloud AI Partner Catalyst - Datadog Challenge

✅ **Google Vertex AI** - 7 Sefirot powered by Gemini 2.5 Pro
✅ **Datadog Observability** - Custom metrics, APM, dashboards
✅ **Production Deployed** - Google Cloud Run (tikun.pro)
✅ **Unique Innovation** - BinahSigma civilizational bias detection
✅ **Real Results** - Verified production analysis of Nvidia-Groq deal

## 🌟 What Makes This Unique?

| Feature | Tikun Olam | Typical AI |
|---------|------------|------------|
| **Ethical Reasoning** | ✅ 10 explicit stages | ❌ Black box |
| **Bias Detection** | ✅ BinahSigma (West vs East) | ❌ Single model |
| **Observability** | ✅ Full Datadog instrumentation | ❌ Basic logs |
| **Auditability** | ✅ Complete reasoning trail | ❌ Opaque |
| **Custom Metrics** | ✅ bias_delta, alignment_score | ❌ Generic |

## 📜 License

MIT - See [LICENSE](LICENSE)

---

<p align="center">
  <strong>Tikun Olam (תיקון עולם)</strong> - "Repairing the world, one decision at a time"
</p>

<p align="center">
  Built for Google Cloud AI Partner Catalyst - Datadog Challenge 2025<br/>
  Powered by Google Vertex AI & Datadog
</p>
