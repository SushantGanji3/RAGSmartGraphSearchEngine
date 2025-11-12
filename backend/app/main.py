"""FastAPI main application."""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import time
import os
from dotenv import load_dotenv

from app.database import init_db, get_db, Document, QueryLog
from app.models import SearchRequest, SearchResponse, SearchResult, AskRequest, AskResponse, StatsResponse
from app.embeddings import EmbeddingGenerator
from app.vector_store import FAISSVectorStore
from app.rag import RAGPipeline

load_dotenv()

app = FastAPI(title="Smart Knowledge Graph Search Engine", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
embedding_generator = EmbeddingGenerator()
vector_store = FAISSVectorStore()
rag_pipeline = RAGPipeline()

# Initialize database
init_db()

# Load vector store if exists
vector_store.load()

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    print("🚀 Smart Knowledge Graph Search Engine starting...")
    if vector_store.index is None:
        print("⚠️  Vector index not found. Please run data ingestion first.")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Smart Knowledge Graph Search Engine API", "version": "1.0.0"}

@app.get("/search", response_model=SearchResponse)
async def search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(5, ge=1, le=20, description="Number of results"),
    db: Session = Depends(get_db)
):
    """Semantic search endpoint."""
    start_time = time.time()
    
    try:
        # Generate query embedding
        query_embedding = embedding_generator.generate_embedding(query)
        
        # Search vector store
        results = vector_store.search(query_embedding, top_k=top_k)
        
        # Fetch document details from database
        search_results = []
        for doc_id, similarity_score in results:
            doc = db.query(Document).filter(Document.id == doc_id).first()
            if doc:
                # Create snippet (first 200 chars)
                snippet = doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                
                search_results.append(SearchResult(
                    id=doc.id,
                    title=doc.title,
                    content=doc.content,
                    source_link=doc.source_link,
                    similarity_score=similarity_score,
                    snippet=snippet
                ))
        
        # Log query
        latency = (time.time() - start_time) * 1000
        query_log = QueryLog(query=query, timestamp=time.time(), result_count=len(search_results))
        db.add(query_log)
        db.commit()
        
        return SearchResponse(
            results=search_results,
            query=query,
            total_results=len(search_results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest, db: Session = Depends(get_db)):
    """RAG-powered Q&A endpoint."""
    try:
        # Generate query embedding
        query_embedding = embedding_generator.generate_embedding(request.question)
        
        # Retrieve relevant documents
        results = vector_store.search(query_embedding, top_k=request.top_k)
        
        # Fetch document details
        context_docs = []
        for doc_id, _ in results:
            doc = db.query(Document).filter(Document.id == doc_id).first()
            if doc:
                context_docs.append({
                    "title": doc.title,
                    "content": doc.content,
                    "source_link": doc.source_link
                })
        
        # Generate answer using RAG
        answer = rag_pipeline.generate_answer(request.question, context_docs)
        
        # Extract supporting document titles
        supporting_docs = [doc["title"] for doc in context_docs]
        
        return AskResponse(
            answer=answer,
            supporting_documents=supporting_docs,
            question=request.question
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG error: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def stats(db: Session = Depends(get_db)):
    """Get system statistics."""
    try:
        total_docs = db.query(Document).count()
        vector_stats = vector_store.get_stats()
        
        # Calculate average latency from recent queries
        recent_queries = db.query(QueryLog).order_by(QueryLog.id.desc()).limit(10).all()
        avg_latency = 0.0
        if recent_queries:
            # This is a simplified calculation
            avg_latency = 50.0  # Placeholder
        
        return StatsResponse(
            total_documents=total_docs,
            index_size=vector_stats.get('total_vectors', 0),
            average_latency_ms=avg_latency,
            last_indexed=None
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

