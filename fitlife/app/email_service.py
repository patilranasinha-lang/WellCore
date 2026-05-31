import smtplib

from flask import current_app, render_template
from flask_mail import Message

from app import mail
from app.models import User
from config import _load_mail_password


def _validate_app_password_format(password: str) -> bool:
    """Gmail App Passwords are 16 characters (spaces optional)."""
    clean = password.replace(" ", "")
    return len(clean) == 16 and clean.isalnum()


def _apply_mail_credentials(app) -> bool:
    password = _load_mail_password()
    username = app.config.get("MAIL_USERNAME")
    if username and password:
        app.config["MAIL_PASSWORD"] = password
        if not app.config.get("MAIL_DEFAULT_SENDER"):
            app.config["MAIL_DEFAULT_SENDER"] = username
        return True
    return False


def is_mail_configured(app=None) -> bool:
    app = app or current_app
    username = app.config.get("MAIL_USERNAME")
    password = _load_mail_password()
    return bool(username and password and str(username).strip() and str(password).strip())


def _get_sender(app) -> str:
    sender = app.config.get("MAIL_DEFAULT_SENDER") or app.config.get("MAIL_USERNAME")
    return str(sender).strip()


def _build_welcome_message(app, user: User) -> Message:
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
        login_url=app.config.get("APP_BASE_URL", "http://127.0.0.1:5000") + "/auth/login",
    )
    return Message(
        subject=subject,
        recipients=[user.email.strip().lower()],
        body=text_body,
        html=html_body,
        sender=_get_sender(app),
        reply_to=app.config.get("MAIL_USERNAME"),
    )


def send_welcome_email(user: User) -> tuple[bool, str | None]:
    """
    Send welcome email to user.email.
    Returns (success, error_key) where error_key is: missing | bad_format | auth_failed | other
    """
    app = current_app._get_current_object()

    if not is_mail_configured(app):
        return False, "missing"

    password = _load_mail_password() or ""
    if not _validate_app_password_format(password):
        app.logger.warning(
            "MAIL_PASSWORD does not look like a Gmail App Password (need 16 characters)."
        )
        return False, "bad_format"

    _apply_mail_credentials(app)

    try:
        with app.app_context():
            msg = _build_welcome_message(app, user)
            mail.send(msg)
            app.logger.info("Welcome email sent to %s", user.email)
            return True, None
    except smtplib.SMTPAuthenticationError:
        app.logger.exception("Gmail rejected MAIL_PASSWORD for %s", user.email)
        return False, "auth_failed"
    except Exception:
        app.logger.exception("Welcome email failed for %s", user.email)
        return False, "other"


def flash_message_for_email_error(error_key: str | None) -> tuple[str, str]:
    if error_key == "missing":
        return (
            "Email not set up. Add MAIL_PASSWORD in fitlife/.env (Gmail App Password) and restart.",
            "warning",
        )
    if error_key == "bad_format":
        return (
            "Gmail rejected your password. MAIL_PASSWORD must be a 16-character App Password "
            "(from https://myaccount.google.com/apppasswords), not your normal Gmail password.",
            "warning",
        )
    if error_key == "auth_failed":
        return (
            "Gmail login failed. Create a new App Password at "
            "https://myaccount.google.com/apppasswords, put it in MAIL_PASSWORD, restart server.",
            "warning",
        )
    return (
        "Could not send email. See fitlife/EMAIL_SETUP.md and restart the server.",
        "warning",
    )
