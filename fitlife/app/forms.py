from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=150)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, max=128)],
    )
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=100)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=150)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, max=128)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    age = IntegerField(
        "Age",
        validators=[DataRequired(), NumberRange(min=13, max=120)],
    )
    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[DataRequired()],
    )
    height_cm = FloatField(
        "Height (cm)",
        validators=[DataRequired(), NumberRange(min=100, max=250)],
    )
    weight_kg = FloatField(
        "Weight (kg)",
        validators=[DataRequired(), NumberRange(min=30, max=300)],
    )
    goal = SelectField(
        "Fitness Goal",
        choices=[
            ("fat loss", "Fat Loss"),
            ("muscle gain", "Muscle Gain"),
            ("maintain", "Maintain"),
        ],
        validators=[DataRequired()],
    )
    diet_type = SelectField(
        "Diet Type",
        choices=[
            ("vegetarian", "Vegetarian"),
            ("non-vegetarian", "Non-Vegetarian"),
            ("vegan", "Vegan"),
        ],
        validators=[DataRequired()],
    )
    activity_level = SelectField(
        "Activity Level",
        choices=[
            ("sedentary", "Sedentary"),
            ("moderate", "Moderate"),
            ("active", "Active"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create Account")
