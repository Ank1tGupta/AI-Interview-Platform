# 🚀 AI Interview Platform

An AI-powered recruitment automation platform built with Django + React.

## 🔥 Features

- Recruiter authentication (JWT)
- Create interview sessions
- Secure token-based candidate access
- AI-generated interview questions
- AI-powered answer evaluation (Gemini API)
- Automatic scoring system
- Recruiter dashboard with reports
- Email-based interview invitations

## 🛠 Tech Stack

Backend:
- Django
- Django REST Framework
- JWT Authentication
- Google Gemini API

Frontend:
- React
- Tailwind CSS
- Axios

## ⚙️ Setup

Backend:

```bash
cd Backend_Enviroment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then fill in GEMINI_API_KEY
python manage.py migrate
python manage.py runserver
```

Frontend:

```bash
cd frontend
npm install
cp .env.example .env        # VITE_API_URL=http://localhost:8000
npm run dev
```

Run the backend tests with `python manage.py test`.

## 🌐 Deployment

The backend serves its API under `/api/`, and the frontend adds that prefix
itself — so `VITE_API_URL` is the backend **origin** only
(`https://your-api.onrender.com`), with no `/api` suffix.

Required backend environment variables in production:

| Variable | Notes |
|---|---|
| `DJANGO_SECRET_KEY` | Required. Startup fails without it when `DJANGO_DEBUG` is not `True`. |
| `DJANGO_DEBUG` | Leave unset in production. |
| `ALLOWED_HOSTS` | Comma-separated. Render's own hostname is added automatically. |
| `FRONTEND_URL` | SPA origin. Used for the interview links emailed to candidates. |
| `CORS_ALLOWED_ORIGINS` | Comma-separated. Defaults to `FRONTEND_URL`. |
| `DATABASE_URL` | Required. Without it the app falls back to sqlite, which is wiped on every deploy. |
| `GEMINI_API_KEY` | Required for question generation and scoring. |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | Omit to log invitation emails to the console instead of sending them. |

## 🧠 How It Works

1. Recruiter creates interview
2. Candidate receives email link
3. Candidate completes interview
4. AI evaluates answers
5. Recruiter views detailed report
