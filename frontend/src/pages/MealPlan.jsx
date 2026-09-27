import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { mealPlan } from '../api/endpoints';
import { MealCard } from '../components/MealCard';
import { EmptyState, LoadingSkeleton } from '../components/EmptyState';
import { Calendar } from 'lucide-react';

export default function MealPlan() {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const planApi = useApi(mealPlan.getTodayPlan); // Assuming backend supports date query or we use getTodayPlan for now

  useEffect(() => {
    planApi.execute();
  }, [date]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white p-6 rounded-2xl border shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Meal Plan</h1>
          <p className="text-gray-500">Your planned meals for {date}</p>
        </div>
        <input 
          type="date" 
          value={date} 
          onChange={(e) => setDate(e.target.value)} 
          className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-brand-500 focus:border-brand-500"
        />
      </div>

      {planApi.loading ? (
        <LoadingSkeleton count={3} />
      ) : planApi.data ? (
        <div className="space-y-8">
          {planApi.data.meals.map((item, idx) => (
            <div key={idx} className="bg-white rounded-xl border p-6">
              <h2 className="text-xl font-bold mb-4 capitalize">{item.meal_type.toLowerCase()}</h2>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <MealCard meal={item.meal} />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border p-12">
          <EmptyState icon={Calendar} title="No Plan Found" description="There is no meal plan generated for this date." />
        </div>
      )}
    </div>
  );
}
