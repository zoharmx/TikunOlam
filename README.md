# Tikun Olam
**An Ethical Reasoning Architecture for AI Decision Systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Research](https://img.shields.io/badge/status-research-orange.svg)]()

---

## The Problem

Current AI alignment approaches focus primarily on preference aggregation, reward optimization, or post-hoc ethical constraints. This works for recommendation systems and consumer tools, but breaks down when AI systems are involved in **irreversible, high-impact decisions** where:

- Value conflict is real and unavoidable
- Cultural assumptions are embedded but invisible  
- Optimization amplifies harm rather than correcting it

**The problem is not bias. The problem is the absence of a formal structure for ethical reasoning itself.**

---

## What Tikun Olam Is

Tikun Olam is an **ethical reasoning architecture**, not a moral doctrine.

It provides:
- ✅ A structured pipeline for ethical evaluation
- ✅ Explicit separation of ethical functions
- ✅ Traceability of value conflict
- ✅ Decision outputs that include ethical cost, not just utility

It is designed to operate as a layer within AI decision systems, alongside existing models.

---

## Core Innovation: BinahSigma

**Explicit Value Bias as Signal**

Instead of attempting to remove cultural or civilizational bias, Tikun Olam:
- **Models it explicitly** using separate AI models
- **Measures its influence** quantitatively
- **Exposes where and how it shapes outcomes**

Bias is treated as **information, not noise**.

This enables comparative ethical evaluation, plural alignment scenarios, and governance-level auditability.

**No other AI alignment framework does this.**

---

## Quick Example

```python
from tikun_orchestrator import TikunOrchestrator

scenario = """
PROPOSAL: Global UBI funded by 1% military spending reduction
TENSION: Sovereignty vs global equity, stability vs justice
"""

orchestrator = TikunOrchestrator()
results = orchestrator.process(scenario)

# BinahSigma output
binah = results['sefirot_results']['binah']
print(f"Bias Delta: {binah['bias_delta']}%")
print(f"West blind spots: {len(binah['sigma_synthesis']['west_blind_spots'])}")
print(f"East blind spots: {len(binah['sigma_synthesis']['east_blind_spots'])}")
```

---

## Validation Results

| Test Case | Alignment | BinahSigma Delta | Decision |
|-----------|-----------|------------------|----------|
| Desalination Infrastructure | 95% | 18% | GO |
| UBI-DAO Governance | 89% | 43% | CONDITIONAL_GO |
| Taiwan Crisis Response | 84% | 52% | CONDITIONAL_GO |
| Turritopsis Rejuvenation | 69% | 12% | NO_GO |

---

## Documentation

- [Full Architecture Details](docs/ARCHITECTURE.md)
- [BinahSigma Technical Spec](docs/BINAH_SIGMA.md)
- [Philosophical Foundations](docs/PHILOSOPHY.md)
- [API Reference](docs/API.md)

---

## Installation

```bash
git clone https://github.com/yourusername/tikun-olam.git
pip install -r requirements.txt
```

See [INSTALL.md](docs/INSTALL.md) for detailed setup.

---

## License

MIT - See [LICENSE](LICENSE)

---

**Tikun Olam** - תיקון עולם - "Repairing the world"
