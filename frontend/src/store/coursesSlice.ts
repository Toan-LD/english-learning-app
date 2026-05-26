/**
 * Courses Redux slice.
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { coursesAPI } from '../api/endpoints';
import type { Course, Lesson, PaginatedResponse } from '../types';

interface CoursesState {
  courses: Course[];
  currentCourse: Course | null;
  currentLesson: Lesson | null;
  lessons: Lesson[];
  loading: boolean;
  error: string | null;
  totalCount: number;
}

const initialState: CoursesState = {
  courses: [],
  currentCourse: null,
  currentLesson: null,
  lessons: [],
  loading: false,
  error: null,
  totalCount: 0,
};

export const fetchCourses = createAsyncThunk(
  'courses/fetchCourses',
  async (params: Record<string, string> | undefined, { rejectWithValue }) => {
    try {
      const response = await coursesAPI.list(params);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch courses');
    }
  }
);

export const fetchCourseDetail = createAsyncThunk(
  'courses/fetchCourseDetail',
  async (slug: string, { rejectWithValue }) => {
    try {
      const response = await coursesAPI.detail(slug);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch course');
    }
  }
);

export const fetchCourseLessons = createAsyncThunk(
  'courses/fetchCourseLessons',
  async (slug: string, { rejectWithValue }) => {
    try {
      const response = await coursesAPI.lessons(slug);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch lessons');
    }
  }
);

export const fetchLessonDetail = createAsyncThunk(
  'courses/fetchLessonDetail',
  async (id: number, { rejectWithValue }) => {
    try {
      const response = await coursesAPI.lessonDetail(id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch lesson');
    }
  }
);

const coursesSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {
    clearCurrentCourse: (state) => {
      state.currentCourse = null;
      state.lessons = [];
    },
    clearCurrentLesson: (state) => {
      state.currentLesson = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch courses
    builder
      .addCase(fetchCourses.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCourses.fulfilled, (state, action: PayloadAction<PaginatedResponse<Course>>) => {
        state.loading = false;
        state.courses = action.payload.results;
        state.totalCount = action.payload.count;
      })
      .addCase(fetchCourses.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Fetch course detail
    builder
      .addCase(fetchCourseDetail.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchCourseDetail.fulfilled, (state, action: PayloadAction<Course>) => {
        state.loading = false;
        state.currentCourse = action.payload;
      })
      .addCase(fetchCourseDetail.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Fetch course lessons
    builder
      .addCase(fetchCourseLessons.fulfilled, (state, action: PayloadAction<Lesson[]>) => {
        state.lessons = action.payload;
      });

    // Fetch lesson detail
    builder
      .addCase(fetchLessonDetail.fulfilled, (state, action: PayloadAction<Lesson>) => {
        state.currentLesson = action.payload;
      });
  },
});

export const { clearCurrentCourse, clearCurrentLesson } = coursesSlice.actions;
export default coursesSlice.reducer;
