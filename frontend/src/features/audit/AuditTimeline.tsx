import type { AuditEvent } from '../../lib/api/audit'

const EVENT_LABELS: Record<string, string> = {
  event_processed: 'Event processed into a ticket',
  credential_revealed: 'Credential revealed',
  tool_proposed: 'Device action proposed',
  tool_executed: 'Device action executed',
}

function describe(event: AuditEvent): string[] {
  const details = event.details
  const lines: string[] = []
  const deviceRef = details.device_ref
  if (typeof deviceRef === 'string') lines.push(`Device: ${deviceRef}`)
  const toolName = details.tool_name
  if (typeof toolName === 'string') lines.push(`Action: ${toolName}`)
  const outcome = details.outcome
  if (typeof outcome === 'string') lines.push(`Outcome: ${outcome}`)
  const credentialType = details.credential_type
  if (typeof credentialType === 'string') lines.push(`Field: ${credentialType}`)
  const severity = details.severity
  if (typeof severity === 'string') lines.push(`Severity: ${severity}`)
  const message = details.message
  if (typeof message === 'string') lines.push(message)
  return lines
}

export function AuditTimeline({ events }: { events: AuditEvent[] }) {
  if (events.length === 0) {
    return (
      <p className="muted-note">
        No recorded activity for this ticket yet. Event processing, credential reveals, and device
        actions appear here as they happen.
      </p>
    )
  }
  return (
    <ol className="audit-timeline">
      {events.map((event) => (
        <li key={event.id} className="audit-entry">
          <p className="audit-type">{EVENT_LABELS[event.event_type] ?? event.event_type}</p>
          <p className="audit-meta">
            {event.actor_name ?? 'System'} · {new Date(event.created_at).toLocaleString()}
          </p>
          {describe(event).length > 0 && (
            <ul className="audit-details">
              {describe(event).map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ol>
  )
}
