/**
 * Progress Redux slice.
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { progressAPI } from '../api/endpoints';
import type { UserProgress, ProgressStats, PaginatedResponse } from '../types';

interface ProgressState {
  progresses: UserProgress[];
  stats: ProgressStats | null;
  loading: boolean;
  error: string | null;
}

const initialState: ProgressState = {
  progresses: [],
  stats: null,
  loading: false,
  error: null,
};

export const fetchProgresses = createAsyncThunk(
  'progress/fetchProgresses',
  async (_, { rejectWithValue }) => {
    try {
      const response = await progressAPI.list();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch progress');
    }
  }
);

export const fetchStats = createAsyncThunk(
  'progress/fetchStats',
  async (_, { rejectWithValue }) => {
    try {
      const response = await progressAPI.getStats();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch stats');
    }
  }
);

export const enrollCourse = createAsyncThunk(
  'progress/enrollCourse',
  async (courseId: number, { rejectWithValue }) => {
    try {
      const response = await progressAPI.enroll(courseId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to enroll');
    }
  }
);

export const completeLesson = createAsyncThunk(
  'progress/completeLesson',
  async ({ progressId, lessonId }: { progressId: number; lessonId: number }, { rejectWithValue }) => {
    try {
      const response = await progressAPI.completeLesson(progressId, lessonId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to complete lesson');
    }
  }
);

const progressSlice = createSlice({
  name: 'progress',
  initialState,
  reducers: {
    clearStats: (state) => {
      state.stats = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch progresses
    builder
      .addCase(fetchProgresses.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchProgresses.fulfilled, (state, action: PayloadAction<PaginatedResponse<UserProgress>>) => {
        state.loading = false;
        state.progresses = action.payload.results;
      })
      .addCase(fetchProgresses.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Fetch stats
    builder
      .addCase(fetchStats.fulfilled, (state, action: PayloadAction<ProgressStats>) => {
        state.stats = action.payload;
      });

    // Enroll course
    builder
      .addCase(enrollCourse.fulfilled, (state, action: PayloadAction<UserProgress>) => {
        state.progresses.push(action.payload);
      });

    // Complete lesson
    builder
      .addCase(completeLesson.fulfilled, (state, action: PayloadAction<UserProgress>) => {
        const index = state.progresses.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.progresses[index] = action.payload;
        }
      });
  },
});

export const { clearStats } = progressSlice.actions;
export default progressSlice.reducer;
