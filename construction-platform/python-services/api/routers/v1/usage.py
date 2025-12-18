# Usage Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/usage.py
# Real usage statistics from system

from fastapi import APIRouter
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/usage", tags=["usage"])


def get_db_connection():
    """Get PostgreSQL database connection"""
    try:
        import psycopg2
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "postgres"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            user=os.getenv("POSTGRES_USER", "construction_user"),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            database=os.getenv("POSTGRES_DB", "construction_db")
        )
    except Exception:
        return None


@router.get("/stats")
async def get_usage_stats(period: str = "30d"):
    """Get system usage statistics"""
    days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
    start_date = datetime.now() - timedelta(days=days)
    
    stats = {
        "period": period,
        "projects": 0,
        "materials": 0,
        "cost_estimates": 0,
        "api_status": "operational"
    }
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Count projects
            cur.execute("SELECT COUNT(*) FROM projects WHERE created_at >= %s", (start_date,))
            result = cur.fetchone()
            stats["projects"] = result[0] if result else 0
            
            # Count materials
            cur.execute("SELECT COUNT(*) FROM materials WHERE created_at >= %s", (start_date,))
            result = cur.fetchone()
            stats["materials"] = result[0] if result else 0
            
            # Count cost estimates
            cur.execute("SELECT COUNT(*) FROM cost_estimates WHERE created_at >= %s", (start_date,))
            result = cur.fetchone()
            stats["cost_estimates"] = result[0] if result else 0
            
            # Total project cost
            cur.execute("SELECT COALESCE(SUM(total_cost), 0) FROM cost_estimates WHERE created_at >= %s", (start_date,))
            result = cur.fetchone()
            stats["total_estimated_cost"] = float(result[0]) if result else 0
            
            cur.close()
            conn.close()
            stats["data_source"] = "database"
        except Exception as e:
            stats["data_source"] = "error"
            stats["error"] = str(e)
    else:
        stats["data_source"] = "unavailable"
    
    return stats


@router.get("/summary")
async def get_usage_summary():
    """Get overall usage summary"""
    summary = {
        "timestamp": datetime.now().isoformat(),
        "system_status": "operational"
    }
    
    # Check QDRANT
    try:
        from qdrant_client import QdrantClient
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        client = QdrantClient(host=qdrant_host, port=qdrant_port, timeout=5)
        collections = client.get_collections()
        summary["qdrant_status"] = "connected"
        summary["qdrant_collections"] = len(collections.collections)
    except Exception as e:
        summary["qdrant_status"] = f"error: {str(e)}"
    
    # Check database
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            conn.close()
            summary["database_status"] = "connected"
        except Exception:
            summary["database_status"] = "error"
    else:
        summary["database_status"] = "unavailable"
    
    return summary
