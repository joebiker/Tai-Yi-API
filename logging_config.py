"""
Structured JSON logging for Cloud Run / Cloud Logging.

Cloud Run automatically ingests stdout/stderr into Cloud Logging.
When logs are valid JSON, Cloud Logging parses them as structured log entries,
enabling filtering and querying on individual fields.

Usage:
    from logging_config import setup_logging
    setup_logging()

    import logging
    logger = logging.getLogger(__name__)
    logger.info("hello", extra={"http_method": "GET"})
"""

import json
import logging
import sys
from datetime import datetime, timezone


# Map Python log level names to Cloud Logging severity strings.
_SEVERITY_MAP = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL",
}


class _CloudJsonFormatter(logging.Formatter):
    """Emit each log record as a single-line JSON object understood by Cloud Logging."""

    def format(self, record: logging.LogRecord) -> str:
        # Build the base structured payload.
        payload: dict = {
            # 'severity' is the field Cloud Logging looks for.
            "severity": _SEVERITY_MAP.get(record.levelname, record.levelname),
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
        }

        # Attach any extra fields the caller passed via the `extra` keyword.
        skip = logging.LogRecord.__dict__.keys() | {
            "message", "asctime", "exc_info", "exc_text", "stack_info",
        }
        for key, value in record.__dict__.items():
            if key not in skip and not key.startswith("_"):
                payload[key] = value

        # Append exception info when present.
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure the root logger to emit structured JSON to stdout.

    Call once at application startup (before the first log statement).
    Silences verbose third-party loggers (uvicorn access logs duplicate
    the middleware logs) while keeping uvicorn error output visible.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_CloudJsonFormatter())

    root = logging.getLogger()
    root.setLevel(level)

    # Avoid adding duplicate handlers when running with uvicorn --reload.
    if not root.handlers:
        root.addHandler(handler)
    else:
        root.handlers.clear()
        root.addHandler(handler)

    # Uvicorn already emits an access line per request; our middleware does
    # the same in structured JSON, so suppress the plain-text duplicate.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
