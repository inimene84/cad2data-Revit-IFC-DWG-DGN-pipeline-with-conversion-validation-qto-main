# Vector DB Integration - Supports both Qdrant and Supabase
# construction-platform/python-services/api/vector_db.py

from typing import Dict, Any, Optional, List
import logging
import os

logger = logging.getLogger(__name__)

# Global vector DB service instance
vector_db_service = None

class VectorDBService:
    """Vector database service for similarity search - supports Qdrant and Supabase"""
    
    def __init__(self, backend: str = "auto", **kwargs):
        """
        Initialize vector database service
        
        Args:
            backend: "qdrant", "supabase", or "auto" (auto-detect from env)
            **kwargs: Backend-specific configuration
        """
        self.backend = backend
        
        if backend == "auto":
            # Auto-detect based on environment variables
            if os.getenv("USE_SUPABASE", "").lower() == "true":
                self.backend = "supabase"
            else:
                self.backend = "qdrant"
        
        logger.info(f"Initializing Vector DB with backend: {self.backend}")
        
        if self.backend == "supabase":
            self._init_supabase(**kwargs)
        else:
            self._init_qdrant(**kwargs)
    
    def _init_supabase(self, **kwargs):
        """Initialize Supabase as vector backend"""
        try:
            from supabase import create_client
            
            supabase_url = kwargs.get("supabase_url") or os.getenv("SUPABASE_URL")
            supabase_key = kwargs.get("supabase_key") or os.getenv("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
            
            self.client = create_client(supabase_url, supabase_key)
            self.table_name = kwargs.get("table_name", "cost_estimates")
            self.collection_name = self.table_name  # Alias for compatibility
            
            logger.info(f"Supabase Vector DB connected: {supabase_url}")
            logger.info(f"Using table: {self.table_name}")
            
        except ImportError:
            logger.error("Supabase library not installed. Install with: pip install supabase")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            self.client = None
    
    def _init_qdrant(self, **kwargs):
        """Initialize Qdrant as vector backend"""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            
            qdrant_url = kwargs.get("qdrant_url") or os.getenv("QDRANT_URL", "http://localhost:6333")
            self.client = QdrantClient(url=qdrant_url)
            self.collection_name = kwargs.get("collection_name", "cost_estimates")
            self._ensure_qdrant_collection()
            
            logger.info(f"Qdrant Vector DB connected: {qdrant_url}")
            
        except ImportError:
            logger.error("Qdrant library not installed. Install with: pip install qdrant-client")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            self.client = None
    
    def _ensure_qdrant_collection(self):
        """Ensure Qdrant collection exists"""
        if not self.client or self.backend != "qdrant":
            return
        
        try:
            from qdrant_client.models import Distance, VectorParams
            
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                logger.info(f"Qdrant collection created: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to ensure Qdrant collection: {e}")
    
    def add_cost_estimate(
        self,
        estimate_id: str,
        vector: List[float],
        metadata: Dict[str, Any]
    ) -> bool:
        """Add cost estimate to vector database"""
        if not self.client:
            return False
        
        try:
            if self.backend == "supabase":
                return self._add_supabase_estimate(estimate_id, vector, metadata)
            else:
                return self._add_qdrant_estimate(estimate_id, vector, metadata)
        except Exception as e:
            logger.error(f"Failed to add cost estimate: {e}")
            return False
    
    def _add_supabase_estimate(self, estimate_id: str, vector: List[float], metadata: Dict[str, Any]) -> bool:
        """Add estimate to Supabase"""
        data = {
            "id": estimate_id,
            "embedding": vector,
            **metadata
        }
        
        result = self.client.table(self.table_name).upsert(data).execute()
        logger.info(f"Supabase: Cost estimate added: {estimate_id}")
        return True
    
    def _add_qdrant_estimate(self, estimate_id: str, vector: List[float], metadata: Dict[str, Any]) -> bool:
        """Add estimate to Qdrant"""
        from qdrant_client.models import PointStruct
        
        point = PointStruct(
            id=estimate_id,
            vector=vector,
            payload=metadata
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        
        logger.info(f"Qdrant: Cost estimate added: {estimate_id}")
        return True
    
    def search_similar_estimates(
        self,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar cost estimates"""
        if not self.client:
            return []
        
        try:
            if self.backend == "supabase":
                return self._search_supabase(query_vector, limit, score_threshold)
            else:
                return self._search_qdrant(query_vector, limit, score_threshold)
        except Exception as e:
            logger.error(f"Failed to search similar estimates: {e}")
            return []
    
    def _search_supabase(self, query_vector: List[float], limit: int, score_threshold: float) -> List[Dict[str, Any]]:
        """Search using Supabase pgvector"""
        # Use RPC function for vector similarity search
        result = self.client.rpc(
            'match_cost_estimates',
            {
                'query_embedding': query_vector,
                'match_threshold': score_threshold,
                'match_count': limit
            }
        ).execute()
        
        similar_estimates = []
        for row in result.data:
            similar_estimates.append({
                "id": row.get("id"),
                "score": row.get("similarity", 0),
                "metadata": {k: v for k, v in row.items() if k not in ["id", "embedding", "similarity"]}
            })
        
        logger.info(f"Supabase: Found {len(similar_estimates)} similar estimates")
        return similar_estimates
    
    def _search_qdrant(self, query_vector: List[float], limit: int, score_threshold: float) -> List[Dict[str, Any]]:
        """Search using Qdrant"""
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold
        )
        
        similar_estimates = []
        for result in results:
            similar_estimates.append({
                "id": result.id,
                "score": result.score,
                "metadata": result.payload
            })
        
        logger.info(f"Qdrant: Found {len(similar_estimates)} similar estimates")
        return similar_estimates
    
    def get_estimate_by_id(self, estimate_id: str) -> Optional[Dict[str, Any]]:
        """Get cost estimate by ID"""
        if not self.client:
            return None
        
        try:
            if self.backend == "supabase":
                result = self.client.table(self.table_name).select("*").eq("id", estimate_id).execute()
                if result.data:
                    row = result.data[0]
                    return {
                        "id": row.get("id"),
                        "metadata": {k: v for k, v in row.items() if k not in ["id", "embedding"]}
                    }
                return None
            else:
                result = self.client.retrieve(
                    collection_name=self.collection_name,
                    ids=[estimate_id]
                )
                
                if result:
                    return {
                        "id": result[0].id,
                        "metadata": result[0].payload
                    }
                
                return None
        except Exception as e:
            logger.error(f"Failed to get estimate by ID: {e}")
            return None
    
    def delete_estimate(self, estimate_id: str) -> bool:
        """Delete cost estimate from vector database"""
        if not self.client:
            return False
        
        try:
            if self.backend == "supabase":
                self.client.table(self.table_name).delete().eq("id", estimate_id).execute()
                logger.info(f"Supabase: Cost estimate deleted: {estimate_id}")
            else:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=[estimate_id]
                )
                logger.info(f"Qdrant: Cost estimate deleted: {estimate_id}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to delete cost estimate: {e}")
            return False


def initialize_vector_db(**kwargs):
    """
    Initialize vector DB service
    
    Supports both Qdrant and Supabase backends.
    Auto-detects from USE_SUPABASE environment variable.
    """
    global vector_db_service
    vector_db_service = VectorDBService(backend="auto", **kwargs)
    return vector_db_service
