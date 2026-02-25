import csv
import logging
import random

from fastapi import APIRouter, Query

from config import APHORISMS_CSV

router = APIRouter(prefix="/aphorism", tags=["Aphorism"])
logger = logging.getLogger(__name__)

_CSV_PATH = APHORISMS_CSV


def _load_aphorisms() -> list[dict]:
    with _CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

"""random.choice(_load_aphorisms()) if you want to check it every time, but it is faster to load it once and reuse it."""
APHORISMS: list[dict] = _load_aphorisms()


@router.get("", summary="Get a random aphorism")
async def get_random_aphorism():
    """Returns a single random aphorism."""
    ap = random.choice(APHORISMS)
    result = {k: v for k, v in ap.items() if v not in (None, "")}
    logger.info(
        "Served aphorism (JSON): '%s' — %s",
        ap.get("text", "")[:60],
        ap.get("author", "unknown"),
        extra={
            "endpoint": "get_random_aphorism",
            "author": ap.get("author"),
            "aphorism_preview": ap.get("text", "")[:80],
        },
    )
    return result


@router.get("/text", summary="Get a random aphorism as plain text")
async def get_random_aphorism_text():
    """Returns a single random aphorism formatted as plain text: 'quote' - Author"""
    ap = random.choice(APHORISMS)
    note = (ap.get("note") or "").strip()
    suffix = f" ({note})" if note else ""
    text = f"'{ap['text']}' - {ap['author']}{suffix}"
    logger.info(
        "Served aphorism (text): '%s' — %s",
        ap.get("text", "")[:60],
        ap.get("author", "unknown"),
        extra={
            "endpoint": "get_random_aphorism_text",
            "author": ap.get("author"),
            "aphorism_preview": ap.get("text", "")[:80],
            "has_note": bool(note),
        },
    )
    return text

