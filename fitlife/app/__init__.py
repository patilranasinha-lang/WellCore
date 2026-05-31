from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    if app.config.get("MAIL_USERNAME") and not app.config.get("MAIL_DEFAULT_SENDER"):
        app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

    if app.config.get("MAIL_USERNAME") and app.config.get("MAIL_PASSWORD"):
        app.logger.info("Mail ready: %s", app.config["MAIL_USERNAME"])
    else:
        app.logger.warning(
            "Mail not configured — welcome emails disabled. %s",
            "Set MAIL_PASSWORD in .env or instance/mail_secret.txt",
        )

    login_manager.login_view = "auth.login_page"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.content import content_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(content_bp, url_prefix="/api")

    return app
