# Tikun Olam - Quick Start Guide

Get started with Tikun Olam in 5 minutes.

## Prerequisites

- Python 3.8+
- API Keys (see below)

## 1. Installation

```bash
# Clone repository
git clone https://github.com/yourusername/tikun-olam.git
cd tikun-olam

# Install dependencies
pip install -r requirements.txt
```

## 2. Get API Keys

You need API keys from:

1. **Google Gemini** (Western AI): https://makersuite.google.com/app/apikey
2. **Anthropic Claude** (Advanced reasoning): https://console.anthropic.com/
3. **DeepSeek** (Eastern AI): https://platform.deepseek.com/

## 3. Configure

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```bash
GEMINI_API_KEY=your_gemini_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
```

## 4. Run Your First Analysis

### Python Script

```python
from tikun import TikunOrchestrator

# Create orchestrator
orchestrator = TikunOrchestrator(verbose=True)

# Define scenario
scenario = """
PROPOSAL: Implement universal basic healthcare in urban areas

GOAL: Provide healthcare access to 500,000 uninsured residents

STAKEHOLDERS:
- Uninsured residents (500,000)
- Healthcare providers
- Insurance companies
- City government
- Taxpayers

FUNDING: $200M/year from progressive taxation

CONCERNS:
- Cost sustainability
- Quality of care
- Provider participation
- Political opposition
"""

# Process (takes 3-5 minutes)
results = orchestrator.process(scenario, case_name="healthcare_proposal")

# View decision
print(f"\nFINAL DECISION: {results['sefirot_results']['malchut']['decision']}")
print(f"CONFIDENCE: {results['sefirot_results']['malchut']['confidence']}")

# View summary
print(orchestrator.get_summary(results))
```

### Using Docker

```bash
# Build image
docker-compose build

# Run analysis (with environment variables)
docker-compose run tikun-api python -c "
from tikun import TikunOrchestrator
orchestrator = TikunOrchestrator()
# ... your scenario here
"
```

### Using REST API

```bash
# Start API server
docker-compose up tikun-api

# Or locally:
uvicorn tikun.api.main:app --reload
```

Then make requests:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "scenario": "Your scenario text here...",
    "case_name": "test_analysis",
    "verbose": false
  }'
```

## 5. Understanding Results

Results include analysis from all 10 Sefirot:

1. **Keter**: Ethical alignment (0-100%), corruption detection
2. **Chochmah**: Wisdom, patterns, precedents
3. **Binah**: Contextual understanding, **BinahSigma** (if geopolitical)
4. **Chesed**: Opportunities, benefits
5. **Gevurah**: Risks, constraints
6. **Tiferet**: Synthesis, balance
7. **Netzach**: Strategy
8. **Hod**: Communication design
9. **Yesod**: Integration, GO/NO-GO recommendation
10. **Malchut**: FINAL DECISION

### BinahSigma

If your scenario is geopolitical, **BinahSigma** activates automatically:

- Analyzes from Western AI (Gemini) and Eastern AI (DeepSeek)
- Calculates **Bias Delta** (divergence %)
- Identifies blind spots each perspective misses
- Generates transcendent synthesis

Keywords that trigger BinahSigma:
- china, russia, usa, nato, brics, un
- military, sanctions, sovereignty
- taiwan, ukraine, israel, palestine

## 6. Export Results

Results are automatically exported to `results/` directory:

- `tikun_<case_name>_<timestamp>.json` - Full results
- `tikun_<case_name>_<timestamp>.txt` - Human-readable

## Common Scenarios

### Community Project

```python
scenario = """
PROPOSAL: Community garden in urban neighborhood
GOAL: Food security + community building
STAKEHOLDERS: 500 households, city, NGOs
BENEFITS: Fresh produce, education, green space
CONCERNS: Maintenance, equitable access
"""
```

### Business Ethics

```python
scenario = """
PROPOSAL: AI-powered hiring system
GOAL: Reduce bias, increase efficiency
STAKEHOLDERS: Job applicants, HR, executives
CONCERNS: Algorithmic bias, privacy, transparency
DATA: Historical hiring data (potentially biased)
"""
```

### Policy Decision

```python
scenario = """
PROPOSAL: Carbon tax ($50/ton)
GOAL: Reduce emissions 30% by 2030
STAKEHOLDERS: Industry, consumers, environment
BENEFITS: Climate action, revenue for renewables
CONCERNS: Economic impact, regressive effects
"""
```

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'tikun'`
**Solution**: Install package: `pip install -e .`

**Issue**: API timeout
**Solution**: Increase timeout in `.env`: `API_TIMEOUT=180`

**Issue**: BinahSigma not activating
**Solution**: Include geopolitical keywords (china, nato, military, etc.)

## Next Steps

- Read [Installation Guide](docs/INSTALL.md) for detailed setup
- Explore [API Documentation](docs/API.md)
- Understand [BinahSigma](docs/BINAH_SIGMA.md)
- Review [Philosophy](PHILOSOPHY.md)

## Example Output

```
TIKUN OLAM ANALYSIS SUMMARY
================================================================================
Case: healthcare_proposal
Duration: 187.3s

KETER - Alignment: 82%
       Corruption: low
       Threshold Met: True

BINAH - Mode: SIMPLE

YESOD - Readiness: 78%
       Quality: good
       Recommendation: CONDITIONAL_GO

MALCHUT - FINAL DECISION: CONDITIONAL_GO
         Confidence: high
         Quality: good

CONDITIONS:
1. Secure long-term funding commitment
2. Establish quality oversight mechanisms
3. Develop provider incentive program
================================================================================
```

---

**Ready to repair the world (תיקון עולם)**
