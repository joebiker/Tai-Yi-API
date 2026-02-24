# Root conftest.py — ensures the project root is on sys.path so tests can
# import `main` and `routers` directly.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
