# Expected Output

This document describes what you should see when running the Smart Knowledge Graph Search Engine.

## 1. Backend Server Output

When you start the backend with `python -m uvicorn app.main:app --reload`, you should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
🚀 Smart Knowledge Graph Search Engine starting...
INFO:     Application startup complete.
```

### API Documentation

Visit `http://localhost:8000/docs` to see the interactive API documentation (Swagger UI).

## 2. Data Ingestion Output

When running `python ingest_data.py "Artificial Intelligence" 50`, you should see:

```
🚀 Starting data ingestion for topic: Artificial Intelligence

📥 Scraping Wikipedia...
Scraped: Artificial intelligence
Scraped: Machine learning
Scraped: Deep learning
...
Scraped 50 documents. Saved to data/Artificial_Intelligence_data.json

💾 Storing documents in database...
✅ Stored 50 documents in database

🔢 Generating embeddings...
100%|████████████████████| 50/50 [00:30<00:00,  1.67it/s]

📊 Building vector index...
✅ Vector index built with 50 vectors

🎉 Data ingestion complete!
```

## 3. Frontend Application

When you open `http://localhost:3000`, you should see:

### Initial Screen:
- **Header**: "🧠 Smart Knowledge Graph" with subtitle "RAG-Powered Semantic Search Engine"
- **Stats Panel**: Shows total documents, index size, and average latency
- **Search Bar**: Two modes - "🔍 Search" and "💬 Ask Question"
- **Empty State**: "Enter a search query or ask a question to get started"

### After Searching (e.g., "machine learning"):
- **Search Results Section**:
  - Title: "Search Results for 'machine learning' (5 results)"
  - 5 result cards, each showing:
    - Document title
    - Similarity score (e.g., "87.3% match")
    - Snippet of content
    - "View source →" link
- **Knowledge Graph**: Interactive D3.js visualization showing document relationships

### After Asking a Question (e.g., "What is neural network?"):
- **Answer Card**:
  - Question displayed at top
  - Generated answer in a white card
  - Supporting documents list below
- **Knowledge Graph**: Shows relationships between supporting documents

## 4. API Response Examples

### GET /search?query=machine%20learning&top_k=5

```json
{
  "results": [
    {
      "id": 1,
      "title": "Machine learning",
      "content": "Machine learning is a method of data analysis...",
      "source_link": "https://en.wikipedia.org/wiki/Machine_learning",
      "similarity_score": 0.9234,
      "snippet": "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence..."
    },
    ...
  ],
  "query": "machine learning",
  "total_results": 5
}
```

### POST /ask

Request:
```json
{
  "question": "What is deep learning?",
  "top_k": 3
}
```

Response:
```json
{
  "answer": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to learn representations of data. It has been particularly successful in areas such as image recognition, natural language processing, and speech recognition...",
  "supporting_documents": [
    "Deep learning",
    "Neural network",
    "Artificial neural network"
  ],
  "question": "What is deep learning?"
}
```

### GET /stats

```json
{
  "total_documents": 50,
  "index_size": 50,
  "average_latency_ms": 45.2,
  "last_indexed": null
}
```

## 5. Console Output (Browser)

When using the frontend, check the browser console (F12) for:
- API request logs
- Any errors (should be none if setup correctly)
- Network requests to `http://localhost:8000`

## 6. Error Scenarios

### If no data is ingested:
- Search returns: "No results found"
- Stats shows: `total_documents: 0, index_size: 0`

### If OpenAI API key is missing:
- RAG answers will use template responses
- Console shows: "Warning: OpenAI API key not found. RAG will return template responses."

### If backend is not running:
- Frontend shows: "Error: Network Error" or "Failed to fetch"
- Browser console shows CORS or connection errors

## 7. Performance Metrics

Expected performance:
- **Search latency**: < 100ms per query
- **Embedding generation**: ~1-2 seconds per batch of 32 documents
- **RAG answer generation**: 2-5 seconds (with OpenAI API)
- **Vector search**: < 50ms for top-5 results

## 8. File Structure After Setup

```
RAGSearchEngine/
├── backend/
│   ├── knowledge_base.db          # SQLite database
│   ├── faiss_index.bin            # FAISS vector index
│   ├── faiss_index_mappings.pkl   # ID mappings
│   ├── data/
│   │   └── Artificial_Intelligence_data.json
│   └── .env                        # Your API keys
├── frontend/
│   └── node_modules/              # Dependencies
└── ...
```

## 9. Docker Output

When running `docker-compose up --build`:

```
Building backend...
Building frontend...
...
backend_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend_1 | Compiled successfully!
frontend_1 | You can now view rag-search-frontend in the browser.
```

Both services should be accessible at their respective ports.

