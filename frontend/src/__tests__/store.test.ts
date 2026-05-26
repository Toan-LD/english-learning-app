import { store } from '../store';

describe('Redux Store', () => {
  test('store has correct initial state', () => {
    const state = store.getState();
    expect(state).toHaveProperty('auth');
    expect(state).toHaveProperty('courses');
    expect(state).toHaveProperty('vocabulary');
    expect(state).toHaveProperty('progress');
  });

  test('auth slice has correct initial state', () => {
    const state = store.getState();
    expect(state.auth).toHaveProperty('user');
    expect(state.auth).toHaveProperty('tokens');
    expect(state.auth).toHaveProperty('isAuthenticated');
    expect(state.auth).toHaveProperty('loading');
    expect(state.auth).toHaveProperty('error');
  });

  test('courses slice has correct initial state', () => {
    const state = store.getState();
    expect(state.courses.courses).toEqual([]);
    expect(state.courses.currentCourse).toBeNull();
    expect(state.courses.loading).toBe(false);
  });

  test('vocabulary slice has correct initial state', () => {
    const state = store.getState();
    expect(state.vocabulary.words).toEqual([]);
    expect(state.vocabulary.flashcardWords).toEqual([]);
    expect(state.vocabulary.loading).toBe(false);
  });

  test('progress slice has correct initial state', () => {
    const state = store.getState();
    expect(state.progress.progresses).toEqual([]);
    expect(state.progress.stats).toBeNull();
    expect(state.progress.loading).toBe(false);
  });
});
