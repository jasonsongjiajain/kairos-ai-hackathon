import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthProvider'
import { TicketsApiError, fetchMyTickets, type AssignedTicket } from '../../lib/api/tickets'
import { severityLabel, statusLabel } from './TicketHeader'

type LoadState = 'loading' | 'ready' | 'error'

function modifier(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-')
}

export function AssignedWorkList() {
  const { session } = useAuth()
  const token = session?.accessToken ?? ''
  const [tickets, setTickets] = useState<AssignedTicket[]>([])
  const [loadState, setLoadState] = useState<LoadState>('loading')
  const [loadError, setLoadError] = useState('')

  const load = useCallback(
    async (signal?: AbortSignal) => {
      setLoadState('loading')
      setLoadError('')
      try {
        const assigned = await fetchMyTickets(token, signal)
        setTickets(assigned)
        setLoadState('ready')
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setLoadState('error')
        setLoadError(
          error instanceof TicketsApiError ? error.message : 'Assigned work could not be loaded.',
        )
      }
    },
    [token],
  )

  useEffect(() => {
    const controller = new AbortController()
    void load(controller.signal)
    return () => controller.abort()
  }, [load])

  return (
    <section className="work-section" aria-labelledby="assigned-work-heading">
      <p className="section-label">MY WORK</p>
      <h2 id="assigned-work-heading">Assigned tickets</h2>

      {loadState === 'loading' && (
        <p className="state-panel" role="status">
          Loading your assigned tickets.
        </p>
      )}

      {loadState === 'error' && (
        <div className="state-panel">
          <p className="form-error" role="alert">
            {loadError}
          </p>
          <button className="process-button" type="button" onClick={() => void load()}>
            Retry loading assigned work
          </button>
        </div>
      )}

      {loadState === 'ready' && tickets.length === 0 && (
        <div className="state-panel">
          <h3>No assigned tickets</h3>
          <p>
            You have no open work right now. New tickets appear here when an operator processes an
            incident and assigns it to you.
          </p>
        </div>
      )}

      {loadState === 'ready' && tickets.length > 0 && (
        <>
          <p className="work-intro">
            {tickets.length === 1
              ? '1 ticket is assigned to you.'
              : `${tickets.length} tickets are assigned to you.`}
          </p>
          <ul className="ticket-list">
            {tickets.map((ticket) => (
              <li key={ticket.id}>
                <Link
                  className="ticket-card"
                  to={`/tickets/${ticket.id}`}
                  aria-label={`Open ticket: ${ticket.summary}`}
                >
                  <span className="ticket-card-top">
                    <span className={`status-pill status-${modifier(ticket.status)}`}>
                      {statusLabel(ticket.status)}
                    </span>
                    <span className={`severity-pill severity-${modifier(ticket.severity)}`}>
                      {severityLabel(ticket.severity)}
                    </span>
                  </span>
                  <span className="ticket-card-summary">{ticket.summary}</span>
                  <span className="ticket-card-meta">
                    {ticket.customer_name}
                    {ticket.service_type ? `, ${ticket.service_type}` : ''}
                  </span>
                  <span className="ticket-card-ref tabular">{ticket.customer_ref}</span>
                </Link>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  )
}
