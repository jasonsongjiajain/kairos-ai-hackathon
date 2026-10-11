from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.tokens import decode_access_token
from app.db.session import get_session
from app.domain.models import Role, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthenticatedUser:
    def __init__(self, *, id: str, email: str, role: str) -> None:
        self.id = id
        self.email = email
        self.role = role


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> AuthenticatedUser:
    try:
        claims = decode_access_token(token)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    user = session.scalar(
        select(User).where(User.id == claims["sub"], User.is_active.is_(True))
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    role = session.get(Role, user.role_id)
    if role is None or role.name != claims["role"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthenticatedUser(id=user.id, email=user.email, role=role.name)


def require_roles(*allowed_roles: str):
    def dependency(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        from app.auth.policy import require_role

        require_role(user.role, allowed_roles)
        return user

    return dependency
