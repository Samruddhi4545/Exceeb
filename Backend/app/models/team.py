from sqlalchemy import Column, Integer, String, ForeignKey, DateTime #type:ignore
from sqlalchemy.orm import relationship #type:ignore
from datetime import datetime

from app.db.session import Base #type:ignore

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="teams")
    manager = relationship("User", foreign_keys=[manager_id])
    members = relationship("User", foreign_keys="User.team_id", back_populates="team")