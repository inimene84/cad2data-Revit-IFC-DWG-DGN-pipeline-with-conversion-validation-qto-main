# Archival Endpoints - Version 1
# construction-platform/python-services/api/routers/v1/archival.py
# File archival and cleanup endpoints

from fastapi import APIRouter, Query
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/archival", tags=["archival"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
ARCHIVE_DIR = os.getenv("ARCHIVE_DIR", "archives")


@router.get("/status")
async def get_archival_status():
    """Get current archival system status"""
    upload_files = 0
    archive_files = 0
    
    if os.path.exists(UPLOAD_DIR):
        upload_files = len([f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))])
    
    if os.path.exists(ARCHIVE_DIR):
        archive_files = len([f for f in os.listdir(ARCHIVE_DIR) if os.path.isfile(os.path.join(ARCHIVE_DIR, f))])
    
    return {
        "status": "operational",
        "upload_directory": UPLOAD_DIR,
        "archive_directory": ARCHIVE_DIR,
        "files_in_uploads": upload_files,
        "files_in_archive": archive_files,
        "retention_days": int(os.getenv("RETENTION_DAYS", "90"))
    }


@router.get("/old-files")
async def list_old_files(days: int = Query(90, description="Files older than this many days")):
    """List files that are candidates for archival"""
    cutoff_date = datetime.now() - timedelta(days=days)
    old_files = []
    
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            filepath = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(filepath):
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mtime < cutoff_date:
                    old_files.append({
                        "filename": filename,
                        "size_bytes": os.path.getsize(filepath),
                        "modified": mtime.isoformat(),
                        "age_days": (datetime.now() - mtime).days
                    })
    
    return {
        "cutoff_date": cutoff_date.isoformat(),
        "cutoff_days": days,
        "files_found": len(old_files),
        "files": old_files[:100]  # Limit to 100 files
    }
