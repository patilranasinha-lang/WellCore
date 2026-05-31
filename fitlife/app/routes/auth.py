from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app import bcrypt, db
from app.email_service import flash_message_for_email_error, send_welcome_email
from app.forms import LoginForm, RegisterForm
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if not user or not bcrypt.check_password_hash(
            user.password_hash, form.password.data
        ):
            flash("Invalid email or password.", "danger")
        else:
            login_user(user, remember=True)
            flash(f"Welcome back, {user.full_name}!", "success")
            return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower().strip()).first():
            flash("An account with this email already exists.", "danger")
        else:
            password_hash = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user = User(
                full_name=form.full_name.data.strip(),
                email=form.email.data.lower().strip(),
                password_hash=password_hash,
                age=form.age.data,
                gender=form.gender.data,
                height_cm=form.height_cm.data,
                weight_kg=form.weight_kg.data,
                goal=form.goal.data,
                diet_type=form.diet_type.data,
                activity_level=form.activity_level.data,
            )
            db.session.add(user)
            db.session.commit()

            email_sent, email_err = send_welcome_email(user)

            login_user(user)
            if email_sent:
                flash(
                    f"Account created! Welcome email sent to {user.email} — check inbox and spam.",
                    "success",
                )
            else:
                flash(
                    f"Account created successfully! Welcome, {user.full_name.split()[0]}!",
                    "success",
                )
                if email_err:
                    msg, cat = flash_message_for_email_error(email_err)
                    flash(msg, cat)
            return redirect(url_for("dashboard.dashboard"))

    return render_template("register.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("dashboard.index"))
