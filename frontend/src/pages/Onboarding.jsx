import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { profile } from '../api/endpoints';

export default function Onboarding() {
  const [step, setStep] = useState(1);
  const [data, setData] = useState({
    age: 30, sex: 'MALE', height_cm: 175, weight_kg: 70,
    activity_level: 'MODERATELY_ACTIVE', goal: 'WEIGHT_MAINTENANCE', diet_type: 'VEGETARIAN'
  });
  const navigate = useNavigate();

  const handleNext = () => setStep(s => s + 1);
  const handleBack = () => setStep(s => s - 1);

  const handleSubmit = async () => {
    try {
      await profile.updateProfile(data);
      navigate('/dashboard');
    } catch (e) {
      console.error("Failed to update profile", e);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="bg-white rounded-xl shadow-lg border p-8 max-w-2xl w-full mx-auto">
        <h2 className="text-2xl font-bold text-center mb-8">Let's personalize your experience</h2>
        
        {step === 1 && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Basic Info</h3>
            <div className="grid grid-cols-2 gap-4">
              <div><label className="block text-sm">Age</label><input type="number" value={data.age} onChange={e=>setData({...data, age: +e.target.value})} className="mt-1 block w-full px-3 py-2 border rounded-md" /></div>
              <div><label className="block text-sm">Sex</label>
                <select value={data.sex} onChange={e=>setData({...data, sex: e.target.value})} className="mt-1 block w-full px-3 py-2 border rounded-md">
                  <option value="MALE">Male</option><option value="FEMALE">Female</option>
                </select>
              </div>
              <div><label className="block text-sm">Height (cm)</label><input type="number" value={data.height_cm} onChange={e=>setData({...data, height_cm: +e.target.value})} className="mt-1 block w-full px-3 py-2 border rounded-md" /></div>
              <div><label className="block text-sm">Weight (kg)</label><input type="number" value={data.weight_kg} onChange={e=>setData({...data, weight_kg: +e.target.value})} className="mt-1 block w-full px-3 py-2 border rounded-md" /></div>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Activity Level</h3>
            {['SEDENTARY', 'LIGHTLY_ACTIVE', 'MODERATELY_ACTIVE', 'VERY_ACTIVE'].map(lvl => (
              <div key={lvl} onClick={() => setData({...data, activity_level: lvl})} className={`p-4 border rounded-lg cursor-pointer ${data.activity_level === lvl ? 'border-brand-500 bg-brand-50' : ''}`}>
                {lvl.replace('_', ' ')}
              </div>
            ))}
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Your Goal</h3>
            {['WEIGHT_LOSS', 'WEIGHT_MAINTENANCE', 'WEIGHT_GAIN', 'MUSCLE_GAIN'].map(goal => (
              <div key={goal} onClick={() => setData({...data, goal})} className={`p-4 border rounded-lg cursor-pointer ${data.goal === goal ? 'border-brand-500 bg-brand-50' : ''}`}>
                {goal.replace('_', ' ')}
              </div>
            ))}
          </div>
        )}

        <div className="mt-8 flex justify-between">
          {step > 1 ? <button onClick={handleBack} className="px-4 py-2 border rounded-md text-gray-700">Back</button> : <div></div>}
          {step < 3 ? <button onClick={handleNext} className="px-4 py-2 bg-brand-600 text-white rounded-md">Next</button>
                    : <button onClick={handleSubmit} className="px-4 py-2 bg-brand-600 text-white rounded-md">Complete Setup</button>}
        </div>
      </div>
    </div>
  );
}
