import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { profile as profileApi } from '../api/endpoints';
import { 
  Settings as SettingsIcon, 
  Save, 
  Download, 
  Trash2, 
  CheckCircle2, 
  Utensils, 
  Flame, 
  DollarSign, 
  Clock, 
  MapPin,
  ShieldAlert
} from 'lucide-react';

export default function Settings() {
  const { user } = useContext(AuthContext);
  const [profileData, setProfileData] = useState({
    regional_preference: 'NORTH_INDIAN',
    diet_type: 'VEGETARIAN',
    preferred_meal_spice_level: 'MEDIUM',
    cooking_time_max_minutes: 30,
    budget_level: 'MEDIUM'
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    profileApi.getProfile()
      .then(res => {
        if (res.data) {
          setProfileData(prev => ({
            ...prev,
            regional_preference: res.data.regional_preference || prev.regional_preference,
            diet_type: res.data.diet_type || prev.diet_type,
            preferred_meal_spice_level: res.data.preferred_meal_spice_level || prev.preferred_meal_spice_level,
            cooking_time_max_minutes: res.data.cooking_time_max_minutes || prev.cooking_time_max_minutes,
            budget_level: res.data.budget_level || prev.budget_level
          }));
        }
      })
      .catch(err => {
        console.error("Error fetching settings:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSavedSuccess(false);

    try {
      await profileApi.updateProfile(profileData);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error("Save error:", err);
      setError("Failed to save preferences. Please check input values.");
    } finally {
      setSaving(false);
    }
  };

  const handleExportData = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(profileData, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `nutriguard_profile_${new Date().toISOString().split('T')[0]}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="bg-white border rounded-2xl p-6 shadow-sm flex items-center justify-between">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-semibold mb-2">
            <SettingsIcon className="w-3.5 h-3.5 text-slate-500" />
            <span>Preferences & Customization</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">Nutrition & Regional Cuisine Settings</h1>
          <p className="text-slate-500 text-sm mt-1">
            Tailor the recommendation engine to your home kitchen habits, regional tastes, and daily prep routine.
          </p>
        </div>
      </div>

      {savedSuccess && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-2xl text-xs font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          Your nutrition and cuisine preferences have been saved successfully!
        </div>
      )}

      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-800 rounded-2xl text-xs font-semibold">
          {error}
        </div>
      )}

      {/* Main Settings Form */}
      <form onSubmit={handleSave} className="bg-white border rounded-2xl p-6 shadow-sm space-y-6">
        <h2 className="text-lg font-bold text-slate-900 border-b pb-3">Kitchen & Culinary Preferences</h2>

        <div className="grid sm:grid-cols-2 gap-6">
          {/* Regional Preference */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-2 flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-emerald-600" />
              Regional Indian Cuisine Preference
            </label>
            <select
              value={profileData.regional_preference}
              onChange={(e) => setProfileData({ ...profileData, regional_preference: e.target.value })}
              className="w-full text-sm p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:bg-white transition"
            >
              <option value="NORTH_INDIAN">North Indian (Rotis, Paneer, Dals, Parathas)</option>
              <option value="SOUTH_INDIAN">South Indian (Idli, Dosa, Sambar, Rasam, Poriyal)</option>
              <option value="WEST_INDIAN">West Indian (Thepla, Khichdi, Poha, Gujarati/Maharashtrian)</option>
              <option value="EAST_INDIAN">East Indian (Rice, Fish, Mustard gravies, Lentils)</option>
              <option value="PAN_INDIAN">Pan-Indian (Balanced diverse regional rotation)</option>
            </select>
          </div>

          {/* Dietary Pattern */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-2 flex items-center gap-1.5">
              <Utensils className="w-3.5 h-3.5 text-emerald-600" />
              Primary Dietary Pattern
            </label>
            <select
              value={profileData.diet_type}
              onChange={(e) => setProfileData({ ...profileData, diet_type: e.target.value })}
              className="w-full text-sm p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:bg-white transition"
            >
              <option value="VEGETARIAN">Vegetarian (Lacto-Vegetarian)</option>
              <option value="VEGAN">Vegan (Plant-based, no dairy)</option>
              <option value="JAIN">Jain (No root vegetables, onions, garlic)</option>
              <option value="EGGETARIAN">Eggetarian (Vegetarian + Eggs)</option>
              <option value="NON_VEGETARIAN">Non-Vegetarian (Chicken, Fish, Eggs, Meat)</option>
            </select>
          </div>

          {/* Spice Level */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-2 flex items-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-amber-600" />
              Preferred Spice Intensity
            </label>
            <select
              value={profileData.preferred_meal_spice_level}
              onChange={(e) => setProfileData({ ...profileData, preferred_meal_spice_level: e.target.value })}
              className="w-full text-sm p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:bg-white transition"
            >
              <option value="MILD">Mild (Subtle cumin, turmeric, no fiery chilis)</option>
              <option value="MEDIUM">Medium (Balanced home-style Indian tadka)</option>
              <option value="SPICY">Spicy (Authentic bold spice and chili punch)</option>
            </select>
          </div>

          {/* Max Cooking Time */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-2 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-blue-600" />
              Maximum Prep & Cooking Time
            </label>
            <select
              value={profileData.cooking_time_max_minutes}
              onChange={(e) => setProfileData({ ...profileData, cooking_time_max_minutes: parseInt(e.target.value, 10) })}
              className="w-full text-sm p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:bg-white transition"
            >
              <option value={15}>Quick & Easy (15 minutes)</option>
              <option value={30}>Standard Daily (30 minutes)</option>
              <option value={45}>Elaborate (45 minutes)</option>
              <option value={60}>Slow-Cooked & Gourmet (60+ minutes)</option>
            </select>
          </div>

          {/* Budget Tier */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-2 flex items-center gap-1.5">
              <DollarSign className="w-3.5 h-3.5 text-emerald-600" />
              Daily Meal Budget Tier
            </label>
            <select
              value={profileData.budget_level}
              onChange={(e) => setProfileData({ ...profileData, budget_level: e.target.value })}
              className="w-full text-sm p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:bg-white transition"
            >
              <option value="BUDGET">Budget-Conscious (₹100 - ₹150 / day staples)</option>
              <option value="MEDIUM">Standard Balanced (₹150 - ₹250 / day)</option>
              <option value="PREMIUM">Premium Diverse (₹250+ / day)</option>
            </select>
          </div>
        </div>

        <div className="pt-4 border-t flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl text-xs shadow-sm transition flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            {saving ? 'Saving...' : 'Save Preferences'}
          </button>
        </div>
      </form>

      {/* Data Management Section */}
      <div className="bg-white border rounded-2xl p-6 shadow-sm space-y-4">
        <h2 className="text-lg font-bold text-slate-900 border-b pb-3">Data Management & Privacy</h2>
        
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-slate-50 rounded-xl border border-slate-100">
          <div>
            <h4 className="font-semibold text-sm text-slate-900">Export Clinical Nutrition Data</h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Download your full profile, nutrient targets, and logged parameters in standard JSON format.
            </p>
          </div>
          <button
            onClick={handleExportData}
            className="inline-flex items-center px-4 py-2 bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 rounded-xl text-xs font-semibold shadow-xs transition"
          >
            <Download className="w-3.5 h-3.5 mr-1.5" />
            Export Data
          </button>
        </div>
      </div>
    </div>
  );
}
