from fastapi import APIRouter, Depends, HTTPException #type:ignore
from sqlalchemy.orm import Session #type:ignore
from datetime import datetime
from pydantic import BaseModel

from app.db.session import get_db
from app.models.tracking import WorkSession, LocationLog, Attendance, AttendanceStatus

router = APIRouter()


class LocationPing(BaseModel):
    work_session_id: int
    latitude: float
    longitude: float


class WorkSessionStart(BaseModel):
    user_id: int


@router.post("/session/start")
def start_work_session(session_in: WorkSessionStart, db: Session = Depends(get_db)):
    """Start active work session and initialize automatic attendance tracking."""
    session = WorkSession(user_id=session_in.user_id, is_active=1)
    db.add(session)
    
    # Auto register present attendance
    attendance = Attendance(
        employee_id=session_in.user_id,
        date=datetime.utcnow(),
        status=AttendanceStatus.PRESENT,
        check_in=datetime.utcnow()
    )
    db.add(attendance)
    db.commit()
    db.refresh(session)
    return {"status": "session_started", "work_session_id": session.id}


@router.post("/location")
def log_gps_location(ping: LocationPing, db: Session = Depends(get_db)):
    """Record continuous 1-minute interval GPS location during an active work session."""
    session = db.query(WorkSession).filter(
        WorkSession.id == ping.work_session_id, WorkSession.is_active == 1
    ).first()
    
    if not session:
        raise HTTPException(status_code=400, detail="Active work session not found")

    log = LocationLog(
        work_session_id=ping.work_session_id,
        latitude=ping.latitude,
        longitude=ping.longitude,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return {"status": "location_logged"}