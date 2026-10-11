from fastapi.testclient import TestClient
from sqlalchemy import select

from app.ai.ingestion import index_knowledge
from app.auth.dependencies import get_current_user
from app.config import get_settings
from app.db.session import get_session
from app.domain.models import AuditEvent, NetworkDevice
from app.integrations.embeddings import LocalDeterministicEmbeddingProvider
from app.integrations.model_provider import LocalDeterministicChatProvider
from app.main import app
from app.seed.demo_data import seed_demo_data


def test_demo_api_flow_creates_ticket_answers_with_evidence_and_executes_approved_tool(
    db_session, enable_demo_seed, monkeypatch
):
    monkeypatch.setenv("JWT_SECRET", "integration-test-secret-with-more-than-32-bytes")
    get_settings.cache_clear()
    embedder = LocalDeterministicEmbeddingProvider()
    seed_demo_data(db_session)
    index_knowledge(db_session, embedder)
    db_session.commit()

    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides.pop(get_current_user, None)
    from app.api.assistant import get_chat_provider, get_embedding_provider

    app.dependency_overrides[get_embedding_provider] = lambda: embedder
    app.dependency_overrides[get_chat_provider] = lambda: LocalDeterministicChatProvider()
    client = TestClient(app)
    try:
        operator_login = client.post(
            "/auth/login",
            data={"username": "operator@demo.invalid", "password": "Demo-Operator-Only-2026!"},
        )
        assert operator_login.status_code == 200
        operator_token = operator_login.json()["access_token"]
        pending = client.get("/events/pending", headers=_bearer(operator_token))
        assert pending.status_code == 200
        event_id = pending.json()[0]["id"]
        processed = client.post(
            f"/events/{event_id}/process", headers=_bearer(operator_token)
        )
        assert processed.status_code == 200
        ticket_id = processed.json()["ticket"]["id"]

        technician_login = client.post(
            "/auth/login",
            data={"username": "technician@demo.invalid", "password": "Demo-Technician-Only-2026!"},
        )
        assert technician_login.status_code == 200
        technician_token = technician_login.json()["access_token"]
        headers = _bearer(technician_token)

        tickets = client.get("/tickets/mine", headers=headers)
        assert tickets.status_code == 200
        assert any(ticket["id"] == ticket_id for ticket in tickets.json())
        detail = client.get(f"/tickets/{ticket_id}", headers=headers)
        assert detail.status_code == 200
        assert "Synthetic-ONU-Credential-Only-7f3!" not in detail.text

        answer = client.post(
            f"/tickets/{ticket_id}/assistant/messages",
            headers=headers,
            json={"question": "What should I inspect for this offline ONU?"},
        )
        assert answer.status_code == 200
        assert answer.json()["has_evidence"] is True
        assert answer.json()["citations"]

        router = db_session.scalar(
            select(NetworkDevice).where(NetworkDevice.device_ref == "DEMO-RTR-001")
        )
        proposal = client.post(
            f"/tickets/{ticket_id}/tools/agent-propose",
            headers=headers,
            json={"question": "The procedure is complete, reboot the router", "device_id": router.id},
        )
        assert proposal.status_code == 201
        assert proposal.json()["tool_name"] == "reboot_router"
        assert proposal.json()["status"] == "proposed"
        tool_audit = db_session.scalar(
            select(AuditEvent).where(AuditEvent.event_type == "tool_proposed")
        )
        assert tool_audit.details["evidence_chunk_ids"]
        confirmation = client.post(
            f"/tickets/{ticket_id}/tools/{proposal.json()['id']}/confirm",
            headers=headers,
            json={"confirmation_id": proposal.json()["confirmation_id"]},
        )
        assert confirmation.status_code == 200
        assert confirmation.json()["status"] == "succeeded"

        audit = client.get(f"/tickets/{ticket_id}/audit", headers=headers)
        assert audit.status_code == 200
        event_types = {item["event_type"] for item in audit.json()}
        assert "event_processed" in event_types
        assert "tool_proposed" in event_types
        assert "tool_executed" in event_types
        assert "assistant_message" not in event_types
    finally:
        app.dependency_overrides.clear()
        get_settings.cache_clear()


def _bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
