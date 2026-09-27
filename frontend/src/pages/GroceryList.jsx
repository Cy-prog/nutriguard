import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { grocery } from '../api/endpoints';
import { EmptyState, LoadingSkeleton } from '../components/EmptyState';
import { ShoppingCart, Printer } from 'lucide-react';

export default function GroceryList() {
  const [view, setView] = useState('daily');
  const dailyApi = useApi(grocery.getDailyGrocery);
  const weeklyApi = useApi(grocery.getWeeklyGrocery);

  useEffect(() => {
    if (view === 'daily') dailyApi.execute();
    else weeklyApi.execute();
  }, [view]);

  const currentApi = view === 'daily' ? dailyApi : weeklyApi;

  const handlePrint = () => window.print();

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center bg-white p-6 rounded-2xl border shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Grocery List</h1>
          <p className="text-gray-500">Everything you need for your meals</p>
        </div>
        <div className="flex space-x-4">
          <div className="bg-gray-100 rounded-lg p-1 flex">
            <button onClick={() => setView('daily')} className={`px-4 py-2 rounded-md ${view === 'daily' ? 'bg-white shadow' : ''}`}>Daily</button>
            <button onClick={() => setView('weekly')} className={`px-4 py-2 rounded-md ${view === 'weekly' ? 'bg-white shadow' : ''}`}>Weekly</button>
          </div>
          <button onClick={handlePrint} className="p-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-600"><Printer className="w-5 h-5" /></button>
        </div>
      </div>

      {currentApi.loading ? (
        <LoadingSkeleton count={3} />
      ) : currentApi.data && Object.keys(currentApi.data.items).length > 0 ? (
        <div className="bg-white rounded-2xl border p-8 shadow-sm">
          {Object.entries(currentApi.data.items).map(([category, items]) => (
            <div key={category} className="mb-8 last:mb-0">
              <h2 className="text-xl font-bold text-brand-600 mb-4 capitalize border-b pb-2">{category.replace('_', ' ')}</h2>
              <ul className="grid md:grid-cols-2 gap-4">
                {items.map((item, i) => (
                  <li key={i} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg border border-gray-100">
                    <input type="checkbox" className="w-5 h-5 text-brand-600 rounded border-gray-300 focus:ring-brand-500" />
                    <span className="flex-1 font-medium">{item.name}</span>
                    <span className="text-gray-600 font-medium bg-white px-2 py-1 rounded shadow-sm">{item.quantity} {item.unit}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border p-12">
          <EmptyState icon={ShoppingCart} title="Empty Grocery List" description="Generate a meal plan first to see your grocery list." />
        </div>
      )}
    </div>
  );
}
