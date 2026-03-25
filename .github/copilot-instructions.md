# Copilot Instructions for Tai-Yi-API

## 1. Purpose
Small FastAPI microservice exposing:
- `/health` (status + UTC timestamp)
- `/calculator` (add/subtract/multiply/divide via JSON POST or GET path + query)
- `/aphorism` (random aphorism from `aphorisms.csv`)

This file is intended for AI helpers (Copilot Chat/agents) to onboard quickly.

## 2. Where to read runtime and dev setup
- `README.md` (primary project overview and run/test commands)
- `main.py` (FastAPI app, router registration, Uvicorn entrypoint)
- `requirements.txt` (dependencies)
- `tests/test_api.py` (canonical test expectations)

## 3. Local development commands
- `pip install -r requirements.txt`
- `python main.py` (server at `http://127.0.0.1:8000`)
- `pytest -v` to run tests

## 4. Code structure and conventions
- `routers/` hosts endpoints in three modules: `health.py`, `calculator.py`, `aphorism.py`
- `config.py` defines `APHORISMS_CSV` path
- Reuse of router `APIRouter(prefix=..., tags=[...])`
- `Pydantic` models used for request/response in calculator
- Error handling uses `fastapi.HTTPException` (e.g., divide-by-zero)
- `aphorisms.csv` is loaded once at module import time via `_load_aphorisms()`

## 5. Best-first tasks for a new PR
- Add a new route in `routers/` plus tests in `tests/test_api.py`
- Expand input validation (e.g., numeric range, operation capabilities)
- Add better CSV hot reload or error fallback in `routers/aphorism.py`
- Add benchmark or CI lint/format gates (pre-commit, black, isort)

## 6. Why this matters
- Keep the API behavior stable: preserve current response schemas
- Follow existing style: concise, explicit docstrings and FastAPI metadata

## 7. Notes
- Two flavor endpoints for calculator exist: POST and GET
- `aphorism/all` and `/aphorism` are in README; implemented on router side.
- If file currently absent, this file is authoritative for Copilot flow.
