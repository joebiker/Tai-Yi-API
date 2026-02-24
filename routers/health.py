from fastapi import APIRouter
from datetime import datetime, timezone

from config import APHORISMS_CSV

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Health check")
async def health_check():
    """Returns the current health status of the API."""
    return {
        "status": "ok" if APHORISMS_CSV.exists() else "CSV not found",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
