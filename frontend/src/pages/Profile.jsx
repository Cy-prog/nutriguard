import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { profile as profileApi } from '../api/endpoints';
import { TagInput } from '../components/TagInput';

export default function Profile() {
  const { user, setUser } = useContext(AuthContext);
  const [data, setData] = useState(user || {});
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (user) setData(user);
  }, [user]);

  const handleSave = async () => {
    try {
      setSaving(true);
      const res = await profileApi.updateProfile(data);
      setUser(res.data);
      setMessage('Profile updated successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (e) {
      setMessage('Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div className="flex justify-between items-center bg-white p-6 rounded-2xl border shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">Profile & Preferences</h1>
        <button onClick={handleSave} disabled={saving} className="px-6 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-700 disabled:opacity-50">
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {message && <div className={`p-4 rounded-lg ${message.includes('success') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>{message}</div>}

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border shadow-sm space-y-4">
          <h2 className="text-xl font-bold border-b pb-2">Physical Details</h2>
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm text-gray-600">Age</label><input type="number" value={data.age || ''} onChange={e => setData({...data, age: +e.target.value})} className="w-full border rounded-lg p-2 mt-1" /></div>
            <div><label className="block text-sm text-gray-600">Sex</label><select value={data.sex || ''} onChange={e => setData({...data, sex: e.target.value})} className="w-full border rounded-lg p-2 mt-1"><option value="MALE">Male</option><option value="FEMALE">Female</option></select></div>
            <div><label className="block text-sm text-gray-600">Height (cm)</label><input type="number" value={data.height_cm || ''} onChange={e => setData({...data, height_cm: +e.target.value})} className="w-full border rounded-lg p-2 mt-1" /></div>
            <div><label className="block text-sm text-gray-600">Weight (kg)</label><input type="number" value={data.weight_kg || ''} onChange={e => setData({...data, weight_kg: +e.target.value})} className="w-full border rounded-lg p-2 mt-1" /></div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border shadow-sm space-y-4">
          <h2 className="text-xl font-bold border-b pb-2">Goals & Diet</h2>
          <div>
            <label className="block text-sm text-gray-600">Activity Level</label>
            <select value={data.activity_level || ''} onChange={e => setData({...data, activity_level: e.target.value})} className="w-full border rounded-lg p-2 mt-1">
              {['SEDENTARY', 'LIGHTLY_ACTIVE', 'MODERATELY_ACTIVE', 'VERY_ACTIVE'].map(v => <option key={v} value={v}>{v.replace('_', ' ')}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600">Goal</label>
            <select value={data.goal || ''} onChange={e => setData({...data, goal: e.target.value})} className="w-full border rounded-lg p-2 mt-1">
              {['WEIGHT_LOSS', 'WEIGHT_MAINTENANCE', 'WEIGHT_GAIN', 'MUSCLE_GAIN'].map(v => <option key={v} value={v}>{v.replace('_', ' ')}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600">Diet Type</label>
            <select value={data.diet_type || ''} onChange={e => setData({...data, diet_type: e.target.value})} className="w-full border rounded-lg p-2 mt-1">
              {['VEGETARIAN', 'VEGAN', 'EGGETARIAN', 'NON_VEGETARIAN', 'JAIN'].map(v => <option key={v} value={v}>{v.replace('_', ' ')}</option>)}
            </select>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border shadow-sm space-y-4 md:col-span-2">
          <h2 className="text-xl font-bold border-b pb-2">Preferences & Health</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div><label className="block text-sm text-gray-600 mb-1">Allergies</label><TagInput tags={data.allergies || []} setTags={t => setData({...data, allergies: t})} placeholder="Add allergy (e.g. peanuts)" /></div>
            <div><label className="block text-sm text-gray-600 mb-1">Disliked Foods</label><TagInput tags={data.disliked_ingredients || []} setTags={t => setData({...data, disliked_ingredients: t})} placeholder="Add food to avoid" /></div>
            <div><label className="block text-sm text-gray-600 mb-1">Health Conditions</label><input type="text" value={data.health_conditions || ''} onChange={e => setData({...data, health_conditions: e.target.value})} placeholder="e.g. Diabetes, PCOS" className="w-full border rounded-lg p-2" /></div>
            <div><label className="block text-sm text-gray-600 mb-1">Region Preference</label>
              <select value={data.region_preference || ''} onChange={e => setData({...data, region_preference: e.target.value})} className="w-full border rounded-lg p-2">
                <option value="">Any</option><option value="NORTH_INDIAN">North Indian</option><option value="SOUTH_INDIAN">South Indian</option><option value="WEST_INDIAN">West Indian</option><option value="EAST_INDIAN">East Indian</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
