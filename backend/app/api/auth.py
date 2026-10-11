from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.auth.passwords import verify_password
from app.auth.tokens import create_access_token
from app.db.session import get_session
from app.domain.models import Role, User

router = APIRouter(prefix="/auth", tags=["authentication"])


class SignInResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user_id: str
    role: str


class SessionResponse(BaseModel):
    user_id: str
    role: str


@router.post("/login", response_model=SignInResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> SignInResponse:
    user = session.scalar(select(User).where(User.email == form.username))
    valid_password = verify_password(form.password, user.password_hash) if user else False
    if not user or not user.is_active or not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    role = session.get(Role, user.role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token, expires_at = create_access_token(user.id, role.name, now=datetime.now(UTC))
    return SignInResponse(access_token=token, expires_at=expires_at, user_id=user.id, role=role.name)


@router.get("/me", response_model=SessionResponse)
def current_session(user: AuthenticatedUser = Depends(get_current_user)) -> SessionResponse:
    return SessionResponse(user_id=user.id, role=user.role)
