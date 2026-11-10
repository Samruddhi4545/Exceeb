from typing import List, Callable
from fastapi import Depends, HTTPException, status #type:ignore
from fastapi.security import OAuth2PasswordBearer #type:ignore
from jose import jwt, JWTError #type:ignore
from sqlalchemy.orm import Session #type:ignore

from app.db.session import get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserRole

# Configures FastAPI to read the 'Bearer <token>' header from requests
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    """Decodes the JWT token and fetches the authenticated user from PostgreSQL."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user account"
        )
    return user

def require_roles(allowed_roles: List[UserRole]) -> Callable:
    """Enforces role permissions on FastAPI endpoints."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your assigned role",
            )
        return current_user
    return role_checker