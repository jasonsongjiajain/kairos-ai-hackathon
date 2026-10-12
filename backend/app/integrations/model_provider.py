"""Chat completion providers selected by ``MODEL_PROVIDER``.

The local provider is deterministic and key-free so the answer path can run in
tests and offline. A hosted OpenAI-compatible provider can replace it.
"""

import json
from collections.abc import Iterator, Sequence

import httpx

from app.ai.ports import ChatCompletionProvider, ChatMessage
from app.config import Settings
from app.integrations.model_http import create_model_client


class LocalDeterministicChatProvider:
    """Key-free provider used for local runs and tests.

    When the caller supplies retrieved evidence, it returns a valid structured
    assistant answer grounded only in those chunks, so the grounded path and its
    citation validation run without an external model. Without evidence it falls
    back to a deterministic echo rather than pretending to reason.
    """

    def complete(self, messages: Sequence[ChatMessage], *, temperature: float = 0.0) -> str:
        if messages and "Choose a tool from this allowlist" in messages[0].content:
            return _local_tool_call(messages)
        evidence = _extract_retrieved_chunks(messages)
        if evidence is not None:
            return _synthesize_grounded_answer(evidence)
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
        tls_verify: bool = True,
        timeout_seconds: float = 60.0,
        max_output_tokens: int | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.tls_verify = tls_verify
        self._client = client
        self.timeout_seconds = timeout_seconds
        self.max_output_tokens = max_output_tokens

    def complete(self, messages: Sequence[ChatMessage], *, temperature: float = 0.0) -> str:
        if not self.api_key or self.api_key.startswith("LOCAL_ONLY"):
            raise RuntimeError("MODEL_PROVIDER=hosted requires a configured MODEL_API_KEY")
        client = self._client or create_model_client(timeout=self.timeout_seconds, tls_verify=self.tls_verify)
        try:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "temperature": temperature,
                    "messages": [{"role": message.role, "content": message.content} for message in messages],
                    **({"max_tokens": self.max_output_tokens} if self.max_output_tokens else {}),
                },
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("The model gateway returned no text response")
            return content
        finally:
            if self._client is None:
                client.close()


def build_chat_provider(settings: Settings, *, timeout_seconds: float = 60.0, max_output_tokens: int | None = None) -> ChatCompletionProvider:
    provider = settings.model_provider.strip().lower()
    if provider in ("", "local", "deterministic"):
        return LocalDeterministicChatProvider()
    if provider == "hosted":
        return HostedChatCompletionProvider(
            base_url=settings.model_base_url,
            api_key=settings.model_api_key,
            model=settings.model_name,
            tls_verify=settings.model_tls_verify,
            timeout_seconds=timeout_seconds,
            max_output_tokens=max_output_tokens,
        )
    raise ValueError(f"Unknown MODEL_PROVIDER: {settings.model_provider}")


def _extract_retrieved_chunks(messages: Sequence[ChatMessage]) -> list[dict] | None:
    for message in reversed(messages):
        if message.role != "user":
            continue
        outermost = _outermost_object(message.content)
        if outermost is not None:
            chunks = _chunks_from(outermost)
            if chunks is not None:
                return chunks
        for candidate in _iter_json_objects(message.content):
            chunks = _chunks_from(candidate)
            if chunks is not None:
                return chunks
    return None


def _chunks_from(text: str) -> list[dict] | None:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None
    chunks = parsed.get("chunks") if isinstance(parsed, dict) else None
    if isinstance(chunks, list):
        return [chunk for chunk in chunks if isinstance(chunk, dict)]
    return None


def _outermost_object(text: str) -> str | None:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start : end + 1]


def _synthesize_grounded_answer(chunks: Sequence[dict]) -> str:
    usable = [
        chunk
        for chunk in chunks
        if isinstance(chunk.get("chunk_id"), str)
        and isinstance(chunk.get("content"), str)
        and chunk["content"].strip()
    ]
    if not usable:
        return json.dumps(
            {
                "answer": "No retrieved evidence was usable for this question.",
                "citations": [],
                "uncertainty": "",
                "next_best_action": None,
            },
            separators=(",", ":"),
        )

    primary = usable[0]
    citations = [
        {
            "chunk_id": chunk["chunk_id"],
            "document_title": str(chunk.get("document_title", "")),
            "section": str(chunk.get("section", "")),
        }
        for chunk in usable[:2]
    ]
    first_step = _first_sentence(primary["content"])
    title = str(primary.get("document_title", "the retrieved procedure"))
    answer = (
        f"Retrieved procedural evidence from {title} states: {first_step} "
        "Treat this as a recommendation from the cited procedure and confirm against the observed "
        "ticket data on site."
    )
    dispatch_required = any(
        keyword in primary["content"].lower() for keyword in ("escalate", "dispatch", "site visit")
    )
    next_best_action = {
        "remediation": first_step,
        "dispatch_required": dispatch_required,
        "suggestion": None,
        "evidence": [primary["chunk_id"]],
        "suggestion_evidence": [],
    }
    return json.dumps(
        {
            "answer": answer,
            "citations": citations,
            "uncertainty": "Deterministic local provider; confirm against the cited section.",
            "next_best_action": next_best_action,
        },
        separators=(",", ":"),
    )


def _local_tool_call(messages: Sequence[ChatMessage]) -> str:
    request = next((message.content for message in reversed(messages) if message.role == "user"), "")
    lowered = request.lower()
    if "reboot" in lowered:
        tool_name = "reboot_router"
    elif "config" in lowered or "channel" in lowered:
        tool_name = "update_config"
    else:
        tool_name = "get_device_status"

    device_id = ""
    data = _first_json_object(request)
    if isinstance(data, dict):
        device_id = str(data.get("device_id", ""))
    arguments: dict[str, object] = {"device_id": device_id}
    if tool_name == "update_config":
        arguments["settings"] = {"wifi_channel": 6}
    return json.dumps({"tool_name": tool_name, "arguments": arguments}, separators=(",", ":"))


def _first_json_object(text: str) -> dict | None:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        value = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _first_sentence(text: str) -> str:
    stripped = text.strip()
    for index, character in enumerate(stripped):
        if character in ".!?" and index + 1 < len(stripped):
            return stripped[: index + 1].strip()
    return stripped


def _iter_json_objects(text: str) -> Iterator[str]:
    depth = 0
    start: int | None = None
    for index, character in enumerate(text):
        if character == "{":
            if depth == 0:
                start = index
            depth += 1
        elif character == "}" and depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                yield text[start : index + 1]
                start = None
