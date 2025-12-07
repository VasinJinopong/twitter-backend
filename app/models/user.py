from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("username", name="uq_user_username"),
        Index("idx_user_email", "email"),
        Index("idx_user_username","username"),
    )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255),nullable=False)
    is_active = Column(Boolean,default=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc),nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc) )

    # Relationships
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")


    # for good debug, logging, professional
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"