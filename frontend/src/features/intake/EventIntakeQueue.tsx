import { useCallback, useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthProvider'
import {
  EventsApiError,
  describeEventType,
  fetchPendingEvents,
  type PendingEvent,
  type ProcessEventResult,
} from '../../lib/api/events'
import { EventReviewPanel } from './EventReviewPanel'

type LoadState = 'loading' | 'ready' | 'error'

export function EventIntakeQueue() {
  const { session } = useAuth()
  const token = session?.accessToken ?? ''
  const [events, setEvents] = useState<PendingEvent[]>([])
  const [loadState, setLoadState] = useState<LoadState>('loading')
  const [loadError, setLoadError] = useState('')
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [result, setResult] = useState<ProcessEventResult | null>(null)

  const load = useCallback(
    async (signal?: AbortSignal) => {
      setLoadState('loading')
      setLoadError('')
      setResult(null)
      try {
        const pending = await fetchPendingEvents(token, signal)
        setEvents(pending)
        setSelectedId((current) =>
          current && pending.some((event) => event.id === current) ? current : pending[0]?.id ?? null,
        )
        setLoadState('ready')
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setLoadState('error')
        setLoadError(error instanceof EventsApiError ? error.message : 'The event queue could not be loaded.')
      }
    },
    [token],
  )

  useEffect(() => {
    const controller = new AbortController()
    void load(controller.signal)
    return () => controller.abort()
  }, [load])

  const selectEvent = (eventId: string) => {
    setSelectedId(eventId)
    setResult(null)
  }

  if (loadState === 'loading') {
    return (
      <section className="intake" aria-labelledby="intake-heading">
        <p className="section-label">INCOMING EVENTS</p>
        <h2 id="intake-heading">Event intake</h2>
        <p className="state-panel" role="status">
          Loading pending events.
        </p>
      </section>
    )
  }

  if (loadState === 'error') {
    return (
      <section className="intake" aria-labelledby="intake-heading">
        <p className="section-label">INCOMING EVENTS</p>
        <h2 id="intake-heading">Event intake</h2>
        <div className="state-panel">
          <p className="form-error" role="alert">
            {loadError}
          </p>
          <button className="process-button" type="button" onClick={() => void load()}>
            Retry loading events
          </button>
        </div>
      </section>
    )
  }

  if (events.length === 0) {
    return (
      <section className="intake" aria-labelledby="intake-heading">
        <p className="section-label">INCOMING EVENTS</p>
        <h2 id="intake-heading">Event intake</h2>
        <div className="state-panel">
          <h3>No pending events</h3>
          <p>
            The seeded intake feed has no unprocessed events. New events appear here when the
            network reports an incident.
          </p>
        </div>
      </section>
    )
  }

  const selected = events.find((event) => event.id === selectedId) ?? events[0]

  return (
    <section className="intake" aria-labelledby="intake-heading">
      <p className="section-label">INCOMING EVENTS</p>
      <h2 id="intake-heading">Event intake</h2>
      <p className="intake-intro">
        {events.length === 1 ? '1 event is waiting to be processed.' : `${events.length} events are waiting to be processed.`}
      </p>

      <ul className="event-list">
        {events.map((event) => {
          const isSelected = event.id === selected.id
          return (
            <li key={event.id}>
              <button
                type="button"
                className={isSelected ? 'event-select is-selected' : 'event-select'}
                aria-pressed={isSelected}
                onClick={() => selectEvent(event.id)}
              >
                <span className="event-type">{describeEventType(event.event_type)}</span>
                <span className="event-ref tabular">{event.source_event_id}</span>
                <span className="event-device">{event.device_name}</span>
              </button>
            </li>
          )
        })}
      </ul>

      <EventReviewPanel
        event={selected}
        token={token}
        result={result}
        onProcessed={setResult}
      />
    </section>
  )
}
