import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_BASE_DIR = Path(__file__).resolve().parent


def _load_mail_password() -> str | None:
    """Read Gmail App Password from .env or instance/mail_secret.txt (not committed)."""
    from_env = (os.getenv("MAIL_PASSWORD") or "").strip().replace(" ", "")
    if from_env:
        return from_env

    secret_file = _BASE_DIR / "instance" / "mail_secret.txt"
    if secret_file.is_file():
        return secret_file.read_text(encoding="utf-8").strip().replace(" ", "")

    return None


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://user:pass@localhost/fitlife_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("true", "1", "yes")
    MAIL_USERNAME = (os.getenv("MAIL_USERNAME") or "").strip() or None
    MAIL_PASSWORD = _load_mail_password()
    MAIL_DEFAULT_SENDER = (
        (os.getenv("MAIL_DEFAULT_SENDER") or MAIL_USERNAME or "").strip() or None
    )
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000").rstrip("/")

    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 86400
