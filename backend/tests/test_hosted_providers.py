import httpx
import pytest

from app.ai.ports import ChatMessage
from app.config import Settings
from app.integrations.embeddings import HostedEmbeddingProvider, build_embedding_provider
from app.integrations.model_provider import (
    HostedChatCompletionProvider,
    build_chat_provider,
)


def settings(**overrides) -> Settings:
    return Settings(
        database_url="sqlite+pysqlite:///:memory:",
        jwt_secret="test-secret",
        model_api_key="test-api-key",
        model_base_url="https://gigx.nexa-dev.tm.com.my/llm/v1",
        model_provider="hosted",
        reasoning_provider="hosted",
        embedding_provider="hosted",
        **overrides,
    )


def test_chat_and_reasoning_builders_select_distinct_gigx_models():
    config = settings()

    chat = build_chat_provider(config)
    reasoning = build_chat_provider(config, purpose="reasoning")

    assert isinstance(chat, HostedChatCompletionProvider)
    assert isinstance(reasoning, HostedChatCompletionProvider)
    assert chat.model == "gigx/gemma-4-e2b-it"
    assert reasoning.model == "gigx/qwen3-vl-4b-instruct"
    assert chat.base_url == "https://gigx.nexa-dev.tm.com.my/llm/v1"


def test_chat_completion_sends_openai_compatible_request():
    request_bodies = []
    request_metadata = []

    def handler(request: httpx.Request) -> httpx.Response:
        request_bodies.append(request.read().decode())
        request_metadata.append((request.url.path, request.headers["authorization"]))
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": '{"answer":"grounded"}'}}]},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    provider = HostedChatCompletionProvider(
        base_url="https://gigx.nexa-dev.tm.com.my/llm/v1",
        api_key="test-api-key",
        model="gigx/gemma-4-e2b-it",
        client=client,
    )

    response = provider.complete([ChatMessage(role="user", content="question")])

    assert response == '{"answer":"grounded"}'
    assert request_metadata[0] == ("/llm/v1/chat/completions", "Bearer test-api-key")
    assert request_bodies[0].startswith("{")
    assert '"model":"gigx/gemma-4-e2b-it"' in request_bodies[0]
    client.close()


def test_hosted_embedding_validates_vector_dimension():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": [{"embedding": [0.25, 0.75]}]})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    provider = HostedEmbeddingProvider(
        base_url="https://gigx.nexa-dev.tm.com.my/llm/v1",
        api_key="test-api-key",
        model="gigx/qwen3-embedding-0.6b",
        dimension=1536,
        client=client,
    )

    with pytest.raises(RuntimeError, match="database schema requires 1536"):
        provider.embed_query("optical signal")
    client.close()


def test_hosted_embedding_builder_uses_configured_model():
    provider = build_embedding_provider(settings())

    assert isinstance(provider, HostedEmbeddingProvider)
    assert provider.model == "gigx/qwen3-embedding-0.6b"
    assert provider.dimension == 1536
