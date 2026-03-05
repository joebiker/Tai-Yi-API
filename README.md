# Tai-Yi API

A FastAPI service running on Uvicorn, providing health checks, calculator operations, and aphorisms.

This branch is dedicated to logging into [Slack](https://slack.com)

## Requirements

- Python 3.11+
- [pip](https://pip.pypa.io/)

## Setup

**1. Clone the repository and navigate to the project folder:**

```bash
cd Tai-Yi-Api
```

**2. (Optional) Create and activate a virtual environment:**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. (Optional) Enable Slack logging for aphorism endpoints:**

Set an incoming webhook URL before starting the server.

PowerShell:

```powershell
$env:SLACK_BUGREPORTS_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

**5. Start the server:**

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`.

---

## Interactive Docs

FastAPI generates documentation automatically:

| Interface | URL |
|-----------|-----|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## Endpoints

### Health

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Returns API status and current UTC timestamp |

**Example response:**
```json
{
  "status": "ok",
  "timestamp": "2026-02-23T10:00:00.000000+00:00"
}
```

---

### Calculator

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/calculator` | Perform a calculation via JSON body |
| `GET` | `/calculator/{operation}?a=&b=` | Perform a calculation via URL parameters |

**Supported operations:** `add`, `subtract`, `multiply`, `divide`

**POST request body:**
```json
{
  "a": 10,
  "b": 3,
  "operation": "add"
}
```

**Example response:**
```json
{
  "a": 10,
  "b": 3,
  "operation": "add",
  "result": 13
}
```

**GET example:**
```
GET /calculator/divide?a=10&b=4
```

> Note: Division by zero returns a `400 Bad Request` error.

---

### Aphorism

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/aphorism` | Returns a single random aphorism |
| `GET` | `/aphorism/all` | Returns a shuffled list of aphorisms |

**Query parameters for `/aphorism/all`:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | `10` | Number of aphorisms to return (1 – 20) |

**Example response (`/aphorism`):**
```json
{
  "text": "The journey of a thousand miles begins with a single step.",
  "author": "Lao Tzu"
}
```

**Example response (`/aphorism/all?limit=2`):**
```json
{
  "count": 2,
  "aphorisms": [
    {
      "text": "In the middle of every difficulty lies opportunity.",
      "author": "Albert Einstein"
    },
    {
      "text": "The unexamined life is not worth living.",
      "author": "Socrates"
    }
  ]
}
```

---

## Project Structure

```
Tai-Yi-Api/
├── main.py              # App entry point and router registration
├── requirements.txt     # Python dependencies
├── pytest.ini           # Pytest configuration
├── conftest.py          # Pytest path setup
├── aphorisms.csv        # Aphorism data source
├── routers/
│   ├── __init__.py
│   ├── health.py        # /health endpoint
│   ├── calculator.py    # /calculator endpoints
│   └── aphorism.py      # /aphorism endpoints
└── tests/
    └── test_api.py      # Integration tests
```

## Dependencies

| Package | Purpose |
|---------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [Uvicorn](https://uvicorn.dev/) | ASGI server |
| [Pydantic](https://docs.pydantic.dev/) | Data validation || [pytest](https://docs.pytest.org/) | Test framework |
| [httpx](https://www.python-httpx.org/) | Async HTTP client (required by FastAPI TestClient) |

---

## Tests

The test suite lives in `tests/test_api.py` and uses FastAPI's built-in `TestClient` (backed by `httpx`) — no running server is required.

**Run all tests:**

```bash
pytest -v
```

**Run a specific test:**

```bash
pytest -v tests/test_api.py::test_health_status_ok
```

### Test coverage

| Group | What is tested |
|-------|----------------|
| CSV loading | File is readable, all rows have `text` and `author`, no blank values |
| Health | Returns `200`, `status` is `"ok"`, `timestamp` is present |
| Calculator POST | `add`, `subtract`, `multiply`, `divide`, negative numbers, zero operand, divide-by-zero `400`, invalid operation `422` |
| Calculator GET | All four operations via URL params, divide-by-zero `400` |
| Aphorism | JSON contains `text` and `author`, `/text` returns a formatted string, empty `note` never produces `()` |

---

## Deploying Local with uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
uvicorn main:app --host 127.0.0.1 --port 8080 --workers 2
```

## Deploying with Docker

```bash
docker build -t tai-yi-api .
docker run -p 8080:8080 tai-yi-api

## or specify port
docker run -p 3000:3000 -e PORT=3000 tai-yi-api
```

## Deploying to Google Cloud (Cloud Run)

The recommended hosting target is **Cloud Run** — fully managed, scales to zero, and supports the FastAPI/uvicorn stack via Docker.

### Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and on your PATH
- A GCP project with billing enabled
- Cloud Run, Cloud Build, and Artifact Registry APIs enabled (the CLI will prompt you if any are off)

### Deploy

```powershell
# One-time: authenticate and set your project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build, push, and deploy in one command
gcloud run deploy tai-yi-api `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --platform managed
```

### Configure environment variables (Cloud Run)

Your app reads the webhook with `os.getenv("SLACK_BUGREPORTS_URL")`, so set that variable on the Cloud Run service.

**Option A: Plain environment variable**

```powershell
gcloud run services update tai-yi-api `
  --region us-south1 `
  --set-env-vars SLACK_BUGREPORTS_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

**Option B (recommended): Google Secret Manager**

```powershell
# Create the secret once
gcloud secrets create slack-webhook-url --replication-policy=automatic

# Add/update the secret value
echo "https://hooks.slack.com/services/XXX/YYY/ZZZ" | gcloud secrets versions add slack-webhook-url --data-file=-

# Grant Cloud Run service account access (replace PROJECT_NUMBER)
gcloud secrets add-iam-policy-binding slack-webhook-url `
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" `
  --role="roles/secretmanager.secretAccessor"

# Map secret to env var name used by the app
gcloud run services update tai-yi-api `
  --region us-south1 `
  --set-secrets SLACK_WEBHOOK_URL=slack-webhook-url:latest
```

After updating env vars or secrets, Cloud Run creates a new revision automatically.

`--source .` uploads your code and triggers a **Cloud Build** automatically — no manual `docker build` or `docker push` required.

Deployment:Deployment failed
ERROR: (gcloud.run.services.update) The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable within the allocated timeout. This can happen when the container port is misconfigured or if the timeout is too short. The health check timeout can be extended. Logs for this revision might contain more information.

https://tai-yi-api-676122701159.us-south1.run.app/docs

### What happens behind the scenes

| Step | What GCP does |
|------|---------------|
| `--source .` | Uploads your code, builds the Docker image via Cloud Build |
| Image stored | Pushed to Artifact Registry automatically |
| Deployed | Container runs on Cloud Run; a public HTTPS URL is returned |

After deployment the `/docs` Swagger UI will be accessible at the returned URL.
