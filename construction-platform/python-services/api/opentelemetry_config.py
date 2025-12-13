# OpenTelemetry Configuration
# construction-platform/python-services/api/opentelemetry_config.py

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import logging

logger = logging.getLogger(__name__)

def setup_opentelemetry(service_name: str = "construction-ai-api", jaeger_endpoint: str = "http://localhost:14268/api/traces"):
    """Setup OpenTelemetry with Jaeger"""
    try:
        # Create tracer provider
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)
        
        # Create Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name="localhost",
            agent_port=6831,
            endpoint=jaeger_endpoint
        )
        
        # Create span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        tracer_provider.add_span_processor(span_processor)
        
        # Instrument FastAPI
        FastAPIInstrumentor.instrument()
        
        # Instrument Redis
        RedisInstrumentor().instrument()
        
        # Instrument requests
        RequestsInstrumentor().instrument()
        
        logger.info(f"OpenTelemetry configured: {service_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry: {e}")
        return False

# Auto-setup if enabled
import os
if os.getenv("ENABLE_OPENTELEMETRY", "false").lower() == "true":
    setup_opentelemetry()
