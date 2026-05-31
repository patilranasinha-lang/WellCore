from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    goal = db.Column(db.String(50), nullable=False)
    diet_type = db.Column(db.String(20), nullable=False)
    activity_level = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    progress_entries = db.relationship(
        "UserProgress",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.email}>"


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    weight_kg = db.Column(db.Float, nullable=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<UserProgress user={self.user_id} weight={self.weight_kg}>"
