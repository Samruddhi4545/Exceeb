from fastapi import APIRouter, Depends, HTTPException, status #type:ignore
from sqlalchemy.orm import Session #type:ignore
from typing import List

from app.db.session import get_db
from app.models.department import Department
from app.schemas.department_team import DepartmentCreate, DepartmentResponse

router = APIRouter()


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(dept_in: DepartmentCreate, db: Session = Depends(get_db)):
    """Create a new company department."""
    existing = db.query(Department).filter(
        (Department.name == dept_in.name) | (Department.code == dept_in.code)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department name or code already exists.")

    db_dept = Department(
        name=dept_in.name,
        code=dept_in.code.upper(),
        description=dept_in.description
    )
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept


@router.get("/", response_model=List[DepartmentResponse])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all active departments."""
    return db.query(Department).offset(skip).limit(limit).all()