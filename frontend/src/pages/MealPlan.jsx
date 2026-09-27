import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { mealPlan } from '../api/endpoints';
import { MealCard } from '../components/MealCard';
import { EmptyState, LoadingSkeleton } from '../components/EmptyState';
import { Calendar, Sparkles, RefreshCw } from 'lucide-react';

export default function MealPlan() {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const planApi = useApi(mealPlan.getTodayPlan);
  const generatePlanApi = useApi(mealPlan.generatePlan);

  useEffect(() => {
    planApi.execute();
  }, [date]);

  const handleGenerate = async () => {
    try {
      await generatePlanApi.execute(date);
      planApi.execute();
    } catch (e) {
      console.error("Failed to generate plan:", e);
    }
  };

  const mealsList = planApi.data?.meals || planApi.data?.items || [];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row justify-between sm:items-center bg-white p-6 rounded-2xl border border-slate-200 shadow-sm gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Today's Meal Plan</h1>
          <p className="text-slate-500 text-sm mt-1">Planned Indian meals optimized for your glycemic index and macro targets.</p>
        </div>
        
        <div className="flex items-center gap-3">
          <input 
            type="date" 
            value={date} 
            onChange={(e) => setDate(e.target.value)} 
            className="border border-slate-200 bg-slate-50 rounded-xl px-3.5 py-2 text-sm focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          />
          <button
            onClick={handleGenerate}
            disabled={generatePlanApi.loading}
            className="inline-flex items-center px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-semibold shadow-xs transition"
          >
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            {generatePlanApi.loading ? 'Generating...' : 'Regenerate'}
          </button>
        </div>
      </div>

      {planApi.loading ? (
        <LoadingSkeleton count={3} />
      ) : mealsList.length > 0 ? (
        <div className="space-y-8">
          {mealsList.map((item, idx) => (
            <div key={idx} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <div className="flex items-center justify-between mb-4 border-b pb-3">
                <h2 className="text-lg font-bold text-slate-900 capitalize">
                  {item.meal_type ? item.meal_type.toLowerCase() : `Meal ${idx + 1}`}
                </h2>
                {item.meal?.calories && (
                  <span className="text-xs text-slate-500 font-medium">
                    Target: ~{Math.round(item.meal.calories)} kcal
                  </span>
                )}
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <MealCard meal={item.meal || item} />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 shadow-sm">
          <EmptyState 
            icon={Calendar} 
            title="No Meal Plan for this Date" 
            description="Generate a fresh, balanced Indian daily meal plan tailored to your nutritional targets." 
            actionText="Generate Daily Plan"
            onAction={handleGenerate}
          />
        </div>
      )}
    </div>
  );
}
