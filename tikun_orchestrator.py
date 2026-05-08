"""
Compatibility wrapper — adds src/ to sys.path so `tikun` resolves
to src/tikun without requiring `pip install -e .`.
"""

import sys
from pathlib import Path

_SRC = str(Path(__file__).parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from tikun.orchestrator import TikunOrchestrator  # noqa: E402
from tikun.config import TikunConfig              # noqa: E402

__all__ = ['TikunOrchestrator', 'TikunConfig']
