WORKOUT_PLANS = {
    "fat loss": {
        "title": "Fat Loss Workout Plan",
        "description": "High calorie burn with strength maintenance and active recovery.",
        "days": [
            {"day": "Day 1", "focus": "Cardio", "workout": "30 min run + 15 min HIIT (burpees, mountain climbers)"},
            {"day": "Day 2", "focus": "Full Body Strength", "workout": "Squats, lunges, push-ups, rows — 3 sets × 12 reps"},
            {"day": "Day 3", "focus": "Active Rest", "workout": "30 min yoga or brisk walk + stretching"},
            {"day": "Day 4", "focus": "Cardio", "workout": "Cycling or jump rope 35 min + core circuit"},
            {"day": "Day 5", "focus": "Full Body Strength", "workout": "Deadlifts, bench press, pull-ups — 3 sets × 10 reps"},
            {"day": "Day 6", "focus": "HIIT + Core", "workout": "20 min HIIT + planks, crunches, leg raises"},
            {"day": "Day 7", "focus": "Rest", "workout": "Complete rest or light stretching only"},
        ],
    },
    "muscle gain": {
        "title": "Muscle Gain Workout Plan",
        "description": "Split training for hypertrophy with adequate recovery.",
        "days": [
            {"day": "Day 1", "focus": "Chest + Triceps", "workout": "Bench press, incline DB press, dips, tricep pushdowns"},
            {"day": "Day 2", "focus": "Back + Biceps", "workout": "Pull-ups, barbell rows, lat pulldown, barbell curls"},
            {"day": "Day 3", "focus": "Legs + Core", "workout": "Squats, leg press, RDL, calf raises, hanging leg raises"},
            {"day": "Day 4", "focus": "Shoulders + Arms", "workout": "OHP, lateral raises, face pulls, hammer curls"},
            {"day": "Day 5", "focus": "Chest + Triceps", "workout": "Repeat Day 1 with heavier weight or more volume"},
            {"day": "Day 6", "focus": "Back + Biceps", "workout": "Repeat Day 2 — focus on progressive overload"},
            {"day": "Day 7", "focus": "Rest", "workout": "Rest and recovery — aim for 7–9 hours sleep"},
        ],
    },
    "maintain": {
        "title": "Maintenance Workout Plan",
        "description": "Balanced strength and cardio to maintain current fitness.",
        "days": [
            {"day": "Mon", "focus": "Strength", "workout": "Full body compound lifts — 3 sets × 10 reps"},
            {"day": "Tue", "focus": "Cardio", "workout": "30 min moderate cardio (run, cycle, or swim)"},
            {"day": "Wed", "focus": "Strength", "workout": "Upper/lower split — push, pull, legs"},
            {"day": "Thu", "focus": "Rest", "workout": "Light walk or mobility work"},
            {"day": "Fri", "focus": "Strength", "workout": "Full body — focus on form and consistency"},
            {"day": "Sat", "focus": "Cardio", "workout": "45 min low-to-moderate intensity cardio"},
            {"day": "Sun", "focus": "Rest", "workout": "Full rest day"},
        ],
    },
}

DIET_PLANS = {
    ("vegetarian", "fat loss"): {
        "title": "Vegetarian Fat Loss Plan",
        "calories": "1500–1800 kcal",
        "meals": [
            ("Breakfast", "Oats + banana + green tea"),
            ("Mid-morning", "Apple + handful almonds"),
            ("Lunch", "Dal + 2 roti + salad + curd"),
            ("Snack", "Sprouts chaat"),
            ("Dinner", "Paneer sabzi + 1 roti + soup"),
        ],
    },
    ("vegetarian", "muscle gain"): {
        "title": "Vegetarian Muscle Gain Plan",
        "calories": "2500–3000 kcal",
        "meals": [
            ("Breakfast", "Paneer paratha + milk"),
            ("Mid-morning", "Banana shake + peanut butter"),
            ("Lunch", "Rajma chawal + curd + salad"),
            ("Pre-workout", "Fruits + dry fruits"),
            ("Post-workout", "Whey protein + banana"),
            ("Dinner", "Tofu stir fry + 2 roti + dal"),
        ],
    },
    ("vegetarian", "maintain"): {
        "title": "Vegetarian Maintenance Plan",
        "calories": "2000–2200 kcal",
        "meals": [
            ("Breakfast", "Vegetable upma + curd"),
            ("Lunch", "Mixed veg + dal + rice + salad"),
            ("Snack", "Roasted chana + fruit"),
            ("Dinner", "Khichdi + sautéed greens + buttermilk"),
        ],
    },
    ("non-vegetarian", "fat loss"): {
        "title": "Non-Vegetarian Fat Loss Plan",
        "calories": "1500–1800 kcal",
        "meals": [
            ("Breakfast", "Boiled eggs (3) + brown bread + tea"),
            ("Mid-morning", "Banana + walnuts"),
            ("Lunch", "Grilled chicken + rice + salad"),
            ("Snack", "Greek yogurt"),
            ("Dinner", "Fish curry + 1 roti + veggies"),
        ],
    },
    ("non-vegetarian", "muscle gain"): {
        "title": "Non-Vegetarian Muscle Gain Plan",
        "calories": "2500–3000 kcal",
        "meals": [
            ("Breakfast", "Eggs (4–5) + oats + milk"),
            ("Mid-morning", "Peanut butter toast"),
            ("Lunch", "Chicken breast + brown rice + salad"),
            ("Pre-workout", "Banana + black coffee"),
            ("Post-workout", "Whey protein shake"),
            ("Dinner", "Mutton/Fish + 2 roti + veggies"),
        ],
    },
    ("non-vegetarian", "maintain"): {
        "title": "Non-Vegetarian Maintenance Plan",
        "calories": "2000–2400 kcal",
        "meals": [
            ("Breakfast", "Eggs + toast + fruit"),
            ("Lunch", "Grilled fish/chicken + veggies + rice"),
            ("Snack", "Protein shake or cottage cheese"),
            ("Dinner", "Lean meat curry + salad + 1 roti"),
        ],
    },
    ("vegan", "fat loss"): {
        "title": "Vegan Fat Loss Plan",
        "calories": "1500–1800 kcal",
        "meals": [
            ("Breakfast", "Oatmeal with almond milk + berries"),
            ("Mid-morning", "Apple + mixed nuts"),
            ("Lunch", "Lentil soup + quinoa + green salad"),
            ("Snack", "Hummus with carrot sticks"),
            ("Dinner", "Tofu stir-fry + brown rice + steamed broccoli"),
        ],
    },
    ("vegan", "muscle gain"): {
        "title": "Vegan Muscle Gain Plan",
        "calories": "2500–3000 kcal",
        "meals": [
            ("Breakfast", "Tofu scramble + whole grain toast + smoothie"),
            ("Mid-morning", "Peanut butter banana shake"),
            ("Lunch", "Chickpea curry + rice + avocado"),
            ("Pre-workout", "Dates + almonds"),
            ("Post-workout", "Plant protein + banana"),
            ("Dinner", "Tempeh bowl + sweet potato + kale"),
        ],
    },
    ("vegan", "maintain"): {
        "title": "Vegan Maintenance Plan",
        "calories": "2000–2200 kcal",
        "meals": [
            ("Breakfast", "Chia pudding + fruit"),
            ("Lunch", "Buddha bowl (beans, grains, greens)"),
            ("Snack", "Trail mix"),
            ("Dinner", "Lentil pasta + marinara + nutritional yeast"),
        ],
    },
}

EXERCISE_LIBRARY = {
    "cardio": [
        {
            "name": "Running",
            "muscle": "Legs, cardiovascular system",
            "instructions": "Maintain steady pace; land mid-foot; keep upright posture.",
            "sets_reps": "20–45 min continuous or intervals",
        },
        {
            "name": "Cycling",
            "muscle": "Quads, glutes, cardio",
            "instructions": "Adjust seat height so knee is slightly bent at bottom of pedal stroke.",
            "sets_reps": "30–60 min moderate intensity",
        },
        {
            "name": "Jump Rope",
            "muscle": "Calves, shoulders, cardio",
            "instructions": "Keep elbows in, wrists rotating rope; land softly on balls of feet.",
            "sets_reps": "5 × 2 min rounds with 1 min rest",
        },
        {
            "name": "Swimming",
            "muscle": "Full body, cardio",
            "instructions": "Focus on long strokes and controlled breathing each lap.",
            "sets_reps": "20–40 min laps",
        },
        {
            "name": "HIIT",
            "muscle": "Full body, cardio",
            "instructions": "Alternate 40 sec max effort with 20 sec rest — burpees, sprints, jacks.",
            "sets_reps": "8–12 rounds, 20 min total",
        },
    ],
    "strength": [
        {
            "name": "Squats",
            "muscle": "Quads, glutes, core",
            "instructions": "Feet shoulder-width, chest up, hips back, knees track over toes.",
            "sets_reps": "4 × 8–12 reps",
        },
        {
            "name": "Deadlifts",
            "muscle": "Hamstrings, glutes, back",
            "instructions": "Hinge at hips, flat back, bar close to shins, drive through heels.",
            "sets_reps": "4 × 6–10 reps",
        },
        {
            "name": "Bench Press",
            "muscle": "Chest, triceps, shoulders",
            "instructions": "Retract scapula, feet flat, lower bar to mid-chest, press up.",
            "sets_reps": "4 × 8–10 reps",
        },
        {
            "name": "Pull-ups",
            "muscle": "Lats, biceps, core",
            "instructions": "Full hang, pull chin over bar, control descent.",
            "sets_reps": "3 × max reps (or assisted)",
        },
        {
            "name": "Barbell Rows",
            "muscle": "Back, biceps",
            "instructions": "Hinge forward 45°, pull bar to lower ribs, squeeze shoulder blades.",
            "sets_reps": "4 × 8–12 reps",
        },
    ],
    "core": [
        {
            "name": "Plank",
            "muscle": "Core, shoulders",
            "instructions": "Forearms and toes on floor, body straight, brace abs.",
            "sets_reps": "3 × 45–60 sec hold",
        },
        {
            "name": "Crunches",
            "muscle": "Rectus abdominis",
            "instructions": "Lower back on floor, lift shoulders toward knees, avoid neck pull.",
            "sets_reps": "3 × 15–20 reps",
        },
        {
            "name": "Leg Raises",
            "muscle": "Lower abs, hip flexors",
            "instructions": "Legs straight, raise to 90°, lower slowly without arching back.",
            "sets_reps": "3 × 12–15 reps",
        },
        {
            "name": "Russian Twists",
            "muscle": "Obliques",
            "instructions": "Seated lean back, rotate torso side to side with weight or hands clasped.",
            "sets_reps": "3 × 20 twists total",
        },
    ],
    "flexibility": [
        {
            "name": "Yoga Flow",
            "muscle": "Full body flexibility",
            "instructions": "Move through sun salutations, warrior poses, and child's pose.",
            "sets_reps": "20–30 min session",
        },
        {
            "name": "Hamstring Stretch",
            "muscle": "Hamstrings, lower back",
            "instructions": "Seated or standing, hinge forward with straight back, hold gently.",
            "sets_reps": "2 × 30 sec each leg",
        },
        {
            "name": "Hip Flexor Stretch",
            "muscle": "Hip flexors",
            "instructions": "Kneeling lunge, tuck pelvis, push hips forward until stretch felt.",
            "sets_reps": "2 × 30 sec each side",
        },
        {
            "name": "Shoulder Mobility",
            "muscle": "Shoulders, thoracic spine",
            "instructions": "Arm circles, band pull-aparts, and wall slides for range of motion.",
            "sets_reps": "10 reps each movement",
        },
    ],
}

PROTEIN_VEG = [
    {"source": "Paneer", "protein": "18g"},
    {"source": "Lentils (Dal)", "protein": "9g"},
    {"source": "Chickpeas", "protein": "19g"},
    {"source": "Greek Yogurt", "protein": "10g"},
    {"source": "Tofu", "protein": "8g"},
    {"source": "Peanuts", "protein": "26g"},
    {"source": "Quinoa", "protein": "4g"},
    {"source": "Soybean", "protein": "36g"},
]

PROTEIN_NON_VEG = [
    {"source": "Chicken Breast", "protein": "31g"},
    {"source": "Eggs", "protein": "13g"},
    {"source": "Tuna", "protein": "30g"},
    {"source": "Salmon", "protein": "25g"},
    {"source": "Cottage Cheese", "protein": "12g"},
    {"source": "Beef (lean)", "protein": "26g"},
    {"source": "Turkey", "protein": "29g"},
]


def get_workout_plan(goal: str) -> dict:
    return WORKOUT_PLANS.get(goal, WORKOUT_PLANS["maintain"])


def get_diet_plan(diet_type: str, goal: str) -> dict:
    key = (diet_type, goal)
    if key in DIET_PLANS:
        return DIET_PLANS[key]
    veg_key = ("vegetarian", goal)
    return DIET_PLANS.get(veg_key, DIET_PLANS[("vegetarian", "maintain")])
