from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status  # type: ignore
from pydantic import BaseModel
from sqlalchemy.orm import Session  # type: ignore

from app.db.session import get_db
from app.api.deps import require_roles, get_current_user
from app.models.task import Task, TaskSubmission, TaskStatus
from app.models.user import User
from app.schemas.user import UserRole
router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    department_id: int
    campaign_id: Optional[int] = None
    assigned_to_id: Optional[int] = None
    created_by_id: int
    deadline: Optional[datetime] = None


class TaskSubmissionCreate(BaseModel):
    task_id: int
    employee_id: int
    comment: Optional[str] = None
    proof_file_url: Optional[str] = None


class TaskVerifyRequest(BaseModel):
    submission_id: int
    approved: bool
    rejection_reason: Optional[str] = None


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            require_roles(
                [
                    UserRole.MAIN_ADMIN,
                    UserRole.ADMIN,
                    UserRole.SUPERVISOR,
                    UserRole.MANAGER,
                ]
            )
        )
    ],
)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task (Restricted to Management roles)."""
    clean_title = task_in.title.strip()
    clean_description = (task_in.description or "").strip() or None

    if not clean_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty or whitespace.",
        )

    db_task = Task(
        title=clean_title,
        description=clean_description,
        department_id=task_in.department_id,
        campaign_id=task_in.campaign_id,
        assigned_to_id=task_in.assigned_to_id,
        created_by_id=current_user.id,
        deadline=task_in.deadline,
        status=TaskStatus.YET_TO_START,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
)
def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Retrieve tasks with deterministic ordering and bounded pagination."""
    return (
        db.query(Task)
        .order_by(Task.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.post("/submit")
@router.post(
    "/submit",
    dependencies=[Depends(get_current_user)],
)
def submit_task_proof(
    submission_in: TaskSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Employee submits task completion request along with proof files."""
    task = db.query(Task).filter(Task.id == submission_in.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    submission = TaskSubmission(
        task_id=submission_in.task_id,
        employee_id=submission_in.employee_id,
        comment=submission_in.comment,
        proof_file_url=submission_in.proof_file_url
    )
    task.status = TaskStatus.SUBMITTED
    
    db.add(submission)
    db.commit()
    return {"status": "success", "message": "Task submitted for manager verification"}


@router.post(
    "/verify",
    dependencies=[
        Depends(
            require_roles(
                [
                    UserRole.MAIN_ADMIN,
                    UserRole.ADMIN,
                    UserRole.SUPERVISOR,
                    UserRole.MANAGER,
                ]
            )
        )
    ],
)
def verify_task(verify_in: TaskVerifyRequest, db: Session = Depends(get_db)):
    """Manager verifies or rejects a submitted task (Restricted to Management roles)."""
    submission = db.query(TaskSubmission).filter(TaskSubmission.id == verify_in.submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission record not found")

    task = db.query(Task).filter(Task.id == submission.task_id).first()
    
    if verify_in.approved:
        task.status = TaskStatus.COMPLETED
    else:
        if not verify_in.rejection_reason:
            raise HTTPException(status_code=400, detail="Rejection reason is required when rejecting a task.")
        task.status = TaskStatus.REJECTED
        submission.rejection_reason = verify_in.rejection_reason

    db.commit()
    return {"status": "success", "task_status": task.status}