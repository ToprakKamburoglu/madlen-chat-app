from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.services.session_service import session_service
from app.telemetry.tracer import get_tracer

router = APIRouter(prefix="/sessions", tags=["sessions"])
tracer = get_tracer(__name__)


# Request/Response models
class CreateSessionRequest(BaseModel):
    model_id: str
    title: str = "New Chat"
    
    model_config = {"protected_namespaces": ()}  # ✅ Uyarıyı kapat


class UpdateSessionRequest(BaseModel):
    title: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    image_url: str | None = None
    timestamp: datetime
    
    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    id: str
    title: str
    model_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    model_config = {"protected_namespaces": (), "from_attributes": True}  # ✅ İkisini birleştir


@router.get("/", response_model=List[SessionResponse])
async def get_all_sessions(db: Session = Depends(get_db)):
    """Get all chat sessions"""
    with tracer.start_as_current_span("endpoint.get_all_sessions"):
        sessions = session_service.get_all_sessions(db)
        return sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    """Get a specific chat session by ID"""
    with tracer.start_as_current_span("endpoint.get_session"):
        session = session_service.get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session


@router.post("/", response_model=SessionResponse)
async def create_session(request: CreateSessionRequest, db: Session = Depends(get_db)):
    """Create a new chat session"""
    with tracer.start_as_current_span("endpoint.create_session"):
        try:
            session = session_service.create_session(
                db,
                model_id=request.model_id,
                title=request.title
            )
            return session
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    request: UpdateSessionRequest,
    db: Session = Depends(get_db)
):
    """Update session title"""
    with tracer.start_as_current_span("endpoint.update_session"):
        session = session_service.update_session_title(db, session_id, request.title)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session


@router.delete("/{session_id}")
async def delete_session(session_id: str, db: Session = Depends(get_db)):
    """Delete a chat session"""
    with tracer.start_as_current_span("endpoint.delete_session"):
        success = session_service.delete_session(db, session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deleted successfully"}