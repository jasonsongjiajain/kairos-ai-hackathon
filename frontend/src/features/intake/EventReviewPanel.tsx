import { Link } from 'react-router-dom'
import { describeEventType, type PendingEvent, type ProcessEventResult } from '../../lib/api/events'
import { ProcessEventButton } from './ProcessEventButton'

type EventReviewPanelProps = {
  event: PendingEvent
  submitting: boolean
  error: string
  result: ProcessEventResult | null
  onProcess: () => void
}

function formatReceivedAt(value: string): string {
  const parsed = Date.parse(value)
  if (!Number.isFinite(parsed)) return value
  return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short' }).format(parsed)
}

function formatValue(value: unknown): string {
  if (value === null) return 'none'
  if (typeof value === 'string') return value
  if (typeof value === 'number' || typeof value === 'boolean') return String(value)
  return JSON.stringify(value)
}

export function EventReviewPanel({ event, submitting, error, result, onProcess }: EventReviewPanelProps) {
  const payloadEntries = Object.entries(event.payload)

  return (
    <section className="review-panel" aria-labelledby="review-heading">
      <p className="section-label">SELECTED EVENT</p>
      <h3 id="review-heading">{describeEventType(event.event_type)}</h3>
      <p className="event-provenance">Seeded demo event</p>

      <dl className="data-list">
        <div className="data-row">
          <dt>Source event</dt>
          <dd className="tabular">{event.source_event_id}</dd>
        </div>
        <div className="data-row">
          <dt>Received</dt>
          <dd className="tabular">{formatReceivedAt(event.received_at)}</dd>
        </div>
        <div className="data-row">
          <dt>Device</dt>
          <dd>
            {event.device_name} ({event.device_ref})
          </dd>
        </div>
        <div className="data-row">
          <dt>Device state</dt>
          <dd>{event.device_status}</dd>
        </div>
        {event.service_ref && (
          <div className="data-row">
            <dt>Service</dt>
            <dd>{event.service_ref}</dd>
          </div>
        )}
      </dl>

      {payloadEntries.length > 0 && (
        <div className="payload-block">
          <h4>Event payload</h4>
          <dl className="data-list">
            {payloadEntries.map(([key, value]) => (
              <div className="data-row" key={key}>
                <dt>{key.replace(/_/g, ' ')}</dt>
                <dd>{formatValue(value)}</dd>
              </div>
            ))}
          </dl>
        </div>
      )}

      {result ? (
        <div className="ticket-confirmation" role="status">
          <h4>{result.duplicate ? 'Ticket already exists' : 'Ticket created'}</h4>
          <p>
            {result.duplicate
              ? 'This event was processed earlier. No duplicate ticket was created.'
              : 'The event was processed and a ticket was assigned.'}
          </p>
          <dl className="data-list">
            <div className="data-row">
              <dt>Ticket</dt>
              <dd className="tabular">{result.ticket.id}</dd>
            </div>
            <div className="data-row">
              <dt>Assigned technician</dt>
              <dd>{result.assigned_technician_name || 'Unnamed technician'}</dd>
            </div>
            <div className="data-row">
              <dt>Severity</dt>
              <dd>{result.ticket.severity}</dd>
            </div>
            <div className="data-row">
              <dt>Status</dt>
              <dd>{result.ticket.status}</dd>
            </div>
          </dl>
          <Link className="inline-link" to={`/tickets/${result.ticket.id}`}>
            Open ticket
          </Link>
        </div>
      ) : (
        <ProcessEventButton submitting={submitting} error={error} onProcess={onProcess} />
      )}
    </section>
  )
}
