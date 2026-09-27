import React, { useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { profile } from '../api/endpoints';
import { NutritionProgress } from '../components/NutritionProgress';
import { LoadingSkeleton } from '../components/EmptyState';
import { Activity } from 'lucide-react';

export default function NutritionDashboard() {
  const targetApi = useApi(profile.getNutritionTargets);

  useEffect(() => {
    targetApi.execute();
  }, []);

  if (targetApi.loading || !targetApi.data) return <LoadingSkeleton count={3} />;
  
  const targets = targetApi.data;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="bg-white p-6 rounded-2xl border shadow-sm flex items-center space-x-4">
        <Activity className="w-8 h-8 text-brand-600" />
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Nutrition Targets</h1>
          <p className="text-gray-500">Your daily macronutrient goals</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-8 rounded-2xl border shadow-sm flex flex-col items-center">
          <h2 className="text-xl font-bold mb-6">Caloric Goal</h2>
          <NutritionProgress actual={targets.daily_calories} target={targets.daily_calories} label="Calories" color="text-brand-500" size={200} />
          <p className="text-gray-500 mt-4 text-center">Calculated based on your TDEE and goal.</p>
        </div>
        
        <div className="bg-white p-8 rounded-2xl border shadow-sm">
          <h2 className="text-xl font-bold mb-6 text-center">Macronutrients</h2>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-1"><span className="font-medium text-gray-700">Protein</span><span>{Math.round(targets.daily_protein_g)}g</span></div>
              <div className="w-full bg-gray-200 rounded-full h-3"><div className="bg-blue-500 h-3 rounded-full" style={{width: '100%'}}></div></div>
            </div>
            <div>
              <div className="flex justify-between mb-1"><span className="font-medium text-gray-700">Carbs</span><span>{Math.round(targets.daily_carbs_g)}g</span></div>
              <div className="w-full bg-gray-200 rounded-full h-3"><div className="bg-yellow-500 h-3 rounded-full" style={{width: '100%'}}></div></div>
            </div>
            <div>
              <div className="flex justify-between mb-1"><span className="font-medium text-gray-700">Fat</span><span>{Math.round(targets.daily_fat_g)}g</span></div>
              <div className="w-full bg-gray-200 rounded-full h-3"><div className="bg-red-500 h-3 rounded-full" style={{width: '100%'}}></div></div>
            </div>
            <div>
              <div className="flex justify-between mb-1"><span className="font-medium text-gray-700">Fiber</span><span>{Math.round(targets.daily_fiber_g || 25)}g</span></div>
              <div className="w-full bg-gray-200 rounded-full h-3"><div className="bg-green-500 h-3 rounded-full" style={{width: '100%'}}></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
