import React from 'react';

const SearchResults = ({ results, query }) => {
  if (!results || results.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No results found for "{query}"</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      <h2 className="text-2xl font-bold mb-6">
        Search Results for "{query}" ({results.length} results)
      </h2>
      
      {results.map((result, index) => (
        <div
          key={result.id}
          className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border-l-4 border-blue-500"
        >
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-xl font-semibold text-gray-800">
              {index + 1}. {result.title}
            </h3>
            <span className="text-sm font-medium text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
              {(result.similarity_score * 100).toFixed(1)}% match
            </span>
          </div>
          
          <p className="text-gray-600 mb-4 line-clamp-3">
            {result.snippet}
          </p>
          
          <a
            href={result.source_link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center gap-1"
          >
            View source →
          </a>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;

