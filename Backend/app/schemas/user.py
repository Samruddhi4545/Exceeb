from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Optional[UserRole] = UserRole.EMPLOYEE
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    employee_id: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str