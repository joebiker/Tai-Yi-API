import logging
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from logging_config import setup_logging
from routers import health, calculator, aphorism

# ── Logging ───────────────────────────────────────────────────────────────────
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI Example",
    description="A FastAPI service providing health checks, calculator operations, and aphorisms.",
    version="1.0.0",
    contact={
        "name": "Joe",
    },
    license_info={
        "name": "Just for fun.",
    },
    note={
        "name": "This is fun, but not displayed anywhere.",
    },
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(calculator.router)
app.include_router(aphorism.router)


# ── Request logging middleware ────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every inbound request with caller IP, method, path and response time."""
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)

    # X-Forwarded-For is set by Cloud Run / load-balancers; fall back to direct client.
    client_ip = (
        request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        or (request.client.host if request.client else "unknown")
    )

    logger.info(
        "%s %s %s",
        request.method,
        request.url.path,
        response.status_code,
        extra={
            "http_method": request.method,
            "path": request.url.path,
            "query": str(request.query_params) or None,
            "status_code": response.status_code,
            "client_ip": client_ip,
            "user_agent": request.headers.get("user-agent"),
            "duration_ms": duration_ms,
        },
    )
    return response


# ── Root redirect ─────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to the aphorism endpoint."""
    return RedirectResponse(url="/aphorism")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, log_level="info")
