import React from 'react';

export const YouTubeEmbed = ({ url }) => {
  if (!url) return <div className="bg-gray-100 p-8 text-center rounded-xl text-gray-500">Video unavailable</div>;
  
  let videoId = '';
  try {
    if (url.includes('youtube.com/watch')) {
      videoId = new URL(url).searchParams.get('v');
    } else if (url.includes('youtu.be/')) {
      videoId = url.split('youtu.be/')[1].split('?')[0];
    }
  } catch (e) {
    // Ignore invalid URLs
  }

  if (!videoId) return <div className="bg-gray-100 p-8 text-center rounded-xl text-gray-500">Video unavailable</div>;

  return (
    <div className="aspect-w-16 aspect-h-9 w-full rounded-xl overflow-hidden">
      <iframe
        className="w-full h-full min-h-[300px]"
        src={`https://www.youtube.com/embed/${videoId}`}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        title="Recipe Video"
      ></iframe>
    </div>
  );
};
