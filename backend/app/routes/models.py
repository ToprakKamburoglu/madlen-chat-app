from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.openrouter import openrouter_service
from app.telemetry.tracer import get_tracer

router = APIRouter(prefix="/models", tags=["models"])
tracer = get_tracer(__name__)


@router.get("/", response_model=List[Dict[str, Any]])
async def get_models():
    """
    Get available AI models from OpenRouter
    
    Returns a list of available models with their details:
    - id: Model identifier
    - name: Human-readable model name
    - description: Model description
    - context_length: Maximum context window
    - pricing: Cost information
    """
    with tracer.start_as_current_span("endpoint.get_models"):
        try:
            models = await openrouter_service.get_models()
            return models
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")
