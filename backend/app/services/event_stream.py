"""Process-local event notifications for the MVP SSE stream."""

import asyncio
import json
from collections.abc import AsyncIterator
from dataclasses import dataclass, field


@dataclass
class RunState:
    status: str = "queued"
    events: list[dict[str, object]] = field(default_factory=list)
    subscribers: set["Subscriber"] = field(default_factory=set)


@dataclass(frozen=True, eq=False)
class Subscriber:
    loop: asyncio.AbstractEventLoop
    queue: asyncio.Queue[str]


class EventStream:
    """Fan out run progress within one API process; reconnecting clients poll run state."""

    def __init__(self) -> None:
        self._runs: dict[str, RunState] = {}

    def create_run(self, run_id: str) -> RunState:
        state = RunState()
        self._runs[run_id] = state
        return state

    def get_run(self, run_id: str) -> RunState | None:
        return self._runs.get(run_id)

    def create_run_if_missing(self, run_id: str) -> RunState:
        return self._runs.setdefault(run_id, RunState())

    async def publish(self, run_id: str, event: str, payload: dict[str, object]) -> None:
        state = self._runs.setdefault(run_id, RunState())
        event_data = {"event": event, **payload}
        state.events.append(event_data)
        if len(state.events) > 64:
            del state.events[:-64]
        state.status = str(payload.get("status", state.status))
        message = _format_event(len(state.events), event_data)
        for subscriber in tuple(state.subscribers):
            subscriber.loop.call_soon_threadsafe(_enqueue, subscriber.queue, message)

    def publish_nowait(self, run_id: str, event: str, payload: dict[str, object]) -> None:
        state = self._runs.setdefault(run_id, RunState())
        event_data = {"event": event, **payload}
        state.events.append(event_data)
        if len(state.events) > 64:
            del state.events[:-64]
        state.status = str(payload.get("status", state.status))
        message = _format_event(len(state.events), event_data)
        for subscriber in tuple(state.subscribers):
            subscriber.loop.call_soon_threadsafe(_enqueue, subscriber.queue, message)

    async def subscribe(self, run_id: str, *, after: int = 0) -> AsyncIterator[str]:
        queue: asyncio.Queue[str] = asyncio.Queue(maxsize=32)
        subscriber = Subscriber(asyncio.get_running_loop(), queue)
        state = self._runs.setdefault(run_id, RunState())
        state.subscribers.add(subscriber)
        try:
            yield f"event: connected\ndata: {{\"run_id\":\"{run_id}\"}}\n\n"
            for index, item in enumerate(state.events, start=1):
                if index > after:
                    yield _format_event(index, item)
            while True:
                try:
                    yield await asyncio.wait_for(queue.get(), timeout=15)
                except TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            state.subscribers.discard(subscriber)


def _format_event(event_id: int, payload: dict[str, object]) -> str:
    event = str(payload.get("event", "message"))
    data = {key: value for key, value in payload.items() if key != "event"}
    return f"id: {event_id}\nevent: {event}\ndata: {json.dumps(data, separators=(',', ':'))}\n\n"


def _enqueue(queue: asyncio.Queue[str], message: str) -> None:
    if queue.full():
        try:
            queue.get_nowait()
        except asyncio.QueueEmpty:
            pass
    queue.put_nowait(message)


event_stream = EventStream()
