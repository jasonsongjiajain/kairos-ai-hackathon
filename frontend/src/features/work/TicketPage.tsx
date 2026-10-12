import { useCallback, useEffect, useRef, useState } from 'react'
import { Button } from '../../components/ui/button'
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
import { IncidentTrace, type IncidentStage } from './IncidentTrace'
import type { ToolExecution } from '../../lib/api/tools'

type PageState = 'loading' | 'ready' | 'error' | 'denied'
type TopologyState = 'loading' | 'ready' | 'error'

export function TicketPage() {
  const { ticketId } = useParams()
  const { session } = useAuth()
  return <TicketWorkspace key={`${ticketId}:${session?.accessToken}`} />
}

function TicketWorkspace() {
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
  const [selectedDeviceId, setSelectedDeviceId] = useState<string>()
  const [evidenceStage, setEvidenceStage] = useState<IncidentStage>({ id: 'evidence', label: 'Evidence', state: 'upcoming', detail: 'Evidence not yet confirmed' })
  const [actionStage, setActionStage] = useState<IncidentStage>({ id: 'action', label: 'Action', state: 'upcoming', detail: 'No confirmed outcome' })
  const [actionOutcome, setActionOutcome] = useState<string>()
  const actionOwner = useRef(0)
  const evidenceRequests = useRef(new Map<number, { message?: string }>())
  const evidenceRequestSequence = useRef(0)
  const reportEvidenceProgress = useCallback((stage: IncidentStage, request: number, settled = false) => {
    const activeRequests = [...evidenceRequests.current.keys()]
    if (request !== Math.max(...activeRequests, 0)) return
    if (!settled) {
      evidenceRequests.current.set(request, { message: stage.detail })
      setEvidenceStage(stage)
      return
    }
    evidenceRequests.current.delete(request)
    const remaining = [...evidenceRequests.current.entries()].sort(([left], [right]) => right - left)[0]
    if (remaining) {
      setEvidenceStage({ id: 'evidence', label: 'Evidence', state: 'current', detail: remaining[1].message ?? 'Investigation still in progress' })
    } else {
      setEvidenceStage(stage)
    }
  }, [])
  const startEvidenceRequest = useCallback(() => {
    const request = ++evidenceRequestSequence.current
    evidenceRequests.current.set(request, {})
    return (stage: IncidentStage) => reportEvidenceProgress(stage, request, stage.state !== 'current')
  }, [reportEvidenceProgress])
  const startAction = useCallback(() => {
    const operation = ++actionOwner.current
    return (stage: IncidentStage, outcome?: ToolExecution) => {
      if (operation !== actionOwner.current) return
      setActionStage(stage)
      setActionOutcome(outcome?.status === 'succeeded' ? outcome.message : undefined)
    }
  }, [])

  useEffect(() => {
    setSelectedDeviceId(undefined)
  }, [ticketId])

  const load = useCallback(
    async (signal?: AbortSignal) => {
      if (!ticketId) {
        setPageState('error')
        setPageError('No ticket was specified.')
        return
      }
      setPageState('loading')
      setPageError('')
      setTopology(null)
      setTopologyState('loading')

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
    <main className="app-shell ticket-workspace">
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
          <Button className="process-button" type="button" onClick={() => void load()}>
            Retry loading ticket
          </Button>
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
          <IncidentTrace key={detail.ticket.id} confirmedActionOutcome={actionOutcome} stages={[
            { id: 'event', label: 'Event', state: 'complete', detail: `Source event: ${detail.ticket.source_event_id}` },
            { id: 'ticket', label: 'Ticket', state: 'current', detail: 'Ticket context loaded' },
            {
              id: 'topology', label: 'Topology',
              state: topologyState === 'error' ? 'blocked'
                : topologyState === 'ready' && topology?.ticket_id === detail.ticket.id && topology.nodes.length > 0
                  ? 'complete' : 'upcoming',
              detail: topologyState === 'error' ? 'Service path unavailable. Retry below.'
                : topologyState === 'loading' ? 'Loading service path'
                  : topology?.nodes.length ? 'Service path loaded' : 'No service path available',
            },
            evidenceStage,
            actionStage,
          ]} />
          <section className="panel topology-panel" aria-labelledby="topology-heading">
            <div className="topology-panel-heading">
              <div>
                <p className="section-label">SERVICE PATH</p>
                <h3 id="topology-heading">Customer network topology</h3>
              </div>
              {topologyState === 'ready' && topology && topology.nodes.length > 0 && (
                <p className="topology-count">{topology.nodes.length} {topology.nodes.length === 1 ? 'device' : 'devices'} · {topology.edges.length} {topology.edges.length === 1 ? 'connection' : 'connections'}</p>
              )}
            </div>

            {topologyState === 'loading' && (
              <p className="muted-note" role="status">Loading the service path.</p>
            )}
            {topologyState === 'error' && (
              <div>
                <p className="form-error" role="alert">{topologyError}</p>
                <Button className="process-button" type="button" onClick={() => void load()}>
                  Retry service path
                </Button>
              </div>
            )}
            {topologyState === 'ready' && topology && (
              <TopologyPath
                key={topology.ticket_id}
                nodes={topology.nodes}
                edges={topology.edges}
                serviceRef={topology.service_ref}
                selectedDeviceId={selectedDeviceId}
                onSelectDevice={setSelectedDeviceId}
                onClearSelection={() => setSelectedDeviceId(undefined)}
              />
            )}
          </section>
          <p className="ticket-audit-link">
            <Link className="inline-link" to={`/tickets/${detail.ticket.id}/audit`}>
              View audit history
            </Link>
          </p>
          <div className="ticket-workbench">
          <TroubleshootingAssistant key={detail.ticket.id} ticketId={detail.ticket.id} token={token} devices={detail.devices}
            onSelectDevice={setSelectedDeviceId} onEvidenceStart={startEvidenceRequest} onActionStart={startAction} />
          <div className="ticket-context">
          <CustomerServiceSummary
            customer={detail.customer}
            services={detail.services}
            devices={detail.devices}
          />

          <SensitiveCredentialReveal ticketId={detail.ticket.id} token={token} devices={detail.devices} />

          <AgentActionsPanel ticketId={detail.ticket.id} token={token} devices={detail.devices}
            onSelectDevice={setSelectedDeviceId} onActionStart={startAction} />

          </div>
          </div>
        </div>
      )}
    </main>
  )
}
