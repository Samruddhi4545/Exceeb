from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime #type:ignore
from sqlalchemy.orm import relationship #type:ignore
from app.db.session import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)  # BPO, MEDIA, MARKETING, etc.
    code = Column(String(10), unique=True, nullable=False)              # e.g., BP, ME, MK
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employees = relationship("User", back_populates="department")
    teams = relationship("Team", back_populates="department")
    tasks = relationship("Task", back_populates="department")