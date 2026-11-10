from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from pydantic import BaseModel
from sqlalchemy.orm import Session  # type: ignore

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.tracking import WorkSession, LocationLog, Attendance, AttendanceStatus
from app.models.user import User

router = APIRouter()


class LocationPing(BaseModel):
    work_session_id: int
    latitude: float
    longitude: float


class WorkSessionStart(BaseModel):
    notes: Optional[str] = None


@router.post(
    "/session/start",
    dependencies=[Depends(get_current_user)],
)
def start_work_session(
    session_in: WorkSessionStart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start active work session and initialize automatic attendance tracking."""
    # Check for existing active session to prevent duplicates
    active_session = (
        db.query(WorkSession)
        .filter(WorkSession.user_id == current_user.id, WorkSession.is_active == 1)
        .first()
    )
    if active_session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An active work session is already running.",
        )

    session = WorkSession(user_id=current_user.id, is_active=1)
    db.add(session)

    # Auto register present attendance
    attendance = Attendance(
        employee_id=current_user.id,
        date=datetime.utcnow(),
        status=AttendanceStatus.PRESENT,
        check_in=datetime.utcnow(),
    )
    db.add(attendance)
    db.commit()
    db.refresh(session)
    return {"status": "session_started", "work_session_id": session.id}

@router.post(
    "/location",
    dependencies=[Depends(get_current_user)],
)
def log_gps_location(
    ping: LocationPing,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record continuous 1-minute interval GPS location during an active work session."""
    session = (
        db.query(WorkSession)
        .filter(
            WorkSession.id == ping.work_session_id,
            WorkSession.user_id == current_user.id,
            WorkSession.is_active == 1,
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active work session not found for the current user.",
        )
    log = LocationLog(
        work_session_id=ping.work_session_id,
        latitude=ping.latitude,
        longitude=ping.longitude,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return {"status": "location_logged"}

@router.get(
    "/session/active",
    dependencies=[Depends(get_current_user)],
)
def get_active_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve the logged-in user's active work session."""
    session = (
        db.query(WorkSession)
        .filter(WorkSession.user_id == current_user.id, WorkSession.is_active == 1)
        .first()
    )
    if not session:
        return {"active": False, "session": None}
    return {"active": True, "session_id": session.id, "start_time": session.start_time}


@router.post(
    "/session/end",
    dependencies=[Depends(get_current_user)],
)
def end_work_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """End the current user's active work session."""
    session = (
        db.query(WorkSession)
        .filter(WorkSession.user_id == current_user.id, WorkSession.is_active == 1)
        .first()
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active work session found.",
        )

    session.is_active = 0
    session.end_time = datetime.utcnow()
    db.commit()
    return {"status": "session_ended"}