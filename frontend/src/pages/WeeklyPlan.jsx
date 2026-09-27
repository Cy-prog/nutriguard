import React, { useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { mealPlan } from '../api/endpoints';
import { EmptyState, LoadingSkeleton } from '../components/EmptyState';
import { CalendarRange } from 'lucide-react';

export default function WeeklyPlan() {
  const weeklyApi = useApi(mealPlan.getWeeklyPlan);
  const generateApi = useApi(mealPlan.generateWeeklyPlan);

  useEffect(() => {
    fetchPlan();
  }, []);

  const fetchPlan = async () => {
    try {
      await weeklyApi.execute();
    } catch (e) {}
  };

  const handleGenerate = async () => {
    await generateApi.execute();
    fetchPlan();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white p-6 rounded-2xl border shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Weekly Plan</h1>
          <p className="text-gray-500">Your meals for the week</p>
        </div>
        <button onClick={handleGenerate} className="px-4 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-700">
          Generate Weekly Plan
        </button>
      </div>

      {weeklyApi.loading ? (
        <LoadingSkeleton count={3} />
      ) : weeklyApi.data ? (
        <div className="grid gap-6">
          {weeklyApi.data.days.map((day, idx) => (
            <div key={idx} className="bg-white rounded-xl border p-6">
              <h3 className="font-bold text-lg mb-4">{day.date}</h3>
              <div className="grid grid-cols-3 gap-4">
                {day.meals.map((m, i) => (
                  <div key={i} className="p-4 border rounded-lg bg-gray-50">
                    <p className="font-medium text-sm text-brand-600 mb-1">{m.meal_type}</p>
                    <p className="font-bold text-gray-900 truncate">{m.meal.name}</p>
                    <p className="text-xs text-gray-500">{Math.round(m.meal.calories)} kcal</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border p-12">
          <EmptyState icon={CalendarRange} title="No Weekly Plan" description="Generate a plan to see your week at a glance." actionText="Generate Plan" onAction={handleGenerate} />
        </div>
      )}
    </div>
  );
}
