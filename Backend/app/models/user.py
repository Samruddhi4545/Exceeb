import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime #type:ignore
from sqlalchemy.orm import relationship #type:ignore

from app.db.session import Base


class UserRole(str, enum.Enum):
    MAIN_ADMIN = "MAIN_ADMIN"
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default=UserRole.EMPLOYEE.value)
    is_active = Column(Boolean, default=True)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="users")
    team = relationship("Team", foreign_keys=[team_id], back_populates="members")
    assigned_tasks = relationship(
        "Task",
        foreign_keys="Task.assigned_to_id",
        back_populates="assigned_to",
    )
    submitted_tasks = relationship("TaskSubmission", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")