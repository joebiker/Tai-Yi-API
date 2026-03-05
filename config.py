import os
from pathlib import Path

APHORISMS_CSV = Path(__file__).parent / "aphorisms.csv"
SLACK_BUGREPORTS_URL = os.getenv("SLACK_BUGREPORTS_URL")
SLACK_CRITICAL_URL = os.getenv("SLACK_CRITICAL_URL")
