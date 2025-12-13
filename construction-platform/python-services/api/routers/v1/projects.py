# Projects Router - Version 1
# construction-platform/python-services/api/routers/v1/projects.py

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime, date
import logging
import math

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["projects"])

# In-memory storage
projects_db: dict = {}
project_counter = 0


def sanitize_value(value: Any) -> Any:
    """Sanitize value for JSON serialization"""
    if value is None:
        return None
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: sanitize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_value(v) for v in value]
    return value


class ProjectCreate(BaseModel):
    name: str
    status: str = "pending"
    progress: int = 0
    deadline: Optional[date] = None
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    deadline: Optional[date] = None
    description: Optional[str] = None


@router.get("")
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None
):
    """List all projects with optional filtering and pagination."""
    projects = list(projects_db.values())
    
    if status:
        projects = [p for p in projects if p["status"] == status]
    
    projects = projects[skip:skip + limit]
    
    return [sanitize_value(p) for p in projects]


@router.get("/{project_id}")
async def get_project(project_id: int):
    """Get a single project by ID."""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return sanitize_value(projects_db[project_id])


@router.post("", status_code=201)
async def create_project(project: ProjectCreate):
    """Create a new project."""
    global project_counter
    project_counter += 1
    
    now = datetime.now()
    new_project = {
        "id": project_counter,
        "name": project.name,
        "status": project.status,
        "progress": project.progress,
        "deadline": project.deadline,
        "description": project.description,
        "materials_count": 0,
        "created_at": now,
        "updated_at": now
    }
    
    projects_db[project_counter] = new_project
    logger.info(f"Created project: {project.name} (ID: {project_counter})")
    
    return sanitize_value(new_project)


@router.put("/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate):
    """Update an existing project."""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    existing = projects_db[project_id]
    
    update_data = project.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            existing[key] = value
    
    existing["updated_at"] = datetime.now()
    projects_db[project_id] = existing
    
    logger.info(f"Updated project ID: {project_id}")
    return sanitize_value(existing)


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int):
    """Delete a project."""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    del projects_db[project_id]
    logger.info(f"Deleted project ID: {project_id}")
    return None


@router.get("/{project_id}/stats")
async def get_project_stats(project_id: int):
    """Get statistics for a project."""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    
    return {
        "project_id": project_id,
        "name": project["name"],
        "materials_count": project["materials_count"],
        "status": project["status"],
        "progress": project["progress"],
        "days_until_deadline": None
    }
