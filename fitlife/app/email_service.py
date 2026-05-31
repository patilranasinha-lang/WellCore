import os
from pathlib import Path

from flask import current_app, render_template
from flask_mail import Message

from app import mail
from app.models import User


def is_mail_configured() -> bool:
    username = current_app.config.get("MAIL_USERNAME")
    password = current_app.config.get("MAIL_PASSWORD")
    return bool(username and password and str(username).strip() and str(password).strip())


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
    (folder / f"welcome_{safe_name}.txt").write_text(
        f"Subject: {subject}\n\n{text_body}",
        encoding="utf-8",
    )
    return filepath


def send_welcome_email(user: User) -> tuple[bool, str]:
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
        + "/login",
    )

    if not is_mail_configured():
        try:
            path = _save_dev_copy(user, subject, html_body, text_body)
            return False, (
                "Mail is not configured. Welcome email saved locally at: "
                f"{path}. Add MAIL_USERNAME and MAIL_PASSWORD (Gmail App Password) to .env"
            )
        except Exception as exc:
            current_app.logger.exception("Failed to save dev email copy")
            return False, f"Mail not configured and dev save failed: {exc}"

    msg = Message(
        subject=subject,
        recipients=[user.email],
        body=text_body,
        html=html_body,
        sender=_get_sender(),
    )

    try:
        mail.send(msg)
        return True, "Welcome email sent successfully."
    except Exception as exc:
        current_app.logger.exception("Welcome email failed for %s", user.email)
        return False, (
            f"Could not send email: {exc}. "
            "Use a Gmail App Password (not your normal password) in .env"
        )
