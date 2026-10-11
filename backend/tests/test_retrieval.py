import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.ai import context as context_module
from app.ai import retrieval
from app.ai.chunking import chunk_id_for
from app.ai.ingestion import embed_missing_chunks
from app.api.knowledge import get_embedding_provider
from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.models import (
    Customer,
    KnowledgeChunk,
    KnowledgeDocument,
    NetworkDevice,
    NetworkEvent,
    Role,
    Service,
    Ticket,
    User,
)
from app.main import app
from app.services.ticket_queries import TicketNotFoundError


@pytest.fixture
def embedder():
    from app.integrations.embeddings import LocalDeterministicEmbeddingProvider

    return LocalDeterministicEmbeddingProvider(1536)


def _add_document(
    session: Session,
    *,
    document_key: str,
    title: str,
    source_type: str,
    sections: dict[str, str],
    version: str = "1.0",
) -> None:
    session.add(
        KnowledgeDocument(
            id=document_key,
            document_key=document_key,
            title=title,
            source_type=source_type,
            version=version,
        )
    )
    for section, content in sections.items():
        session.add(
            KnowledgeChunk(
                id=chunk_id_for(document_key, version, section),
                document_id=document_key,
                section=section,
                content=content,
            )
        )
    session.flush()


def _workspace(session: Session) -> dict[str, object]:
    technician_role = Role(name="technician")
    session.add(technician_role)
    session.flush()

    technician = User(
        email="technician@test.invalid",
        display_name="Test Technician",
        password_hash="synthetic-test-hash",
        role_id=technician_role.id,
        is_active=True,
    )
    customer = Customer(customer_ref="CUST-1", name="Test Customer", address="1 Test Way")
    session.add_all([technician, customer])
    session.flush()

    service = Service(
        customer_id=customer.id,
        service_type="Granite",
        service_ref="SVC-1",
        status="active",
        details={
            "onu_password": "Synthetic-Secret-Only",
            "account_ref": "ACC-1",
            "note": "password marker in a non-credential field",
        },
    )
    device = NetworkDevice(
        customer_id=customer.id,
        device_ref="DEV-1",
        device_type="ONU",
        name="Test ONU",
        status="offline",
    )
    session.add_all([service, device])
    session.flush()

    event = NetworkEvent(
        source_event_id="EVT-1",
        event_type="ONU_OFFLINE",
        device_id=device.id,
        service_id=service.id,
        payload={"signal_state": "no_link"},
    )
    session.add(event)
    session.flush()

    ticket = Ticket(
        source_event_id=event.id,
        customer_id=customer.id,
        service_id=service.id,
        assigned_technician_id=technician.id,
        severity="high",
        status="open",
        summary="ONU offline at the test customer",
    )
    session.add(ticket)
    session.commit()

    return {"technician": technician, "customer": customer, "service": service, "ticket": ticket}


def _technician_actor(workspace: dict[str, object]) -> AuthenticatedUser:
    technician = workspace["technician"]
    return AuthenticatedUser(id=technician.id, email=technician.email, role="technician")


def _seed_category_corpus(session: Session, embedder) -> None:
    _add_document(
        session,
        document_key="kb-granite-v1",
        title="Granite Handoff Checks",
        source_type="Granite",
        sections={"Granite checks": "Verify the Granite service handoff and optical readings."},
    )
    _add_document(
        session,
        document_key="kb-hsi-v1",
        title="HSI Session Checks",
        source_type="HSI",
        sections={"HSI checks": "Verify the HSI router session and authentication."},
    )
    _add_document(
        session,
        document_key="kb-general-v1",
        title="General Field Checks",
        source_type="curated_procedure",
        sections={"General checks": "Confirm service impact before dispatch."},
    )
    embed_missing_chunks(session, embedder)
    session.commit()


def test_retrieval_returns_relevant_chunk_with_citation_metadata(db_session, embedder):
    _add_document(
        db_session,
        document_key="kb-optical-v1",
        title="Optical Loss Triage",
        source_type="curated_procedure",
        sections={
            "Field inspection": "Inspect connectors and cable routing for contamination, strain, or tight bends.",
            "Record and route": "Record the measured receive level and equipment identifiers.",
        },
    )
    _add_document(
        db_session,
        document_key="kb-router-v1",
        title="Router Reboot",
        source_type="curated_procedure",
        sections={"Reboot steps": "Power cycle the home router and wait for the status light."},
    )
    embed_missing_chunks(db_session, embedder)
    db_session.commit()

    matches = retrieval.retrieve(db_session, "optical inspection", embedder, limit=5)

    assert matches
    top = matches[0]
    assert top.document_id == "kb-optical-v1"
    assert top.document_title == "Optical Loss Triage"
    assert top.section == "Field inspection"
    assert top.content.startswith("Inspect connectors")
    assert top.chunk_id == "kb-optical-v1:1.0:field-inspection"
    assert [match.score for match in matches] == sorted(
        [match.score for match in matches], reverse=True
    )


def test_retrieval_applies_service_category_filter_and_allows_global(db_session, embedder):
    _seed_category_corpus(db_session, embedder)

    granite = retrieval.retrieve(db_session, "service checks", embedder, service_category="Granite", limit=10)
    granite_ids = {match.document_id for match in granite}
    assert "kb-granite-v1" in granite_ids
    assert "kb-general-v1" in granite_ids
    assert "kb-hsi-v1" not in granite_ids

    hsi = retrieval.retrieve(db_session, "service checks", embedder, service_category="HSI", limit=10)
    hsi_ids = {match.document_id for match in hsi}
    assert "kb-hsi-v1" in hsi_ids
    assert "kb-general-v1" in hsi_ids
    assert "kb-granite-v1" not in hsi_ids

    unfiltered = retrieval.retrieve(db_session, "service checks", embedder, limit=10)
    assert {match.document_id for match in unfiltered} == {
        "kb-granite-v1",
        "kb-hsi-v1",
        "kb-general-v1",
    }


def test_empty_retrieval_returns_no_matches(db_session, embedder):
    assert retrieval.retrieve(db_session, "anything at all", embedder) == []


def test_retrieve_for_ticket_uses_the_authorized_service_category(db_session, embedder):
    workspace = _workspace(db_session)
    _seed_category_corpus(db_session, embedder)

    matches = retrieval.retrieve_for_ticket(
        db_session,
        workspace["ticket"].id,
        _technician_actor(workspace),
        "service checks",
        embedder,
        limit=10,
    )

    ids = {match.document_id for match in matches}
    assert "kb-granite-v1" in ids
    assert "kb-general-v1" in ids
    assert "kb-hsi-v1" not in ids


def test_retrieve_for_ticket_denies_an_unassigned_technician(db_session, embedder):
    workspace = _workspace(db_session)
    _seed_category_corpus(db_session, embedder)
    intruder = AuthenticatedUser(id="someone-else", email="intruder@test.invalid", role="technician")

    with pytest.raises(HTTPException) as error:
        retrieval.retrieve_for_ticket(db_session, workspace["ticket"].id, intruder, "checks", embedder)

    assert error.value.status_code == 404


def test_retrieve_for_ticket_raises_not_found_for_unknown_ticket(db_session, embedder):
    workspace = _workspace(db_session)

    with pytest.raises(TicketNotFoundError):
        retrieval.retrieve_for_ticket(
            db_session,
            "does-not-exist",
            _technician_actor(workspace),
            "checks",
            embedder,
        )


def test_knowledge_search_endpoint_scopes_to_ticket(db_session, embedder):
    workspace = _workspace(db_session)
    _seed_category_corpus(db_session, embedder)

    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: _technician_actor(workspace)
    app.dependency_overrides[get_embedding_provider] = lambda: embedder
    try:
        response = TestClient(app).get(
            "/knowledge/search",
            params={"q": "service checks", "ticket_id": workspace["ticket"].id},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    document_ids = {item["document_id"] for item in response.json()}
    assert "kb-granite-v1" in document_ids
    assert "kb-hsi-v1" not in document_ids


def test_context_excludes_secrets_and_redacts_credential_values(db_session, embedder):
    workspace = _workspace(db_session)

    context = context_module.assemble_context(
        db_session,
        workspace["ticket"].id,
        _technician_actor(workspace),
    )

    service = context.services[0]
    assert "onu_password" not in service.details
    assert service.details["account_ref"] == "ACC-1"
    assert service.details["note"] == "[redacted]"
    assert "Synthetic-Secret-Only" not in context.as_prompt_text()
