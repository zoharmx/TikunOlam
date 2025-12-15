"""
Tikun Olam - An Ethical Reasoning Architecture for AI Decision Systems

תיקון עולם - "Repairing the world"

This package provides a structured, multi-stage ethical reasoning pipeline
for AI decision systems, with explicit value bias detection and traceability.
"""

__version__ = "1.0.0"
__author__ = "Tikun Olam Contributors"
__license__ = "MIT"

from tikun.orchestrator import TikunOrchestrator
from tikun.config import TikunConfig

__all__ = [
    "TikunOrchestrator",
    "TikunConfig",
    "__version__",
]
