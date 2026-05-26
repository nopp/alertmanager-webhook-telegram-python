import logging
import time

import requests

logger = logging.getLogger(__name__)


class TelegramClient:
    def __init__(self, bot_token: str, chat_id: str, max_retries: int = 3) -> None:
        self.chat_id = chat_id
        self.max_retries = max_retries
        self._url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, text: str) -> None:
        """Send a message to Telegram with retry on transient errors."""
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}

        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.post(self._url, json=payload, timeout=10)
                resp.raise_for_status()
                return
            except requests.exceptions.HTTPError:
                if resp.status_code == 429:
                    wait = int(resp.headers.get("Retry-After", 30))
                    logger.warning("Rate limited, waiting %ds (attempt %d/%d)…", wait, attempt, self.max_retries)
                    time.sleep(wait)
                else:
                    raise
            except requests.exceptions.Timeout:
                logger.warning("Timeout (attempt %d/%d), retrying in 60s…", attempt, self.max_retries)
                time.sleep(60)
            except requests.exceptions.ConnectionError as exc:
                logger.warning("Network error (attempt %d/%d): %s", attempt, self.max_retries, exc)
                time.sleep(60)

        raise RuntimeError(f"Failed to reach Telegram after {self.max_retries} attempts")
