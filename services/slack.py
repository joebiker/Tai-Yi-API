import json
import logging
from typing import Any

import httpx
from fastapi import BackgroundTasks

from config import SLACK_BUGREPORTS_URL

_logger = logging.getLogger(__name__)


async def send_to_slack(message: str) -> None:
    if not SLACK_BUGREPORTS_URL:
        return

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(SLACK_BUGREPORTS_URL, json={"text": message})
            response.raise_for_status()
    except httpx.HTTPError as exc:
        _logger.warning("Failed to send Slack log: %s", exc)


def queue_slack_message(background_tasks: BackgroundTasks, payload: Any) -> None:
    if isinstance(payload, str):
        message = payload
    else:
        message = json.dumps(payload, ensure_ascii=False)

    background_tasks.add_task(send_to_slack, message)