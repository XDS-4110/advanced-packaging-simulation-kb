"""Compatibility entry point; implementation lives in tooling/rebuild_metadata.py."""
import runpy
from pathlib import Path
import sys

tooling = Path(__file__).resolve().parents[2] / "tooling"
sys.path.insert(0, str(tooling))
runpy.run_path(str(tooling / "rebuild_metadata.py"), run_name="__main__")
