import React, { useState, useEffect } from 'react';
import { foods } from '../api/endpoints';
import { 
  Database, 
  Search, 
  Filter, 
  Sparkles, 
  Info, 
  CheckCircle2, 
  X, 
  AlertCircle,
  BookOpen,
  Wheat,
  Activity,
  Layers
} from 'lucide-react';

const CATEGORIES = [
  { id: 'all', label: 'All Categories' },
  { id: 'grain', label: 'Grains & Millets' },
  { id: 'pulse', label: 'Pulses & Dal' },
  { id: 'vegetable', label: 'Vegetables' },
  { id: 'dairy', label: 'Dairy' },
  { id: 'fruit', label: 'Fruits' },
  { id: 'snack', label: 'Nuts & Snacks' },
  { id: 'spice', label: 'Spices & Condiments' },
];

export default function FoodDatabase() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [foodItems, setFoodItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFood, setSelectedFood] = useState(null);

  useEffect(() => {
    fetchFoods();
  }, [selectedCategory]);

  const fetchFoods = async (searchQuery = '') => {
    setLoading(true);
    try {
      const params = {};
      if (selectedCategory !== 'all') params.category = selectedCategory;
      if (searchQuery) params.search = searchQuery;
      params.limit = 60;

      const res = await foods.searchRawFoods(params);
      setFoodItems(res.data.foods || []);
    } catch (err) {
      console.error("Failed to load food composition:", err);
      setFoodItems([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchFoods(searchTerm);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="bg-white border rounded-2xl p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold mb-2">
            <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
            <span>ICMR-NIN IFCT 2017 & USDA FoodData Central</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">Indian Food Composition Database</h1>
          <p className="text-slate-500 text-sm mt-1">
            Authoritative biochemical composition for raw Indian agricultural staples, spices, pulses, and greens.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right hidden sm:block">
            <div className="text-xl font-bold text-slate-900">{foodItems.length}</div>
            <div className="text-xs text-slate-400">Verified Profiles Loaded</div>
          </div>
        </div>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="bg-white border rounded-2xl p-4 shadow-sm space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by English, Hindi, or botanical alias (e.g. Palak, Spinach, Methi, Rajma, Moong)..."
              className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold rounded-xl shadow-sm transition"
          >
            Search
          </button>
        </form>

        {/* Category Filter Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {CATEGORIES.map(cat => (
            <button
              key={cat.id}
              onClick={() => {
                setSelectedCategory(cat.id);
                setSearchTerm('');
              }}
              className={`whitespace-nowrap px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                selectedCategory === cat.id
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Foods Grid / Cards */}
      {loading ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-white border rounded-2xl p-5 space-y-3 animate-pulse">
              <div className="h-5 bg-slate-200 rounded w-2/3" />
              <div className="h-4 bg-slate-100 rounded w-1/3" />
              <div className="h-16 bg-slate-50 rounded" />
            </div>
          ))}
        </div>
      ) : foodItems.length === 0 ? (
        <div className="bg-white border rounded-2xl p-12 text-center space-y-3 shadow-sm">
          <Database className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No Food Profiles Found</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Try adjusting your search keywords or resetting the category filter.
          </p>
          <button
            onClick={() => {
              setSelectedCategory('all');
              setSearchTerm('');
              fetchFoods();
            }}
            className="mt-2 inline-flex items-center px-4 py-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg hover:bg-emerald-100 transition"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {foodItems.map(food => (
            <div
              key={food.food_id}
              onClick={() => setSelectedFood(food)}
              className="bg-white border border-slate-200 hover:border-emerald-400 rounded-2xl p-5 shadow-xs hover:shadow-md transition cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="font-bold text-slate-900 group-hover:text-emerald-700 transition">
                      {food.name}
                    </h3>
                    {food.aliases && food.aliases.length > 0 && (
                      <p className="text-xs text-slate-500 font-medium">
                        aka: {food.aliases.slice(0, 3).join(', ')}
                      </p>
                    )}
                  </div>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                    {food.category}
                  </span>
                </div>

                {/* Clinical / Biochemical Badges */}
                <div className="flex flex-wrap gap-1.5 mt-3">
                  {food.glycemic_index !== null && (
                    <span className={`text-[10px] px-2 py-0.5 rounded-md font-semibold ${
                      food.glycemic_index < 55
                        ? 'bg-emerald-100 text-emerald-800'
                        : food.glycemic_index < 70
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-rose-100 text-rose-800'
                    }`}>
                      GI: {food.glycemic_index} ({food.glycemic_index < 55 ? 'Low' : food.glycemic_index < 70 ? 'Med' : 'High'})
                    </span>
                  )}
                  {food.purine_level && (
                    <span className="text-[10px] px-2 py-0.5 rounded-md font-semibold bg-blue-100 text-blue-800">
                      Purine: {food.purine_level}
                    </span>
                  )}
                  {food.vitamin_k_mcg !== null && (
                    <span className="text-[10px] px-2 py-0.5 rounded-md font-semibold bg-purple-100 text-purple-800">
                      Vit K: {Math.round(food.vitamin_k_mcg)} mcg
                    </span>
                  )}
                  {food.is_gluten_free && (
                    <span className="text-[10px] px-2 py-0.5 rounded-md font-semibold bg-teal-50 text-teal-700 border border-teal-200">
                      Gluten-Free
                    </span>
                  )}
                </div>

                {/* Key Nutrients Preview (100g) */}
                <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-3 gap-2 text-center text-xs">
                  {food.nutrients?.slice(0, 3).map((n, i) => (
                    <div key={i} className="bg-slate-50 p-1.5 rounded-lg">
                      <div className="font-bold text-slate-800">{Math.round(n.amount)} {n.unit}</div>
                      <div className="text-[10px] text-slate-400 truncate">{n.name}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-4 pt-2 flex items-center justify-between text-[11px] text-slate-400">
                <span className="flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                  {food.nutrient_source}
                </span>
                <span className="text-emerald-600 font-semibold group-hover:underline">
                  View Full Profile →
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Food Detail Modal */}
      {selectedFood && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-6 shadow-2xl">
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b pb-4">
              <div>
                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-emerald-50 text-emerald-800 text-xs font-semibold rounded-full mb-1">
                  <span>Source: {selectedFood.nutrient_source}</span>
                </div>
                <h2 className="text-2xl font-bold text-slate-900">{selectedFood.name}</h2>
                {selectedFood.aliases?.length > 0 && (
                  <p className="text-xs text-slate-500">
                    Regional Names: {selectedFood.aliases.join(', ')}
                  </p>
                )}
              </div>
              <button
                onClick={() => setSelectedFood(null)}
                className="p-2 text-slate-400 hover:text-slate-700 rounded-full hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Clinical Highlights */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div className="text-xs text-slate-400">Glycemic Index</div>
                <div className="text-lg font-bold text-slate-800">
                  {selectedFood.glycemic_index ?? 'N/A'}
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div className="text-xs text-slate-400">Purine Level</div>
                <div className="text-lg font-bold text-slate-800 capitalize">
                  {selectedFood.purine_level ?? 'Normal'}
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div className="text-xs text-slate-400">Vitamin K</div>
                <div className="text-lg font-bold text-slate-800">
                  {selectedFood.vitamin_k_mcg !== null ? `${Math.round(selectedFood.vitamin_k_mcg)} mcg` : 'Trace'}
                </div>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <div className="text-xs text-slate-400">Diet Suitability</div>
                <div className="text-xs font-bold text-slate-800 mt-1">
                  {selectedFood.is_vegetarian ? 'Veg' : 'Non-Veg'}{selectedFood.is_jain ? ' • Jain' : ''}
                </div>
              </div>
            </div>

            {/* All Nutrients Breakdown */}
            <div>
              <h3 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-1.5">
                <Activity className="w-4 h-4 text-emerald-600" />
                Micronutrient & Macronutrient Profile (per 100g raw)
              </h3>
              {selectedFood.nutrients && selectedFood.nutrients.length > 0 ? (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                  {selectedFood.nutrients.map((n, idx) => (
                    <div key={idx} className="p-2.5 bg-slate-50 rounded-xl border border-slate-100 flex justify-between items-center text-xs">
                      <span className="text-slate-600 font-medium">{n.name}</span>
                      <span className="font-bold text-slate-900">{n.amount} {n.unit}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500 italic">Nutrient records derived from baseline ICMR-NIN composite table.</p>
              )}
            </div>

            <div className="p-3 rounded-xl bg-amber-50 border border-amber-200 text-[11px] text-amber-800">
              <strong>Clinical Guardrail:</strong> NutriGuard cross-references this food table against registered prescription drugs and medical conditions before recommending any meal containing this staple.
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setSelectedFood(null)}
                className="px-5 py-2 bg-slate-900 text-white rounded-xl text-xs font-semibold hover:bg-slate-800 transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
