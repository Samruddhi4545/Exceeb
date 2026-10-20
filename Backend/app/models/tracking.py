import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum #type:ignore
from sqlalchemy.orm import relationship #type:ignore
from app.db.session import Base


class AttendanceStatus(str, enum.Enum):
    PRESENT = "PRESENT"
    ON_TIME = "ON_TIME"
    LATE = "LATE"
    EARLY_CHECKOUT = "EARLY_CHECKOUT"
    HALF_DAY = "HALF_DAY"
    LEAVE = "LEAVE"
    HOLIDAY = "HOLIDAY"
    ABSENT = "ABSENT"


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1)

    locations = relationship("LocationLog", back_populates="work_session")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(SQLEnum(AttendanceStatus), default=AttendanceStatus.ABSENT)
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)

    employee = relationship("User", back_populates="attendances")


class LocationLog(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    work_session_id = Column(Integer, ForeignKey("work_sessions.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    work_session = relationship("WorkSession", back_populates="locations")


class Geofence(Base):
    __tablename__ = "geofences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_meters = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)