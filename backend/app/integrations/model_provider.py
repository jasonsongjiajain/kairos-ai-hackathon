"""Chat completion providers selected by ``MODEL_PROVIDER``.

The local provider is deterministic and key-free so the answer path can run in
tests and offline. A hosted OpenAI-compatible provider can replace it.
"""

import json
from collections.abc import Sequence

import httpx

from app.ai.ports import ChatCompletionProvider, ChatMessage
from app.config import Settings


class LocalDeterministicChatProvider:
    """Key-free stub used for local runs and tests.

    It returns a deterministic echo rather than pretending to reason, so it can
    never fabricate evidence; the assistant layer supplies retrieved citations.
    """

    def complete(self, messages: Sequence[ChatMessage], *, temperature: float = 0.0) -> str:
        last_user = next((message.content for message in reversed(messages) if message.role == "user"), "")
        return json.dumps(
            {"provider": "local-deterministic", "prompt_excerpt": last_user[:200]},
            separators=(",", ":"),
        )


class HostedChatCompletionProvider:
    """OpenAI-compatible ``/chat/completions`` calls for a configured provider."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self._client = client

    def complete(self, messages: Sequence[ChatMessage], *, temperature: float = 0.0) -> str:
        if not self.api_key or self.api_key.startswith("LOCAL_ONLY"):
            raise RuntimeError("MODEL_PROVIDER=hosted requires a configured MODEL_API_KEY")
        client = self._client or httpx.Client(timeout=60.0)
        try:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "temperature": temperature,
                    "messages": [{"role": message.role, "content": message.content} for message in messages],
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        finally:
            if self._client is None:
                client.close()


def build_chat_provider(settings: Settings) -> ChatCompletionProvider:
    provider = settings.model_provider.strip().lower()
    if provider in ("", "local", "deterministic"):
        return LocalDeterministicChatProvider()
    if provider == "hosted":
        return HostedChatCompletionProvider(
            base_url=settings.model_base_url,
            api_key=settings.model_api_key,
            model=settings.model_name,
        )
    raise ValueError(f"Unknown MODEL_PROVIDER: {settings.model_provider}")
