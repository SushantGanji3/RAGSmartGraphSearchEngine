import React, { useState, useEffect } from 'react';
import { searchAPI } from '../services/api';

const StatsPanel = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await searchAPI.getStats();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-gray-100 rounded-lg p-6 text-center">
        <p>Loading statistics...</p>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  return (
    <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg shadow-md p-6 mb-8">
      <h3 className="text-xl font-bold text-gray-800 mb-4">📊 System Statistics</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <p className="text-sm text-gray-600">Total Documents</p>
          <p className="text-3xl font-bold text-blue-600">{stats.total_documents}</p>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <p className="text-sm text-gray-600">Vector Index Size</p>
          <p className="text-3xl font-bold text-green-600">{stats.index_size}</p>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <p className="text-sm text-gray-600">Avg Latency</p>
          <p className="text-3xl font-bold text-purple-600">{stats.average_latency_ms.toFixed(0)}ms</p>
        </div>
      </div>
    </div>
  );
};

export default StatsPanel;

