"""Embedding providers selected by ``EMBEDDING_PROVIDER``.

The local provider is deterministic and key-free, so the app and tests run
without an external model. A hosted OpenAI-compatible provider can replace it.
"""

import hashlib
import json
import math
import re
from collections.abc import Sequence

import httpx

from app.ai.ports import EmbeddingProvider
from app.ai.embedding_space import EmbeddingError, validate_vector
from app.config import Settings
from app.integrations.model_http import create_model_client

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
LOCAL_EMBEDDING_PROFILE = "local:sha256-bow-v1:1536"
QWEN_QUERY_INSTRUCTION = "Given a telecom support question, retrieve relevant troubleshooting procedures."


class LocalDeterministicEmbeddingProvider:
    """Stable hashed bag-of-words vectors; no network and no API key."""

    def __init__(self, dimension: int = 1536) -> None:
        if dimension != 1536:
            raise ValueError("The local embedding provider is fixed at 1536 dimensions")
        self.dimension = dimension
        self.profile = LOCAL_EMBEDDING_PROFILE

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
        query_instruction: str | None = None,
        tls_verify: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.dimension = dimension
        self.tls_verify = tls_verify
        if dimension not in (1024, 1536):
            raise EmbeddingError("Supported embedding dimensions are 1024 and 1536")
        self.query_instruction = query_instruction
        if self.query_instruction is None:
            self.query_instruction = QWEN_QUERY_INSTRUCTION if "qwen3-embedding" in model.lower() else ""
        identity = json.dumps({
            "base_url": self.base_url, "model": model, "dimension": dimension,
            "query_instruction": self.query_instruction, "format": "text-v1",
        }, sort_keys=True, separators=(",", ":"))
        self.profile = "hosted:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()
        self._client = client

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._request(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        if self.query_instruction:
            text = f"Instruct: {self.query_instruction}\nQuery:{text}"
        return self._request(text)

    def _request(self, text: str) -> list[float]:
        if not self.api_key or self.api_key.startswith("LOCAL_ONLY"):
            raise EmbeddingError("EMBEDDING_PROVIDER=hosted requires a configured MODEL_API_KEY")
        client = self._client or create_model_client(timeout=30.0, tls_verify=self.tls_verify)
        try:
            response = client.post(
                f"{self.base_url}/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "input": text},
            )
            if response.status_code >= 400:
                raise EmbeddingError(f"Embedding gateway returned HTTP {response.status_code}; check gateway access and credentials")
            try:
                payload = response.json()
                data = payload.get("data") if isinstance(payload, dict) else None
                if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], dict):
                    raise ValueError("Invalid embedding response")
                vector = data[0].get("embedding")
            except ValueError as error:
                raise EmbeddingError("Embedding gateway returned an unreadable response") from error
            return validate_vector(vector, self.dimension)
        except httpx.RequestError as error:
            raise EmbeddingError("Cannot reach the embedding gateway; check the URL, company VPN and Docker network access") from error
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
            tls_verify=settings.model_tls_verify,
        )
    raise ValueError(f"Unknown EMBEDDING_PROVIDER: {settings.embedding_provider}")


def _features(text: str) -> list[str]:
    tokens = _TOKEN_PATTERN.findall(text.lower())
    bigrams = [f"{first} {second}" for first, second in zip(tokens, tokens[1:])]
    return tokens + bigrams
