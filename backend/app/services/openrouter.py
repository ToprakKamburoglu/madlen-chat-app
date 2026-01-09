import httpx
from typing import List, Dict, Any, Optional
from app.config import settings
from app.telemetry.tracer import get_tracer

tracer = get_tracer(__name__)


class OpenRouterService:
    """Service for interacting with OpenRouter API"""
    
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    async def get_models(self) -> List[Dict[str, Any]]:
        """Get available FREE AI models from OpenRouter with vision support detection"""
        with tracer.start_as_current_span("openrouter.get_models"):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{self.base_url}/models",
                        headers=self.headers,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    all_models = data.get("data", [])
                    
                    # Only FREE models (pricing.prompt == "0")
                    free_models = [
                        model for model in all_models
                        if model.get("pricing", {}).get("prompt", "1") == "0"
                        and model.get("pricing", {}).get("completion", "1") == "0"
                    ]
                    
                    for model in free_models:
                        # Check if model supports images (multi-modal)
                        supports_vision = self._check_vision_support(model)
                        model["supports_vision"] = supports_vision
                        
                        if supports_vision and "📷" not in model.get("name", ""):
                            model["name"] = f"📷 {model['name']}"
                        
                        desc = model.get("description", "")
                        if len(desc) > 150:
                            model["description"] = desc[:150] + "..."
                    
                    free_models.sort(key=lambda x: (
                        not x.get("supports_vision", False),  # Vision models first
                        x.get("name", "")
                    ))
                    
                    print(f"✅ Loaded {len(free_models)} FREE models ({sum(1 for m in free_models if m.get('supports_vision'))} with vision support)")
                    
                    return free_models
                    
            except Exception as e:
                print(f"Error fetching models: {e}")
                # Return some default free models if API fails
                return self._get_default_models()
    
    def _check_vision_support(self, model: Dict[str, Any]) -> bool:
        """Check if a model supports vision/image inputs"""
        # Check architecture for image support
        arch = model.get("architecture", {})
        input_modalities = arch.get("input_modalities", [])
        
        # Check if "image" is in input modalities
        if "image" in input_modalities:
            return True
        
        # Check model ID/name for vision keywords
        model_id = model.get("id", "").lower()
        model_name = model.get("name", "").lower()
        
        vision_keywords = ["vision", "visual", "image", "multimodal", "multi-modal", "vlm"]
        
        for keyword in vision_keywords:
            if keyword in model_id or keyword in model_name:
                return True
        
        return False
    
    def _get_default_models(self) -> List[Dict[str, Any]]:
        """Return default free models as fallback"""
        return [
            {
                "id": "meta-llama/llama-3.2-3b-instruct:free",
                "name": "Llama 3.2 3B Instruct (Free)",
                "description": "Fast and efficient small model",
                "context_length": 131072,
                "pricing": {"prompt": "0", "completion": "0"},
                "supports_vision": False
            },
            {
                "id": "google/gemma-2-9b-it:free",
                "name": "Gemma 2 9B (Free)",
                "description": "Google's efficient model",
                "context_length": 8192,
                "pricing": {"prompt": "0", "completion": "0"},
                "supports_vision": False
            },
            {
                "id": "microsoft/phi-3-mini-128k-instruct:free",
                "name": "Phi-3 Mini 128K (Free)",
                "description": "Microsoft's compact model",
                "context_length": 128000,
                "pricing": {"prompt": "0", "completion": "0"},
                "supports_vision": False
            },
        ]
    
    async def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Send chat completion request to OpenRouter"""
        with tracer.start_as_current_span("openrouter.chat_completion") as span:
            span.set_attribute("model", model)
            span.set_attribute("message_count", len(messages))
            
            try:
                async with httpx.AsyncClient() as client:
                    payload = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                    }
                    
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=self.headers,
                        json=payload,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    result = response.json()
                    
                    span.set_attribute("completion_tokens", 
                                      result.get("usage", {}).get("completion_tokens", 0))
                    
                    return result
            except httpx.HTTPError as e:
                span.record_exception(e)
                raise Exception(f"OpenRouter API error: {str(e)}")
            except Exception as e:
                span.record_exception(e)
                raise Exception(f"Unexpected error: {str(e)}")


# Global service instance
openrouter_service = OpenRouterService()