from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ChatSession(Base):
    """Chat session model"""
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, default="New Chat")
    model_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    """Message model"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  
    content = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)  
    timestamp = Column(DateTime, default=datetime.utcnow)
    extra_metadata = Column(JSON, nullable=True)  
    
    # Relationship
    session = relationship("ChatSession", back_populates="messages")