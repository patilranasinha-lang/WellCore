"""Test Gmail SMTP. Usage: python scripts/test_email.py recipient@gmail.com"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app import create_app, mail
from config import _load_mail_password
from flask_mail import Message


def main():
    to = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()
    if not to or "@" not in to:
        print("Usage: python scripts/test_email.py recipient@gmail.com")
        sys.exit(1)

    app = create_app()
    pwd = _load_mail_password()
    user = app.config.get("MAIL_USERNAME")

    if not user or not pwd:
        print("FAIL: MAIL_USERNAME or MAIL_PASSWORD missing.")
        print("Add MAIL_PASSWORD to .env or instance/mail_secret.txt")
        sys.exit(1)

    app.config["MAIL_PASSWORD"] = pwd

    with app.app_context():
        msg = Message(
            subject="FitLife — test email",
            recipients=[to],
            body="If you see this, FitLife can send welcome emails.",
            sender=app.config.get("MAIL_DEFAULT_SENDER") or user,
        )
        try:
            mail.send(msg)
            print(f"OK: Test email sent to {to}")
            print(f"    From: {user}")
        except Exception as e:
            print(f"FAIL: {e}")
            print("Use a Gmail App Password, not your normal login password.")
            sys.exit(1)


if __name__ == "__main__":
    main()
