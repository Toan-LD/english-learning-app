/**
 * API endpoint functions.
 */
import api from './axios';
import type {
  LoginRequest,
  RegisterRequest,
  User,
  Course,
  Lesson,
  Word,
  UserWord,
  Quiz,
  QuizAttempt,
  QuizSubmitResult,
  UserProgress,
  DailyActivity,
  ProgressStats,
  PaginatedResponse,
} from '../types';

// Auth endpoints
export const authAPI = {
  login: (data: LoginRequest) =>
    api.post('/users/login/', data),

  register: (data: RegisterRequest) =>
    api.post('/users/register/', data),

  logout: (refresh: string) =>
    api.post('/users/logout/', { refresh }),

  getProfile: () =>
    api.get<User>('/users/profile/'),

  updateProfile: (data: Partial<User>) =>
    api.patch<User>('/users/profile/', data),

  changePassword: (data: { old_password: string; new_password: string; new_password_confirm: string }) =>
    api.post('/users/change-password/', data),

  getStats: () =>
    api.get('/users/stats/'),
};

// Course endpoints
export const coursesAPI = {
  list: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<Course>>('/courses/', { params }),

  detail: (slug: string) =>
    api.get<Course>(`/courses/${slug}/`),

  lessons: (slug: string) =>
    api.get<Lesson[]>(`/courses/${slug}/lessons/`),

  lessonDetail: (id: number) =>
    api.get<Lesson>(`/courses/lessons/${id}/`),
};

// Vocabulary endpoints
export const vocabularyAPI = {
  listWords: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<Word>>('/vocabulary/words/', { params }),

  wordDetail: (id: number) =>
    api.get<Word>(`/vocabulary/words/${id}/`),

  randomWords: (count: number = 10, difficulty?: string) =>
    api.get<Word[]>('/vocabulary/words/random/', { params: { count, difficulty } }),

  markLearned: (id: number) =>
    api.post(`/vocabulary/words/${id}/mark_learned/`),

  listUserWords: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<UserWord>>('/vocabulary/user-words/', { params }),

  reviewWord: (id: number, isCorrect: boolean) =>
    api.post(`/vocabulary/user-words/${id}/review/`, { is_correct: isCorrect }),
};

// Quiz endpoints
export const quizAPI = {
  list: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<Quiz>>('/quiz/', { params }),

  detail: (id: number) =>
    api.get<Quiz>(`/quiz/${id}/`),

  start: (id: number) =>
    api.post<QuizAttempt>(`/quiz/${id}/start/`),

  submit: (id: number, data: { answers: Record<string, string>; time_taken: number }) =>
    api.post<QuizSubmitResult>(`/quiz/${id}/submit/`, data),

  listAttempts: () =>
    api.get<PaginatedResponse<QuizAttempt>>('/quiz/attempts/'),
};

// Progress endpoints
export const progressAPI = {
  list: () =>
    api.get<PaginatedResponse<UserProgress>>('/progress/'),

  enroll: (courseId: number) =>
    api.post('/progress/', { course: courseId }),

  completeLesson: (progressId: number, lessonId: number) =>
    api.post(`/progress/${progressId}/complete_lesson/`, { lesson_id: lessonId }),

  logTime: (progressId: number, minutes: number) =>
    api.post(`/progress/${progressId}/log_time/`, { minutes }),

  getStats: () =>
    api.get<ProgressStats>('/progress/stats/'),

  getActivities: (params?: Record<string, string>) =>
    api.get<PaginatedResponse<DailyActivity>>('/progress/activities/', { params }),
};
