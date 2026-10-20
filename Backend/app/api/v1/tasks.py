from fastapi import APIRouter, Depends, HTTPException, status #type:ignore
from sqlalchemy.orm import Session #type:ignore
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.db.session import get_db
from app.models.task import Task, TaskSubmission, TaskStatus

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


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task and assign it department-wise or employee-wise."""
    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        department_id=task_in.department_id,
        campaign_id=task_in.campaign_id,
        assigned_to_id=task_in.assigned_to_id,
        created_by_id=task_in.created_by_id,
        deadline=task_in.deadline,
        status=TaskStatus.YET_TO_START
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.post("/submit")
def submit_task_proof(submission_in: TaskSubmissionCreate, db: Session = Depends(get_db)):
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


@router.post("/verify")
def verify_task(verify_in: TaskVerifyRequest, db: Session = Depends(get_db)):
    """Manager verifies or rejects a submitted task."""
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