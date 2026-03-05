import os
from pathlib import Path

APHORISMS_CSV = Path(__file__).parent / "aphorisms.csv"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
