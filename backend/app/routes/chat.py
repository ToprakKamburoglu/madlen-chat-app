from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from app.database import get_db
from app.services.openrouter import openrouter_service
from app.services.session_service import session_service
from app.telemetry.tracer import get_tracer

router = APIRouter(prefix="/chat", tags=["chat"])
tracer = get_tracer(__name__)


# Request models
class ChatMessage(BaseModel):
    role: str
    content: Union[str, List[Dict[str, Any]]]  # Support multi-modal (text + image)


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    session_id: Optional[str] = None
    max_tokens: int = 1000
    temperature: float = 0.7


@router.post("/")
async def chat_completion(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a chat message and get AI response
    
    Supports:
    - Text-only messages
    - Multi-modal messages (text + images)
    - Session persistence
    - OpenTelemetry tracing
    """
    with tracer.start_as_current_span("endpoint.chat_completion") as span:
        span.set_attribute("model", request.model)
        span.set_attribute("message_count", len(request.messages))
        
        try:
            # Prepare messages for OpenRouter API
            api_messages = []
            for msg in request.messages:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Call OpenRouter API
            response = await openrouter_service.chat_completion(
                model=request.model,
                messages=api_messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            # Save to session if session_id is provided
            if request.session_id:
                span.set_attribute("session_id", request.session_id)
                
                # ✅ Extract user message content and image
                last_user_msg = request.messages[-1]
                user_content = last_user_msg.content
                user_image_url = None
                
                # Handle multi-modal content
                if isinstance(user_content, list):
                    # Extract text content
                    text_parts = []
                    for item in user_content:
                        if isinstance(item, dict):
                            if item.get("type") == "text":
                                text_parts.append(item.get("text", ""))
                            elif item.get("type") == "image_url":
                                # ✅ Extract image URL
                                user_image_url = item.get("image_url", {}).get("url")
                    
                    user_content = " ".join(text_parts) if text_parts else ""
                
                # Save user message
                session_service.add_message(
                    db,
                    session_id=request.session_id,
                    role="user",
                    content=user_content,
                    image_url=user_image_url,  # ✅ Save image URL
                    extra_metadata={"model": request.model}
                )
                
                # Save assistant response
                assistant_content = response["choices"][0]["message"]["content"]
                session_service.add_message(
                    db,
                    session_id=request.session_id,
                    role="assistant",
                    content=assistant_content,
                    extra_metadata={
                        "model": request.model,
                        "usage": response.get("usage")
                    }
                )
            
            # Return raw response (no validation)
            return response
            
        except Exception as e:
            span.record_exception(e)
            raise HTTPException(
                status_code=500,
                detail=f"Chat completion failed: {str(e)}"
            )