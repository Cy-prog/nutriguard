import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, Flame, RefreshCw, XCircle, Heart, Utensils } from 'lucide-react';

export const MealCard = ({ meal, onReplace, onRandomize }) => {
  const navigate = useNavigate();
  const mealId = meal.meal_id || meal.id;
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    if (!mealId) return;
    const favorites = JSON.parse(localStorage.getItem('nutriguard_favorites') || '[]');
    setIsFavorite(favorites.includes(mealId));
  }, [mealId]);

  const toggleFavorite = (e) => {
    e.stopPropagation();
    if (!mealId) return;
    const favorites = JSON.parse(localStorage.getItem('nutriguard_favorites') || '[]');
    let updated;
    if (favorites.includes(mealId)) {
      updated = favorites.filter(id => id !== mealId);
      setIsFavorite(false);
    } else {
      updated = [...favorites, mealId];
      setIsFavorite(true);
    }
    localStorage.setItem('nutriguard_favorites', JSON.stringify(updated));
  };

  const calories = Math.round(meal.calories || 0);
  const protein = Math.round(meal.protein_g || 0);
  const carbs = Math.round(meal.carbohydrates_g || meal.carbs_g || 0);
  const fat = Math.round(meal.fat_g || 0);
  const prepTime = meal.preparation_time_minutes || meal.prep_time_minutes || 20;
  const isVeg = meal.is_vegetarian ?? (meal.diet_type === 'VEGETARIAN');
  const isVegan = meal.is_vegan ?? (meal.diet_type === 'VEGAN');
  const isJain = meal.is_jain_friendly ?? (meal.diet_type === 'JAIN');

  return (
    <div className="bg-white rounded-2xl shadow-xs hover:shadow-md border border-slate-200 overflow-hidden flex flex-col h-full transition group">
      <div 
        className="h-44 bg-gradient-to-br from-emerald-50 via-teal-50 to-slate-100 flex items-center justify-center cursor-pointer relative"
        onClick={() => navigate(`/meals/${mealId}`)}
      >
        <Utensils className="w-12 h-12 text-emerald-400/80 group-hover:scale-110 transition duration-300" />
        
        {/* Diet Badges */}
        <div className="absolute top-3 left-3 flex space-x-1.5">
          {isVegan ? (
            <span className="bg-emerald-600 text-white text-[10px] px-2 py-0.5 rounded-full font-bold shadow-xs">VEGAN</span>
          ) : isVeg ? (
            <span className="bg-emerald-100 text-emerald-800 border border-emerald-300 text-[10px] px-2 py-0.5 rounded-full font-bold shadow-xs">VEG</span>
          ) : (
            <span className="bg-rose-100 text-rose-800 border border-rose-300 text-[10px] px-2 py-0.5 rounded-full font-bold shadow-xs">NON-VEG</span>
          )}
          {isJain && (
            <span className="bg-amber-100 text-amber-900 border border-amber-300 text-[10px] px-2 py-0.5 rounded-full font-bold shadow-xs">JAIN</span>
          )}
        </div>

        {/* Favorite Bookmark */}
        <button
          onClick={toggleFavorite}
          className="absolute top-3 right-3 p-1.5 rounded-full bg-white/90 hover:bg-white text-slate-400 hover:text-rose-500 shadow-xs transition"
          title={isFavorite ? "Remove from Favorites" : "Save to Favorites"}
        >
          <Heart className={`w-4 h-4 ${isFavorite ? 'fill-rose-500 text-rose-500' : ''}`} />
        </button>

        {meal.cuisine_region && (
          <div className="absolute bottom-2 left-3 text-[10px] font-semibold text-slate-500 bg-white/80 backdrop-blur-xs px-2 py-0.5 rounded-md">
            {meal.cuisine_region.replace('_', ' ')}
          </div>
        )}
      </div>
      
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="text-base font-bold text-slate-900 truncate group-hover:text-emerald-700 transition" title={meal.name}>
          {meal.name}
        </h3>
        {meal.local_name && (
          <p className="text-xs text-slate-500 truncate" title={meal.local_name}>{meal.local_name}</p>
        )}
        
        {/* Macronutrient Pills */}
        <div className="mt-4 grid grid-cols-4 gap-1.5 text-center text-xs bg-slate-50 p-2 rounded-xl border border-slate-100">
          <div><span className="block font-bold text-slate-900">{calories}</span><span className="text-[10px] text-slate-400">kcal</span></div>
          <div><span className="block font-bold text-slate-900">{protein}g</span><span className="text-[10px] text-slate-400">Protein</span></div>
          <div><span className="block font-bold text-slate-900">{carbs}g</span><span className="text-[10px] text-slate-400">Carbs</span></div>
          <div><span className="block font-bold text-slate-900">{fat}g</span><span className="text-[10px] text-slate-400">Fat</span></div>
        </div>
        
        <div className="mt-3 flex items-center justify-between text-xs text-slate-500 mb-4">
          <div className="flex items-center"><Clock className="w-3.5 h-3.5 mr-1 text-slate-400"/> {prepTime}m</div>
          <div className="capitalize font-medium text-slate-600">{meal.difficulty || 'Easy'}</div>
        </div>
        
        <div className="mt-auto flex space-x-2">
          <button 
            onClick={() => navigate(`/meals/${mealId}`)}
            className="flex-1 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 px-3 py-2 rounded-xl text-xs font-semibold transition"
          >
            View Recipe
          </button>
          {onReplace && (
            <button 
              onClick={onReplace} 
              className="p-2 text-slate-500 hover:text-emerald-600 hover:bg-slate-100 rounded-xl border border-slate-200 transition"
              title="Replace this meal"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          )}
          {onRandomize && (
            <button 
              onClick={onRandomize} 
              className="p-2 text-slate-500 hover:text-rose-600 hover:bg-slate-100 rounded-xl border border-slate-200 transition"
              title="Remove meal"
            >
              <XCircle className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
