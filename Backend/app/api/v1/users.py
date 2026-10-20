from fastapi import APIRouter, Depends, HTTPException, status #type:ignore
from sqlalchemy.orm import Session #type:ignore
from typing import List

from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash
from app.utils.employee_id import generate_employee_id

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create a new user and assign automatically generated Employee ID."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    emp_id = None
    if user_in.department_id:
        emp_id = generate_employee_id(
            db=db,
            batch_number=user_in.batch_number or "1",
            location_code=user_in.location_code or "MA",
            department_id=user_in.department_id
        )

    db_user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_main_admin=user_in.is_main_admin,
        current_employee_id=emp_id,
        department_id=user_in.department_id,
        team_id=user_in.team_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all users."""
    return db.query(User).offset(skip).limit(limit).all()