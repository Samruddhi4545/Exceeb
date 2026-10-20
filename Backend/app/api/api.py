from fastapi import APIRouter #type:ignore
from app.api.v1 import auth, users, departments, teams, tasks, tracking

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(departments.router, prefix="/departments", tags=["Departments"])
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Field & Tracking"])