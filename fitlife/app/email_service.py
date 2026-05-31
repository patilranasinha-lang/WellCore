from flask import current_app, render_template
from flask_mail import Message

from app import mail
from app.models import User
from config import _load_mail_password


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


def send_welcome_email(user: User) -> bool:
    """
    Send welcome email to user.email (signup address). No UI messages — caller handles flash.
    Returns True if sent successfully.
    """
    app = current_app._get_current_object()

    if not is_mail_configured(app):
        return False

    _apply_mail_credentials(app)

    try:
        with app.app_context():
            msg = _build_welcome_message(app, user)
            mail.send(msg)
            app.logger.info("Welcome email sent to %s", user.email)
            return True
    except Exception:
        app.logger.exception("Welcome email failed for %s", user.email)
        return False
