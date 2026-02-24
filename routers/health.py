from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Health check")
async def health_check():
    """Returns the current health status of the API."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
