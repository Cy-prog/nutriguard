import React from 'react';
import { X } from 'lucide-react';

export const ReplaceMealModal = ({ isOpen, onClose, alternatives, onSelect, selectedId }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="bg-white rounded-2xl w-full max-w-lg max-h-[80vh] flex flex-col shadow-xl">
        <div className="p-4 border-b flex justify-between items-center">
          <h2 className="text-xl font-bold">Alternative Meals</h2>
          <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded-lg text-gray-500">
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <div className="p-4 overflow-y-auto flex-1 space-y-3">
          {alternatives.map(meal => (
            <div 
              key={meal.id}
              className={`p-4 border rounded-xl flex justify-between items-center ${selectedId === meal.id ? 'border-brand-500 bg-brand-50' : 'hover:border-gray-300'}`}
            >
              <div>
                <h3 className="font-bold text-gray-900">{meal.name}</h3>
                <p className="text-sm text-gray-500">{Math.round(meal.calories)} kcal • {Math.round(meal.protein_g)}g protein • {meal.prep_time_minutes}m prep</p>
              </div>
              <button 
                onClick={() => onSelect(meal)}
                className={`px-4 py-2 rounded-lg font-medium ${selectedId === meal.id ? 'bg-brand-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
              >
                {selectedId === meal.id ? 'Selected' : 'Select'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
