import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchAPI = {
  search: async (query, topK = 5) => {
    const response = await api.get('/search', {
      params: { query, top_k: topK },
    });
    return response.data;
  },

  ask: async (question, topK = 3) => {
    const response = await api.post('/ask', {
      question,
      top_k: topK,
    });
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/stats');
    return response.data;
  },
};

export default api;

