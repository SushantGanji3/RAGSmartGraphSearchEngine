# Smart Knowledge Graph Search Engine (RAG-Powered)

A semantic search engine that scrapes structured text data, generates vector embeddings, and performs semantic search with RAG (Retrieval-Augmented Generation).

## 🎯 Features

- ✅ Large-scale information retrieval
- ✅ Semantic ranking with vector databases (FAISS)
- ✅ RAG-powered contextual answers
- ✅ Knowledge graph visualization
- ✅ Scalable backend system design
- ✅ Modern web UI with React and Tailwind CSS

## 🏗️ Architecture

```
Frontend (React + Tailwind) 
    ↓ REST API
Backend (FastAPI)
    ↓
┌─────────────┬──────────────┬──────────────┐
│ PostgreSQL  │ FAISS Vector │ LangChain    │
│ (Metadata)  │ (Embeddings) │ (RAG)        │
└─────────────┴──────────────┴──────────────┘
    ↓              ↓
Data Ingestion  Knowledge Graph
(Wikipedia API)  (NetworkX)
```

## 🚀 Quick Start

See [SETUP.md](SETUP.md) for detailed setup instructions.

### Quick Setup

1. **Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI API key
python ingest_data.py "Artificial Intelligence" 50
python -m uvicorn app.main:app --reload
```

2. **Frontend Setup:**
```bash
cd frontend
npm install
npm start
```

3. **Or use Docker:**
```bash
docker-compose up --build
```

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./knowledge_base.db
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
```

## 📁 Project Structure

```
smart-knowledge-search/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── rag.py
│   │   └── scraper.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   └── services/
│   └── package.json
└── README.md
```

## 🔧 API Endpoints

- `GET /search?query=...` - Semantic search
- `POST /ask` - RAG-powered Q&A
- `GET /stats` - System statistics

## 📊 Technologies

- **Frontend**: React.js, Tailwind CSS, D3.js
- **Backend**: FastAPI, Python
- **Vector DB**: FAISS
- **Embeddings**: OpenAI / SentenceTransformers
- **RAG**: LangChain
- **Database**: SQLite / PostgreSQL
- **Graph**: NetworkX

## 📝 License

MIT

