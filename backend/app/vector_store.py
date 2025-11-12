"""FAISS vector store for semantic search."""
import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple

class FAISSVectorStore:
    """FAISS-based vector store for efficient similarity search."""
    
    def __init__(self, dimension: int = 384, index_path: str = "faiss_index.bin"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = None
        self.id_to_doc = {}  # Map FAISS ID to document ID
        self.doc_to_id = {}  # Map document ID to FAISS ID
        
    def create_index(self, use_gpu: bool = False):
        """Create a new FAISS index."""
        # Use IndexFlatL2 for exact search (can upgrade to IndexIVFFlat for speed)
        self.index = faiss.IndexFlatL2(self.dimension)
        if use_gpu:
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)
    
    def add_vectors(self, vectors: np.ndarray, doc_ids: List[int]):
        """Add vectors to the index."""
        if self.index is None:
            self.create_index()
        
        # Normalize vectors for cosine similarity
        faiss.normalize_L2(vectors)
        
        start_id = self.index.ntotal
        self.index.add(vectors.astype('float32'))
        
        # Map FAISS IDs to document IDs
        for i, doc_id in enumerate(doc_ids):
            faiss_id = start_id + i
            self.id_to_doc[faiss_id] = doc_id
            self.doc_to_id[doc_id] = faiss_id
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[int, float]]:
        """Search for similar vectors."""
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Normalize query vector
        query_vector = query_vector.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query_vector)
        
        # Search
        distances, indices = self.index.search(query_vector, top_k)
        
        # Convert FAISS IDs to document IDs
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx != -1:  # Valid result
                doc_id = self.id_to_doc.get(idx, idx)
                similarity = 1 - dist  # Convert L2 distance to similarity
                results.append((doc_id, float(similarity)))
        
        return results
    
    def save(self, path: str = None):
        """Save index and mappings to disk."""
        path = path or self.index_path
        if self.index is not None:
            faiss.write_index(self.index, path)
            # Save mappings
            mapping_path = path.replace('.bin', '_mappings.pkl')
            with open(mapping_path, 'wb') as f:
                pickle.dump({
                    'id_to_doc': self.id_to_doc,
                    'doc_to_id': self.doc_to_id,
                    'dimension': self.dimension
                }, f)
    
    def load(self, path: str = None):
        """Load index and mappings from disk."""
        path = path or self.index_path
        if os.path.exists(path):
            self.index = faiss.read_index(path)
            # Load mappings
            mapping_path = path.replace('.bin', '_mappings.pkl')
            if os.path.exists(mapping_path):
                with open(mapping_path, 'rb') as f:
                    mappings = pickle.load(f)
                    self.id_to_doc = mappings.get('id_to_doc', {})
                    self.doc_to_id = mappings.get('doc_to_id', {})
                    self.dimension = mappings.get('dimension', 384)
            return True
        return False
    
    def get_stats(self) -> dict:
        """Get index statistics."""
        return {
            'total_vectors': self.index.ntotal if self.index else 0,
            'dimension': self.dimension,
            'index_type': type(self.index).__name__ if self.index else None
        }

