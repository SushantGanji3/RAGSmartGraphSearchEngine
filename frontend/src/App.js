import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import AnswerCard from './components/AnswerCard';
import KnowledgeGraph from './components/KnowledgeGraph';
import StatsPanel from './components/StatsPanel';
import { searchAPI } from './services/api';

function App() {
  const [searchResults, setSearchResults] = useState([]);
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentQuery, setCurrentQuery] = useState('');

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    setAnswer(null);
    setCurrentQuery(query);
    
    try {
      const data = await searchAPI.search(query, 5);
      setSearchResults(data.results || []);
    } catch (err) {
      setError(err.message || 'Search failed. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async (question) => {
    setLoading(true);
    setError(null);
    setSearchResults([]);
    setCurrentQuery(question);
    
    try {
      const data = await searchAPI.ask(question, 3);
      setAnswer(data);
    } catch (err) {
      setError(err.message || 'Failed to generate answer. Please try again.');
      console.error('Ask error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            🧠 Smart Knowledge Graph
          </h1>
          <p className="text-xl text-gray-600">
            RAG-Powered Semantic Search Engine
          </p>
        </header>

        {/* Stats Panel */}
        <StatsPanel />

        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} onAsk={handleAsk} loading={loading} />

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Searching...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6 max-w-4xl mx-auto">
            <p className="font-semibold">Error:</p>
            <p>{error}</p>
          </div>
        )}

        {/* Answer Card (for Ask mode) */}
        {answer && !loading && (
          <AnswerCard
            answer={answer.answer}
            question={answer.question}
            supportingDocuments={answer.supporting_documents}
          />
        )}

        {/* Search Results */}
        {searchResults.length > 0 && !loading && (
          <>
            <SearchResults results={searchResults} query={currentQuery} />
            <KnowledgeGraph results={searchResults} />
          </>
        )}

        {/* Empty State */}
        {!loading && !error && searchResults.length === 0 && !answer && (
          <div className="text-center py-12 text-gray-500">
            <p className="text-lg">Enter a search query or ask a question to get started</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="text-center py-6 text-gray-600 mt-12">
        <p>Smart Knowledge Graph Search Engine - Powered by RAG & FAISS</p>
      </footer>
    </div>
  );
}

export default App;

