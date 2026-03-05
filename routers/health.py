import logging
from fastapi import APIRouter
from datetime import datetime, timezone

from config import APHORISMS_CSV

router = APIRouter(prefix="/health", tags=["Health"])
logger = logging.getLogger(__name__)


@router.get("", summary="Health check")
async def health_check():
    """Returns the current health status of the API."""
    csv_ok = APHORISMS_CSV.exists()
    status = "ok" if csv_ok else "CSV not found"
    ts = datetime.now(timezone.utc).isoformat()

    logger.info(
        "Health check: %s",
        status,
        extra={
            "endpoint": "health_check",
            "csv_present": csv_ok,
            "server_time": ts,
        },
    )
    return {"status": status, "timestamp": ts}
