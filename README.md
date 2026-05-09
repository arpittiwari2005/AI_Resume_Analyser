<div align="center">

# 🤖 AI Resume Analyzer

**An intelligent full-stack web application that helps job seekers analyze resumes, detect skill gaps, generate cover letters, simulate mock interviews, and assess job fit — powered by NLP & AI.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Overview

**AI Resume Analyzer** bridges the gap between candidates and their dream jobs by providing smart, data-driven feedback on resumes. Users upload their resume, paste a job description, and instantly receive AI-powered insights to improve their job application.

---

## ✨ Features

- 📄 **Resume Upload & Parsing** — Supports PDF and DOCX; text is auto-extracted
- 🔍 **Resume–JD Match Scoring** — TF-IDF cosine similarity scoring (0–100%)
- 🧠 **Missing Skills Detection** — NLP gap analysis against 100+ known tech skills
- ✉️ **Cover Letter Generator** — AI-tailored cover letters from resume + job description
- 🎤 **Mock Interview Simulator** — Role-specific questions with scoring & feedback
- 📊 **Job Fit Analysis** — Detailed match report with actionable suggestions
- 🔐 **JWT Authentication** — Secure login, registration, and role-based access
- 🔑 **Password Reset** — Email-based secure password reset flow
- 📁 **Resume Versioning** — Track multiple resume iterations over time

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 14 (App Router), TypeScript, React 18, CSS Modules |
| **Backend** | FastAPI, SQLAlchemy, SQLite |
| **NLP / AI** | scikit-learn (TF-IDF + Cosine Similarity), spaCy (`en_core_web_sm`) |
| **Auth** | JWT (python-jose), Passlib (bcrypt) |
| **File Parsing** | PyPDF2, python-docx |
| **Email** | SMTP (for password reset) |

---

## 🗂️ Project Structure

```
AI_Resume_analyzer/
├── backend/                    # FastAPI Python backend
│   ├── main.py                 # App entry point & CORS config
│   ├── database.py             # SQLAlchemy engine & session
│   ├── models.py               # DB models: User, Resume, Job, Interview...
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── security.py             # JWT & password hashing
│   ├── routes/
│   │   ├── auth.py             # Register, login, password reset
│   │   ├── resume.py           # Upload, parse & score resumes
│   │   ├── interview.py        # Mock interview Q&A and scoring
│   │   ├── cover_letter.py     # Cover letter generation
│   │   └── job_fit.py          # Job fit analysis
│   └── services/
│       ├── nlp_service.py      # TF-IDF similarity & skill extraction
│       └── email_service.py    # SMTP email service
│
└── frontend/                   # Next.js TypeScript frontend
    └── src/app/
        ├── page.tsx            # Landing page
        ├── dashboard/          # User dashboard
        ├── login/              # Login page
        ├── register/           # Registration page
        ├── cover-letter/       # Cover letter tool
        ├── interview/          # Mock interview simulator
        ├── job-fit/            # Job fit analysis
        ├── forgot-password/    # Forgot password
        └── reset-password/     # Reset password
```

---

## ⚙️ Getting Started

### Prerequisites

- Python **3.9+**
- Node.js **18+** & npm

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI_Resume_analyzer.git
cd AI_Resume_analyzer
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# source venv/Scripts/activate    # Windows

# Install dependencies
pip install fastapi uvicorn sqlalchemy pyjwt passlib python-jose \
            PyPDF2 python-docx scikit-learn spacy python-multipart

# Download spaCy language model
python -m spacy download en_core_web_sm

# Start the server
uvicorn main:app --reload
```

> Backend runs at **http://localhost:8000** — Interactive docs at **http://localhost:8000/docs**

---

### 3. Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

> Frontend runs at **http://localhost:3000**

---

### 4. Environment Variables

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (for password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

---

## 🔗 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Login & receive JWT token |
| `POST` | `/api/auth/forgot-password` | Send reset email |
| `POST` | `/api/auth/reset-password` | Reset password via token |
| `POST` | `/api/resume/upload` | Upload & analyze a resume |
| `GET` | `/api/resume/list` | List user's resumes |
| `POST` | `/api/interview/generate` | Generate mock interview questions |
| `POST` | `/api/interview/submit` | Submit answers & get scored |
| `POST` | `/api/cover-letter/generate` | Generate tailored cover letter |
| `POST` | `/api/job-fit/analyze` | Run job fit analysis |

---

## 🧠 How It Works

### Resume–JD Matching
1. Resume text is extracted from uploaded PDF/DOCX
2. Both resume and job description are vectorized using **TF-IDF**
3. **Cosine similarity** measures alignment between the two documents
4. A percentage **match score** is returned

### Skill Gap Detection
1. A curated whitelist of **100+ technical skills** is maintained (languages, frameworks, cloud, tools)
2. The job description is scanned for matching skills
3. The resume is scanned for the same
4. Skills **in the JD but missing from the resume** are flagged

---

## 👥 User Roles

| Role | Access |
|---|---|
| 🎓 **Student** | Upload resumes, view scores, cover letters, mock interviews, job fit |
| 🛠️ **Admin** | Post job descriptions, view all applicant resumes and scores |

---
