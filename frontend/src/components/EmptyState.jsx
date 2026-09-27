import React from 'react';

export const EmptyState = ({ icon: Icon, title, description, actionText, onAction }) => (
  <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
      {Icon && <Icon className="w-8 h-8 text-gray-400" />}
    </div>
    <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
    <p className="text-gray-500 max-w-sm mb-6">{description}</p>
    {actionText && onAction && (
      <button
        onClick={onAction}
        className="px-6 py-2 bg-brand-600 text-white font-medium rounded-lg hover:bg-brand-700 transition"
      >
        {actionText}
      </button>
    )}
  </div>
);

export const LoadingSkeleton = ({ count = 1 }) => (
  <div className="space-y-4">
    {Array.from({ length: count }).map((_, i) => (
      <div key={i} className="animate-pulse bg-white p-4 rounded-xl border flex space-x-4">
        <div className="rounded-lg bg-gray-200 h-24 w-24"></div>
        <div className="flex-1 space-y-3 py-1">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    ))}
  </div>
);
