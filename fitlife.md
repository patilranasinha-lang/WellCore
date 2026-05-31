# FitLife — Health & Fitness Web App
### Full Project Plan (Flask + PostgreSQL + Bootstrap)

---

## Project Overview

**App Name:** FitLife  
**Type:** Single-page dynamic website (SPA feel via sections + AJAX)  
**Stack:** HTML, CSS, Bootstrap 5 | Flask (Python) | PostgreSQL | Flask-Mail  
**Goal:** User auth + profile + health content (gym, diet, exercises, weight plan, protein sources)

---

## Phase 1 — Project Setup & Environment

### Step 1.1 — Folder Structure
```
fitlife/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # DB models
│   ├── routes/
│   │   ├── auth.py          # Login / Register / Logout
│   │   ├── dashboard.py     # User dashboard
│   │   └── content.py       # Health content endpoints
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html       # Landing + Login/Register modals
│   │   └── dashboard.html   # Main single-page app
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── images/
├── config.py
├── requirements.txt
└── run.py
```

### Step 1.2 — Dependencies (`requirements.txt`)
```
Flask
Flask-SQLAlchemy
Flask-Login
Flask-Mail
Flask-Bcrypt
Flask-WTF
psycopg2-binary
python-dotenv
email-validator
```

### Step 1.3 — Environment Variables (`.env`)
```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:pass@localhost/fitlife_db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_USE_TLS=True
```

---

## Phase 2 — Database Design (PostgreSQL)

### Table: `users`
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | Auto |
| full_name | VARCHAR(100) | Required |
| email | VARCHAR(150) UNIQUE | Login key |
| password_hash | TEXT | Bcrypt |
| age | INTEGER | Required |
| gender | VARCHAR(10) | Male/Female/Other |
| height_cm | FLOAT | For BMI calc |
| weight_kg | FLOAT | Current weight |
| goal | VARCHAR(50) | Fat loss / Muscle gain / Maintain |
| diet_type | VARCHAR(20) | Vegetarian / Non-Vegetarian / Vegan |
| activity_level | VARCHAR(30) | Sedentary / Moderate / Active |
| created_at | TIMESTAMP | Auto |

### Table: `user_progress` *(optional Phase 2 feature)*
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| user_id | FK → users.id | |
| weight_kg | FLOAT | Log entry |
| logged_at | TIMESTAMP | |

---

## Phase 3 — Authentication System

### Step 3.1 — Register Flow
1. User opens landing page → clicks "Sign Up"
2. Modal form collects: name, email, password, age, gender, height, weight, goal, diet type, activity level
3. POST `/auth/register` → validate → hash password → save to DB
4. **Trigger welcome email** via Flask-Mail
5. Redirect to dashboard

### Step 3.2 — Login Flow
1. User clicks "Login" → modal form (email + password)
2. POST `/auth/login` → verify bcrypt hash → Flask-Login session
3. Redirect to dashboard

### Step 3.3 — Welcome Email Template
```
Subject: Welcome to FitLife, {name}! 💪

Hi {name},

Welcome to FitLife — your personal health & fitness companion!

Your account is ready. Based on your profile:
- Goal: {goal}
- Diet: {diet_type}

We've prepared a personalized plan for you. Login anytime to explore!

Stay fit,
Team FitLife
```

### Step 3.4 — Logout
- GET `/auth/logout` → clear session → redirect to landing

---

## Phase 4 — Single Page Dashboard

All content loads on one page. JS + Bootstrap tabs handle section switching without reload.

### Sections (Tabs/Navbar):
1. **My Profile** — show user info + BMI calculator result
2. **Workout Plans** — based on user goal
3. **Diet Plans** — veg / non-veg based on profile
4. **Exercises** — with categories (cardio, strength, flexibility)
5. **Protein Sources** — veg vs non-veg protein list
6. **Weight Tracker** — log + view progress

---

## Phase 5 — Content Modules

### 5.1 — BMI Calculator (auto on dashboard load)
- Formula: `BMI = weight / (height_m)²`
- Show category: Underweight / Normal / Overweight / Obese
- Display personalized message

### 5.2 — Workout Plans
**Fat Loss Plan:**
- Day 1: Cardio (30 min run + HIIT)
- Day 2: Full body strength
- Day 3: Active rest (yoga/walk)
- Day 4–6: Repeat with variation
- Day 7: Rest

**Muscle Gain Plan:**
- Day 1: Chest + Triceps
- Day 2: Back + Biceps
- Day 3: Legs + Core
- Day 4: Shoulders + Arms
- Day 5–6: Repeat
- Day 7: Rest

**Maintenance Plan:**
- 3 days strength + 2 days cardio + 2 days rest

### 5.3 — Diet Plans

**Vegetarian Fat Loss (1500–1800 kcal):**
| Meal | Food |
|---|---|
| Breakfast | Oats + banana + green tea |
| Mid-morning | Apple + handful almonds |
| Lunch | Dal + 2 roti + salad + curd |
| Snack | Sprouts chaat |
| Dinner | Paneer sabzi + 1 roti + soup |

**Non-Vegetarian Fat Loss (1500–1800 kcal):**
| Meal | Food |
|---|---|
| Breakfast | Boiled eggs (3) + brown bread + tea |
| Mid-morning | Banana + walnuts |
| Lunch | Grilled chicken + rice + salad |
| Snack | Greek yogurt |
| Dinner | Fish curry + 1 roti + veggies |

**Vegetarian Muscle Gain (2500–3000 kcal):**
| Meal | Food |
|---|---|
| Breakfast | Paneer paratha + milk |
| Mid-morning | Banana shake + peanut butter |
| Lunch | Rajma chawal + curd + salad |
| Pre-workout | Fruits + dry fruits |
| Post-workout | Whey protein + banana |
| Dinner | Tofu stir fry + 2 roti + dal |

**Non-Vegetarian Muscle Gain (2500–3000 kcal):**
| Meal | Food |
|---|---|
| Breakfast | Eggs (4–5) + oats + milk |
| Mid-morning | Peanut butter toast |
| Lunch | Chicken breast + brown rice + salad |
| Pre-workout | Banana + black coffee |
| Post-workout | Whey protein shake |
| Dinner | Mutton/Fish + 2 roti + veggies |

### 5.4 — Exercise Library
**Cardio:** Running, Cycling, Jump rope, Swimming, HIIT  
**Strength:** Squats, Deadlifts, Bench press, Pull-ups, Rows  
**Core:** Plank, Crunches, Leg raises, Russian twists  
**Flexibility:** Yoga, Stretching routines  

Each exercise card shows: name + muscle group + instructions + sets/reps suggestion

### 5.5 — Protein Sources
**Vegetarian:**
| Source | Protein per 100g |
|---|---|
| Paneer | 18g |
| Lentils (Dal) | 9g |
| Chickpeas | 19g |
| Greek Yogurt | 10g |
| Tofu | 8g |
| Peanuts | 26g |
| Quinoa | 4g |
| Soybean | 36g |

**Non-Vegetarian:**
| Source | Protein per 100g |
|---|---|
| Chicken Breast | 31g |
| Eggs | 13g |
| Tuna | 30g |
| Salmon | 25g |
| Cottage Cheese | 12g |
| Beef (lean) | 26g |
| Turkey | 29g |

---

## Phase 6 — Frontend Design

### Landing Page (`index.html`)
- Hero section: FitLife banner + tagline
- Features section (icons: gym, diet, track)
- Login button → Bootstrap modal
- Register button → Bootstrap modal (full form)
- Navbar: Logo | Features | Login | Sign Up

### Dashboard Page (`dashboard.html`)
- Top navbar: Logo | Tab links | User name + Logout
- Bootstrap tab system for all sections
- Cards for workout/diet plans
- BMI display card (auto-calculated)
- Progress chart (Chart.js — simple line)
- Responsive mobile-first layout

---

## Phase 7 — Flask Routes Map

```
GET  /                    → Landing page
POST /auth/register       → Register user + send welcome mail
POST /auth/login          → Login + session
GET  /auth/logout         → Logout
GET  /dashboard           → Main dashboard (login required)
GET  /api/user-profile    → JSON user data for JS
POST /api/log-weight      → Log weight entry
GET  /api/weight-history  → JSON weight log for chart
```

---

## Phase 8 — Email Integration (Flask-Mail)

```python
# config.py
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Send on register
def send_welcome_email(user):
    msg = Message(
        subject=f"Welcome to FitLife, {user.full_name}!",
        recipients=[user.email],
        body=f"Hi {user.full_name}, welcome to FitLife! Your goal: {user.goal}."
    )
    mail.send(msg)
```

---

## Phase 9 — Security Checklist

- [ ] Passwords hashed with `Flask-Bcrypt` (never store plain text)
- [ ] CSRF protection via `Flask-WTF`
- [ ] `@login_required` on all dashboard routes
- [ ] Input validation server-side (email format, age range, etc.)
- [ ] SQL injection safe via SQLAlchemy ORM
- [ ] `.env` file in `.gitignore`
- [ ] Session timeout configured

---

## Phase 10 — Development Order (Build Sequence)

```
Week 1:
  Day 1–2  → Setup Flask app, DB, models, config
  Day 3–4  → Auth routes (register, login, logout)
  Day 5    → Welcome email integration + test

Week 2:
  Day 1–2  → Landing page HTML/CSS (Bootstrap)
  Day 3    → Login/Register modals + form validation
  Day 4–5  → Dashboard layout + Bootstrap tabs

Week 3:
  Day 1–2  → Content sections (workout, diet, exercises)
  Day 3    → Protein sources section
  Day 4    → BMI calculator (JS + Flask)
  Day 5    → Weight tracker + Chart.js graph

Week 4:
  Day 1–2  → Connect all frontend to Flask APIs (AJAX/fetch)
  Day 3    → Testing (auth, mail, DB, forms)
  Day 4    → Bug fixes + responsive check
  Day 5    → Final polish + deployment prep
```

---

## Phase 11 — Deployment (Optional)

**Free options:**
- **Backend:** Render.com or Railway.app (Flask)
- **Database:** Supabase (free PostgreSQL) or ElephantSQL
- **Email:** Gmail SMTP (free with app password)
- **Frontend:** Served via Flask (no separate hosting needed)

---

## Summary — Feature Checklist

| Feature | Status |
|---|---|
| User registration with full profile | ✅ Planned |
| User login / logout | ✅ Planned |
| Welcome email on register | ✅ Planned |
| BMI calculator | ✅ Planned |
| Workout plans (3 goals) | ✅ Planned |
| Diet plan — Vegetarian | ✅ Planned |
| Diet plan — Non-Vegetarian | ✅ Planned |
| Exercise library | ✅ Planned |
| Protein sources (veg + non-veg) | ✅ Planned |
| Weight progress tracker | ✅ Planned |
| Responsive mobile design | ✅ Planned |
| PostgreSQL database | ✅ Planned |
| Secure auth (bcrypt + sessions) | ✅ Planned |

---

*Built with Flask + PostgreSQL + Bootstrap 5 | FitLife Project Plan v1.0*
