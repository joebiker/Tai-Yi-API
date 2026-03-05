import csv
import random

from fastapi import APIRouter, BackgroundTasks

from config import APHORISMS_CSV
from services.slack import queue_slack_message

router = APIRouter(prefix="/aphorism", tags=["Aphorism"])

_CSV_PATH = APHORISMS_CSV


def _load_aphorisms() -> list[dict]:
    with _CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

"""random.choice(_load_aphorisms()) if you want to check it every time, but it is faster to load it once and reuse it."""
APHORISMS: list[dict] = _load_aphorisms()


@router.get("", summary="Get a random aphorism")
async def get_random_aphorism(background_tasks: BackgroundTasks):
    """Returns a single random aphorism."""
    ap = random.choice(APHORISMS)
    payload = {k: v for k, v in ap.items() if v not in (None, "")}
    queue_slack_message(background_tasks, payload)
    return payload


@router.get("/text", summary="Get a random aphorism as plain text")
async def get_random_aphorism_text(background_tasks: BackgroundTasks):
    """Returns a single random aphorism formatted as plain text: 'quote' - Author"""
    ap = random.choice(APHORISMS)
    note = (ap.get("note") or "").strip()
    suffix = f" ({note})" if note else ""
    payload = f"'{ap['text']}' - {ap['author']}{suffix}"
    queue_slack_message(background_tasks, payload)
    return payload

