# Error Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/errors.py
# Error tracking and analytics

from fastapi import APIRouter, Query
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/errors", tags=["errors"])


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


@router.get("/recent")
async def get_recent_errors(
    limit: int = Query(50, description="Maximum number of errors to return"),
    hours: int = Query(24, description="Errors from the last N hours")
):
    """Get recent errors"""
    start_date = datetime.now() - timedelta(hours=hours)
    errors = []
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Check if error_logs table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'error_logs'
                )
            """)
            if cur.fetchone()[0]:
                cur.execute("""
                    SELECT id, error_type, message, endpoint, timestamp, stack_trace
                    FROM error_logs 
                    WHERE timestamp >= %s
                    ORDER BY timestamp DESC
                    LIMIT %s
                """, (start_date, limit))
                
                for row in cur.fetchall():
                    errors.append({
                        "id": row[0],
                        "type": row[1],
                        "message": row[2],
                        "endpoint": row[3],
                        "timestamp": row[4].isoformat() if row[4] else None
                    })
            
            cur.close()
            conn.close()
        except Exception:
            pass
    
    return {
        "period_hours": hours,
        "total_errors": len(errors),
        "errors": errors
    }


@router.get("/summary")
async def get_error_summary(days: int = Query(7, description="Summary for the last N days")):
    """Get error summary statistics"""
    start_date = datetime.now() - timedelta(days=days)
    
    summary = {
        "period_days": days,
        "total_errors": 0,
        "errors_by_type": {},
        "errors_by_endpoint": {},
        "system_status": "healthy"
    }
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'error_logs'
                )
            """)
            if cur.fetchone()[0]:
                # Errors by type
                cur.execute("""
                    SELECT error_type, COUNT(*) as count
                    FROM error_logs 
                    WHERE timestamp >= %s
                    GROUP BY error_type
                    ORDER BY count DESC
                """, (start_date,))
                
                for row in cur.fetchall():
                    summary["errors_by_type"][row[0] or "unknown"] = row[1]
                    summary["total_errors"] += row[1]
                
                # Errors by endpoint
                cur.execute("""
                    SELECT endpoint, COUNT(*) as count
                    FROM error_logs 
                    WHERE timestamp >= %s
                    GROUP BY endpoint
                    ORDER BY count DESC
                    LIMIT 10
                """, (start_date,))
                
                for row in cur.fetchall():
                    summary["errors_by_endpoint"][row[0] or "unknown"] = row[1]
            
            cur.close()
            conn.close()
        except Exception:
            pass
    
    # Set system status based on error count
    if summary["total_errors"] > 100:
        summary["system_status"] = "degraded"
    elif summary["total_errors"] > 500:
        summary["system_status"] = "critical"
    
    return summary
