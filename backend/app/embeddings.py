"""Generate embeddings for text using OpenAI or SentenceTransformers."""
import os
from typing import List
from dotenv import load_dotenv
import numpy as np

load_dotenv()

class EmbeddingGenerator:
    """Generate vector embeddings for text."""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL", "sentence-transformers")
        self.model = None
        self.use_openai = False
        self.client = None
        
        # Try OpenAI first if API key is available
        if os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                self.use_openai = True
                self.model_name = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
                print(f"Using OpenAI embeddings: {self.model_name}")
            except Exception as e:
                print(f"OpenAI not available ({e}), falling back to SentenceTransformers")
                self._init_sentence_transformers()
        else:
            print("No OpenAI API key found, using SentenceTransformers")
            self._init_sentence_transformers()
    
    def _init_sentence_transformers(self):
        """Initialize SentenceTransformers model."""
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Using SentenceTransformers: all-MiniLM-L6-v2")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        if self.use_openai:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text
            )
            return np.array(response.data[0].embedding)
        else:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for multiple texts in batches."""
        embeddings = []
        
        if self.use_openai:
            # OpenAI batch processing
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.client.embeddings.create(
                    model=self.model_name,
                    input=batch
                )
                batch_embeddings = [np.array(item.embedding) for item in response.data]
                embeddings.extend(batch_embeddings)
        else:
            # SentenceTransformers batch processing
            embeddings = self.model.encode(texts, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=True)
        
        return np.array(embeddings)

