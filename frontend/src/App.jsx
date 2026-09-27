import { Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
// Lazy load pages for now by importing them as basic components or defining them if they don't exist yet
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';
import MealPlan from './pages/MealPlan';
import WeeklyPlan from './pages/WeeklyPlan';
import MealDetail from './pages/MealDetail';
import ExploreMeals from './pages/ExploreMeals';
import NutritionDashboard from './pages/NutritionDashboard';
import GroceryList from './pages/GroceryList';
import Profile from './pages/Profile';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/onboarding" element={<ProtectedRoute><Onboarding /></ProtectedRoute>} />
      
      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/meal-plan" element={<MealPlan />} />
        <Route path="/meal-plan/weekly" element={<WeeklyPlan />} />
        <Route path="/meals" element={<ExploreMeals />} />
        <Route path="/meals/:mealId" element={<MealDetail />} />
        <Route path="/nutrition" element={<NutritionDashboard />} />
        <Route path="/grocery" element={<GroceryList />} />
        <Route path="/profile" element={<Profile />} />
      </Route>
    </Routes>
  );
}

export default App;
