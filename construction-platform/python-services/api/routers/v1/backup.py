# Backup Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/backup.py
# Database and file backup status

from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter(prefix="/backup", tags=["backup"])

BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")


@router.get("/status")
async def get_backup_status():
    """Get backup system status"""
    backup_count = 0
    latest_backup = None
    total_size = 0
    
    if os.path.exists(BACKUP_DIR):
        files = []
        for filename in os.listdir(BACKUP_DIR):
            filepath = os.path.join(BACKUP_DIR, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                files.append({
                    "filename": filename,
                    "size": size,
                    "modified": mtime
                })
                total_size += size
        
        backup_count = len(files)
        if files:
            files.sort(key=lambda x: x["modified"], reverse=True)
            latest_backup = {
                "filename": files[0]["filename"],
                "size_bytes": files[0]["size"],
                "date": files[0]["modified"].isoformat()
            }
    
    return {
        "status": "operational",
        "backup_directory": BACKUP_DIR,
        "directory_exists": os.path.exists(BACKUP_DIR),
        "total_backups": backup_count,
        "total_size_bytes": total_size,
        "latest_backup": latest_backup
    }


@router.get("/list")
async def list_backups():
    """List all available backups"""
    backups = []
    
    if os.path.exists(BACKUP_DIR):
        for filename in os.listdir(BACKUP_DIR):
            filepath = os.path.join(BACKUP_DIR, filename)
            if os.path.isfile(filepath):
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                backups.append({
                    "filename": filename,
                    "size_bytes": os.path.getsize(filepath),
                    "created": mtime.isoformat()
                })
        
        backups.sort(key=lambda x: x["created"], reverse=True)
    
    return {
        "total_backups": len(backups),
        "backups": backups[:50]  # Limit to 50
    }
