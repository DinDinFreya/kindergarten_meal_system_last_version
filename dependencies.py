# backend/app/auth/dependencies.py (or app/dependencies.py)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.config import settings
from app.core import security as core_security # Renamed to avoid conflict
from app.models.user import User as UserModel
from app.schemas.token import TokenData # Assuming this schema exists
from app.crud import user as crud_user

# This should point to your token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = core_security.decode_token(token)
    if payload is None or not isinstance(payload.get("sub"), str):
        raise credentials_exception
    
    user_email: str = payload.get("sub")
    user = crud_user.get_by_email(db, email=user_email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: UserModel = Depends(get_current_active_user)):
        # Ensure the user's role is loaded and has a name attribute
        if not current_user.role or not hasattr(current_user.role, 'name'):
            # This might happen if the role relationship isn't eagerly loaded or doesn't exist
            # Or if the role object itself wasn't properly fetched/associated during user retrieval
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User role information is missing or improperly configured."
            )
        
        if current_user.role.name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{current_user.role.name}' is not authorized for this resource. Allowed roles: {self.allowed_roles}",
            )
        return current_user

require_admin = RoleChecker(["Admin"])
require_manager = RoleChecker(["Admin", "Manager"])
require_cook = RoleChecker(["Admin", "Cook"])
# For endpoints accessible by multiple specific roles if needed:
# require_manager_or_cook = RoleChecker(["Admin", "Manager", "Cook"])