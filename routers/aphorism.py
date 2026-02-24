import csv
import random

from fastapi import APIRouter, Query

from config import APHORISMS_CSV

router = APIRouter(prefix="/aphorism", tags=["Aphorism"])

_CSV_PATH = APHORISMS_CSV


def _load_aphorisms() -> list[dict]:
    with _CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


APHORISMS: list[dict] = _load_aphorisms()


@router.get("", summary="Get a random aphorism")
async def get_random_aphorism():
    """Returns a single random aphorism."""
    """will load from the file on disk every time, which is inefficient. Instead, we load once at startup and keep in memory."""
    return random.choice(_load_aphorisms())
    """Will load from the memory list of aphorisms, which is more efficient than reading from disk on every request."""
    """return random.choice(APHORISMS)"""


@router.get("/text", summary="Get a random aphorism as plain text")
async def get_random_aphorism_text():
    """Returns a single random aphorism formatted as plain text: 'quote' - Author"""
    ap = random.choice(APHORISMS)
    note = (ap.get("note") or "").strip()
    suffix = f" ({note})" if note else ""
    return f"'{ap['text']}' - {ap['author']}{suffix}"

