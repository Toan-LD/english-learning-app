/**
 * Vocabulary Redux slice.
 */
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { vocabularyAPI } from '../api/endpoints';
import type { Word, UserWord, PaginatedResponse } from '../types';

interface VocabularyState {
  words: Word[];
  flashcardWords: Word[];
  userWords: UserWord[];
  loading: boolean;
  error: string | null;
}

const initialState: VocabularyState = {
  words: [],
  flashcardWords: [],
  userWords: [],
  loading: false,
  error: null,
};

export const fetchWords = createAsyncThunk(
  'vocabulary/fetchWords',
  async (params: Record<string, string> | undefined, { rejectWithValue }) => {
    try {
      const response = await vocabularyAPI.listWords(params);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch words');
    }
  }
);

export const fetchRandomWords = createAsyncThunk(
  'vocabulary/fetchRandomWords',
  async ({ count, difficulty }: { count: number; difficulty?: string }, { rejectWithValue }) => {
    try {
      const response = await vocabularyAPI.randomWords(count, difficulty);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch words');
    }
  }
);

export const fetchUserWords = createAsyncThunk(
  'vocabulary/fetchUserWords',
  async (params: Record<string, string> | undefined, { rejectWithValue }) => {
    try {
      const response = await vocabularyAPI.listUserWords(params);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch user words');
    }
  }
);

export const markWordLearned = createAsyncThunk(
  'vocabulary/markWordLearned',
  async (wordId: number, { rejectWithValue }) => {
    try {
      await vocabularyAPI.markLearned(wordId);
      return wordId;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to mark word');
    }
  }
);

const vocabularySlice = createSlice({
  name: 'vocabulary',
  initialState,
  reducers: {
    clearFlashcards: (state) => {
      state.flashcardWords = [];
    },
  },
  extraReducers: (builder) => {
    // Fetch words
    builder
      .addCase(fetchWords.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchWords.fulfilled, (state, action: PayloadAction<PaginatedResponse<Word>>) => {
        state.loading = false;
        state.words = action.payload.results;
      })
      .addCase(fetchWords.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Fetch random words for flashcards
    builder
      .addCase(fetchRandomWords.fulfilled, (state, action: PayloadAction<Word[]>) => {
        state.flashcardWords = action.payload;
      });

    // Fetch user words
    builder
      .addCase(fetchUserWords.fulfilled, (state, action: PayloadAction<PaginatedResponse<UserWord>>) => {
        state.userWords = action.payload.results;
      });
  },
});

export const { clearFlashcards } = vocabularySlice.actions;
export default vocabularySlice.reducer;
