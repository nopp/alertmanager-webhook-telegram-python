import pytest
from unittest.mock import MagicMock

from app import create_app
from app.config import Config


class TestConfig(Config):
    SECRET_KEY = "test-secret"
    BASIC_AUTH_FORCE = False
    BASIC_AUTH_USERNAME = "test"
    BASIC_AUTH_PASSWORD = "test"
    TELEGRAM_BOT_TOKEN = "fake-token"
    TELEGRAM_CHAT_ID = "-123456789"
    MAX_RETRIES = 3


@pytest.fixture
def mock_telegram():
    return MagicMock()


@pytest.fixture
def app(mock_telegram):
    application = create_app(TestConfig())
    application.telegram = mock_telegram  # type: ignore[attr-defined]
    application.config["TESTING"] = True
    return application


@pytest.fixture
def client(app):
    return app.test_client()
