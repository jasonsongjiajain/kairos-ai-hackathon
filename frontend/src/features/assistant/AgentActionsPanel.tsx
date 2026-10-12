import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Button } from '../../components/ui/button'
import { Card } from '../../components/ui/card'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Select, SelectItem } from '../../components/ui/select'
import type { Device } from '../../lib/api/tickets'
import { TicketsApiError } from '../../lib/api/tickets'
import {
  confirmTool,
  executionFromProposal,
  fetchToolCatalog,
  proposeTool,
  type ToolCatalogItem,
  type ToolExecution,
  type ToolProposal,
} from '../../lib/api/tools'
import { ActionProposal } from './ActionProposal'
import { ToolExecutionResult } from './ToolExecutionResult'
import { ToolActivity } from './ToolActivity'
import { Check, X } from '@phosphor-icons/react'
import {
  Confirmation,
  ConfirmationAccepted,
  ConfirmationAction,
  ConfirmationActions,
  ConfirmationRejected,
  ConfirmationRequest,
  ConfirmationTitle,
} from '@/components/ai/confirmation'
import type { IncidentStage } from '../work/IncidentTrace'

type State = 'idle' | 'preparing' | 'proposed' | 'executing' | 'done'

type AgentActionsPanelProps = {
  ticketId: string
  token: string
  devices: Device[]
  onSelectDevice?: (deviceId: string) => void
  onActionProgress?: (stage: IncidentStage, outcome?: ToolExecution) => void
  onActionStart?: (deviceId?: string) => NonNullable<AgentActionsPanelProps['onActionProgress']>
}

const CONFIG_FIELDS: { key: string; label: string; min: number; max: number }[] = [
  { key: 'wifi_channel', label: 'Wi-Fi channel (1-13)', min: 1, max: 13 },
  { key: 'tx_power_dbm', label: 'Transmit power dBm (0-30)', min: 0, max: 30 },
]

// Tools whose parameters are only the target device (plus update_config's
// explicit fields) can be prepared from this direct picker. Tools that need
// typed arguments (SSID, band, MAC, service) are offered through the agent plan.
const DIRECT_ACTION_NAMES = new Set([
  'get_device_status',
  'list_connected_clients',
  'run_speed_test',
  'run_optical_diagnostics',
  'reboot_router',
  'reboot_ont',
  'refresh_ont_registration',
  'reset_optical_port',
  'flush_dns_cache',
  'update_config',
])

export function AgentActionsPanel(props: AgentActionsPanelProps) {
  return <ActionsSession key={`${props.ticketId}:${props.token}`} {...props} />
}

function ActionsSession({ ticketId, token, devices, onSelectDevice, onActionProgress, onActionStart }: AgentActionsPanelProps) {
  const active = useRef(true)
  const proposalProgress = useRef<AgentActionsPanelProps['onActionProgress']>()
  useEffect(() => { active.current = true; return () => { active.current = false } }, [])
  const [catalog, setCatalog] = useState<ToolCatalogItem[] | null>(null)
  const [catalogState, setCatalogState] = useState<'idle' | 'loading' | 'ready' | 'error'>('idle')
  const [catalogError, setCatalogError] = useState('')

  const [toolName, setToolName] = useState('')
  const [deviceId, setDeviceId] = useState('')
  const [configValues, setConfigValues] = useState<Record<string, string>>({ wifi_channel: '6', tx_power_dbm: '18' })
  const [state, setState] = useState<State>('idle')
  const [proposal, setProposal] = useState<ToolProposal | null>(null)
  const [execution, setExecution] = useState<ToolExecution | null>(null)
  const [attempts, setAttempts] = useState<{ proposal: ToolProposal | null; execution: ToolExecution }[]>([])
  const [error, setError] = useState('')

  const loadCatalog = useCallback(async () => {
    setCatalogState('loading')
    setCatalogError('')
    try {
      const items = (await fetchToolCatalog(ticketId, token)).filter((item) =>
        DIRECT_ACTION_NAMES.has(item.name),
      )
      if (!active.current) return
      setCatalog(items)
      setCatalogState('ready')
      const first = items[0]
      if (first) {
        setToolName((current) => current || first.name)
        setDeviceId((current) => current || devices[0]?.id || '')
      }
    } catch (caught) {
      if (!active.current) return
      setCatalogState('error')
      setCatalogError(caught instanceof TicketsApiError ? caught.message : 'The action catalog could not be loaded.')
    }
  }, [ticketId, token, devices])

  const selected = useMemo(() => catalog?.find((item) => item.name === toolName) ?? null, [catalog, toolName])

  const prepare = async () => {
    if (!selected || !deviceId || state === 'preparing' || state === 'executing') return
    if (selected.name === 'update_config' && CONFIG_FIELDS.some((field) => {
      const value = Number(configValues[field.key])
      return !configValues[field.key]?.trim() || !Number.isInteger(value) || value < field.min || value > field.max
    })) {
      setError('Enter whole numbers within the configuration ranges.')
      return
    }
    setState('preparing')
    const report = onActionStart?.(deviceId) ?? onActionProgress
    proposalProgress.current = report
    if (execution) setAttempts((current) => [...current, { proposal, execution }])
    setProposal(null)
    report?.({ id: 'action', label: 'Action', state: 'current', detail: 'Preparing proposal' })
    setError('')
    setExecution(null)
    try {
      const parameters =
        selected.name === 'update_config'
          ? Object.fromEntries(CONFIG_FIELDS.map((field) => [field.key, Number(configValues[field.key])]))
          : {}
      const created = await proposeTool(ticketId, { toolName: selected.name, deviceId, parameters }, token)
      if (!active.current) return
      setProposal(created)
      const result = executionFromProposal(created)
      setExecution(result)
      setState(result ? 'done' : 'proposed')
      if (result) {
        report?.({ id: 'action', label: 'Action', state: result.status === 'succeeded' ? 'complete' : 'blocked', detail: result.message }, result)
      } else {
        report?.({ id: 'action', label: 'Action', state: 'current', detail: 'Proposal ready for review' })
      }
    } catch (caught) {
      if (!active.current) return
      setState('idle')
      report?.({ id: 'action', label: 'Action', state: 'blocked', detail: 'Proposal request failed' })
      setError(caught instanceof TicketsApiError ? caught.message : 'The action could not be prepared.')
    }
  }

  const confirm = async () => {
    if (!proposal || execution || !proposal.requires_confirmation || proposal.status !== 'proposed' || state === 'executing') return
    setState('executing')
    const report = onActionStart?.(deviceId) ?? onActionProgress
    setExecution(null)
    report?.({ id: 'action', label: 'Action', state: 'current', detail: 'Executing approved action' })
    setError('')
    try {
      const result = await confirmTool(ticketId, proposal.id, proposal.confirmation_id, token)
      if (!active.current) return
      setExecution(result)
      if (result.status === 'succeeded') setProposal(null)
      setState('done')
      report?.({ id: 'action', label: 'Action', state: result.status === 'succeeded' ? 'complete' : 'blocked', detail: result.message }, result)
    } catch (caught) {
      if (!active.current) return
      report?.({ id: 'action', label: 'Action', state: 'blocked', detail: 'Execution request failed' })
      setState('proposed')
      setError(caught instanceof TicketsApiError ? caught.message : 'The action could not be executed.')
    }
  }

  const reset = () => {
    if (execution) setAttempts((current) => [...current, { proposal, execution }])
    setState('idle')
    setProposal(null)
    setExecution(null)
    setError('')
  }

  return (
    <Card className="panel" aria-labelledby="actions-heading">
      <h3 id="actions-heading">Choose a device action</h3>
      <p className="muted-note">
        Select an allowlisted action directly. State-changing actions run only after you review and
        approve them, and every run is recorded in the ticket audit history.
      </p>

      {catalogState === 'idle' && (
        <Button className="process-button" type="button" onClick={() => void loadCatalog()}>
          Load available actions
        </Button>
      )}

      {catalogState === 'loading' && (
        <p className="muted-note" role="status">
          Loading available actions.
        </p>
      )}

      {catalogState === 'error' && (
        <div>
          <p className="form-error" role="alert">
            {catalogError}
          </p>
          <Button className="process-button" type="button" onClick={() => void loadCatalog()}>
            Retry loading actions
          </Button>
        </div>
      )}

      {catalogState === 'ready' && catalog && state !== 'done' && (
        <fieldset className="action-form" disabled={state === 'preparing' || state === 'executing' || Boolean(proposal)}>
          <Label className="field">
            <span>Action</span>
            <Select
              value={toolName}
              onValueChange={(value) => {
                setToolName(value)
                setProposal(null)
                setState('idle')
              }}
              aria-label="Action"
            >
              {catalog.map((item) => (
                <SelectItem key={item.name} value={item.name}>
                  {item.description}
                </SelectItem>
              ))}
            </Select>
          </Label>

          <Label className="field">
            <span>Target device</span>
            <Select value={deviceId} onValueChange={setDeviceId} aria-label="Target device">
              {devices.map((device) => (
                <SelectItem key={device.id} value={device.id}>
                  {device.device_ref} ({device.device_type})
                </SelectItem>
              ))}
            </Select>
          </Label>

          {selected?.name === 'update_config' && (
            <div className="config-grid">
              {CONFIG_FIELDS.map((field) => (
                <Label className="field" key={field.key}>
                  <span>{field.label}</span>
                  <Input
                    type="number"
                    min={field.min}
                    max={field.max}
                    value={configValues[field.key]}
                    onChange={(event) =>
                      setConfigValues((current) => ({ ...current, [field.key]: event.target.value }))
                    }
                  />
                </Label>
              ))}
            </div>
          )}

          <Button className="process-button" type="button" onClick={() => void prepare()} disabled={state === 'preparing'}>
            {state === 'preparing' ? 'Preparing...' : 'Prepare proposal'}
          </Button>

          {error && (
            <p className="form-error" role="alert">
              {error}
            </p>
          )}
        </fieldset>
      )}

      {(state !== 'idle' || error) && <ToolActivity
        state={error || (execution && execution.status !== 'succeeded') ? 'failed' : state === 'done' ? 'completed' : state === 'proposed' ? 'needs-approval' : 'pending'}
        label={state === 'preparing' ? 'Preparing proposal' : state === 'executing' ? 'Executing action' : 'Device action'}
        description={error || (state === 'preparing' ? selected?.description ?? 'Requesting proposal' : proposal?.tool_name ?? execution?.tool_name ?? 'Waiting for response')} />}

      {proposal && !execution && proposal.requires_confirmation && (
        <>
          <ActionProposal proposal={proposal} onSelectDevice={onSelectDevice} />
          <Confirmation approval={{ id: proposal.id }} state="approval-requested" className="action-confirmation">
            <ConfirmationTitle>
              <ConfirmationRequest>
                <span className="confirmation-request-text">
                  Approve this simulated change before it runs on the target device.
                </span>
              </ConfirmationRequest>
              <ConfirmationAccepted>
                <Check size={16} className="action-approved-icon" aria-hidden="true" />
                <span>You approved this simulated action</span>
              </ConfirmationAccepted>
              <ConfirmationRejected>
                <X size={16} className="action-rejected-icon" aria-hidden="true" />
                <span>You rejected this simulated action</span>
              </ConfirmationRejected>
            </ConfirmationTitle>
            <ConfirmationActions>
              <ConfirmationAction variant="outline" disabled={state === 'executing'}
                onClick={() => {
                  proposalProgress.current?.({ id: 'action', label: 'Action', state: 'upcoming', detail: 'Proposal rejected locally; no execution requested' })
                  reset()
                }}>
                Reject
              </ConfirmationAction>
              <ConfirmationAction disabled={state === 'executing'} onClick={() => void confirm()}>
                {state === 'executing' ? 'Executing…' : 'Approve and run'}
              </ConfirmationAction>
            </ConfirmationActions>
          </Confirmation>
        </>
      )}

      {proposal && !execution && <Button type="button" variant="quiet" disabled={state === 'executing'}
        onClick={() => {
          proposalProgress.current?.({ id: 'action', label: 'Action', state: 'upcoming', detail: 'Proposal discarded locally; no execution requested' })
          reset()
        }}>
        Discard proposal
      </Button>}

      {execution?.status === 'failed' && proposal && proposal.requires_confirmation && <ActionProposal proposal={proposal} recorded onSelectDevice={onSelectDevice} />}
      {execution && <ToolExecutionResult key={execution.id} execution={execution}
        onRunAnother={execution.status === 'failed' ? () => void prepare() : reset}
        runAnotherLabel={execution.status === 'failed' ? 'Retry with new proposal' : undefined} onSelectDevice={onSelectDevice} />}
      {attempts.map((attempt) => <section key={attempt.execution.id} aria-label="Previous action attempt">
        {attempt.proposal?.requires_confirmation && <ActionProposal proposal={attempt.proposal} recorded onSelectDevice={onSelectDevice} />}
        <ToolExecutionResult execution={attempt.execution} onSelectDevice={onSelectDevice} />
      </section>)}
    </Card>
  )
}
