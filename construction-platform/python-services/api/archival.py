# Automated Archival
# construction-platform/python-services/api/archival.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import os
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

class ArchivalService:
    """Automated archival service for old files"""
    def __init__(self, archive_dir: str = "archives", retention_days: int = 90, s3_client=None):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
        self.retention_days = retention_days
        self.s3_client = s3_client
        self.archived_files: Dict[str, Dict[str, Any]] = {}
    
    def archive_file(self, file_path: str, tenant_id: str = "default") -> bool:
        """Archive file to S3 Glacier or local archive"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                logger.warning(f"File not found: {file_path}")
                return False
            
            # Generate archive path
            archive_path = self.archive_dir / tenant_id / file_path_obj.name
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file to archive
            shutil.copy2(file_path, archive_path)
            
            # If S3 client available, upload to S3 Glacier
            if self.s3_client:
                try:
                    s3_key = f"archives/{tenant_id}/{file_path_obj.name}"
                    self.s3_client.upload_file(
                        file_path,
                        "construction-ai-archives",
                        s3_key,
                        ExtraArgs={"StorageClass": "GLACIER"}
                    )
                    logger.info(f"File archived to S3 Glacier: {s3_key}")
                except Exception as e:
                    logger.error(f"Failed to upload to S3: {e}")
            
            # Record archival
            self.archived_files[file_path] = {
                "tenant_id": tenant_id,
                "original_path": file_path,
                "archive_path": str(archive_path),
                "archived_at": datetime.now().isoformat(),
                "file_size": file_path_obj.stat().st_size
            }
            
            # Delete original file
            file_path_obj.unlink()
            
            logger.info(f"File archived: {file_path} -> {archive_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to archive file: {e}")
            return False
    
    def archive_old_files(self, tenant_id: str = "default", days_old: int = None) -> int:
        """Archive files older than specified days"""
        try:
            days_old = days_old or self.retention_days
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            archived_count = 0
            
            # Get files from uploads directory
            uploads_dir = Path("uploads") / tenant_id
            if uploads_dir.exists():
                for file_path in uploads_dir.iterdir():
                    if file_path.is_file():
                        file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_mtime < cutoff_date:
                            if self.archive_file(str(file_path), tenant_id):
                                archived_count += 1
            
            logger.info(f"Archived {archived_count} old files for tenant {tenant_id}")
            return archived_count
        except Exception as e:
            logger.error(f"Failed to archive old files: {e}")
            return 0
    
    def restore_file(self, archive_path: str, restore_path: str) -> bool:
        """Restore file from archive"""
        try:
            archive_path_obj = Path(archive_path)
            if not archive_path_obj.exists():
                logger.warning(f"Archive file not found: {archive_path}")
                return False
            
            restore_path_obj = Path(restore_path)
            restore_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file from archive
            shutil.copy2(archive_path, restore_path)
            
            logger.info(f"File restored: {archive_path} -> {restore_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore file: {e}")
            return False
    
    def get_archived_files(self, tenant_id: str = "default") -> List[Dict[str, Any]]:
        """Get list of archived files"""
        try:
            archived_files = []
            
            archive_dir = self.archive_dir / tenant_id
            if archive_dir.exists():
                for file_path in archive_dir.iterdir():
                    if file_path.is_file():
                        archived_files.append({
                            "file_name": file_path.name,
                            "archive_path": str(file_path),
                            "file_size": file_path.stat().st_size,
                            "archived_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })
            
            return archived_files
        except Exception as e:
            logger.error(f"Failed to get archived files: {e}")
            return []

# Global archival service instance
archival_service = None

def initialize_archival_service(archive_dir: str = "archives", retention_days: int = 90, s3_client=None):
    """Initialize archival service"""
    global archival_service
    archival_service = ArchivalService(archive_dir, retention_days, s3_client)
    return archival_service
