"""
Integration tests for the Tai-Yi API.
Run with:  pytest tests/
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ── Aphorism CSV loading (expanded from last manual test) ─────────────────────

def test_aphorisms_csv_loads():
    """The CSV file must be readable and contain at least one entry."""
    from routers.aphorism import _load_aphorisms
    aphorisms = _load_aphorisms()
    assert len(aphorisms) > 0, "CSV returned no aphorisms"


def test_aphorisms_have_required_keys():
    """Every row must have at least 'text' and 'author' columns."""
    from routers.aphorism import _load_aphorisms
    for ap in _load_aphorisms():
        assert "text" in ap, f"Missing 'text' key in row: {ap}"
        assert "author" in ap, f"Missing 'author' key in row: {ap}"


def test_aphorisms_no_empty_text_or_author():
    """No row should have a blank text or author."""
    from routers.aphorism import _load_aphorisms
    for ap in _load_aphorisms():
        assert ap["text"].strip(), f"Empty 'text' in row: {ap}"
        assert ap["author"].strip(), f"Empty 'author' in row: {ap}"


# ── Health ────────────────────────────────────────────────────────────────────

def test_health_status_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_has_timestamp():
    response = client.get("/health")
    data = response.json()
    assert "timestamp" in data
    assert data["timestamp"]  # non-empty string


# ── Calculator POST ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("a, b, operation, expected", [
    (5,   3,   "add",      8.0),
    (10,  4,   "subtract", 6.0),
    (3,   7,   "multiply", 21.0),
    (10,  4,   "divide",   2.5),
    (-5,  3,   "add",     -2.0),
    (0,   99,  "multiply", 0.0),
])
def test_calculator_post(a, b, operation, expected):
    response = client.post("/calculator", json={"a": a, "b": b, "operation": operation})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == pytest.approx(expected)
    assert data["operation"] == operation


def test_calculator_post_divide_by_zero():
    response = client.post("/calculator", json={"a": 5, "b": 0, "operation": "divide"})
    assert response.status_code == 400
    assert "zero" in response.json()["detail"].lower()


def test_calculator_post_invalid_operation():
    response = client.post("/calculator", json={"a": 5, "b": 3, "operation": "modulo"})
    assert response.status_code == 422  # Pydantic validation error


# ── Calculator GET ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("operation, a, b, expected", [
    ("add",      5, 3, 8.0),
    ("subtract", 5, 3, 2.0),
    ("multiply", 5, 3, 15.0),
    ("divide",   9, 3, 3.0),
])
def test_calculator_get(operation, a, b, expected):
    response = client.get(f"/calculator/{operation}?a={a}&b={b}")
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(expected)


def test_calculator_get_divide_by_zero():
    response = client.get("/calculator/divide?a=5&b=0")
    assert response.status_code == 400


# ── Aphorism endpoints ────────────────────────────────────────────────────────

def test_aphorism_random_returns_text_and_author():
    response = client.get("/aphorism")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "author" in data
    assert data["text"]
    assert data["author"]


def test_aphorism_text_returns_string():
    response = client.get("/aphorism/text")
    assert response.status_code == 200
    text = response.json()
    assert isinstance(text, str)
    assert " - " in text  # format: 'quote' - Author


def test_aphorism_text_note_omitted_when_empty():
    """If the selected aphorism has no note, the response must not contain '()'."""
    # Run several times to increase the chance of hitting a note-less row
    for _ in range(20):
        response = client.get("/aphorism/text")
        assert "()" not in response.json(), "Empty parentheses found in text response"
