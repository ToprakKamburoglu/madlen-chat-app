from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from app.config import settings


_telemetry_initialized = False


def setup_telemetry_early():
    """Setup OpenTelemetry tracer provider BEFORE FastAPI app is created"""
    global _telemetry_initialized
    
    if not settings.ENABLE_TRACING:
        print("🔍 OpenTelemetry tracing is disabled")
        return
    
    if _telemetry_initialized:
        return
    
    try:
    
        resource = Resource(attributes={
            "service.name": settings.OTEL_SERVICE_NAME,
            "service.version": settings.APP_VERSION,
        })
       
        provider = TracerProvider(resource=resource)
        
        # OTLP exporter (for Jaeger)
        otlp_exporter = OTLPSpanExporter(
            endpoint=settings.JAEGER_ENDPOINT,
            insecure=True  # For local development
        )
        
        # span processor
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        
        # global tracer provider
        trace.set_tracer_provider(provider)
        
        # Instrument HTTP clients 
        HTTPXClientInstrumentor().instrument()
        
        _telemetry_initialized = True
        print(f"✅ OpenTelemetry initialized: {settings.JAEGER_ENDPOINT}")
        
    except Exception as e:
        print(f"⚠️  Failed to setup OpenTelemetry: {e}")
        print("🔍 Continuing without tracing...")


def instrument_app(app):
    """Instrument FastAPI app AFTER it's created"""
    if not settings.ENABLE_TRACING or not _telemetry_initialized:
        return
    
    try:
        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(app)
        print(f"✅ FastAPI instrumented for tracing")
        
    except Exception as e:
        print(f"⚠️  Failed to instrument FastAPI: {e}")


def get_tracer(name: str = __name__):
    """Get a tracer instance"""
    return trace.get_tracer(name)