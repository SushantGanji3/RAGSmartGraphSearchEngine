# Setup Instructions

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- (Optional) OpenAI API key for enhanced RAG features

## Step 1: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key (optional but recommended):
```env
OPENAI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./knowledge_base.db
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
```

5. Ingest data from Wikipedia:
```bash
python ingest_data.py "Artificial Intelligence" 50
```

This will:
- Scrape 50 Wikipedia articles about AI
- Generate embeddings
- Build the FAISS vector index
- Store metadata in SQLite

6. Start the backend server:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Step 2: Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Step 3: Using Docker (Alternative)

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

This will start both backend and frontend services.

## Testing the Application

1. Open `http://localhost:3000` in your browser
2. Try searching for topics like:
   - "machine learning"
   - "neural networks"
   - "deep learning"
3. Use the "Ask Question" mode to get RAG-powered answers
4. View the knowledge graph visualization

## API Endpoints

- `GET /search?query=...&top_k=5` - Semantic search
- `POST /ask` - RAG-powered Q&A
  ```json
  {
    "question": "What is machine learning?",
    "top_k": 3
  }
  ```
- `GET /stats` - System statistics

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure all dependencies are installed
- **FAISS errors**: Ensure `faiss-cpu` is installed correctly
- **OpenAI errors**: Check your API key is valid

### Frontend Issues

- **CORS errors**: Ensure backend is running on port 8000
- **API connection errors**: Check `REACT_APP_API_URL` in environment

### Data Ingestion Issues

- **Wikipedia rate limits**: Reduce the number of pages or add delays
- **Memory issues**: Process data in smaller batches

## Expected Output

When running the project, you should see:

1. **Backend**: FastAPI server running on port 8000 with API documentation at `/docs`
2. **Frontend**: React app with search interface, results display, and knowledge graph
3. **Search Results**: Ranked documents with similarity scores
4. **RAG Answers**: Contextual answers based on retrieved documents
5. **Knowledge Graph**: Interactive visualization of document relationships

