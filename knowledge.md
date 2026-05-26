# English Learning Platform - System Architecture & Documentation

## 1. System Architecture Overview

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   React App     │────▶│   Nginx      │────▶│   Django    │
│   (TypeScript)  │     │   (Proxy)    │     │   REST API  │
└─────────────────┘     └──────────────┘     └──────┬──────┘
                                                     │
                    ┌────────────────────────────────┼────────────┐
                    │                                │            │
              ┌─────▼─────┐                  ┌──────▼─────┐ ┌───▼────┐
              │ PostgreSQL │                  │   Redis    │ │ Celery │
              │  Database  │                  │  (Cache)   │ │ Worker │
              └────────────┘                  └────────────┘ └────────┘
```

### Components

| Service | Technology | Port | Purpose |
|---------|-----------|------|---------|
| Frontend | React 18 + TypeScript + Nginx | 80 | User interface |
| Backend | Django 4.2 + DRF | 8000 | REST API server |
| Database | PostgreSQL 15 | 5432 | Data persistence |
| Cache/Broker | Redis 7 | 6379 | Caching & task broker |
| Celery Worker | Celery 5.3 | - | Background tasks |
| Celery Beat | Celery Beat | - | Scheduled tasks |

## 2. Database Schema

### Users App
- **User**: Custom user model extending AbstractUser
  - Fields: email (unique), username, learning_level, daily_goal, streak_days, total_xp

### Courses App
- **Course**: title, slug, description, difficulty, estimated_hours, is_published
- **Lesson**: FK→Course, title, slug, content (HTML), lesson_type, order, duration_minutes

### Vocabulary App
- **Word**: word (unique), phonetic, part_of_speech, definition, example_sentence, difficulty
- **UserWord**: FK→User, FK→Word, is_learned, review_status, times_reviewed, correct_count

### Quiz App
- **Quiz**: title, quiz_type, time_limit, passing_score
- **Question**: FK→Quiz, question_text, options (JSON), correct_answer, points
- **QuizAttempt**: FK→User, FK→Quiz, score, answers (JSON), status

### Progress App
- **UserProgress**: FK→User, FK→Course, status, progress_percentage, completed_lessons (M2M)
- **DailyActivity**: FK→User, date, minutes_studied, words_learned, xp_earned

## 3. API Endpoints

### Authentication (`/api/users/`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register/` | Create new account | No |
| POST | `/login/` | Login, get JWT tokens | No |
| POST | `/logout/` | Blacklist refresh token | Yes |
| POST | `/token/refresh/` | Refresh access token | No |
| GET/PATCH | `/profile/` | Get/update user profile | Yes |
| POST | `/change-password/` | Change password | Yes |
| GET | `/stats/` | User statistics | Yes |

### Courses (`/api/courses/`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List all courses | Yes |
| GET | `/{slug}/` | Get course detail | Yes |
| POST | `/` | Create course | Yes |
| GET | `/{slug}/lessons/` | List course lessons | Yes |
| CRUD | `/lessons/` | Manage lessons | Yes |

### Vocabulary (`/api/vocabulary/`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/words/` | List words (filterable) | Yes |
| GET | `/words/{id}/` | Get word detail | Yes |
| GET | `/words/random/` | Get random flashcard words | Yes |
| POST | `/words/{id}/mark_learned/` | Mark word as learned (+5 XP) | Yes |
| GET | `/user-words/` | List user's words | Yes |
| POST | `/user-words/{id}/review/` | Record word review | Yes |

### Quiz (`/api/quiz/`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List quizzes | Yes |
| GET | `/{id}/` | Get quiz with questions | Yes |
| POST | `/{id}/start/` | Start quiz attempt | Yes |
| POST | `/{id}/submit/` | Submit answers, get score | Yes |
| GET | `/attempts/` | View attempt history | Yes |

### Progress (`/api/progress/`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List user course progress | Yes |
| POST | `/` | Enroll in course | Yes |
| POST | `/{id}/complete_lesson/` | Mark lesson complete | Yes |
| POST | `/{id}/log_time/` | Log study time | Yes |
| GET | `/stats/` | Comprehensive statistics | Yes |
| GET | `/activities/` | Daily activity history | Yes |

## 4. Frontend Architecture

### State Management (Redux Toolkit)
- **authSlice**: User auth state, tokens, login/register/logout
- **coursesSlice**: Course list, current course, lessons
- **vocabularySlice**: Words, flashcards, user words
- **progressSlice**: Course progress, stats, activities

### Pages
| Page | Route | Description |
|------|-------|-------------|
| Login | `/login` | Email/password login form |
| Register | `/register` | Account creation with level selection |
| Dashboard | `/` | Stats overview with Recharts |
| CourseList | `/courses` | Browse all courses |
| CourseDetail | `/courses/:slug` | Course content and enrollment |
| LessonView | `/lessons/:id` | Lesson content with TTS |
| VocabularyFlashcard | `/vocabulary` | Flip cards with pronunciation |
| Quiz | `/quiz` | Multiple choice & fill-in-blank |
| Profile | `/profile` | User settings and progress |

### Key Components
- **Layout/Navbar**: Navigation with XP and streak display
- **Flashcard**: 3D CSS flip animation, Web Speech API integration
- **Quiz**: Multiple choice with progress bar and review mode
- **ProgressChart**: Recharts BarChart for weekly activity

## 5. Authentication Flow

```
1. User enters credentials → POST /api/users/login/
2. Server returns { access, refresh } JWT tokens
3. Frontend stores tokens in localStorage
4. Axios interceptor attaches Bearer token to all requests
5. On 401 response → automatic token refresh via /token/refresh/
6. If refresh fails → redirect to login page
7. Logout → POST /api/users/logout/ (blacklist refresh token)
```

## 6. Spaced Repetition Algorithm

The vocabulary review system uses a simplified spaced repetition:

- Review intervals: 1, 3, 7, 14, 30 days
- Status progression: NEW → LEARNING → REVIEWING → MASTERED
- Mastery criteria: ≥80% accuracy AND ≥5 reviews
- XP rewards: +5 for marking learned, +3 for mastering a word

## 7. XP & Gamification

| Action | XP Earned |
|--------|-----------|
| Mark word as learned | +5 XP |
| Master a word (80%+ accuracy, 5+ reviews) | +3 XP |
| Complete a lesson | +10 XP |
| Complete a quiz | Score/10 + correct × 2 |
| Complete a course | +50 XP |

## 8. Setup & Deployment

### Development
```bash
docker-compose up --build
```

### Production Checklist
1. Set `DEBUG=False` in backend settings
2. Generate a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Set up proper SSL/TLS
5. Use managed PostgreSQL (RDS/Cloud SQL)
6. Configure Redis with authentication
7. Set up proper CORS origins
8. Enable Django security middleware
9. Configure media file storage (S3/GCS)
10. Set up monitoring (Sentry, CloudWatch)

## 9. Testing Summary

### Backend Tests (pytest) - 20+ tests
- **test_users.py**: Registration, login, profile CRUD, model tests
- **test_courses.py**: Course listing, creation, search, lesson CRUD
- **test_vocabulary.py**: Word CRUD, mark learned, review, accuracy calc
- **test_quiz.py**: Quiz listing, start, submit correct/wrong answers

### Frontend Tests (Jest + RTL) - 9+ tests
- **App.test.tsx**: Rendering, login form, navigation links
- **store.test.ts**: Redux store initialization, slice state verification

## 10. Environment Variables

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=english_platform
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_NAME=English Learning Platform
```
