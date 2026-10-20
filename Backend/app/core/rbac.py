from enum import Enum
from fastapi import HTTPException, status #type:ignore


class RoleEnum(str, Enum):
    MAIN_ADMIN = "MAIN_ADMIN"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    CLIENT = "CLIENT"


def check_role_permission(user_role: str, allowed_roles: list[RoleEnum]) -> bool:
    """Check if a user's role is permitted to perform an operation."""
    if user_role not in [role.value for role in allowed_roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return True


def validate_admin_modification_protection(target_is_main_admin: bool, current_user_role: str) -> None:
    """Enforces rule: Added Admins cannot modify permissions/access of Main Admins."""
    if target_is_main_admin and current_user_role != RoleEnum.MAIN_ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Main Admins can modify or manage Main Admin accounts."
        )