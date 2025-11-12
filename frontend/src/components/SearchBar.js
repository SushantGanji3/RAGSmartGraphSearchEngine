import React, { useState } from 'react';

const SearchBar = ({ onSearch, onAsk, loading }) => {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('search'); // 'search' or 'ask'

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      if (mode === 'search') {
        onSearch(query);
      } else {
        onAsk(query);
      }
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-8">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex gap-2 mb-4">
          <button
            type="button"
            onClick={() => setMode('search')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              mode === 'search'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            🔍 Search
          </button>
          <button
            type="button"
            onClick={() => setMode('ask')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              mode === 'ask'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            💬 Ask Question
          </button>
        </div>
        
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={mode === 'search' ? "Search the knowledge base..." : "Ask a question..."}
            className="flex-1 px-6 py-4 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? '⏳' : mode === 'search' ? 'Search' : 'Ask'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SearchBar;

