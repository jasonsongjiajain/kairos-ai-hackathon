"""Embedding providers selected by ``EMBEDDING_PROVIDER``.

The local provider is deterministic and key-free, so the app and tests run
without an external model. A hosted OpenAI-compatible provider can replace it.
"""

import hashlib
import math
import re
from collections.abc import Sequence

import httpx

from app.ai.ports import EmbeddingProvider
from app.config import Settings

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


class LocalDeterministicEmbeddingProvider:
    """Stable hashed bag-of-words vectors; no network and no API key."""

    def __init__(self, dimension: int = 1536) -> None:
        if dimension != 1536:
            raise ValueError("The local embedding provider is fixed at 1536 dimensions")
        self.dimension = dimension

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        for feature in _features(text):
            digest = hashlib.sha256(feature.encode("utf-8")).digest()
            vector[int.from_bytes(digest[:8], "big") % self.dimension] += 1.0
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0.0:
            fallback = [0.0] * self.dimension
            fallback[0] = 1.0
            return fallback
        return [value / norm for value in vector]


class HostedEmbeddingProvider:
    """OpenAI-compatible ``/embeddings`` calls for a configured provider."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        dimension: int,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.dimension = dimension
        self._client = client

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._request(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._request(text)

    def _request(self, text: str) -> list[float]:
        if not self.api_key or self.api_key.startswith("LOCAL_ONLY"):
            raise RuntimeError("EMBEDDING_PROVIDER=hosted requires a configured MODEL_API_KEY")
        client = self._client or httpx.Client(timeout=30.0)
        try:
            response = client.post(
                f"{self.base_url}/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "input": text},
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        finally:
            if self._client is None:
                client.close()


def build_embedding_provider(settings: Settings) -> EmbeddingProvider:
    provider = settings.embedding_provider.strip().lower()
    if provider in ("", "local", "deterministic"):
        return LocalDeterministicEmbeddingProvider(settings.embedding_dimensions)
    if provider == "hosted":
        return HostedEmbeddingProvider(
            base_url=settings.model_base_url,
            api_key=settings.model_api_key,
            model=settings.embedding_model,
            dimension=settings.embedding_dimensions,
        )
    raise ValueError(f"Unknown EMBEDDING_PROVIDER: {settings.embedding_provider}")


def _features(text: str) -> list[str]:
    tokens = _TOKEN_PATTERN.findall(text.lower())
    bigrams = [f"{first} {second}" for first, second in zip(tokens, tokens[1:])]
    return tokens + bigrams
