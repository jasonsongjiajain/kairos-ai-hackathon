import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useAuth } from '../auth/AuthProvider'
import { TicketsApiError, fetchTicket, type TicketDetail } from '../../lib/api/tickets'
import { fetchTicketTopology, type TopologyPath as TopologyPathData } from '../../lib/api/topology'
import { TopologyPath } from '../topology/TopologyPath'
import { TroubleshootingAssistant } from '../assistant/TroubleshootingAssistant'
import { CustomerServiceSummary } from './CustomerServiceSummary'
import { SensitiveCredentialReveal } from './SensitiveCredentialReveal'
import { TicketHeader } from './TicketHeader'
import { AgentActionsPanel } from '../assistant/AgentActionsPanel'

type PageState = 'loading' | 'ready' | 'error' | 'denied'
type TopologyState = 'loading' | 'ready' | 'error'

export function TicketPage() {
  const { ticketId } = useParams()
  const { session } = useAuth()
  const token = session?.accessToken ?? ''
  const backTo = session?.role === 'technician' ? '/work' : '/operations'

  const [detail, setDetail] = useState<TicketDetail | null>(null)
  const [pageState, setPageState] = useState<PageState>('loading')
  const [pageError, setPageError] = useState('')
  const [topology, setTopology] = useState<TopologyPathData | null>(null)
  const [topologyState, setTopologyState] = useState<TopologyState>('loading')
  const [topologyError, setTopologyError] = useState('')

  const load = useCallback(
    async (signal?: AbortSignal) => {
      if (!ticketId) {
        setPageState('error')
        setPageError('No ticket was specified.')
        return
      }
      setPageState('loading')
      setPageError('')

      try {
        const loaded = await fetchTicket(ticketId, token, signal)
        setDetail(loaded)
        setPageState('ready')
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') return
        if (error instanceof TicketsApiError && (error.status === 403 || error.status === 404)) {
          setPageState('denied')
          return
        }
        setPageState('error')
        setPageError(error instanceof TicketsApiError ? error.message : 'The ticket could not be loaded.')
        return
      }

      setTopologyState('loading')
      setTopologyError('')
      try {
        const path = await fetchTicketTopology(ticketId, token, signal)
        setTopology(path)
        setTopologyState('ready')
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setTopologyState('error')
        setTopologyError(
          error instanceof TicketsApiError ? error.message : 'The service path could not be loaded.',
        )
      }
    },
    [ticketId, token],
  )

  useEffect(() => {
    const controller = new AbortController()
    void load(controller.signal)
    return () => controller.abort()
  }, [load])

  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-context">FIELD OPERATIONS</p>
        <h1>Field Force Incident Assistant</h1>
        <Link className="inline-link" to={backTo}>
          {session?.role === 'technician' ? 'Back to my work' : 'Back to event intake'}
        </Link>
      </header>

      {pageState === 'loading' && (
        <p className="state-panel" role="status">
          Loading ticket details.
        </p>
      )}

      {pageState === 'error' && (
        <div className="state-panel">
          <p className="form-error" role="alert">
            {pageError}
          </p>
          <button className="process-button" type="button" onClick={() => void load()}>
            Retry loading ticket
          </button>
        </div>
      )}

      {pageState === 'denied' && (
        <section className="state-panel" aria-labelledby="denied-heading">
          <h3 id="denied-heading">Ticket not available</h3>
          <p>
            This ticket is not part of your assigned work. Return to your list to open a ticket assigned
            to you.
          </p>
          <Link className="inline-link" to={backTo}>
            {session?.role === 'technician' ? 'Back to my work' : 'Back to event intake'}
          </Link>
        </section>
      )}

      {pageState === 'ready' && detail && (
        <div className="ticket-page">
          <TicketHeader detail={detail} />
          <p className="ticket-audit-link">
            <Link className="inline-link" to={`/tickets/${detail.ticket.id}/audit`}>
              View audit history
            </Link>
          </p>
          <CustomerServiceSummary
            customer={detail.customer}
            services={detail.services}
            devices={detail.devices}
          />

          <section className="panel" aria-labelledby="topology-heading">
            <p className="section-label">SERVICE PATH</p>
            <h3 id="topology-heading">Customer topology</h3>

            {topologyState === 'loading' && (
              <p className="muted-note" role="status">
                Loading the service path.
              </p>
            )}
            {topologyState === 'error' && (
              <div>
                <p className="form-error" role="alert">
                  {topologyError}
                </p>
                <button className="process-button" type="button" onClick={() => void load()}>
                  Retry service path
                </button>
              </div>
            )}
            {topologyState === 'ready' && topology && (
              <TopologyPath
                nodes={topology.nodes}
                edges={topology.edges}
                serviceRef={topology.service_ref}
              />
            )}
          </section>

          <SensitiveCredentialReveal ticketId={detail.ticket.id} token={token} devices={detail.devices} />

          <AgentActionsPanel ticketId={detail.ticket.id} token={token} devices={detail.devices} />

          <TroubleshootingAssistant ticketId={detail.ticket.id} token={token} />
        </div>
      )}
    </main>
  )
}
