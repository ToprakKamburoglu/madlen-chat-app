from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid
from app.models import ChatSession, Message
from app.telemetry.tracer import get_tracer

tracer = get_tracer(__name__)


class SessionService:
    """Service for managing chat sessions"""
    
    @staticmethod
    def create_session(db: Session, model_id: str, title: str = "New Chat") -> ChatSession:
        """Create a new chat session"""
        with tracer.start_as_current_span("session.create"):
            session = ChatSession(
                id=str(uuid.uuid4()),
                title=title,
                model_id=model_id,
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return session
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        with tracer.start_as_current_span("session.get"):
            return db.query(ChatSession).filter(ChatSession.id == session_id).first()
    
    @staticmethod
    def get_all_sessions(db: Session, limit: int = 50) -> List[ChatSession]:
        """Get all chat sessions"""
        with tracer.start_as_current_span("session.get_all"):
            return db.query(ChatSession).order_by(
                ChatSession.updated_at.desc()
            ).limit(limit).all()
    
    @staticmethod
    def update_session_title(db: Session, session_id: str, title: str) -> Optional[ChatSession]:
        """Update session title"""
        with tracer.start_as_current_span("session.update_title"):
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if session:
                session.title = title
                session.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(session)
            return session
    
    @staticmethod
    def delete_session(db: Session, session_id: str) -> bool:
        """Delete a chat session"""
        with tracer.start_as_current_span("session.delete"):
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if session:
                db.delete(session)
                db.commit()
                return True
            return False
    
    @staticmethod
    def add_message(
        db: Session,
        session_id: str,
        role: str,
        content: str,
        image_url: Optional[str] = None,
        extra_metadata: Optional[dict] = None  
    ) -> Message:
        """Add a message to a session"""
        with tracer.start_as_current_span("session.add_message") as span:
            span.set_attribute("role", role)
            span.set_attribute("content_length", len(content))
            
            message = Message(
                id=str(uuid.uuid4()),
                session_id=session_id,
                role=role,
                content=content,
                image_url=image_url,
                extra_metadata=extra_metadata  
            )
            db.add(message)
            
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if session:
                session.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(message)
            return message


session_service = SessionService()