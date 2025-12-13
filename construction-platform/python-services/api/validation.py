# Input Validation Layer with Pydantic
# construction-platform/python-services/api/validation.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum
import re

class FileType(str, Enum):
    """Supported file types"""
    PDF = "pdf"
    EXCEL = "excel"
    DWG = "dwg"
    IFC = "ifc"
    RVT = "rvt"
    DGN = "dgn"
    IMAGE = "image"

class UploadFileRequest(BaseModel):
    """Request model for file upload"""
    file_name: str = Field(..., min_length=1, max_length=255)
    file_type: FileType
    file_size: int = Field(..., gt=0, le=100_000_000)  # Max 100MB
    project_name: Optional[str] = Field(None, min_length=1, max_length=100)
    workflow_type: Optional[str] = Field("auto", min_length=1, max_length=50)
    
    @validator("file_name")
    def validate_file_name(cls, v):
        """Validate file name"""
        if not re.match(r"^[a-zA-Z0-9._-]+$", v):
            raise ValueError("Invalid file name format")
        return v
    
    @validator("file_type")
    def validate_file_type(cls, v):
        """Validate file type"""
        if v not in FileType:
            raise ValueError(f"Unsupported file type: {v}")
        return v

class AnalyticsRequest(BaseModel):
    """Request model for analytics"""
    period: str = Field("30d", pattern="^(7d|30d|90d|1y)$")
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    @validator("period")
    def validate_period(cls, v):
        """Validate period"""
        valid_periods = ["7d", "30d", "90d", "1y"]
        if v not in valid_periods:
            raise ValueError(f"Invalid period: {v}. Must be one of {valid_periods}")
        return v

class MaterialCalculationRequest(BaseModel):
    """Request model for material calculation"""
    materials: List[Dict[str, Any]] = Field(..., min_length=1)
    region: str = Field("Tartu", min_length=1, max_length=50)
    include_vat: bool = Field(True)
    
    @validator("materials")
    def validate_materials(cls, v):
        """Validate materials list"""
        required_fields = ["material", "quantity", "unit"]
        for material in v:
            for field in required_fields:
                if field not in material:
                    raise ValueError(f"Missing required field: {field}")
        return v

class ReportGenerationRequest(BaseModel):
    """Request model for report generation"""
    project_name: str = Field(..., min_length=1, max_length=100)
    summary: Dict[str, Any] = Field(..., min_items=1)
    include_vat: bool = Field(True)
    include_suppliers: bool = Field(False)
    
    @validator("summary")
    def validate_summary(cls, v):
        """Validate summary"""
        if not isinstance(v, dict):
            raise ValueError("Summary must be a dictionary")
        return v
