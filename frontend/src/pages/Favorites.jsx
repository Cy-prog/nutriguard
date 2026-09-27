import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { meals } from '../api/endpoints';
import { MealCard } from '../components/MealCard';
import { EmptyState, LoadingSkeleton } from '../components/EmptyState';
import { Heart, Utensils, Sparkles, Plus } from 'lucide-react';

export default function Favorites() {
  const navigate = useNavigate();
  const [favoriteMeals, setFavoriteMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState('ALL');

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    setLoading(true);
    try {
      // Read saved favorite IDs from localStorage
      const savedIds = JSON.parse(localStorage.getItem('nutriguard_favorites') || '[]');
      
      if (savedIds.length === 0) {
        // Fallback: fetch a few top Indian recipes as default suggestions
        const res = await meals.listMeals({ page_size: 4 });
        const list = res.data.meals || res.data.items || [];
        setFavoriteMeals(list);
      } else {
        const mealPromises = savedIds.map(id => meals.getMeal(id).catch(() => null));
        const results = await Promise.all(mealPromises);
        setFavoriteMeals(results.filter(Boolean).map(r => r.data));
      }
    } catch (err) {
      console.error("Error loading favorites:", err);
      setFavoriteMeals([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredMeals = favoriteMeals.filter(m => {
    if (activeFilter === 'ALL') return true;
    return (m.meal_type || '').toUpperCase() === activeFilter;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="bg-white border rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold mb-2">
            <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
            <span>Saved Recipes & Quick Planning</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">Favorite Indian Meals</h1>
          <p className="text-slate-500 text-sm mt-1">
            Your hand-picked collection of balanced regional recipes and quick-prep staples.
          </p>
        </div>

        <button
          onClick={() => navigate('/meals')}
          className="inline-flex items-center px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-xl shadow-sm transition"
        >
          <Plus className="w-4 h-4 mr-1.5" />
          Explore More Meals
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {['ALL', 'BREAKFAST', 'LUNCH', 'DINNER', 'SNACK'].map((filter) => (
          <button
            key={filter}
            onClick={() => setActiveFilter(filter)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition ${
              activeFilter === filter
                ? 'bg-slate-900 text-white shadow-xs'
                : 'bg-white border text-slate-600 hover:bg-slate-50'
            }`}
          >
            {filter === 'ALL' ? 'All Favorites' : filter.charAt(0) + filter.slice(1).toLowerCase()}
          </button>
        ))}
      </div>

      {/* Meals Grid */}
      {loading ? (
        <LoadingSkeleton count={3} />
      ) : filteredMeals.length > 0 ? (
        <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredMeals.map((meal) => (
            <MealCard key={meal.meal_id || meal.id} meal={meal} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border p-12 shadow-sm">
          <EmptyState
            icon={Heart}
            title="No Favorite Meals Found"
            description="You haven't bookmarked any meals for this category yet. Explore our curated Indian kitchen recipes to find dishes you love."
            actionText="Browse Recipes"
            onAction={() => navigate('/meals')}
          />
        </div>
      )}
    </div>
  );
}
