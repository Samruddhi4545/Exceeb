from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TeamBase(BaseModel):
    name: str
    department_id: int
    manager_id: Optional[int] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None


class TeamResponse(TeamBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True