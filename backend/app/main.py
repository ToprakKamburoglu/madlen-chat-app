from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db
from app.routes import chat, models, sessions
from app.telemetry.tracer import setup_telemetry_early


setup_telemetry_early()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the application"""
    print("🚀 Starting Madlen AI Chat Backend...")
    print(f"📦 Version: {settings.APP_VERSION}")
    print(f"🔧 Debug Mode: {settings.DEBUG}")
    
    init_db()
    print("✅ Database initialized")
    
    print("✅ Backend is ready!")
    print(f"📡 API Documentation: http://localhost:8000/docs")
    
    yield
    
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Chat Backend with OpenRouter integration and OpenTelemetry tracing",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.telemetry.tracer import instrument_app
instrument_app(app)


app.include_router(chat.router)
app.include_router(models.router)
app.include_router(sessions.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Madlen AI Chat Backend",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tracing_enabled": settings.ENABLE_TRACING
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )