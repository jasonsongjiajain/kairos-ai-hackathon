from datetime import UTC, datetime, timedelta

import jwt
from jwt import InvalidTokenError

from app.config import get_settings

ALGORITHM = "HS256"
ACCESS_TOKEN_TTL = timedelta(minutes=15)


def create_access_token(user_id: str, role: str, *, now: datetime | None = None) -> tuple[str, datetime]:
    issued_at = now or datetime.now(UTC)
    expires_at = issued_at + ACCESS_TOKEN_TTL
    token = jwt.encode(
        {"sub": user_id, "role": role, "iat": issued_at, "exp": expires_at},
        get_settings().jwt_secret,
        algorithm=ALGORITHM,
    )
    return token, expires_at


def decode_access_token(token: str) -> dict[str, str]:
    try:
        payload = jwt.decode(token, get_settings().jwt_secret, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        role = payload.get("role")
        if (
            not isinstance(subject, str)
            or not isinstance(role, str)
            or not isinstance(payload.get("exp"), (int, float))
        ):
            raise InvalidTokenError("Required claims are missing")
        return {"sub": subject, "role": role}
    except InvalidTokenError as error:
        raise ValueError("Invalid or expired access token") from error
