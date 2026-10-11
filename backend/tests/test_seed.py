from collections import Counter

from argon2 import PasswordHasher
from sqlalchemy import select

from app.domain import models
from app.domain.models import NetworkEvent, Role, User
from app.seed.demo_data import DEMO_ACCOUNTS, seed_demo_data


def test_seed_is_idempotent_and_contains_expected_demo_records(db_session):
    seed_demo_data(db_session)
    counts_after_first_run = _model_counts(db_session)

    seed_demo_data(db_session)
    counts_after_second_run = _model_counts(db_session)

    assert counts_after_second_run == counts_after_first_run
    assert db_session.scalar(select(NetworkEvent).where(NetworkEvent.processed_at.is_(None)))
    assert len(db_session.scalars(select(NetworkEvent).where(NetworkEvent.processed_at.is_(None))).all()) == 1
    users = {user.email: user for user in db_session.scalars(select(User)).all()}
    assert set(DEMO_ACCOUNTS) <= users.keys()
    assert all(user.password_hash.startswith("$argon2id$") for user in users.values())
    assert all(PasswordHasher().verify(user.password_hash, password) for email, password in DEMO_ACCOUNTS.items() for user in [users[email]])
    assert {role.name for role in db_session.scalars(select(Role)).all()} >= {"operator", "technician"}


def _model_counts(session):
    return Counter(
        {
            mapper.class_.__tablename__: len(session.scalars(select(mapper.class_)).all())
            for mapper in models.Base.registry.mappers
        }
    )
