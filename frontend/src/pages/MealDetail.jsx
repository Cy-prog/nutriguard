import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import { meals } from '../api/endpoints';
import { YouTubeEmbed } from '../components/YouTubeEmbed';
import { LoadingSkeleton } from '../components/EmptyState';
import { Clock, ChefHat, Users } from 'lucide-react';

export default function MealDetail() {
  const { mealId } = useParams();
  const mealApi = useApi(meals.getMeal);
  const recipeApi = useApi(meals.getRecipe);

  useEffect(() => {
    mealApi.execute(mealId);
    recipeApi.execute(mealId);
  }, [mealId]);

  if (mealApi.loading || recipeApi.loading) return <LoadingSkeleton count={2} />;
  
  const meal = mealApi.data;
  const recipe = recipeApi.data;

  if (!meal) return <div>Meal not found</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <div className="bg-white rounded-2xl border overflow-hidden shadow-sm">
        <div className="h-64 bg-gradient-to-br from-brand-500 to-brand-700 p-8 flex flex-col justify-end">
          <div className="flex space-x-2 mb-4">
            <span className="bg-white/20 text-white px-3 py-1 rounded-full text-sm backdrop-blur-sm">{meal.diet_type}</span>
            {meal.cuisine_region && <span className="bg-white/20 text-white px-3 py-1 rounded-full text-sm backdrop-blur-sm">{meal.cuisine_region}</span>}
          </div>
          <h1 className="text-4xl font-bold text-white">{meal.name}</h1>
          {meal.local_name && <p className="text-xl text-brand-100 mt-2">{meal.local_name}</p>}
        </div>
        
        <div className="p-8">
          <div className="grid grid-cols-3 gap-6 text-center divide-x border-b pb-8 mb-8">
            <div><Clock className="w-6 h-6 mx-auto text-gray-400 mb-2" /><span className="font-bold">{meal.preparation_time_minutes || meal.prep_time_minutes || 25} mins</span></div>
            <div><ChefHat className="w-6 h-6 mx-auto text-gray-400 mb-2" /><span className="font-bold capitalize">{meal.difficulty ? meal.difficulty.toLowerCase() : 'moderate'}</span></div>
            <div><Users className="w-6 h-6 mx-auto text-gray-400 mb-2" /><span className="font-bold">{meal.serving_description || "1 Serving"}</span></div>
          </div>

          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h2 className="text-2xl font-bold mb-6">Ingredients</h2>
              {(recipe?.ingredients || meal?.ingredients)?.length > 0 ? (
                <ul className="space-y-3">
                  {(recipe?.ingredients || meal?.ingredients).map((ing, i) => (
                    <li key={i} className="flex items-center space-x-3 text-gray-700">
                      <div className="w-2 h-2 rounded-full bg-brand-500"></div>
                      <span>{ing.quantity ? `${ing.quantity} ${ing.unit || ''}` : ''} {ing.name}</span>
                    </li>
                  ))}
                </ul>
              ) : <p className="text-gray-500 text-sm">Authentic Indian pantry staples.</p>}
            </div>

            <div>
              <h2 className="text-2xl font-bold mb-6">Nutrition per serving</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 p-4 rounded-xl"><div className="text-sm text-gray-500">Calories</div><div className="text-xl font-bold">{Math.round(meal.calories || 0)} kcal</div></div>
                <div className="bg-gray-50 p-4 rounded-xl"><div className="text-sm text-gray-500">Protein</div><div className="text-xl font-bold">{Math.round(meal.protein_g || 0)} g</div></div>
                <div className="bg-gray-50 p-4 rounded-xl"><div className="text-sm text-gray-500">Carbs</div><div className="text-xl font-bold">{Math.round(meal.carbohydrates_g || meal.carbs_g || 0)} g</div></div>
                <div className="bg-gray-50 p-4 rounded-xl"><div className="text-sm text-gray-500">Fat</div><div className="text-xl font-bold">{Math.round(meal.fat_g || 0)} g</div></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border p-8 shadow-sm">
        <h2 className="text-2xl font-bold mb-6">Preparation Steps</h2>
        {(recipe?.preparation_steps || recipe?.instructions)?.length > 0 ? (
          <div className="space-y-6">
            {(recipe?.preparation_steps || recipe?.instructions).map((step, i) => (
              <div key={i} className="flex space-x-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-100 text-brand-600 flex items-center justify-center font-bold">{i + 1}</div>
                <p className="text-gray-700 mt-1">{step}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">{recipe?.recipe_text || "Cook according to traditional Indian home-style method."}</p>
        )}
      </div>

      <div className="bg-white rounded-2xl border p-8 shadow-sm">
        <h2 className="text-2xl font-bold mb-6">Recipe Video</h2>
        <YouTubeEmbed url={meal.video_url} />
      </div>
    </div>
  );
}
