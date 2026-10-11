import type { TicketDetail } from '../../lib/api/tickets'

export function statusLabel(status: string): string {
  switch (status.toLowerCase()) {
    case 'open':
      return 'Open'
    case 'in_progress':
    case 'in progress':
      return 'In progress'
    case 'resolved':
      return 'Resolved'
    case 'closed':
      return 'Closed'
    case 'active':
      return 'Active'
    case 'suspended':
      return 'Suspended'
    default:
      return status.replace(/_/g, ' ')
  }
}

export function severityLabel(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'high':
      return 'High severity'
    case 'medium':
      return 'Medium severity'
    case 'low':
      return 'Low severity'
    default:
      return severity
  }
}

function modifier(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-')
}

type TicketHeaderProps = {
  detail: TicketDetail
}

export function TicketHeader({ detail }: TicketHeaderProps) {
  const { ticket, customer, assigned_technician_name } = detail

  return (
    <section className="panel ticket-header" aria-labelledby="ticket-heading">
      <p className="section-label">ASSIGNED WORK</p>
      <h2 id="ticket-heading">{ticket.summary}</h2>
      <p className="ticket-status-line">
        <span className={`status-pill status-${modifier(ticket.status)}`}>{statusLabel(ticket.status)}</span>
        <span className={`severity-pill severity-${modifier(ticket.severity)}`}>
          {severityLabel(ticket.severity)}
        </span>
      </p>
      <dl className="data-list">
        <div className="data-row">
          <dt>Customer</dt>
          <dd>
            {customer.name} <span className="tabular">({customer.customer_ref})</span>
          </dd>
        </div>
        <div className="data-row">
          <dt>Assigned technician</dt>
          <dd>{assigned_technician_name || 'Unassigned'}</dd>
        </div>
        <div className="data-row">
          <dt>Source event</dt>
          <dd className="tabular">{ticket.source_event_id}</dd>
        </div>
      </dl>
    </section>
  )
}
