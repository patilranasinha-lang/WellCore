def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m**2), 1)

    if bmi < 18.5:
        category = "Underweight"
        message = (
            "Consider a balanced muscle-gain plan and consult a nutritionist "
            "if you want to reach a healthier weight."
        )
    elif bmi < 25:
        category = "Normal"
        message = (
            "Great job! You're in a healthy range. Stay consistent with "
            "your workouts and nutrition."
        )
    elif bmi < 30:
        category = "Overweight"
        message = (
            "A structured fat-loss plan with cardio and strength training "
            "can help you progress safely."
        )
    else:
        category = "Obese"
        message = (
            "Start with low-impact cardio and gradual calorie control. "
            "Consider speaking with a healthcare provider for guidance."
        )

    return {"value": bmi, "category": category, "message": message}
