from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    topic = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    type = Column(String(50), nullable=False, default="professional", index=True)
    date = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    content_hash = Column(String(64), unique=True, index=True, nullable=False)
    document_context = Column(Text, nullable=True)

    owner = relationship("User", back_populates="posts")

