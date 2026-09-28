import client from './client';

// NOTE: client.js baseURL already includes /api/v1.
// All paths here must be relative to that (e.g. '/auth/login', NOT '/api/v1/auth/login').

export const authApi = {
  login: async (formData) => {
    const { data } = await client.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return data;
  }
};

export const chatApi = {
  foodChat: async (req) => {
    const { data } = await client.post('/chat/food', req);
    return data;
  }
};

export const recommendationsApi = {
  evaluateFood: async (foodId, context) => {
    const { data } = await client.post(`/recommendations/evaluate/${foodId}`, context);
    return data;
  }
};
