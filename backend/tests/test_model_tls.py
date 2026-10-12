import logging

import httpx
import pytest

from app.ai.ports import ChatMessage
from app.config import Settings
from app.integrations.embeddings import build_embedding_provider
from app.integrations.model_provider import build_chat_provider


def _settings(**overrides):
    return Settings(
        _env_file=None,
        database_url="sqlite+pysqlite:///:memory:",
        jwt_secret="test-only-secret",
        model_base_url="https://gateway.example.test/v1",
        model_api_key="test-key-not-for-logging",
        model_name="test-chat",
        embedding_model="qwen3-embedding-0.6b",
        embedding_provider="hosted",
        model_provider="hosted",
        embedding_dimensions=1024,
        **overrides,
    )


def test_tls_defaults_remain_secure(monkeypatch):
    monkeypatch.delenv("APP_ENVIRONMENT", raising=False)
    monkeypatch.delenv("MODEL_TLS_VERIFY", raising=False)
    settings = _settings()
    assert settings.app_environment == "production"
    assert settings.model_tls_verify is True
    assert build_embedding_provider(settings).tls_verify is True
    assert build_chat_provider(settings).tls_verify is True


@pytest.mark.parametrize("environment", ["production", "test"])
def test_insecure_tls_rejected_outside_development(environment):
    with pytest.raises(ValueError, match="requires APP_ENVIRONMENT=development"):
        _settings(app_environment=environment, model_tls_verify=False)


def test_environment_variables_enable_explicit_development_override(monkeypatch):
    monkeypatch.setenv("APP_ENVIRONMENT", "development")
    monkeypatch.setenv("MODEL_TLS_VERIFY", "false")
    assert _settings().model_tls_verify is False
    monkeypatch.setenv("APP_ENVIRONMENT", "production")
    with pytest.raises(ValueError, match="requires APP_ENVIRONMENT=development"):
        _settings()


@pytest.mark.parametrize("tls_verify", [True, False])
@pytest.mark.parametrize("provider_kind", ["embedding", "chat"])
def test_model_client_verification_and_secret_free_warning(monkeypatch, caplog, tls_verify, provider_kind):
    settings = _settings(app_environment="development", model_tls_verify=tls_verify)
    created = []
    requests = []
    real_client = httpx.Client

    def handler(request):
        requests.append(request)
        if provider_kind == "embedding":
            return httpx.Response(200, json={"data": [{"embedding": [1.0] + [0.0] * 1023}]})
        return httpx.Response(200, json={"choices": [{"message": {"content": "test answer"}}]})

    def client_factory(**kwargs):
        client = real_client(transport=httpx.MockTransport(handler), **kwargs)
        created.append((kwargs, client))
        return client

    monkeypatch.setattr("app.integrations.model_http.httpx.Client", client_factory)
    with caplog.at_level(logging.WARNING, logger="app.integrations.model_http"):
        if provider_kind == "embedding":
            assert len(build_embedding_provider(settings).embed_query("generic test")) == 1024
        else:
            assert build_chat_provider(settings).complete([ChatMessage(role="user", content="generic test")]) == "test answer"
    assert created[0][0] == {"timeout": 30.0 if provider_kind == "embedding" else 60.0, "verify": tls_verify}
    assert created[0][1].is_closed
    assert requests[0].headers["Authorization"] == "Bearer test-key-not-for-logging"
    assert ("DEVELOPMENT ONLY" in caplog.text) is (not tls_verify)
    assert "test-key-not-for-logging" not in caplog.text
    assert "gateway.example.test" not in caplog.text


def test_tls_override_does_not_change_embedding_identity():
    secure = build_embedding_provider(_settings(app_environment="development", model_tls_verify=True))
    insecure = build_embedding_provider(_settings(app_environment="development", model_tls_verify=False))
    assert secure.profile == insecure.profile
