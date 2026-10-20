from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


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


class TeamResponse(TeamBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True