/**
 * Axios instance with JWT interceptors.
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - attach JWT token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const tokensStr = localStorage.getItem('tokens');
      if (tokensStr) {
        try {
          const tokens = JSON.parse(tokensStr);
          if (tokens.access) {
            config.headers.Authorization = `Bearer ${tokens.access}`;
          }
        } catch (e) {
          console.error('Failed to parse tokens', e);
        }
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried, try to refresh token
    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (typeof window !== 'undefined') {
        const tokensStr = localStorage.getItem('tokens');
        if (tokensStr) {
          try {
            const tokens = JSON.parse(tokensStr);
            const response = await axios.post(
              `${API_BASE_URL}/users/token/refresh/`,
              { refresh: tokens.refresh }
            );
            const newTokens = {
              access: response.data.access,
              refresh: response.data.refresh || tokens.refresh,
            };
            localStorage.setItem('tokens', JSON.stringify(newTokens));
            originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;
            return api(originalRequest);
          } catch (refreshError) {
            // Refresh failed, log out
            localStorage.removeItem('tokens');
            localStorage.removeItem('user');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;
