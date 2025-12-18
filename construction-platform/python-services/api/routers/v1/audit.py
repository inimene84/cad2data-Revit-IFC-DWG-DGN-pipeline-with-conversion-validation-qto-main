# Audit Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/audit.py
# Audit logging and compliance endpoints

from fastapi import APIRouter, Query
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/audit", tags=["audit"])


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


@router.get("/logs")
async def get_audit_logs(
    limit: int = Query(100, description="Maximum number of logs to return"),
    days: int = Query(7, description="Logs from the last N days")
):
    """Get recent audit logs"""
    start_date = datetime.now() - timedelta(days=days)
    logs = []
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Check if audit_logs table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'audit_logs'
                )
            """)
            if cur.fetchone()[0]:
                cur.execute("""
                    SELECT id, action, entity_type, entity_id, user_id, timestamp, details
                    FROM audit_logs 
                    WHERE timestamp >= %s
                    ORDER BY timestamp DESC
                    LIMIT %s
                """, (start_date, limit))
                
                for row in cur.fetchall():
                    logs.append({
                        "id": row[0],
                        "action": row[1],
                        "entity_type": row[2],
                        "entity_id": row[3],
                        "user_id": row[4],
                        "timestamp": row[5].isoformat() if row[5] else None,
                        "details": row[6]
                    })
            
            cur.close()
            conn.close()
        except Exception as e:
            return {"error": str(e), "logs": []}
    
    return {
        "period_days": days,
        "total_logs": len(logs),
        "logs": logs
    }


@router.get("/summary")
async def get_audit_summary(days: int = Query(30, description="Summary for the last N days")):
    """Get audit summary statistics"""
    start_date = datetime.now() - timedelta(days=days)
    
    summary = {
        "period_days": days,
        "start_date": start_date.isoformat(),
        "end_date": datetime.now().isoformat(),
        "total_actions": 0,
        "actions_by_type": {}
    }
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'audit_logs'
                )
            """)
            if cur.fetchone()[0]:
                cur.execute("""
                    SELECT action, COUNT(*) as count
                    FROM audit_logs 
                    WHERE timestamp >= %s
                    GROUP BY action
                """, (start_date,))
                
                for row in cur.fetchall():
                    summary["actions_by_type"][row[0]] = row[1]
                    summary["total_actions"] += row[1]
            
            cur.close()
            conn.close()
        except Exception:
            pass
    
    return summary
