import React from 'react';

export const NutritionBar = ({ label, actual, target, colorClass }) => {
  const percentage = Math.min(100, (actual / target) * 100) || 0;
  
  return (
    <div className="w-full">
      <div className="flex justify-between mb-1">
        <span className="font-medium text-gray-700">{label}</span>
        <span className="text-gray-600">{Math.round(actual)}g / {Math.round(target)}g</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div className={`${colorClass} h-3 rounded-full transition-all`} style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  );
};
