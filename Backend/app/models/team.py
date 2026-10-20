from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey #type:ignore
from sqlalchemy.orm import relationship #type:ignore
from app.db.session import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="teams")
    manager = relationship("User", foreign_keys=[manager_id])
    members = relationship("User", foreign_keys="User.team_id", back_populates="team")