from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

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
