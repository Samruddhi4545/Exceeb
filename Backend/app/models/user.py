import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum #type:ignore
from sqlalchemy.orm import relationship #type:ignore
from app.db.session import Base


class UserRole(str, enum.Enum):
    MAIN_ADMIN = "MAIN_ADMIN"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    CLIENT = "CLIENT"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    is_main_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Generated Employee ID format: Batch + Location + Dept + Seq (e.g., 1MAME01)
    current_employee_id = Column(String(50), unique=True, index=True, nullable=True)
    
    # Foreign Keys
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="employees")
    team = relationship("Team", back_populates="members")
    id_history = relationship("EmployeeIDHistory", back_populates="user")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to_id", back_populates="assigned_to")
    submitted_tasks = relationship("TaskSubmission", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")


class EmployeeIDHistory(Base):
    __tablename__ = "employee_id_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    previous_employee_id = Column(String(50), nullable=False)
    reason_for_change = Column(String(255), nullable=True)  # e.g., Location or Department change
    changed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="id_history")