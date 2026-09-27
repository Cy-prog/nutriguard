import React, { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthContext } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';

// Public & Auth Pages
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';

// Authenticated Application Pages
import Dashboard from './pages/Dashboard';
import AIAssistant from './pages/AIAssistant';
import MealPlan from './pages/MealPlan';
import WeeklyPlan from './pages/WeeklyPlan';
import ExploreMeals from './pages/ExploreMeals';
import MealDetail from './pages/MealDetail';
import FoodDatabase from './pages/FoodDatabase';
import Favorites from './pages/Favorites';
import NutritionDashboard from './pages/NutritionDashboard';
import GroceryList from './pages/GroceryList';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import AdminDashboard from './pages/AdminDashboard';
import SystemHealth from './pages/SystemHealth';

function RootRoute() {
  const { user, loading } = useContext(AuthContext);
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-500 font-medium">
        Loading NutriGuard...
      </div>
    );
  }
  return user ? <Navigate to="/dashboard" replace /> : <LandingPage />;
}

function App() {
  return (
    <Routes>
      {/* Public Landing & Marketing */}
      <Route path="/" element={<RootRoute />} />
      <Route path="/welcome" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/onboarding" element={<ProtectedRoute><Onboarding /></ProtectedRoute>} />
      
      {/* Protected Main Workspace */}
      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/assistant" element={<AIAssistant />} />
        <Route path="/meal-plan" element={<MealPlan />} />
        <Route path="/meal-plan/weekly" element={<WeeklyPlan />} />
        <Route path="/meals" element={<ExploreMeals />} />
        <Route path="/meals/:mealId" element={<MealDetail />} />
        <Route path="/foods" element={<FoodDatabase />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/nutrition" element={<NutritionDashboard />} />
        <Route path="/grocery" element={<GroceryList />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/system-health" element={<SystemHealth />} />
      </Route>

      {/* Catch-all redirect */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
