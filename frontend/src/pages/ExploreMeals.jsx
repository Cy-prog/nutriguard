import React, { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import { meals } from '../api/endpoints';
import { MealCard } from '../components/MealCard';
import { LoadingSkeleton } from '../components/EmptyState';
import { Search } from 'lucide-react';

export default function ExploreMeals() {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('ALL');
  const listApi = useApi(meals.listMeals);

  useEffect(() => {
    // Adding timeout for debounce
    const t = setTimeout(() => {
      listApi.execute({ q: search, limit: 20, diet: filter === 'ALL' ? undefined : filter });
    }, 500);
    return () => clearTimeout(t);
  }, [search, filter]);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl border shadow-sm space-y-4">
        <h1 className="text-2xl font-bold text-gray-900">Explore Meals</h1>
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search meals..."
              className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-brand-500 focus:border-brand-500"
            />
          </div>
          <select 
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="border rounded-lg px-4 py-2 focus:ring-brand-500"
          >
            <option value="ALL">All Diets</option>
            <option value="VEGETARIAN">Vegetarian</option>
            <option value="VEGAN">Vegan</option>
            <option value="NON_VEGETARIAN">Non-Vegetarian</option>
          </select>
        </div>
      </div>

      {listApi.loading ? (
        <LoadingSkeleton count={3} />
      ) : (
        <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {listApi.data?.items?.map(meal => (
            <MealCard key={meal.id} meal={meal} />
          ))}
        </div>
      )}
    </div>
  );
}
