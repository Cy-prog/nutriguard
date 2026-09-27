import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { mealPlan } from '../api/endpoints';
import { NutritionProgress } from '../components/NutritionProgress';
import { MealCard } from '../components/MealCard';
import { EmptyState, LoadingSkeleton } from '../components/EmptyState';
import { Calendar, RefreshCw, PlusCircle } from 'lucide-react';
import { useApi } from '../hooks/useApi';

export default function Dashboard() {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const todayPlanApi = useApi(mealPlan.getTodayPlan);
  const generatePlanApi = useApi(mealPlan.generatePlan);
  const [plan, setPlan] = useState(null);

  useEffect(() => {
    fetchPlan();
  }, []);

  const fetchPlan = async () => {
    try {
      const data = await todayPlanApi.execute();
      setPlan(data);
    } catch (e) {
      if (e.response?.status === 404) setPlan(null);
    }
  };

  const handleGenerate = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const data = await generatePlanApi.execute(today);
      setPlan(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-6 rounded-2xl border shadow-sm flex flex-col md:flex-row items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Good Morning, {user?.name}! 👋</h1>
          <p className="text-gray-500 mt-1">Here's your nutrition overview for today.</p>
        </div>
        <div className="mt-4 md:mt-0 flex gap-4">
          <button onClick={() => navigate('/meal-plan')} className="px-4 py-2 bg-brand-50 text-brand-600 rounded-lg font-medium">View Full Plan</button>
        </div>
      </div>

      {todayPlanApi.loading ? (
        <LoadingSkeleton count={2} />
      ) : plan ? (
        <>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="bg-white p-4 rounded-xl border flex flex-col items-center">
              <NutritionProgress actual={plan.total_calories || plan.actual_calories || 0} target={plan.target_calories || 2000} label="Calories" color="text-brand-500" />
            </div>
            <div className="bg-white p-4 rounded-xl border flex flex-col items-center">
              <NutritionProgress actual={plan.total_protein || plan.actual_protein_g || 0} target={plan.target_protein || plan.target_protein_g || 120} label="Protein (g)" color="text-blue-500" />
            </div>
            <div className="bg-white p-4 rounded-xl border flex flex-col items-center">
              <NutritionProgress actual={plan.total_carbs || plan.actual_carbs_g || 0} target={plan.target_carbs || plan.target_carbs_g || 250} label="Carbs (g)" color="text-yellow-500" />
            </div>
            <div className="bg-white p-4 rounded-xl border flex flex-col items-center">
              <NutritionProgress actual={plan.total_fat || plan.actual_fat_g || 0} target={plan.target_fat || plan.target_fat_g || 65} label="Fat (g)" color="text-red-500" />
            </div>
            <div className="bg-white p-4 rounded-xl border flex flex-col items-center justify-center">
               <div className="text-center">
                 <div className="text-2xl font-bold text-gray-900">{Math.round(plan.health_score || plan.overall_score || plan.nutrition_score || 85)}/100</div>
                 <div className="text-sm text-gray-500">Health Score</div>
               </div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900">Today's Meals</h2>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              {(plan.meals || plan.items || []).map((item, idx) => (
                <MealCard key={item.id || item.meal_id || idx} meal={item.meal || item} />
              ))}
            </div>
          </div>
        </>
      ) : (
        <div className="bg-white rounded-2xl border p-12">
          <EmptyState 
            icon={Calendar} 
            title="No Meal Plan for Today" 
            description="Generate a personalized meal plan based on your goals and preferences."
            actionText="Generate Plan"
            onAction={handleGenerate}
          />
        </div>
      )}
    </div>
  );
}
