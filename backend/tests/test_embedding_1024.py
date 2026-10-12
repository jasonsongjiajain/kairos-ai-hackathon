import json

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.ai.embedding_space import EmbeddingError, space_for, validate_vector
from app.ai.ingestion import embed_missing_chunks, index_knowledge, verify_embeddings
from app.ai.retrieval import cosine_similarity, retrieve
from app.api.knowledge import get_embedding_provider
from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.config import Settings
from app.db.session import get_session
from app.domain.models import KnowledgeChunk
from app.integrations.embeddings import HostedEmbeddingProvider, LocalDeterministicEmbeddingProvider, build_embedding_provider
from app.main import app


class FakeQwen:
    dimension = 1024
    profile = "test:qwen:1024"

    def __init__(self):
        self.calls = 0

    def embed_documents(self, texts):
        self.calls += len(texts)
        return [[0.6, 0.8] + [0.0] * 1022 for _ in texts]

    def embed_query(self, text):
        return [0.6, 0.8] + [0.0] * 1022


def _hosted(handler, **kwargs):
    return HostedEmbeddingProvider(
        base_url="https://gateway.example.test/llm/v1", api_key="test-secret-never-log",
        model="qwen3-embedding-0.6b", dimension=1024,
        client=httpx.Client(transport=httpx.MockTransport(handler)), **kwargs,
    )


def test_1024_index_preserves_1536_vectors_and_reuses_only_matching_model(db_session):
    index_knowledge(db_session, LocalDeterministicEmbeddingProvider())
    db_session.commit()
    original = {chunk.id: list(chunk.embedding) for chunk in db_session.scalars(select(KnowledgeChunk))}
    qwen = FakeQwen()
    assert embed_missing_chunks(db_session, qwen) == (6, 0)
    db_session.commit()
    assert embed_missing_chunks(db_session, qwen) == (0, 6)
    assert qwen.calls == 6
    for chunk in db_session.scalars(select(KnowledgeChunk)):
        assert list(chunk.embedding) == original[chunk.id]
        assert len(chunk.embedding_1024) == 1024
        assert chunk.embedding_1024_profile == qwen.profile
    assert len(retrieve(db_session, "slow internet", qwen, limit=10)) == 6


def test_models_of_equal_dimensions_are_never_mixed(db_session):
    qwen = FakeQwen()
    index_knowledge(db_session, qwen)
    db_session.commit()
    different = FakeQwen()
    different.profile = "test:different-model:1024"
    assert retrieve(db_session, "question", different) == []
    assert embed_missing_chunks(db_session, different) == (6, 0)
    db_session.commit()
    assert retrieve(db_session, "question", qwen) == []
    assert len(retrieve(db_session, "question", different)) == 5


def test_verification_requires_a_complete_matching_model_index(db_session):
    qwen = FakeQwen()
    with pytest.raises(EmbeddingError, match="no knowledge text"):
        verify_embeddings(db_session, qwen)
    index_knowledge(db_session, qwen)
    db_session.commit()
    assert verify_embeddings(db_session, qwen) == 6
    chunk = db_session.scalar(select(KnowledgeChunk))
    chunk.embedding_1024_profile = "test:another-model"
    db_session.commit()
    with pytest.raises(EmbeddingError, match="1 of 6"):
        verify_embeddings(db_session, qwen)


def test_legacy_vectors_are_not_a_fallback_for_missing_qwen_vectors(db_session):
    local = LocalDeterministicEmbeddingProvider()
    index_knowledge(db_session, local)
    db_session.commit()
    assert retrieve(db_session, "optical loss", local)
    assert retrieve(db_session, "optical loss", FakeQwen()) == []


def test_unlabelled_legacy_local_vectors_are_verified_without_replacing_values(db_session):
    local = LocalDeterministicEmbeddingProvider()
    index_knowledge(db_session, local)
    chunks = list(db_session.scalars(select(KnowledgeChunk)))
    original = {chunk.id: list(chunk.embedding) for chunk in chunks}
    for chunk in chunks:
        chunk.embedding_profile = None
    db_session.commit()
    assert retrieve(db_session, "optical loss", local) == []
    assert embed_missing_chunks(db_session, local) == (0, 6)
    db_session.commit()
    assert {chunk.id: list(chunk.embedding) for chunk in chunks} == original
    assert retrieve(db_session, "optical loss", local)


def test_unknown_legacy_vectors_are_not_mislabelled_or_overwritten(db_session):
    local = LocalDeterministicEmbeddingProvider()
    index_knowledge(db_session, local)
    chunk = db_session.scalar(select(KnowledgeChunk).order_by(KnowledgeChunk.id))
    chunk.embedding = [1.0] + [0.0] * 1535
    chunk.embedding_profile = None
    db_session.commit()
    with pytest.raises(EmbeddingError, match="could not be verified"):
        embed_missing_chunks(db_session, local)
    db_session.rollback()
    assert chunk.embedding_profile is None
    assert list(chunk.embedding) == [1.0] + [0.0] * 1535


def test_gateway_failure_rolls_back_partial_index_and_preserves_old_vectors(db_session):
    index_knowledge(db_session, LocalDeterministicEmbeddingProvider())
    db_session.commit()
    class FailsMidway(FakeQwen):
        def embed_documents(self, texts):
            if self.calls == 2:
                raise EmbeddingError("Gateway unavailable")
            return super().embed_documents(texts)
    with pytest.raises(EmbeddingError):
        embed_missing_chunks(db_session, FailsMidway())
    db_session.rollback()
    for chunk in db_session.scalars(select(KnowledgeChunk)):
        assert chunk.embedding is not None
        assert chunk.embedding_1024 is None and chunk.embedding_1024_profile is None


def test_adapter_validates_gateway_vectors_and_adds_qwen_query_instruction():
    requests = []
    def handler(request):
        requests.append(request)
        return httpx.Response(200, json={"data": [{"index": 0, "embedding": [1.0] + [0.0] * 1023}]})
    provider = _hosted(handler)
    document = "Check router speed and optical signal."
    assert len(provider.embed_documents([document])[0]) == 1024
    assert len(provider.embed_query("Why is my Internet slow?")) == 1024
    assert requests[0].url.path == "/llm/v1/embeddings"
    assert requests[0].headers["Authorization"] == "Bearer test-secret-never-log"
    assert json.loads(requests[0].content)["input"] == document
    query = json.loads(requests[1].content)["input"]
    assert query.startswith("Instruct: ") and "\nQuery:Why is my Internet slow?" in query


@pytest.mark.parametrize("vector", [
    [1.0] * 1536, [0.0] * 1024, [float("nan")] + [1.0] * 1023,
    [float("inf")] + [1.0] * 1023, [True] + [1.0] * 1023, ["1"] * 1024, None,
])
def test_invalid_vectors_are_rejected_without_truncation(vector):
    with pytest.raises(EmbeddingError):
        validate_vector(vector, 1024)


@pytest.mark.parametrize("payload", [{}, {"data": []}, {"data": [None]}, {"data": [{"embedding": [1, 2]}]}])
def test_malformed_gateway_responses_are_rejected(payload):
    provider = _hosted(lambda request: httpx.Response(200, json=payload))
    with pytest.raises(EmbeddingError):
        provider.embed_query("test")


def test_safe_gateway_errors_do_not_reveal_response_body_or_key():
    provider = _hosted(lambda request: httpx.Response(401, text="private response test-secret-never-log"))
    with pytest.raises(EmbeddingError, match="HTTP 401") as error:
        provider.embed_query("test")
    assert "private response" not in str(error.value) and "test-secret" not in str(error.value)
    def unavailable(request):
        raise httpx.ConnectError("DNS lookup failed", request=request)
    with pytest.raises(EmbeddingError, match="VPN"):
        _hosted(unavailable).embed_query("test")


def test_profile_changes_with_model_gateway_and_prompt_but_not_key_rotation():
    handler = lambda request: httpx.Response(200, json={"data": [{"embedding": [1.0] + [0.0] * 1023}]})
    original = _hosted(handler)
    rotated_key = HostedEmbeddingProvider(base_url=original.base_url + "/", api_key="new-secret", model=original.model, dimension=1024)
    assert rotated_key.profile == original.profile
    changed_prompt = _hosted(handler, query_instruction="Different retrieval task")
    changed_model = HostedEmbeddingProvider(base_url=original.base_url, api_key="secret", model="different", dimension=1024)
    changed_gateway = HostedEmbeddingProvider(base_url="https://other.example.test/v1", api_key="secret", model=original.model, dimension=1024)
    assert len({original.profile, changed_prompt.profile, changed_model.profile, changed_gateway.profile}) == 4


def test_storage_dimensions_are_fixed_independently_of_settings():
    settings = Settings(embedding_provider="hosted", embedding_dimensions=1024)
    assert build_embedding_provider(settings).dimension == 1024
    assert KnowledgeChunk.__table__.c.embedding.type.dim == 1536
    assert KnowledgeChunk.__table__.c.embedding_1024.type.dim == 1024
    assert space_for(FakeQwen()).vector_attribute == "embedding_1024"
    with pytest.raises(ValueError, match="fixed at 1536"):
        LocalDeterministicEmbeddingProvider(1024)
    with pytest.raises(EmbeddingError, match="different dimensions"):
        cosine_similarity([1.0, 0.0], [1.0])


def test_bad_embedding_response_becomes_safe_502_in_search_endpoint(db_session):
    provider = _hosted(lambda request: httpx.Response(200, json={"data": [{"embedding": [1, 2]}]}))
    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(id="staff", email="staff@test.invalid", role="operator")
    app.dependency_overrides[get_embedding_provider] = lambda: provider
    try:
        response = TestClient(app).get("/knowledge/search", params={"q": "slow internet"})
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 502
    assert "1024" in response.json()["detail"]
    assert "test-secret" not in response.text
