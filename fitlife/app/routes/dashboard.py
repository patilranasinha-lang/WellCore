from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.email_service import flash_message_for_email_error, send_welcome_email
from app.models import UserProgress
from app.routes.content import get_user_content
from app.routes.content_data import get_diet_plan, get_workout_plan
from app.utils import calculate_bmi

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("index.html")


@dashboard_bp.route("/resend-welcome-email", methods=["POST"])
@login_required
def resend_welcome_email():
    sent, err = send_welcome_email(current_user)
    if sent:
        flash(
            f"Welcome email sent to {current_user.email}. Check inbox and spam folder.",
            "success",
        )
    else:
        msg, cat = flash_message_for_email_error(err)
        flash(msg, cat)
    return redirect(url_for("dashboard.dashboard") + "#my-profile")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    bmi_data = calculate_bmi(current_user.weight_kg, current_user.height_cm)
    content = get_user_content(current_user)
    return render_template(
        "dashboard.html",
        user=current_user,
        bmi=bmi_data,
        workout=content["workout"],
        diet=content["diet"],
        exercises=content["exercises"],
        protein_veg=content["protein_veg"],
        protein_non_veg=content["protein_non_veg"],
    )


@dashboard_bp.route("/api/user-profile")
@login_required
def user_profile():
    bmi_data = calculate_bmi(current_user.weight_kg, current_user.height_cm)
    return jsonify(
        {
            "full_name": current_user.full_name,
            "email": current_user.email,
            "age": current_user.age,
            "gender": current_user.gender,
            "height_cm": current_user.height_cm,
            "weight_kg": current_user.weight_kg,
            "goal": current_user.goal,
            "diet_type": current_user.diet_type,
            "activity_level": current_user.activity_level,
            "created_at": current_user.created_at.isoformat(),
            "bmi": bmi_data,
            "workout": get_workout_plan(current_user.goal),
            "diet": get_diet_plan(current_user.diet_type, current_user.goal),
        }
    )


@dashboard_bp.route("/api/log-weight", methods=["POST"])
@login_required
def log_weight():
    data = request.get_json(silent=True) or {}
    try:
        weight = float(data.get("weight_kg", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid weight value."}), 400

    if weight < 30 or weight > 300:
        return jsonify({"error": "Weight must be between 30 and 300 kg."}), 400

    entry = UserProgress(user_id=current_user.id, weight_kg=weight)
    current_user.weight_kg = weight
    db.session.add(entry)
    db.session.commit()

    bmi_data = calculate_bmi(weight, current_user.height_cm)
    return jsonify(
        {
            "success": True,
            "entry": {
                "id": entry.id,
                "weight_kg": entry.weight_kg,
                "logged_at": entry.logged_at.isoformat(),
            },
            "bmi": bmi_data,
        }
    )


@dashboard_bp.route("/api/weight-history")
@login_required
def weight_history():
    entries = (
        UserProgress.query.filter_by(user_id=current_user.id)
        .order_by(UserProgress.logged_at.asc())
        .all()
    )
    if not entries:
        entries_data = [
            {
                "weight_kg": current_user.weight_kg,
                "logged_at": current_user.created_at.isoformat(),
            }
        ]
    else:
        entries_data = [
            {"weight_kg": e.weight_kg, "logged_at": e.logged_at.isoformat()}
            for e in entries
        ]
    return jsonify({"entries": entries_data})
