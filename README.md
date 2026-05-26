# English Learning Platform

A full-stack English learning application built with **Django REST Framework** (backend) and **React + TypeScript** (frontend), featuring vocabulary flashcards, quizzes, course management, and progress tracking.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### Run with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd english-learning-app

# Start all services
docker-compose up --build

# The application will be available at:
# Frontend: http://localhost
# Backend API: http://localhost:8000
# Swagger Docs: http://localhost:8000/swagger/
# Admin Panel: http://localhost:8000/admin/
```

### Seed Data

The database is automatically seeded with:
- **50 common English words** with definitions, phonetics, examples
- **3 sample courses** with 5 lessons each
- **Quizzes** for each course

## 📁 Project Structure

```
english-learning-app/
├── backend/                    # Django REST Framework
│   ├── english_platform/       # Project settings
│   ├── users/                  # User authentication & profiles
│   ├── courses/                # Course & lesson management
│   ├── vocabulary/             # Word bank & flashcards
│   ├── quiz/                   # Quiz system
│   ├── progress/               # Learning progress tracking
│   ├── seed_data/              # Database seed data
│   ├── tests/                  # Backend tests (pytest)
│   └── Dockerfile
├── frontend/                   # React + TypeScript
│   ├── src/
│   │   ├── api/                # Axios API layer
│   │   ├── components/         # Reusable components
│   │   ├── pages/              # Page components
│   │   ├── store/              # Redux Toolkit slices
│   │   ├── types/              # TypeScript definitions
│   │   └── utils/              # Utility functions
│   ├── nginx.conf              # Nginx configuration
│   └── Dockerfile
├── docker-compose.yml          # Service orchestration
├── knowledge.md                # Detailed documentation
└── README.md
```

## 🔧 Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations and seed
python manage.py migrate
python manage.py seed_db

# Start server
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm start
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📋 Features

- **JWT Authentication**: Secure login/register with token refresh
- **Course Management**: Browse courses, enroll, track lesson progress
- **Vocabulary Flashcards**: Flip card UI with pronunciation (Web Speech API)
- **Quiz System**: Multiple choice & fill-in-the-blank with instant grading
- **Progress Dashboard**: Charts showing study activity (Recharts)
- **XP & Streak System**: Gamification to encourage daily practice
- **Admin Panel**: Full CRUD via Django admin with customization
- **API Documentation**: Swagger/OpenAPI at `/swagger/`
- **Background Tasks**: Celery for daily reminders via Redis

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, DRF, PostgreSQL, Celery, Redis |
| Frontend | React 18, TypeScript, Redux Toolkit, TailwindCSS |
| Auth | JWT (djangorestframework-simplejwt) |
| Charts | Recharts |
| API Docs | drf-yasg (Swagger/OpenAPI) |
| Testing | pytest (backend), Jest + RTL (frontend) |
| Deployment | Docker, Nginx |

## 📝 License

MIT License
