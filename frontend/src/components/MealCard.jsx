import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, Flame, RefreshCw, XCircle } from 'lucide-react';

export const MealCard = ({ meal, onReplace, onRandomize }) => {
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden flex flex-col h-full">
      <div 
        className="h-48 bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center cursor-pointer relative"
        onClick={() => navigate(`/meals/${meal.id}`)}
      >
        <Flame className="w-12 h-12 text-brand-300" />
        <div className="absolute top-2 right-2 flex space-x-1">
          {meal.diet_type === 'VEGETARIAN' && <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-bold">V</span>}
          {meal.diet_type === 'VEGAN' && <span className="bg-green-200 text-green-900 text-xs px-2 py-1 rounded-full font-bold">VG</span>}
          {meal.diet_type === 'JAIN' && <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full font-bold">J</span>}
        </div>
      </div>
      
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="text-lg font-bold text-gray-900 truncate">{meal.name}</h3>
        {meal.local_name && <p className="text-sm text-gray-500 truncate">{meal.local_name}</p>}
        
        <div className="mt-4 grid grid-cols-4 gap-2 text-center text-sm border-t border-b py-2">
          <div><span className="block font-bold text-gray-900">{Math.round(meal.calories)}</span><span className="text-xs text-gray-500">kcal</span></div>
          <div><span className="block font-bold text-gray-900">{Math.round(meal.protein_g)}g</span><span className="text-xs text-gray-500">P</span></div>
          <div><span className="block font-bold text-gray-900">{Math.round(meal.carbs_g)}g</span><span className="text-xs text-gray-500">C</span></div>
          <div><span className="block font-bold text-gray-900">{Math.round(meal.fat_g)}g</span><span className="text-xs text-gray-500">F</span></div>
        </div>
        
        <div className="mt-4 flex items-center justify-between text-sm text-gray-600 mb-4">
          <div className="flex items-center"><Clock className="w-4 h-4 mr-1"/> {meal.prep_time_minutes}m</div>
          <div>{meal.difficulty}</div>
        </div>
        
        <div className="mt-auto flex space-x-2">
          <button 
            onClick={() => navigate(`/meals/${meal.id}`)}
            className="flex-1 bg-brand-50 text-brand-600 px-3 py-2 rounded-lg font-medium hover:bg-brand-100 transition"
          >
            Recipe
          </button>
          {onReplace && (
            <button onClick={onReplace} className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg border">
              <RefreshCw className="w-5 h-5" />
            </button>
          )}
          {onRandomize && (
            <button onClick={onRandomize} className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg border">
              <XCircle className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
