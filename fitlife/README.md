# FitLife — Health & Fitness Web App

Full-stack health and fitness platform built with Flask, PostgreSQL, Bootstrap 5, and Flask-Mail.

## Quick Start

### 1. Create virtual environment

```bash
cd fitlife
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill in your values:

```
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:pass@localhost/fitlife_db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_gmail_app_password
FLASK_APP=run.py
```

Create the PostgreSQL database:

```sql
CREATE DATABASE fitlife_db;
```

### 4. Run migrations

```bash
set FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the app

```bash
flask run
```

Open http://127.0.0.1:5000

## Features

- User registration & login (bcrypt + Flask-Login)
- Welcome email on signup (Flask-Mail / Gmail SMTP)
- Single-page dashboard with 6 Bootstrap tabs
- BMI calculator, workout & diet plans, exercise library
- Protein source tables, weight tracker with Chart.js

## Project Structure

```
fitlife/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── utils.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── content.py
│   │   └── content_data.py
│   ├── templates/
│   └── static/
├── config.py
├── requirements.txt
└── run.py
```
