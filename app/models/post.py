from sqlalchemy import Column, Integer, Boolean, DateTime, String, ForeignKey, Index, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        Index("idx_post_owner_id", "owner_id"),
        Index("idx_post_created_at", " created_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False,index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc))

    # Relationship
    owner = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, owner_id={self.owner_id})>"
