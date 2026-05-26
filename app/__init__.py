import logging

from flask import Flask
from flask_basicauth import BasicAuth

from .config import Config
from .routes import bp
from .telegram import TelegramClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


def create_app(config: Config | None = None) -> Flask:
    app = Flask(__name__)

    cfg = config or Config()

    if not cfg.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")
    if not cfg.TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID is required")
    app.secret_key = cfg.SECRET_KEY
    app.config["BASIC_AUTH_FORCE"] = cfg.BASIC_AUTH_FORCE
    app.config["BASIC_AUTH_USERNAME"] = cfg.BASIC_AUTH_USERNAME
    app.config["BASIC_AUTH_PASSWORD"] = cfg.BASIC_AUTH_PASSWORD

    BasicAuth(app)

    app.telegram = TelegramClient(  # type: ignore[attr-defined]
        bot_token=cfg.TELEGRAM_BOT_TOKEN,
        chat_id=cfg.TELEGRAM_CHAT_ID,
        max_retries=cfg.MAX_RETRIES,
    )

    app.register_blueprint(bp)

    return app
