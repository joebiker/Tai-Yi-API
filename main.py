import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import health, calculator, aphorism

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


# ── Root redirect ─────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to the interactive API docs."""
    return RedirectResponse(url="/docs")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, log_level="info")
