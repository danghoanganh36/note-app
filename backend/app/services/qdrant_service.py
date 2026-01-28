"""
Qdrant client utility for Handbook Compass
Provides async operations for vector search and document storage
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any, Optional
from app.core.config import settings


class QdrantService:
    """Service for interacting with Qdrant vector database"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_CLUSTER_ENDPOINT,
            api_key=settings.QDRANT_API_KEY,
        )
        self.collection_name = settings.QDRANT_COLLECTION_NAME
    
    def ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,  # sentence-transformers/all-MiniLM-L6-v2
                    distance=Distance.COSINE
                )
            )
    
    def upsert_vectors(
        self,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Insert or update vectors in Qdrant
        
        Args:
            vectors: List of embedding vectors
            payloads: List of metadata for each vector
            ids: Optional list of IDs (auto-generated if not provided)
        """
        points = [
            PointStruct(
                id=ids[i] if ids else i,
                vector=vectors[i],
                payload=payloads[i]
            )
            for i in range(len(vectors))
        ]
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_vector: Query embedding vector
            limit: Number of results to return
            score_threshold: Minimum similarity score
            
        Returns:
            List of search results with payload and score
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        
        return [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload
            }
            for hit in results
        ]
    
    def delete_by_filter(self, filter_condition: Dict[str, Any]) -> None:
        """Delete vectors matching filter condition"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=filter_condition
        )
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection statistics"""
        info = self.client.get_collection(self.collection_name)
        return {
            "name": info.config.params.vectors,
            "points_count": info.points_count,
            "status": info.status
        }


# Singleton instance
qdrant_service = QdrantService()
