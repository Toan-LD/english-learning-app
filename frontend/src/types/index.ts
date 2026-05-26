/**
 * Type definitions for the English Learning Platform.
 */

// User types
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  bio: string;
  avatar: string | null;
  learning_level: LearningLevel;
  daily_goal: number;
  streak_days: number;
  last_active_date: string | null;
  total_xp: number;
  is_notification_enabled: boolean;
  words_learned: number;
  courses_enrolled: number;
  created_at: string;
  updated_at: string;
}

export type LearningLevel = 'beginner' | 'intermediate' | 'advanced' | 'proficient';

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  learning_level: LearningLevel;
}

// Course types
export interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  thumbnail: string | null;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  is_published: boolean;
  total_lessons: number;
  estimated_hours: number;
  lesson_count: number;
  lessons?: Lesson[];
  created_at: string;
  updated_at?: string;
}

export interface Lesson {
  id: number;
  course: number;
  course_title?: string;
  title: string;
  slug: string;
  content: string;
  lesson_type: 'video' | 'reading' | 'quiz' | 'practice';
  order: number;
  duration_minutes: number;
  video_url: string;
  is_free: boolean;
  created_at: string;
}

// Vocabulary types
export interface Word {
  id: number;
  word: string;
  phonetic: string;
  part_of_speech: string;
  definition: string;
  example_sentence: string;
  example_sentence_vi: string;
  definition_vi: string;
  synonym: string;
  antonym: string;
  difficulty: 'basic' | 'intermediate' | 'advanced';
  image: string | null;
  audio_url: string;
}

export interface UserWord {
  id: number;
  user: number;
  word: Word;
  is_learned: boolean;
  review_status: 'new' | 'learning' | 'reviewing' | 'mastered';
  times_reviewed: number;
  correct_count: number;
  incorrect_count: number;
  accuracy: number;
  last_reviewed_at: string | null;
  next_review_at: string | null;
}

// Quiz types
export interface Quiz {
  id: number;
  title: string;
  description: string;
  quiz_type: 'multiple_choice' | 'fill_in_blank' | 'matching' | 'listening';
  lesson: number | null;
  time_limit: number;
  passing_score: number;
  is_active: boolean;
  question_count: number;
  questions?: Question[];
  created_at: string;
}

export interface Question {
  id: number;
  quiz: number;
  word: number | null;
  question_text: string;
  question_type: string;
  options: string[];
  points: number;
  order: number;
  correct_answer?: string;
  explanation?: string;
}

export interface QuizAttempt {
  id: number;
  user: number;
  quiz: number;
  quiz_title: string;
  score: number;
  total_questions: number;
  correct_answers: number;
  time_taken: number;
  status: 'in_progress' | 'completed' | 'abandoned';
  answers: Record<string, string>;
  percentage: number;
  started_at: string;
  completed_at: string | null;
}

export interface QuizSubmitResult {
  attempt: QuizAttempt;
  score: number;
  correct_answers: number;
  total_questions: number;
  xp_earned: number;
  passed: boolean;
  questions_review: Question[];
}

// Progress types
export interface UserProgress {
  id: number;
  user: number;
  course: number;
  course_title: string;
  course_slug: string;
  course_thumbnail: string | null;
  status: 'enrolled' | 'in_progress' | 'completed' | 'dropped';
  progress_percentage: number;
  total_time_spent: number;
  total_lessons: number;
  completed_lesson_count: number;
  enrolled_at: string;
  last_activity_at: string | null;
  completed_at: string | null;
}

export interface DailyActivity {
  id: number;
  user: number;
  date: string;
  minutes_studied: number;
  words_learned: number;
  lessons_completed: number;
  quizzes_taken: number;
  xp_earned: number;
}

export interface ProgressStats {
  total_courses_enrolled: number;
  courses_completed: number;
  total_words_learned: number;
  total_quizzes_taken: number;
  average_quiz_score: number;
  total_study_time: number;
  current_streak: number;
  total_xp: number;
  learning_level: LearningLevel;
  weekly_activity: DailyActivity[];
}

// API Response types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  [key: string]: string | string[] | undefined;
}
