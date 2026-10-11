from argon2 import PasswordHasher
from sqlalchemy import func, select

from app.domain.models import (
    AssistantMessage, AssistantSession, AuditEvent, Customer, KnowledgeChunk,
    KnowledgeDocument, NetworkDevice, NetworkEvent, Role, Service, Ticket,
    ToolExecution, TopologyEdge, User,
)
from app.seed.demo_data import DEMO_ACCOUNTS, seed_demo_data


def test_seed_is_idempotent_and_contains_expected_demo_records(db_session):
    seed_demo_data(db_session)
    counts_after_first_run = _seed_counts(db_session)

    seed_demo_data(db_session)
    counts_after_second_run = _seed_counts(db_session)

    assert counts_after_first_run == {
        "users": 2,
        "customers": 1,
        "services": 3,
        "network_devices": 3,
        "topology_edges": 2,
        "network_events": 1,
        "pending_events": 1,
        "tickets": 0,
        "knowledge_documents": 2,
        "knowledge_chunks": 6,
        "assistant_sessions": 0,
        "assistant_messages": 0,
        "tool_executions": 0,
        "audit_events": 0,
    }
    assert counts_after_second_run == counts_after_first_run

    users = {user.email: user for user in db_session.scalars(select(User).where(User.email.in_(DEMO_ACCOUNTS))).all()}
    assert set(users) == set(DEMO_ACCOUNTS)
    assert all(user.password_hash.startswith("$argon2id$") for user in users.values())
    assert all(PasswordHasher().verify(user.password_hash, DEMO_ACCOUNTS[email]) for email, user in users.items())
    roles = {role.id: role.name for role in db_session.scalars(select(Role)).all()}
    assert roles[users["operator@demo.invalid"].role_id] == "operator"
    assert roles[users["technician@demo.invalid"].role_id] == "technician"
    assert all(user.is_active for user in users.values())


def _count(session, model, criterion=None):
    statement = select(func.count()).select_from(model)
    if criterion is not None:
        statement = statement.where(criterion)
    return session.scalar(statement)


def _seed_counts(session):
    return {
        "users": _count(session, User),
        "customers": _count(session, Customer),
        "services": _count(session, Service),
        "network_devices": _count(session, NetworkDevice),
        "topology_edges": _count(session, TopologyEdge),
        "network_events": _count(session, NetworkEvent),
        "pending_events": _count(session, NetworkEvent, NetworkEvent.processed_at.is_(None)),
        "tickets": _count(session, Ticket),
        "knowledge_documents": _count(session, KnowledgeDocument),
        "knowledge_chunks": _count(session, KnowledgeChunk),
        "assistant_sessions": _count(session, AssistantSession),
        "assistant_messages": _count(session, AssistantMessage),
        "tool_executions": _count(session, ToolExecution),
        "audit_events": _count(session, AuditEvent),
    }
