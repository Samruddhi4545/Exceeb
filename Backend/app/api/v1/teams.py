from fastapi import APIRouter, Depends, HTTPException, status #type:ignore
from sqlalchemy.orm import Session #type:ignore
from typing import List

from app.db.session import get_db
from app.models.team import Team
from app.schemas.department_team import TeamCreate, TeamResponse

router = APIRouter()


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(team_in: TeamCreate, db: Session = Depends(get_db)):
    """Create a new team under a department."""
    db_team = Team(
        name=team_in.name,
        department_id=team_in.department_id,
        manager_id=team_in.manager_id
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/", response_model=List[TeamResponse])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all teams."""
    return db.query(Team).offset(skip).limit(limit).all()