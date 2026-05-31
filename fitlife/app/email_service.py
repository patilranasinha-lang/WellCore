from pathlib import Path

from flask import current_app, render_template
from flask_mail import Message

from app import mail
from app.models import User


def is_mail_configured() -> bool:
    username = current_app.config.get("MAIL_USERNAME")
    password = current_app.config.get("MAIL_PASSWORD")
    return bool(username and password and str(username).strip() and str(password).strip())


def mail_setup_hint() -> str:
    return (
        "To enable welcome emails: add your Gmail App Password to "
        "fitlife/.env as MAIL_PASSWORD=xxxx, or create fitlife/instance/mail_secret.txt "
        "with the 16-character password (see mail_secret.example.txt). Restart the server."
    )


def _get_sender() -> str:
    sender = current_app.config.get("MAIL_DEFAULT_SENDER") or current_app.config.get(
        "MAIL_USERNAME"
    )
    return str(sender).strip()


def _save_dev_copy(user: User, subject: str, html_body: str, text_body: str) -> Path:
    folder = Path(current_app.instance_path) / "sent_emails"
    folder.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() else "_" for c in user.email)
    filepath = folder / f"welcome_{safe_name}.html"
    filepath.write_text(
        f"<!-- Subject: {subject} -->\n{html_body}",
        encoding="utf-8",
    )
    return filepath


def send_welcome_email(user: User) -> tuple[bool, str, str]:
    """
    Returns (sent_ok, user_flash_message, flash_category).
    flash_category: success | info | warning
    """
    subject = f"Welcome to FitLife, {user.full_name}!"
    text_body = (
        f"Hi {user.full_name},\n\n"
        "Welcome to FitLife — your personal health & fitness companion!\n\n"
        "Your account is ready. Based on your profile:\n"
        f"- Goal: {user.goal.title()}\n"
        f"- Diet: {user.diet_type.replace('-', ' ').title()}\n\n"
        "We've prepared a personalized plan for you. Login anytime to explore!\n\n"
        "Stay fit,\nTeam FitLife"
    )
    html_body = render_template(
        "emails/welcome.html",
        user=user,
        login_url=current_app.config.get("APP_BASE_URL", "http://127.0.0.1:5000")
        + "/auth/login",
    )

    if not is_mail_configured():
        try:
            _save_dev_copy(user, subject, html_body, text_body)
        except Exception:
            current_app.logger.exception("Could not save local email copy")
        return (
            False,
            "Account created! Welcome email is off until you add a Gmail App Password.",
            "info",
        )

    msg = Message(
        subject=subject,
        recipients=[user.email],
        body=text_body,
        html=html_body,
        sender=_get_sender(),
    )

    try:
        mail.send(msg)
        return (
            True,
            f"Account created! Welcome email sent to {user.email}.",
            "success",
        )
    except Exception as exc:
        current_app.logger.exception("Welcome email failed for %s", user.email)
        err = str(exc).lower()
        if "authentication" in err or "535" in err or "534" in err:
            hint = "Check MAIL_PASSWORD — use a Gmail App Password, not your normal password."
        else:
            hint = "Check MAIL_USERNAME and MAIL_PASSWORD in .env, then restart the server."
        return (
            False,
            f"Account created, but email could not be sent. {hint}",
            "warning",
        )
