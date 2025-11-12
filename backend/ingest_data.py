"""Script to ingest data from Wikipedia and build the vector index."""
import os
import sys
from sqlalchemy.orm import Session
from app.database import init_db, SessionLocal, Document
from app.scraper import WikipediaScraper
from app.embeddings import EmbeddingGenerator
from app.vector_store import FAISSVectorStore
import numpy as np

def ingest_data(topic: str = "Artificial Intelligence", max_pages: int = 50):
    """Ingest Wikipedia data and build vector index."""
    print(f"🚀 Starting data ingestion for topic: {topic}")
    
    # Initialize components
    scraper = WikipediaScraper()
    embedding_gen = EmbeddingGenerator()
    vector_store = FAISSVectorStore()
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Scrape Wikipedia
        print("\n📥 Scraping Wikipedia...")
        documents = scraper.scrape_topic(topic, max_pages=max_pages)
        
        if not documents:
            print("❌ No documents scraped. Exiting.")
            return
        
        # Store in database and prepare for embedding
        print("\n💾 Storing documents in database...")
        texts = []
        doc_ids = []
        
        for doc in documents:
            # Check if document already exists
            existing = db.query(Document).filter(Document.title == doc["title"]).first()
            if existing:
                continue
            
            db_doc = Document(
                title=doc["title"],
                content=doc["content"],
                source_link=doc["source_link"],
                related_entities=doc.get("related_entities", [])
            )
            db.add(db_doc)
            db.flush()  # Get the ID
            
            # Prepare text for embedding (use summary + first part of content)
            text_for_embedding = f"{doc.get('summary', '')} {doc['content'][:1000]}"
            texts.append(text_for_embedding)
            doc_ids.append(db_doc.id)
        
        db.commit()
        print(f"✅ Stored {len(doc_ids)} documents in database")
        
        # Generate embeddings
        print("\n🔢 Generating embeddings...")
        embeddings = embedding_gen.generate_embeddings_batch(texts, batch_size=32)
        
        # Update dimension if needed
        if embeddings.shape[1] != vector_store.dimension:
            vector_store.dimension = embeddings.shape[1]
            vector_store.create_index()
        elif vector_store.index is None:
            vector_store.create_index()
        
        # Add to vector store
        print("\n📊 Building vector index...")
        vector_store.add_vectors(embeddings, doc_ids)
        
        # Update embedding_id in database
        for i, doc_id in enumerate(doc_ids):
            doc = db.query(Document).filter(Document.id == doc_id).first()
            if doc:
                doc.embedding_id = i
        
        db.commit()
        
        # Save vector store
        vector_store.save()
        print(f"✅ Vector index built with {len(doc_ids)} vectors")
        
        print("\n🎉 Data ingestion complete!")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exception(*sys.exc_info())
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Artificial Intelligence"
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    ingest_data(topic, max_pages)

