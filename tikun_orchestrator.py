"""
Compatibility wrapper for backward compatibility.

This module exists to maintain compatibility with existing code
that imports from tikun_orchestrator.

Prefer importing from tikun package directly:
    from tikun import TikunOrchestrator
"""

# Import from main package
from src.tikun.orchestrator import TikunOrchestrator
from src.tikun.config import TikunConfig

__all__ = ['TikunOrchestrator', 'TikunConfig']
