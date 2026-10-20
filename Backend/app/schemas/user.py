from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole = UserRole.EMPLOYEE
    is_main_admin: bool = False
    department_id: Optional[int] = None
    team_id: Optional[int] = None


class UserCreate(UserBase):
    password: str
    batch_number: Optional[str] = "1"
    location_code: Optional[str] = "MA"  # e.g., MA for Mangalore


class UserResponse(UserBase):
    id: int
    current_employee_id: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None