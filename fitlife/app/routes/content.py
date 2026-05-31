from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from app.routes.content_data import (
    EXERCISE_LIBRARY,
    PROTEIN_NON_VEG,
    PROTEIN_VEG,
    get_diet_plan,
    get_workout_plan,
)

content_bp = Blueprint("content", __name__)


@content_bp.route("/exercises")
@login_required
def exercises_api():
    return jsonify(EXERCISE_LIBRARY)


@content_bp.route("/protein-sources")
@login_required
def protein_api():
    diet = current_user.diet_type
    if diet in ("vegetarian", "vegan"):
        return jsonify({"type": diet, "sources": PROTEIN_VEG})
    return jsonify({"type": "non-vegetarian", "sources": PROTEIN_NON_VEG})


def get_user_content(user):
    return {
        "workout": get_workout_plan(user.goal),
        "diet": get_diet_plan(user.diet_type, user.goal),
        "exercises": EXERCISE_LIBRARY,
        "protein_veg": PROTEIN_VEG,
        "protein_non_veg": PROTEIN_NON_VEG,
    }
