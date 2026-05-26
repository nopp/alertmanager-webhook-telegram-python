import pytest
import requests
from unittest.mock import MagicMock, patch

from app.telegram import TelegramClient


@pytest.fixture
def telegram():
    return TelegramClient(bot_token="fake-token", chat_id="-123456", max_retries=3)


def mock_response(status_code=200, headers=None):
    resp = MagicMock()
    resp.status_code = status_code
    resp.headers = headers or {}
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.exceptions.HTTPError(response=resp)
    else:
        resp.raise_for_status.return_value = None
    return resp


def test_send_success(telegram):
    with patch("app.telegram.requests.post", return_value=mock_response(200)) as mock_post:
        telegram.send("hello")
        mock_post.assert_called_once()


def test_send_uses_markdown_parse_mode(telegram):
    with patch("app.telegram.requests.post", return_value=mock_response(200)) as mock_post:
        telegram.send("hello")
        _, kwargs = mock_post.call_args
        assert kwargs["json"]["parse_mode"] == "Markdown"
        assert kwargs["json"]["chat_id"] == "-123456"


def test_send_retries_on_rate_limit(telegram):
    with patch("app.telegram.requests.post", side_effect=[
        mock_response(429, headers={"Retry-After": "1"}),
        mock_response(200),
    ]) as mock_post:
        with patch("app.telegram.time.sleep") as mock_sleep:
            telegram.send("hello")
            mock_sleep.assert_called_once_with(1)
            assert mock_post.call_count == 2


def test_send_retries_on_timeout(telegram):
    with patch("app.telegram.requests.post", side_effect=[
        requests.exceptions.Timeout,
        mock_response(200),
    ]) as mock_post:
        with patch("app.telegram.time.sleep"):
            telegram.send("hello")
            assert mock_post.call_count == 2


def test_send_retries_on_connection_error(telegram):
    with patch("app.telegram.requests.post", side_effect=[
        requests.exceptions.ConnectionError("network down"),
        mock_response(200),
    ]) as mock_post:
        with patch("app.telegram.time.sleep"):
            telegram.send("hello")
            assert mock_post.call_count == 2


def test_send_raises_after_max_retries_exceeded(telegram):
    with patch("app.telegram.requests.post", side_effect=requests.exceptions.Timeout):
        with patch("app.telegram.time.sleep"):
            with pytest.raises(RuntimeError, match="Failed to reach Telegram after 3 attempts"):
                telegram.send("hello")


def test_send_raises_on_non_retryable_http_error(telegram):
    with patch("app.telegram.requests.post", return_value=mock_response(500)):
        with pytest.raises(requests.exceptions.HTTPError):
            telegram.send("hello")
