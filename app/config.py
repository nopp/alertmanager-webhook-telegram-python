import os


class Config:
    SECRET_KEY: str | bytes = os.environ.get("SECRET_KEY", os.urandom(24))
    BASIC_AUTH_FORCE: bool = os.environ.get("BASIC_AUTH_FORCE", "true").lower() == "true"
    BASIC_AUTH_USERNAME: str = os.environ.get("BASIC_AUTH_USERNAME", "")
    BASIC_AUTH_PASSWORD: str = os.environ.get("BASIC_AUTH_PASSWORD", "")
    TELEGRAM_BOT_TOKEN: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.environ.get("TELEGRAM_CHAT_ID", "")
    MAX_RETRIES: int = int(os.environ.get("MAX_RETRIES", "3"))
