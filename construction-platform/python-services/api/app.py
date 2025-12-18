from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge, Info
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
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
try:
    from routers.v1 import v1_router
    API_VERSIONING_AVAILABLE = True
except ImportError:
    API_VERSIONING_AVAILABLE = False
    v1_router = None
    logger.warning("API versioning not available - routers not found")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log Phase 2 status
if not PHASE2_IMPROVEMENTS_AVAILABLE:
    logger.warning("Phase 2 improvements not available - continuing without them")

# Initialize Redis for caching
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'redis'), 
        port=6379, 
        db=0, 
        decode_responses=True
    )
    redis_client.ping()
    logger.info("Redis connected successfully")
    redis_available = True
except Exception as e:
    redis_client = None
    redis_available = False
    logger.warning(f"Redis not available: {e}, caching disabled")

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
    'https://app.thorinvest.org,https://n8n.thorinvest.org,http://localhost:8501,http://localhost:5678,http://localhost:3000'
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

# Auto-instrument with default metrics
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics", "/health"],
    inprogress_name="construction_api_requests_inprogress",
    inprogress_labels=True
)

# Custom metrics for construction operations
pdf_processing_counter = Counter(
    'construction_pdf_processed_total',
    'Total number of PDFs processed',
    ['status', 'cached']
)

excel_processing_counter = Counter(
    'construction_excel_processed_total',
    'Total number of Excel files processed',
    ['status', 'sheets']
)

material_calculation_counter = Counter(
    'construction_material_calculations_total',
    'Total material calculations performed',
    ['region', 'status']
)

document_processing_time = Histogram(
    'construction_document_processing_seconds',
    'Time spent processing construction documents',
    ['document_type', 'operation'],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
)

materials_detected_histogram = Histogram(
    'construction_materials_detected',
    'Number of materials detected in documents',
    buckets=[0, 5, 10, 25, 50, 100, 200, 500]
)

cache_hit_counter = Counter(
    'construction_cache_hits_total',
    'Total cache hits',
    ['operation']
)

cache_miss_counter = Counter(
    'construction_cache_misses_total',
    'Total cache misses',
    ['operation']
)

redis_connection_status = Gauge(
    'construction_redis_connected',
    'Redis connection status (1=connected, 0=disconnected)'
)

estonian_pricing_requests = Counter(
    'construction_estonian_pricing_requests_total',
    'Estonian material pricing requests',
    ['region', 'material_type']
)

total_cost_calculated = Histogram(
    'construction_total_cost_eur',
    'Total project costs calculated in EUR',
    buckets=[100, 500, 1000, 5000, 10000, 50000, 100000, 500000]
)

# Set initial Redis status
redis_connection_status.set(1 if redis_available else 0)

# Instrument app and expose metrics
instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=True)

logger.info("Prometheus metrics instrumentation enabled at /metrics")

# Cache helper functions
def get_cache_key(file_content: bytes, operation: str) -> str:
    """Generate cache key for file operations"""
    file_hash = hashlib.md5(file_content).hexdigest()
    return f"construction_ai:{operation}:{file_hash}"

async def get_cached_result(cache_key: str, operation: str) -> Optional[Dict]:
    """Get cached result if available"""
    if not redis_client:
        cache_miss_counter.labels(operation=operation).inc()
        return None
    try:
        cached = redis_client.get(cache_key)
        if cached:
            cache_hit_counter.labels(operation=operation).inc()
            return json.loads(cached)
        else:
            cache_miss_counter.labels(operation=operation).inc()
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
        cache_miss_counter.labels(operation=operation).inc()
    return None

async def set_cached_result(cache_key: str, result: Dict, ttl: int = 3600):
    """Cache result with TTL"""
    if not redis_client:
        return
    try:
        redis_client.setex(cache_key, ttl, json.dumps(result))
    except Exception as e:
        logger.warning(f"Cache write error: {e}")
        redis_connection_status.set(0)

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

def process_pdf_page(page, page_num: int, material_keywords: List[str]) -> Dict:
    """Process a single PDF page"""
    try:
        text = page.get_text()
        
        # If minimal text, try OCR
        if len(text.strip()) < 50:
            try:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img, lang='eng+est')  # Added Estonian
            except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError) as e:
                logger.warning(f"OCR failed on page {page_num + 1}: {e}")
                return {"page": page_num + 1, "text": "", "construction_items": []}

        # Process lines for construction data
        lines = text.split('\n')
        page_data = []
        construction_items = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 5:
                # Check for material keywords
                line_lower = line.lower()
                for keyword in material_keywords:
                    if keyword in line_lower:
                        # Try to extract quantity
                        import re
                        numbers = re.findall(r'\d+(?:\.\d+)?', line)
                        quantity = float(numbers[0]) if numbers else None

                        construction_items.append({
                            'material': keyword,
                            'text': line,
                            'page': page_num + 1,
                            'quantity': quantity,
                            'unit': 'unit'  # Default unit
                        })
                        break

                page_data.append({
                    'page': page_num + 1,
                    'text': line
                })

        return {
            "page": page_num + 1,
            "text": page_data,
            "construction_items": construction_items
        }
    except Exception as e:
        logger.error(f"Error processing page {page_num + 1}: {e}")
        return {"page": page_num + 1, "text": [], "construction_items": []}

@app.post("/extract-pdf")
async def extract_pdf_data(file: UploadFile = File(...)):
    """Extract construction data from PDF files with caching and async processing"""
    start_time = datetime.now()
    
    try:
        content = await file.read()
        
        # Check cache first
        cache_key = get_cache_key(content, "pdf_extraction")
        cached_result = await get_cached_result(cache_key, "pdf_extraction")
        if cached_result:
            logger.info(f"Returning cached result for {file.filename}")
            pdf_processing_counter.labels(status='success', cached='true').inc()
            return cached_result

        # Save to temp file to avoid stream issues
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name
            
        try:
            # Open PDF document from disk
            logger.info(f"Opening PDF from disk: {tmp_path}")
            doc = fitz.open(tmp_path)
            logger.info(f"PDF opened, pages: {len(doc)}")

            # Process pages sequentially
            page_results = []
            for page_num in range(len(doc)):
                logger.info(f"Processing page {page_num + 1}/{len(doc)}")
                page = doc[page_num]
                result = process_pdf_page(
                    page, 
                    page_num, 
                    MATERIAL_KEYWORDS
                )
                page_results.append(result)
            
            # Combine results
            extracted_data = []
            construction_items = []
            
            for result in page_results:
                extracted_data.extend(result["text"])
                construction_items.extend(result["construction_items"])

            doc.close()
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        # Record metrics
        processing_time = (datetime.now() - start_time).total_seconds()
        document_processing_time.labels(
            document_type='pdf', 
            operation='extraction'
        ).observe(processing_time)
        
        materials_detected_histogram.observe(len(construction_items))
        pdf_processing_counter.labels(status='success', cached='false').inc()

        result = {
            "status": "success",
            "filename": file.filename,
            "pages_processed": len(doc),
            "total_lines": len(extracted_data),
            "construction_items": construction_items,
            "sample_data": extracted_data[:10],
            "processing_time_seconds": processing_time,
            "cached": False
        }

        # Cache the result
        await set_cached_result(cache_key, result, ttl=7200)  # 2 hours cache
        
        return result

    except Exception as e:
        pdf_processing_counter.labels(status='error', cached='false').inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-excel")
async def extract_excel_data(file: UploadFile = File(...)):
    """Extract construction data from Excel files with caching and async processing"""
    start_time = datetime.now()
    
    try:
        content = await file.read()
        
        # Check cache first
        cache_key = get_cache_key(content, "excel_extraction")
        cached_result = await get_cached_result(cache_key, "excel_extraction")
        if cached_result:
            logger.info(f"Returning cached result for {file.filename}")
            excel_processing_counter.labels(status='success', sheets='unknown').inc()
            return cached_result

        # Load Excel file
        try:
            excel_file = pd.ExcelFile(io.BytesIO(content))
        except Exception as e:
            logger.error(f"Invalid Excel file: {e}")
            raise HTTPException(status_code=400, detail="Invalid Excel file")

        sheets_data = {}
        construction_items = []
        sheet_count = len(excel_file.sheet_names)

        for sheet_name in excel_file.sheet_names:
            try:
                # Read sheet into dataframe
                df = pd.read_excel(excel_file, sheet_name=sheet_name)

                if not df.empty:
                    logger.info(f"First row: {df.iloc[0].to_dict()}")

                # Find construction-related columns
                column_mapping = {}
                
                # FIRST: Check if this is CAD export data (has Handle, Color, Linetype columns)
                cad_columns = ['Handle', 'ParentID', 'Color', 'Linetype', 'Lineweight']
                has_cad_data = sum(1 for col in cad_columns if col in df.columns) >= 3
                
                if has_cad_data and 'Name' in df.columns:
                    # This is CAD export - use Name column for elements
                    column_mapping['material'] = 'Name'
                    # Map CAD geometric columns
                    if 'Area' in df.columns:
                        column_mapping['area'] = 'Area'
                    if 'Length' in df.columns:
                        column_mapping['length'] = 'Length'
                    if 'Perimeter' in df.columns:
                        column_mapping['perimeter'] = 'Perimeter'
                    if 'Radius' in df.columns:
                        column_mapping['radius'] = 'Radius'
                    logger.info(f"Detected CAD export format, using 'Name' column and geometric data: {list(column_mapping.keys())}")
                else:
                    # Standard Excel - search for familiar column names
                    for col in df.columns:
                        col_str = str(col).lower()
                        # Material/element name columns
                        if 'material' in col_str or 'item' in col_str or 'element' in col_str or 'materjal' in col_str or 'kirjeldus' in col_str or 'nimetus' in col_str:
                            if 'material' not in column_mapping:
                                column_mapping['material'] = col
                        # Description can also be material name
                        if 'description' in col_str and 'material' not in column_mapping:
                            column_mapping['material'] = col
                        if 'quantity' in col_str or 'amount' in col_str or 'qty' in col_str or 'count' in col_str or 'kogus' in col_str or 'maht' in col_str:
                            column_mapping['quantity'] = col
                        if col_str == 'unit' or 'ühik' in col_str or 'mõõt' in col_str:
                            column_mapping['unit'] = col
                        if 'price' in col_str or 'cost' in col_str or 'hind' in col_str or 'maksumus' in col_str:
                            column_mapping['price'] = col
                
                logger.info(f"Column mapping for '{sheet_name}': {column_mapping}")

                # Extract construction items if material column found
                if 'material' in column_mapping:
                    for _, row in df.iterrows():
                        material = row[column_mapping['material']]
                        
                        # Skip empty rows
                        if pd.isna(material) or material is None or str(material).strip() == "":
                            continue
                            
                        quantity = row.get(column_mapping.get('quantity'))
                        unit = row.get(column_mapping.get('unit'), 'unit')
                        price = row.get(column_mapping.get('price'))
                        
                        # Extract CAD geometric data
                        area = row.get(column_mapping.get('area'))
                        length = row.get(column_mapping.get('length'))
                        perimeter = row.get(column_mapping.get('perimeter'))
                        radius = row.get(column_mapping.get('radius'))

                        # Safely convert types
                        def safe_float(val):
                            try:
                                if val is not None and not pd.isna(val):
                                    return float(val)
                            except (ValueError, TypeError):
                                pass
                            return None
                        
                        quantity = safe_float(quantity) or 0.0
                        price = safe_float(price) or 0.0
                        area = safe_float(area)
                        length = safe_float(length)
                        perimeter = safe_float(perimeter)
                        radius = safe_float(radius)

                        item = {
                            'material': str(material),
                            'quantity': quantity,
                            'unit': str(unit) if unit is not None else 'unit',
                            'price': price,
                            'sheet': sheet_name
                        }
                        
                        # Add CAD geometric data if available
                        if area is not None:
                            item['area'] = round(area, 2)
                        if length is not None:
                            item['length'] = round(length, 2)
                        if perimeter is not None:
                            item['perimeter'] = round(perimeter, 2)
                        if radius is not None:
                            item['radius'] = round(radius, 2)
                            
                        construction_items.append(item)

                # Convert dataframe to simple dict for preview (10 rows max)
                df = df.head(10).astype(str).where(pd.notnull(df), None)
                
                sheets_data[sheet_name] = {
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "construction_columns": list(column_mapping.values()),
                    "sample_data": df.to_dict('records')
                }
                
            except Exception as e:
                logger.warning(f"Error processing sheet {sheet_name}: {e}")
                sheets_data[sheet_name] = {"error": str(e)}
        
        # Record metrics
        processing_time = (datetime.now() - start_time).total_seconds()
        document_processing_time.labels(
            document_type='excel',
            operation='extraction'
        ).observe(processing_time)
        
        excel_processing_counter.labels(
            status='success',
            sheets=str(sheet_count)
        ).inc()

        # Deduplicate CAD elements - group by material name and aggregate quantities
        if construction_items:
            # Check if this looks like CAD data (many duplicate names, no quantities)
            material_counts = {}
            total_qty_zero = sum(1 for item in construction_items if item.get('quantity', 0) == 0)
            is_cad_data = total_qty_zero > len(construction_items) * 0.8  # 80%+ have no quantity
            
            if is_cad_data:
                logger.info(f"Detected CAD layer data, deduplicating {len(construction_items)} items")
                for item in construction_items:
                    mat_name = item['material']
                    # Clean up CAD layer names (remove prefixes like "New_")
                    clean_name = mat_name.replace('New_', '').replace('_Pen_No_', ' ').strip()
                    # Further cleanup - extract meaningful part
                    if '__' in clean_name:
                        clean_name = clean_name.split('__')[0]
                    clean_name = clean_name.strip('_ ')
                    
                    if clean_name:
                        if clean_name not in material_counts:
                            material_counts[clean_name] = {
                                'material': clean_name,
                                'quantity': 0,
                                'unit': 'item',
                                'price': 0.0,
                                'sheet': item['sheet'],
                                'total_area': 0.0,
                                'total_length': 0.0,
                                'total_perimeter': 0.0,
                                'element_count': 0
                            }
                        material_counts[clean_name]['quantity'] += 1
                        material_counts[clean_name]['element_count'] += 1
                        
                        # Aggregate geometric data
                        if 'area' in item:
                            material_counts[clean_name]['total_area'] += item['area']
                        if 'length' in item:
                            material_counts[clean_name]['total_length'] += item['length']
                        if 'perimeter' in item:
                            material_counts[clean_name]['total_perimeter'] += item['perimeter']
                
                # Convert aggregated data to final format with smart units
                final_items = []
                for name, data in material_counts.items():
                    item = {
                        'material': name,
                        'sheet': data['sheet'],
                        'price': 0.0
                    }
                    
                    # Determine element category and default price based on layer name
                    name_lower = name.lower()
                    
                    # Category detection and default pricing (Estonian construction avg prices)
                    if any(k in name_lower for k in ['wall', 'sein', 'seinad']):
                        category = 'walls'
                        price_per_m2 = 85.0  # €/m² for wall work
                    elif any(k in name_lower for k in ['floor', 'põrand', 'vahelagi']):
                        category = 'floors'
                        price_per_m2 = 65.0  # €/m² for flooring
                    elif any(k in name_lower for k in ['roof', 'katus', 'lagi']):
                        category = 'roofing'
                        price_per_m2 = 95.0  # €/m² for roofing
                    elif any(k in name_lower for k in ['door', 'uks', 'uksed']):
                        category = 'doors'
                        price_per_item = 450.0  # €/item for doors
                    elif any(k in name_lower for k in ['window', 'aken', 'akna']):
                        category = 'windows'
                        price_per_item = 380.0  # €/item for windows
                    elif any(k in name_lower for k in ['pipe', 'toru', 'kanal']):
                        category = 'piping'
                        price_per_m = 45.0  # €/m for pipes
                    elif any(k in name_lower for k in ['wire', 'kaabel', 'elekter', 'electric']):
                        category = 'electrical'
                        price_per_m = 25.0  # €/m for electrical
                    elif any(k in name_lower for k in ['fill', 'täide', 'hatch']):
                        category = 'areas'
                        price_per_m2 = 15.0  # €/m² for general areas
                    elif any(k in name_lower for k in ['text', 'dim', 'annot', 'symbol']):
                        category = 'annotations'
                        price_per_m2 = 0.0  # No cost for annotations
                    else:
                        category = 'general'
                        price_per_m2 = 25.0  # Default €/m² for general elements
                    
                    # Choose best quantity/unit based on available data and assign price
                    if data['total_area'] > 0:
                        item['quantity'] = round(data['total_area'] / 1000000, 2)  # Convert to m²
                        item['unit'] = 'm²'
                        item['total_area_mm2'] = round(data['total_area'], 2)
                        # Apply area-based pricing
                        unit_price = price_per_m2 if 'price_per_m2' in dir() else 25.0
                        item['price'] = round(item['quantity'] * unit_price, 2)
                        item['unit_price'] = unit_price
                    elif data['total_length'] > 0:
                        item['quantity'] = round(data['total_length'] / 1000, 2)  # Convert to m
                        item['unit'] = 'm'
                        item['total_length_mm'] = round(data['total_length'], 2)
                        # Apply length-based pricing
                        unit_price = price_per_m if 'price_per_m' in dir() else 35.0
                        item['price'] = round(item['quantity'] * unit_price, 2)
                        item['unit_price'] = unit_price
                    else:
                        item['quantity'] = data['element_count']
                        item['unit'] = 'item'
                        # Apply item-based pricing
                        unit_price = price_per_item if 'price_per_item' in dir() else 50.0
                        item['price'] = round(item['quantity'] * unit_price, 2)
                        item['unit_price'] = unit_price
                    
                    item['element_count'] = data['element_count']
                    item['category'] = category
                    final_items.append(item)
                
                construction_items = final_items
                logger.info(f"Deduplicated to {len(construction_items)} unique elements with aggregated quantities")

        return {
            "status": "success", 
            "filename": file.filename,
            "sheets": list(excel_file.sheet_names),
            "sheets_data": sheets_data,
            "construction_items": construction_items,
            "processing_time_seconds": processing_time
        }

    except Exception as e:
        excel_processing_counter.labels(status='error', sheets='0').inc()
        raise HTTPException(status_code=500, detail=str(e))

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
