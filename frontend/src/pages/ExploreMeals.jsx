import React, { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import { meals } from '../api/endpoints';
import { MealCard } from '../components/MealCard';
import { EmptyState, LoadingSkeleton } from '../components/EmptyState';
import { Search, Utensils, Filter } from 'lucide-react';

export default function ExploreMeals() {
  const [search, setSearch] = useState('');
  const [dietFilter, setDietFilter] = useState('ALL');
  const [mealTypeFilter, setMealTypeFilter] = useState('ALL');
  const [regionFilter, setRegionFilter] = useState('ALL');
  const listApi = useApi(meals.listMeals);

  useEffect(() => {
    const t = setTimeout(() => {
      const params = {
        page: 1,
        page_size: 40,
      };
      if (search.trim()) params.search = search.trim();
      if (dietFilter !== 'ALL') params.diet = dietFilter.toLowerCase();
      if (mealTypeFilter !== 'ALL') params.meal_type = mealTypeFilter;
      if (regionFilter !== 'ALL') params.cuisine_region = regionFilter;

      listApi.execute(params);
    }, 300);

    return () => clearTimeout(t);
  }, [search, dietFilter, mealTypeFilter, regionFilter]);

  const mealItems = listApi.data?.meals || listApi.data?.items || [];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header and Search Filters */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Explore Authentic Indian Meals</h1>
          <p className="text-sm text-slate-500 mt-1">
            Browse 120+ home-style Indian preparations with full macro breakdowns, cooking times, and clinical safety tags.
          </p>
        </div>

        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search dishes by name (e.g. Khichdi, Sambar, Poha, Palak, Thepla, Rajma)..."
              className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-emerald-500 focus:bg-white focus:outline-none transition"
            />
          </div>

          <div className="grid grid-cols-3 gap-2">
            <select 
              value={dietFilter}
              onChange={(e) => setDietFilter(e.target.value)}
              className="border border-slate-200 bg-slate-50 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:ring-2 focus:ring-emerald-500"
            >
              <option value="ALL">All Diets</option>
              <option value="VEGETARIAN">Vegetarian</option>
              <option value="VEGAN">Vegan</option>
              <option value="JAIN">Jain Friendly</option>
              <option value="NON_VEG">Non-Vegetarian</option>
            </select>

            <select 
              value={mealTypeFilter}
              onChange={(e) => setMealTypeFilter(e.target.value)}
              className="border border-slate-200 bg-slate-50 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:ring-2 focus:ring-emerald-500"
            >
              <option value="ALL">All Meals</option>
              <option value="BREAKFAST">Breakfast</option>
              <option value="LUNCH">Lunch</option>
              <option value="DINNER">Dinner</option>
              <option value="SNACK">Snacks</option>
            </select>

            <select 
              value={regionFilter}
              onChange={(e) => setRegionFilter(e.target.value)}
              className="border border-slate-200 bg-slate-50 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:ring-2 focus:ring-emerald-500"
            >
              <option value="ALL">All Regions</option>
              <option value="NORTH_INDIAN">North</option>
              <option value="SOUTH_INDIAN">South</option>
              <option value="WEST_INDIAN">West</option>
              <option value="EAST_INDIAN">East</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Section */}
      {listApi.loading ? (
        <LoadingSkeleton count={4} />
      ) : mealItems.length > 0 ? (
        <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {mealItems.map(meal => (
            <MealCard key={meal.meal_id || meal.id} meal={meal} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center shadow-sm">
          <EmptyState
            icon={Utensils}
            title="No Meals Match Your Filters"
            description="Try relaxing your search query or choosing 'All Diets' / 'All Regions' to see more dishes."
            actionText="Clear Filters"
            onAction={() => {
              setSearch('');
              setDietFilter('ALL');
              setMealTypeFilter('ALL');
              setRegionFilter('ALL');
            }}
          />
        </div>
      )}
    </div>
  );
}
