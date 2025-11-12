# 🚀 Quick Start Guide - How to Run the Project

## Prerequisites Check

Make sure you have:
- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed
- ✅ All dependencies installed (already done!)

## Step-by-Step Instructions

### Step 1: Ingest Data (First Time Only)

Before you can search, you need to populate the knowledge base with data:

```bash
cd backend
source venv/bin/activate
python ingest_data.py "Artificial Intelligence" 50
```

**Expected Output:**
```
🚀 Starting data ingestion for topic: Artificial Intelligence

📥 Scraping Wikipedia...
Scraped: Artificial intelligence
Scraped: Machine learning
Scraped: Deep learning
Scraped: Neural network
... (continues for 50 articles)

Scraped 50 documents. Saved to data/Artificial_Intelligence_data.json

💾 Storing documents in database...
✅ Stored 50 documents in database

🔢 Generating embeddings...
100%|████████████████████| 50/50 [00:30<00:00,  1.67it/s]

📊 Building vector index...
✅ Vector index built with 50 vectors

🎉 Data ingestion complete!
```

**Time:** ~2-5 minutes depending on your internet speed

### Step 2: Start Backend Server

Open a terminal and run:

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Will watch for changes
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
🚀 Smart Knowledge Graph Search Engine starting...
No OpenAI API key found, using SentenceTransformers
Using SentenceTransformers: all-MiniLM-L6-v2
Warning: OpenAI API key not found. RAG will return template responses.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Backend is now running on http://localhost:8000**

### Step 3: Start Frontend (New Terminal)

Open a **new terminal window** and run:

```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiling...
Compiled successfully!

You can now view rag-search-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

**✅ Frontend is now running on http://localhost:3000**

### Step 4: Open in Browser

Open your browser and go to:
```
http://localhost:3000
```

## What You'll See

### Initial Screen

1. **Header**: "🧠 Smart Knowledge Graph" with subtitle
2. **Stats Panel**: Shows system statistics
   - Total Documents: 50
   - Vector Index Size: 50
   - Average Latency: ~50ms
3. **Search Bar**: Two buttons
   - 🔍 Search (default)
   - 💬 Ask Question
4. **Empty State**: "Enter a search query or ask a question to get started"

### After Searching (e.g., "machine learning")

**Search Results Section:**
- Title: "Search Results for 'machine learning' (5 results)"
- 5 result cards, each showing:
  - Document title (e.g., "Machine learning")
  - Similarity score badge (e.g., "87.3% match")
  - Content snippet (first 200 characters)
  - "View source →" link to Wikipedia

**Knowledge Graph:**
- Interactive D3.js visualization
- Nodes representing documents
- Edges showing relationships
- Draggable nodes

### After Asking a Question (e.g., "What is neural network?")

**Answer Card:**
- Question displayed at top
- Generated answer in white card
- Supporting documents list below

**Knowledge Graph:**
- Shows relationships between supporting documents

## Testing the API Directly

You can also test the backend API directly:

### 1. Visit API Documentation
```
http://localhost:8000/docs
```
Interactive Swagger UI where you can test endpoints

### 2. Test Search Endpoint
```bash
curl "http://localhost:8000/search?query=machine%20learning&top_k=5"
```

**Expected Response:**
```json
{
  "results": [
    {
      "id": 1,
      "title": "Machine learning",
      "content": "Machine learning is a method...",
      "source_link": "https://en.wikipedia.org/wiki/Machine_learning",
      "similarity_score": 0.9234,
      "snippet": "Machine learning is a method of data analysis..."
    },
    ...
  ],
  "query": "machine learning",
  "total_results": 5
}
```

### 3. Test Ask Endpoint
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is deep learning?", "top_k": 3}'
```

**Expected Response:**
```json
{
  "answer": "Based on the retrieved documents (Deep learning, Neural network, Artificial neural network), here's what I found related to your question: 'What is deep learning?'. Please review the search results for detailed information.",
  "supporting_documents": [
    "Deep learning",
    "Neural network",
    "Artificial neural network"
  ],
  "question": "What is deep learning?"
}
```

### 4. Test Stats Endpoint
```bash
curl "http://localhost:8000/stats"
```

**Expected Response:**
```json
{
  "total_documents": 50,
  "index_size": 50,
  "average_latency_ms": 50.0,
  "last_indexed": null
}
```

## Example Queries to Try

### Search Mode:
- "machine learning"
- "neural networks"
- "deep learning"
- "artificial intelligence"
- "natural language processing"

### Ask Question Mode:
- "What is machine learning?"
- "How do neural networks work?"
- "What are the applications of AI?"
- "Explain deep learning"

## Troubleshooting

### Backend won't start
- ✅ Check virtual environment is activated
- ✅ Check port 8000 is not in use
- ✅ Verify data was ingested (check for `faiss_index.bin`)

### Frontend won't start
- ✅ Check port 3000 is not in use
- ✅ Verify `node_modules` exists
- ✅ Check backend is running first

### No search results
- ✅ Make sure you ran `ingest_data.py` first
- ✅ Check `knowledge_base.db` exists
- ✅ Verify `faiss_index.bin` exists

### CORS errors
- ✅ Backend CORS is configured for localhost:3000
- ✅ Both servers must be running

## Performance Expectations

- **Search latency**: < 100ms per query
- **Embedding generation**: ~1-2 seconds per batch
- **RAG answer**: 2-5 seconds (with OpenAI) or instant (template)
- **Vector search**: < 50ms for top-5 results

## Next Steps

1. Try different search queries
2. Explore the knowledge graph visualization
3. Test the Ask Question feature
4. Check the API documentation at `/docs`
5. (Optional) Add OpenAI API key for better results

## Stopping the Servers

- **Backend**: Press `CTRL+C` in the backend terminal
- **Frontend**: Press `CTRL+C` in the frontend terminal

---

**You're all set! Enjoy exploring the Smart Knowledge Graph Search Engine! 🎉**

