import asyncio

from fastapi import HTTPException

from app.auth.dependencies import AuthenticatedUser
from app.auth.policy import require_role
from app.domain.event_rules import EVENT_PROCESSING_ROLES
from app.services.event_stream import EventStream


def test_event_stream_fans_out_run_events():
    async def scenario():
        stream = EventStream()
        subscriber = stream.subscribe("run-1")
        connected = await anext(subscriber)
        await asyncio.to_thread(
            stream.publish_nowait, "run-1", "ticket_created", {"ticket_id": "ticket-1"}
        )
        message = await asyncio.wait_for(anext(subscriber), timeout=1)
        await subscriber.aclose()
        return connected, message

    connected, message = asyncio.run(scenario())
    assert "event: connected" in connected
    assert "event: ticket_created" in message
    assert '"ticket_id":"ticket-1"' in message


def test_event_stream_replays_events_after_cursor():
    async def scenario():
        stream = EventStream()
        stream.create_run("run-1")
        stream.publish_nowait("run-1", "processing", {"status": "processing"})
        stream.publish_nowait("run-1", "ticket_created", {"status": "completed"})
        subscriber = stream.subscribe("run-1", after=1)
        connected = await anext(subscriber)
        replayed = await anext(subscriber)
        await subscriber.aclose()
        return connected, replayed

    connected, replayed = asyncio.run(scenario())
    assert "event: connected" in connected
    assert "event: ticket_created" in replayed
    assert "event: processing" not in replayed


def test_sse_endpoint_rejects_technicians():
    technician = AuthenticatedUser(id="tech-1", email="tech@test.invalid", role="technician")
    try:
        require_role(technician.role, EVENT_PROCESSING_ROLES)
    except HTTPException as error:
        assert error.status_code == 403
    else:
        raise AssertionError("technicians must not subscribe to event intake progress")
