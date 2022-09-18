"""
Adversarial Robustness Evaluation Test Bed
"""

from typing import Dict, Any
from pathlib import Path

from armory.logs import log
from armory.version import get_version

__all__ = (
    '__version__',
    'armory'
)

__version__ = Path(Path(__file__).parent / 'VERSION').read_text().strip()


# typedef for a widely used JSON-like configuration specification
Config = Dict[str, Any]

END_SENTINEL = "Scenario has finished running cleanly"
