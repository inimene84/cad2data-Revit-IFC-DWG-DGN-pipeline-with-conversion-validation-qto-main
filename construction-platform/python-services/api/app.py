from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List
from prometheus_client import Counter, Histogram, Gauge, Info
import pandas as pd
import io
import json
import math
from typing import Dict, Any, List, Optional
import logging
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import asyncio
import aiofiles
import redis
from datetime import datetime, timedelta
import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
import uvicorn

# Custom JSON encoder to handle infinity/NaN values
class SafeJSONEncoder(json.JSONEncoder):
    """JSON encoder that converts inf/nan to null to avoid serialization errors"""
    def default(self, obj):
        try:
            if isinstance(obj, float):
                if math.isnan(obj) or math.isinf(obj):
                    return None
            return super().default(obj)
        except TypeError:
            return str(obj)

def sanitize_for_json(obj):
    """Recursively sanitize an object for JSON serialization"""
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif hasattr(obj, 'isoformat'):  # datetime objects
        return obj.isoformat()
    return obj

# Phase 2 Improvements - Import with graceful degradation
try:
    from rate_limiting import rate_limit_middleware
    from cache import CacheService, CACHE_NAMESPACES
    from error_handler import ErrorHandler, ErrorType
    from validation import UploadFileRequest, AnalyticsRequest, MaterialCalculationRequest
    from circuit_breaker import CircuitBreaker, circuit_breaker
    PHASE2_IMPROVEMENTS_AVAILABLE = True
except ImportError as e:
    # Phase 2 improvements not available - continue without them
    PHASE2_IMPROVEMENTS_AVAILABLE = False
    rate_limit_middleware = None
    CacheService = None
    CACHE_NAMESPACES = {}
    ErrorHandler = None
    ErrorType = None
    UploadFileRequest = None
    AnalyticsRequest = None
    MaterialCalculationRequest = None
    CircuitBreaker = None
    circuit_breaker = None

# Phase 3 Improvements - Import with graceful degradation
try:
    from multi_tenancy import tenant_manager, get_tenant_id, require_tenant
    from usage_analytics import UsageTracker, initialize_usage_tracker
    from billing import billing_manager
    from error_analytics import ErrorAnalytics, initialize_error_analytics
    from audit_logging import AuditLogger, initialize_audit_logger, AuditEventType
    from vector_db import VectorDBService, initialize_vector_db
    from archival import ArchivalService, initialize_archival_service
    from opentelemetry_config import setup_opentelemetry
    PHASE3_IMPROVEMENTS_AVAILABLE = True
except ImportError as e:
    # Phase 3 improvements not available - continue without them
    PHASE3_IMPROVEMENTS_AVAILABLE = False
    tenant_manager = None
    get_tenant_id = None
    require_tenant = None
    UsageTracker = None
    initialize_usage_tracker = None
    billing_manager = None
    ErrorAnalytics = None
    initialize_error_analytics = None
    AuditLogger = None
    initialize_audit_logger = None
    AuditEventType = None
    VectorDBService = None
    initialize_vector_db = None
    ArchivalService = None
    initialize_archival_service = None
    setup_opentelemetry = None

# Phase 4 Improvements - Import with graceful degradation
try:
    from db_optimization import db_optimizer, initialize_db_optimizer
    from automation_rules import automation_engine, RuleTrigger, RuleAction
    from security import (
        SecurityHeadersMiddleware,
        RateLimitMiddleware,
        AuthenticationMiddleware,
        CSRFProtectionMiddleware
    )
    from backup_recovery import backup_manager
    PHASE4_IMPROVEMENTS_AVAILABLE = True
except ImportError as e:
    # Phase 4 improvements not available - continue without them
    PHASE4_IMPROVEMENTS_AVAILABLE = False
    db_optimizer = None
    initialize_db_optimizer = None
    automation_engine = None
    RuleTrigger = None
    RuleAction = None
    SecurityHeadersMiddleware = None
    RateLimitMiddleware = None
    AuthenticationMiddleware = None
    CSRFProtectionMiddleware = None
    backup_manager = None

from config import MATERIAL_KEYWORDS, REGIONAL_MULTIPLIERS

# API Versioning
# API Versioning
# Import directly to ensure we fail fast if routers are broken
from routers.v1 import v1_router
from routers.v1.materials import materials_db, material_counter
API_VERSIONING_AVAILABLE = True

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log Phase 2 status
if not PHASE2_IMPROVEMENTS_AVAILABLE:
    logger.warning("Phase 2 improvements not available - continuing without them")

from utils.redis_client import redis_client, redis_available

# Thread pool for CPU-intensive tasks
executor = ThreadPoolExecutor(max_workers=4)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket client: {e}")
    
    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            self.disconnect(conn)

websocket_manager = ConnectionManager()


# API Versioning
from routers.v1 import v1_router
from routers.v1.extraction import router as extraction_router

app = FastAPI(
    title="Construction AI Agent API",
    version="2.0.0",
    description="Estonian Construction Material Takeoff & Cost Estimation API",
    openapi_version="3.1.0",
    openapi_tags=[
        {"name": "v1", "description": "API Version 1 endpoints"},
        {"name": "health", "description": "Health check endpoints"},
        {"name": "analytics", "description": "Analytics endpoints"},
        {"name": "usage", "description": "Usage analytics endpoints"},
        {"name": "billing", "description": "Billing endpoints"},
        {"name": "errors", "description": "Error analytics endpoints"},
        {"name": "audit", "description": "Audit logging endpoints"},
        {"name": "vector", "description": "Vector database endpoints"},
        {"name": "archival", "description": "Archival endpoints"},
        {"name": "automation", "description": "Automation rules endpoints"},
        {"name": "backup", "description": "Backup and recovery endpoints"},
    ],
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configuration - restrict origins for security
allowed_origins = os.getenv(
    'ALLOWED_ORIGINS',
    '*'
).split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Custom middleware to sanitize JSON responses (prevent inf/nan errors)
@app.middleware("http")
async def sanitize_json_response(request: Request, call_next):
    """Middleware to catch and fix JSON serialization errors"""
    try:
        response = await call_next(request)
        return response
    except ValueError as e:
        if "Out of range float values" in str(e) or "not JSON compliant" in str(e):
            logger.warning(f"JSON serialization error caught and handled: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Data serialization error", "detail": "Response contained non-serializable values"}
            )
        raise

# Include versioned routers
app.include_router(v1_router)

# Mount static files
os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/output", StaticFiles(directory="output"), name="output")

# Phase 2: Add rate limiting middleware
if PHASE2_IMPROVEMENTS_AVAILABLE and rate_limit_middleware:
    app.middleware("http")(rate_limit_middleware)
    logger.info("Rate limiting middleware enabled")
    
    # Initialize enhanced cache service
    if CacheService and redis_client:
        try:
            cache_service = CacheService(redis_client)
            logger.info("Enhanced cache service initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize enhanced cache service: {e}")
            cache_service = None
    else:
        cache_service = None
else:
    cache_service = None
    logger.info("Phase 2 improvements not available or disabled")

# Phase 3: Initialize advanced features
if PHASE3_IMPROVEMENTS_AVAILABLE:
    # Initialize usage tracker
    if redis_client:
        initialize_usage_tracker(redis_client)
        logger.info("Usage tracker initialized")
    
    # Initialize error analytics
    if redis_client:
        initialize_error_analytics(redis_client)
        logger.info("Error analytics initialized")
    
    # Initialize audit logger
    if redis_client:
        initialize_audit_logger(redis_client)
        logger.info("Audit logger initialized")
    
    # Initialize vector DB
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    initialize_vector_db(qdrant_url)
    logger.info("Vector DB initialized")
    
    # Initialize archival service
    archive_dir = os.getenv("ARCHIVE_DIR", "archives")
    retention_days = int(os.getenv("RETENTION_DAYS", "90"))
    initialize_archival_service(archive_dir, retention_days)
    logger.info("Archival service initialized")
    
    # Setup OpenTelemetry if enabled
    if os.getenv("ENABLE_OPENTELEMETRY", "false").lower() == "true":
        setup_opentelemetry()
        logger.info("OpenTelemetry configured")
else:
    logger.info("Phase 3 improvements not available or disabled")

# Phase 4: Initialize optimization features
if PHASE4_IMPROVEMENTS_AVAILABLE:
    # Initialize database optimizer
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/construction_ai")
    pool_size = int(os.getenv("DB_POOL_SIZE", "20"))
    max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    try:
        initialize_db_optimizer(database_url, pool_size, max_overflow)
        logger.info("Database optimizer initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize database optimizer: {e}")
    
    # Add security middlewares
    if SecurityHeadersMiddleware:
        try:
            app.add_middleware(SecurityHeadersMiddleware)
            logger.info("Security headers middleware enabled")
        except Exception as e:
            logger.warning(f"Failed to enable security headers middleware: {e}")
    
    if RateLimitMiddleware:
        try:
            rate_limit_calls = int(os.getenv("RATE_LIMIT_CALLS", "100"))
            rate_limit_period = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
            app.add_middleware(RateLimitMiddleware, calls=rate_limit_calls, period=rate_limit_period)
            logger.info("Rate limiting middleware enabled")
        except Exception as e:
            logger.warning(f"Failed to enable rate limiting middleware: {e}")
    
    if AuthenticationMiddleware:
        try:
            api_keys = os.getenv("API_KEYS", "").split(",")
            api_keys = [key.strip() for key in api_keys if key.strip()]
            if api_keys:
                app.add_middleware(AuthenticationMiddleware, api_keys=api_keys)
                logger.info("Authentication middleware enabled")
        except Exception as e:
            logger.warning(f"Failed to enable authentication middleware: {e}")
    
    if CSRFProtectionMiddleware:
        try:
            app.add_middleware(CSRFProtectionMiddleware)
            logger.info("CSRF protection middleware enabled")
        except Exception as e:
            logger.warning(f"Failed to enable CSRF protection middleware: {e}")
else:
    logger.info("Phase 4 improvements not available or disabled")

# ==========================================
# PROMETHEUS METRICS SETUP
# ==========================================

from utils.metrics import (
    instrumentator, 
    pdf_processing_counter, 
    excel_processing_counter,
    material_calculation_counter,
    document_processing_time,
    materials_detected_histogram,
    cache_hit_counter,
    cache_miss_counter,
    redis_connection_status,
    estonian_pricing_requests,
    total_cost_calculated
)
from utils.redis_client import redis_available, redis_client

# Set initial Redis status
redis_connection_status.set(1 if redis_available else 0)

# Instrument app and expose metrics
instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=True)

logger.info("Prometheus metrics instrumentation enabled at /metrics")

# Cache helper functions


@app.get("/")
async def root():
    return {
        "message": "Construction AI Agent API v2.0.0", 
        "status": "running", 
        "features": ["caching", "async_processing", "estonian_support", "prometheus_metrics"],
        "metrics_endpoint": "/metrics"
    }

@app.get("/health")
async def health():
    cache_status = "connected" if redis_client else "disconnected"
    redis_connection_status.set(1 if redis_client else 0)
    
    return {
        "status": "healthy", 
        "version": "2.0.0",
        "cache": cache_status,
        "timestamp": datetime.now().isoformat(),
        "metrics_enabled": True
    }

# Logic moved to services/pdf_processing.py

# Extraction endpoints moved to routers/v1/extraction.py
app.include_router(extraction_router)

# Load Estonian Material Cost Database from JSON file
try:
    with open('material_prices.json', 'r', encoding='utf-8') as f:
        ESTONIAN_MATERIAL_COSTS = json.load(f)
    logger.info(f"Loaded {len(ESTONIAN_MATERIAL_COSTS)} material prices from JSON file.")
except FileNotFoundError:
    ESTONIAN_MATERIAL_COSTS = {}
    logger.warning("material_prices.json not found, using empty dict. Material costs will use defaults.")
except Exception as e:
    ESTONIAN_MATERIAL_COSTS = {}
    logger.error(f"Error loading material_prices.json: {e}, using empty dict")

def get_estonian_material_cost(material_name: str, region: str = "Tartu") -> Dict:
    """Get current material cost in Estonia"""
    material_lower = material_name.lower()
    
    multiplier = REGIONAL_MULTIPLIERS.get(region, 1.00)
    
    # Track pricing requests
    material_type = 'other'
    for material_key in ESTONIAN_MATERIAL_COSTS.keys():
        if material_key in material_lower:
            material_type = material_key
            break
    
    estonian_pricing_requests.labels(
        region=region,
        material_type=material_type
    ).inc()
    
    # Find matching material
    for material_key, cost_data in ESTONIAN_MATERIAL_COSTS.items():
        if material_key in material_lower:
            result = cost_data.copy()
            result["price"] *= multiplier
            result["region"] = region
            result["last_updated"] = datetime.now().isoformat()
            return result
    
    # Default cost if not found
    logger.warning(f"Material '{material_name}' not found in Estonian price database. Using default.")
    return {
        "price": 50.00,
        "unit": "unit",
        "currency": "EUR",
        "supplier": "Unknown",
        "region": region,
        "last_updated": datetime.now().isoformat()
    }

@app.post("/calculate-materials")
async def calculate_materials(materials: List[Dict], region: str = "Tartu"):
    """Calculate total cost for a list of materials."""
    start_time = datetime.now()
    
    total_cost = 0
    summary = []
    
    for item in materials:
        material_name = item.get('material')
        quantity = item.get('quantity')
        
        if not material_name or not quantity:
            continue
            
        cost_data = get_estonian_material_cost(material_name, region)
        
        item_cost = cost_data['price'] * quantity
        total_cost += item_cost
        
        summary.append({
            "material": material_name,
            "quantity": quantity,
            "unit": cost_data['unit'],
            "cost_per_unit": cost_data['price'],
            "total_cost": item_cost,
            "supplier": cost_data.get('supplier', 'N/A')
        })

    vat_amount = total_cost * 0.22  # Estonian VAT 2024-2025 (changed from 22% to 22%)
    total_cost_with_vat = total_cost + vat_amount
    
    # Record metrics
    material_calculation_counter.labels(region=region, status='success').inc()
    total_cost_calculated.observe(total_cost_with_vat)
    
    processing_time = (datetime.now() - start_time).total_seconds()

    return {
        "status": "success",
        "region": region,
        "total_cost_without_vat": round(total_cost, 2),
        "vat_amount": round(vat_amount, 2),
        "total_cost_with_vat": round(total_cost_with_vat, 2),
        "material_types": len(summary),
        "summary": summary,
        "processing_time_seconds": processing_time
    }

@app.post("/generate-report")
async def generate_report(report_data: Dict):
    """Generate a PDF report."""
    try:
        project_name = report_data.get("project_name", "Construction Project")
        summary = report_data.get("summary", {})
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Title
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, 750, project_name)
        
        # Summary
        p.setFont("Helvetica", 12)
        p.drawString(100, 720, f"Total Cost (excl. VAT): €{summary.get('total_cost_without_vat', 0):.2f}")
        p.drawString(100, 700, f"VAT (24%): €{summary.get('vat_amount', 0):.2f}")
        p.drawString(100, 680, f"Total Cost (incl. VAT): €{summary.get('total_cost_with_vat', 0):.2f}")
        
        # Material details
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 640, "Material Breakdown")
        
        p.setFont("Helvetica", 10)
        y = 610
        for item in summary.get("summary", []):
            p.drawString(100, y, f"- {item['material']}: {item['quantity']} {item['unit']} @ €{item['cost_per_unit']}/{item['unit']} = €{item['total_cost']:.2f}")
            y -= 20
            if y < 50:
                p.showPage()
                y = 750

        p.save()
        
        pdf_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {"status": "success", "pdf_base64": pdf_base64}

    except Exception as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time workflow updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or process message
            await websocket_manager.send_personal_message({
                "type": "echo",
                "message": data
            }, websocket)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

# Function to broadcast workflow updates
async def broadcast_workflow_update(workflow_id: str, status: str, progress: int, message: str = ""):
    """Broadcast workflow update to all connected WebSocket clients"""
    await websocket_manager.broadcast({
        "type": "workflow_update",
        "id": workflow_id,
        "status": status,
        "progress": progress,
        "message": message
    })

# Analytics API endpoints
@app.get("/api/analytics/cost-trends")
async def get_cost_trends(period: str = "30d"):
    """Get cost trends for the specified period"""
    from datetime import datetime, timedelta
    days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}.get(period, 30)
    start_date = datetime.now() - timedelta(days=days)
    
    # Placeholder data - replace with actual database query
    trends = [
        {"date": "2025-01-01", "total_cost": 50000, "material_cost": 30000, "labor_cost": 20000},
        {"date": "2025-01-02", "total_cost": 55000, "material_cost": 32000, "labor_cost": 23000},
        {"date": "2025-01-03", "total_cost": 52000, "material_cost": 31000, "labor_cost": 21000},
        {"date": "2025-01-04", "total_cost": 58000, "material_cost": 34000, "labor_cost": 24000},
    ]
    
    return trends

@app.get("/api/analytics/material-breakdown")
async def get_material_breakdown(period: str = "30d"):
    """Get material breakdown for the specified period"""
    # Placeholder data - replace with actual database query
    breakdown = [
        {"name": "Concrete", "value": 15000},
        {"name": "Steel", "value": 12000},
        {"name": "Wood", "value": 8000},
        {"name": "Brick", "value": 6000},
        {"name": "Other", "value": 5000}
    ]
    
    return breakdown

@app.get("/api/analytics/processing-metrics")
async def get_processing_metrics(period: str = "30d"):
    """Get processing metrics for the specified period"""
    # Placeholder data - replace with actual database query
    metrics = {
        "files_processed": 150,
        "avg_processing_time": 12.5,
        "success_rate": 95.5,
        "total_elements": 276931
    }
    
    return metrics


# Phase 3: Usage Analytics API endpoints
if PHASE3_IMPROVEMENTS_AVAILABLE:
    from fastapi import Request
    from usage_analytics import usage_tracker
    from error_analytics import error_analytics
    from audit_logging import audit_logger
    from vector_db import vector_db_service
    from archival import archival_service
    
    def get_tenant_id_from_request(request: Request) -> str:
        """Get tenant ID from request"""
        if tenant_manager:
            return tenant_manager.get_tenant_id(request)
        return "default"
    
    @app.get("/api/usage/stats")
    async def get_usage_stats_api(request: Request, period: str = "30d"):
        """Get usage statistics for tenant"""
        tenant_id = get_tenant_id_from_request(request)
        if usage_tracker:
            return usage_tracker.get_usage_stats(tenant_id, period)
        return {"error": "Usage tracker not available"}
    
    @app.get("/api/usage/breakdown")
    async def get_usage_breakdown_api(request: Request, period: str = "30d"):
        """Get usage breakdown by endpoint"""
        tenant_id = get_tenant_id_from_request(request)
        if usage_tracker:
            return usage_tracker.get_usage_breakdown(tenant_id, period)
        return {"error": "Usage tracker not available"}
    
    @app.get("/api/billing/summary")
    async def get_billing_summary_api(request: Request):
        """Get billing summary for tenant"""
        tenant_id = get_tenant_id_from_request(request)
        if billing_manager:
            return billing_manager.get_billing_summary(tenant_id)
        return {"error": "Billing manager not available"}
    
    @app.get("/api/billing/invoice")
    async def generate_invoice_api(request: Request, period: str = "monthly"):
        """Generate invoice for tenant"""
        tenant_id = get_tenant_id_from_request(request)
        if billing_manager:
            return billing_manager.generate_invoice(tenant_id, period)
        return {"error": "Billing manager not available"}
    
    @app.get("/api/errors/stats")
    async def get_error_stats_api(request: Request, period: str = "30d"):
        """Get error statistics"""
        tenant_id = get_tenant_id_from_request(request)
        if error_analytics:
            return error_analytics.get_error_stats(tenant_id, period)
        return {"error": "Error analytics not available"}
    
    @app.get("/api/errors/analysis")
    async def analyze_errors_api(request: Request, period: str = "30d"):
        """Analyze error patterns"""
        tenant_id = get_tenant_id_from_request(request)
        if error_analytics:
            return error_analytics.analyze_error_patterns(tenant_id, period)
        return {"error": "Error analytics not available"}
    
    @app.get("/api/audit/logs")
    async def get_audit_logs_api(request: Request, limit: int = 100):
        """Get audit logs"""
        tenant_id = get_tenant_id_from_request(request)
        if audit_logger:
            return audit_logger.get_audit_logs(tenant_id, limit=limit)
        return {"error": "Audit logger not available"}
    
    @app.post("/api/vector/search")
    async def search_similar_estimates_api(query_vector: List[float], limit: int = 10):
        """Search for similar cost estimates"""
        if vector_db_service:
            return vector_db_service.search_similar_estimates(query_vector, limit)
        return {"error": "Vector DB service not available"}
    
    @app.post("/api/archival/archive")
    async def archive_old_files_api(request: Request, days_old: int = 90):
        """Archive old files"""
        tenant_id = get_tenant_id_from_request(request)
        if archival_service:
            archived_count = archival_service.archive_old_files(tenant_id, days_old)
            return {"status": "success", "archived_count": archived_count}
        return {"error": "Archival service not available"}



# Phase 2: Add global exception handler
if PHASE2_IMPROVEMENTS_AVAILABLE and ErrorHandler:
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler with user-friendly error messages"""
        return await ErrorHandler.exception_handler(request, exc)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
