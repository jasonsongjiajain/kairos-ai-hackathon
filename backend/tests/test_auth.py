from datetime import UTC, datetime, timedelta

import jwt
from fastapi.testclient import TestClient

from app.auth.passwords import hash_password
from app.auth.tokens import ALGORITHM
from app.config import get_settings
from app.db.session import get_session
from app.domain.models import Role, User
from app.main import app


def test_login_returns_signed_token_and_public_user_fields(db_session):
    role = Role(name="technician")
    db_session.add(role)
    db_session.flush()
    user = User(
        email="field@example.test",
        display_name="Field Technician",
        password_hash=hash_password("correct horse battery"),
        role_id=role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    app.dependency_overrides[get_session] = lambda: db_session
    try:
        response = TestClient(app).post(
            "/auth/login",
            data={"username": user.email, "password": "correct horse battery"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == user.id
    assert body["role"] == "technician"
    assert body["token_type"] == "bearer"
    claims = jwt.decode(body["access_token"], get_settings().jwt_secret, algorithms=[ALGORITHM])
    assert claims["sub"] == user.id
    assert claims["role"] == "technician"
    assert datetime.fromisoformat(body["expires_at"].replace("Z", "+00:00")) > datetime.now(UTC)
    assert "password_hash" not in body
    assert user.password_hash not in response.text


def test_login_rejects_invalid_password(db_session):
    role = Role(name="operator")
    db_session.add(role)
    db_session.flush()
    db_session.add(User(
        email="operator@example.test",
        display_name="Operator",
        password_hash=hash_password("correct horse battery"),
        role_id=role.id,
        is_active=True,
    ))
    db_session.commit()

    app.dependency_overrides[get_session] = lambda: db_session
    try:
        response = TestClient(app).post(
            "/auth/login",
            data={"username": "operator@example.test", "password": "incorrect"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_protected_route_rejects_missing_and_expired_tokens(db_session):
    role = Role(name="technician")
    db_session.add(role)
    db_session.flush()
    user = User(
        email="field@example.test",
        display_name="Field Technician",
        password_hash=hash_password("correct horse battery"),
        role_id=role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        client = TestClient(app)
        missing = client.get("/auth/me")
        expired_token = jwt.encode(
            {"sub": user.id, "role": "technician", "exp": datetime.now(UTC) - timedelta(minutes=1)},
            get_settings().jwt_secret,
            algorithm=ALGORITHM,
        )
        expired = client.get("/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    finally:
        app.dependency_overrides.clear()

    assert missing.status_code == 401
    assert expired.status_code == 401


def test_protected_route_rejects_malformed_and_unsupported_role_tokens(db_session):
    role = Role(name="technician")
    db_session.add(role)
    db_session.flush()
    user = User(
        email="field@example.test",
        display_name="Field Technician",
        password_hash=hash_password("correct horse battery"),
        role_id=role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    now = datetime.now(UTC)
    malformed_claims = jwt.encode(
        {"sub": user.id, "role": "technician", "exp": now + timedelta(minutes=5)},
        get_settings().jwt_secret,
        algorithm=ALGORITHM,
    )
    wrong_role_claims = jwt.encode(
        {"sub": user.id, "role": "auditor", "iat": now, "exp": now + timedelta(minutes=5)},
        get_settings().jwt_secret,
        algorithm=ALGORITHM,
    )
    future_issue_claims = jwt.encode(
        {"sub": user.id, "role": "technician", "iat": now + timedelta(minutes=5), "exp": now + timedelta(minutes=10)},
        get_settings().jwt_secret,
        algorithm=ALGORITHM,
    )

    app.dependency_overrides[get_session] = lambda: db_session
    try:
        client = TestClient(app)
        malformed = client.get("/auth/me", headers={"Authorization": f"Bearer {malformed_claims}"})
        wrong_role = client.get("/auth/me", headers={"Authorization": f"Bearer {wrong_role_claims}"})
        future_issue = client.get("/auth/me", headers={"Authorization": f"Bearer {future_issue_claims}"})
    finally:
        app.dependency_overrides.clear()

    assert malformed.status_code == 401
    assert wrong_role.status_code == 401
    assert future_issue.status_code == 401
