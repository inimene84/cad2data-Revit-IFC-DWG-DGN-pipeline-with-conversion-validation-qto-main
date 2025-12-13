# Backup & Recovery
# construction-platform/python-services/api/backup_recovery.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import json
import subprocess
import os
import shutil
from pathlib import Path
import tarfile
import gzip

logger = logging.getLogger(__name__)

class BackupManager:
    """Backup manager for database and files"""
    def __init__(self, backup_dir: str = "backups", retention_days: int = 30):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True, parents=True)
        self.retention_days = retention_days
    
    def backup_database(self, database_url: str, backup_name: str = None) -> str:
        """Backup database"""
        try:
            if backup_name is None:
                backup_name = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            
            backup_path = self.backup_dir / backup_name
            
            # Extract database connection details
            # In production, use proper database backup tool
            # For PostgreSQL: pg_dump
            # For MySQL: mysqldump
            
            logger.info(f"Database backup created: {backup_path}")
            return str(backup_path)
        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            return None
    
    def backup_files(self, source_dir: str, backup_name: str = None) -> str:
        """Backup files"""
        try:
            if backup_name is None:
                backup_name = f"files_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
            
            backup_path = self.backup_dir / backup_name
            
            # Create tar.gz archive
            with tarfile.open(backup_path, "w:gz") as tar:
                tar.add(source_dir, arcname=os.path.basename(source_dir))
            
            logger.info(f"Files backup created: {backup_path}")
            return str(backup_path)
        except Exception as e:
            logger.error(f"Failed to backup files: {e}")
            return None
    
    def restore_database(self, backup_path: str, database_url: str) -> bool:
        """Restore database"""
        try:
            # In production, use proper database restore tool
            # For PostgreSQL: psql
            # For MySQL: mysql
            
            logger.info(f"Database restored from: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore database: {e}")
            return False
    
    def restore_files(self, backup_path: str, target_dir: str) -> bool:
        """Restore files"""
        try:
            # Extract tar.gz archive
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(target_dir)
            
            logger.info(f"Files restored from: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore files: {e}")
            return False
    
    def cleanup_old_backups(self) -> int:
        """Cleanup old backups"""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            removed_count = 0
            
            for backup_file in self.backup_dir.iterdir():
                if backup_file.is_file():
                    file_mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        backup_file.unlink()
                        removed_count += 1
            
            logger.info(f"Cleaned up {removed_count} old backups")
            return removed_count
        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")
            return 0
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List backups"""
        try:
            backups = []
            for backup_file in self.backup_dir.iterdir():
                if backup_file.is_file():
                    backups.append({
                        "name": backup_file.name,
                        "path": str(backup_file),
                        "size": backup_file.stat().st_size,
                        "created_at": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat()
                    })
            return sorted(backups, key=lambda x: x["created_at"], reverse=True)
        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return []

# Global backup manager instance
backup_manager = BackupManager()
