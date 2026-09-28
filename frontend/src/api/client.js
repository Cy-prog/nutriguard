import axios from 'axios';

// Single source of truth for API configuration.
// VITE_API_URL should be the backend root (e.g. https://nutriguard-api.onrender.com)
// If empty/unset, uses relative paths so Vercel rewrites can proxy to backend.
const rawApiUrl = import.meta.env.VITE_API_URL;
const baseURL = rawApiUrl ? `${rawApiUrl.replace(/\/$/, '')}/api/v1` : '/api/v1';

const client = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token on every request
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 → clear token and redirect to login
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      // Only redirect if not already on login/register page
      if (!window.location.pathname.startsWith('/login') && !window.location.pathname.startsWith('/register')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default client;
