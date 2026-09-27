import client from './client';

export const auth = {
  login: (data) => client.post('/auth/login', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),
  register: (data) => client.post('/auth/register', data),
};

export const profile = {
  getProfile: () => client.get('/profile'),
  updateProfile: (data) => client.put('/profile', data),
  getNutritionTargets: () => client.get('/profile/targets'),
};

export const mealPlan = {
  generatePlan: (date) => client.post('/meal-plan/generate', { date }),
  getTodayPlan: () => client.get('/meal-plan/today'),
  getWeeklyPlan: () => client.get('/meal-plan/weekly'),
  generateWeeklyPlan: () => client.post('/meal-plan/weekly/generate'),
  randomizeDay: (date) => client.post('/meal-plan/randomize', { date }),
  randomizeMeal: (mealType, date) => client.post('/meal-plan/randomize-meal', { mealType, date }),
  replaceMeal: (mealType, mealId, date) => client.post('/meal-plan/replace', { mealType, mealId, date }),
  getExplanation: (mealType, date) => client.get(`/meal-plan/explanation?mealType=${mealType}&date=${date}`),
};

export const meals = {
  listMeals: (params) => client.get('/meals', { params }),
  getMeal: (id) => client.get(`/meals/${id}`),
  getRecipe: (id) => client.get(`/meals/${id}/recipe`),
  getNutrition: (id) => client.get(`/meals/${id}/nutrition`),
  getVideo: (id) => client.get(`/meals/${id}/video`),
};

export const grocery = {
  getDailyGrocery: () => client.get('/grocery/daily'),
  getWeeklyGrocery: () => client.get('/grocery/weekly'),
};
