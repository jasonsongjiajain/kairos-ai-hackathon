import { useCallback, useMemo, useState } from 'react'
import { Button } from '../../components/ui/button'
import { Card } from '../../components/ui/card'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Select, SelectItem } from '../../components/ui/select'
import type { Device } from '../../lib/api/tickets'
import { TicketsApiError } from '../../lib/api/tickets'
import {
  confirmTool,
  fetchToolCatalog,
  proposeTool,
  type ToolCatalogItem,
  type ToolExecution,
  type ToolProposal,
} from '../../lib/api/tools'
import { ActionApprovalDialog } from './ActionApprovalDialog'
import { ActionProposal } from './ActionProposal'
import { ToolExecutionResult } from './ToolExecutionResult'

type State = 'idle' | 'preparing' | 'proposed' | 'executing' | 'done'

type AgentActionsPanelProps = {
  ticketId: string
  token: string
  devices: Device[]
}

const CONFIG_FIELDS: { key: string; label: string; min: number; max: number }[] = [
  { key: 'wifi_channel', label: 'Wi-Fi channel (1-13)', min: 1, max: 13 },
  { key: 'tx_power_dbm', label: 'Transmit power dBm (0-30)', min: 0, max: 30 },
]

export function AgentActionsPanel({ ticketId, token, devices }: AgentActionsPanelProps) {
  const [catalog, setCatalog] = useState<ToolCatalogItem[] | null>(null)
  const [catalogState, setCatalogState] = useState<'idle' | 'loading' | 'ready' | 'error'>('idle')
  const [catalogError, setCatalogError] = useState('')

  const [toolName, setToolName] = useState('')
  const [deviceId, setDeviceId] = useState('')
  const [configValues, setConfigValues] = useState<Record<string, string>>({ wifi_channel: '6', tx_power_dbm: '18' })
  const [state, setState] = useState<State>('idle')
  const [proposal, setProposal] = useState<ToolProposal | null>(null)
  const [execution, setExecution] = useState<ToolExecution | null>(null)
  const [error, setError] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)

  const loadCatalog = useCallback(async () => {
    setCatalogState('loading')
    setCatalogError('')
    try {
      const items = await fetchToolCatalog(ticketId, token)
      setCatalog(items)
      setCatalogState('ready')
      const first = items[0]
      if (first) {
        setToolName((current) => current || first.name)
        setDeviceId((current) => current || devices[0]?.id || '')
      }
    } catch (caught) {
      setCatalogState('error')
      setCatalogError(caught instanceof TicketsApiError ? caught.message : 'The action catalog could not be loaded.')
    }
  }, [ticketId, token, devices])

  const selected = useMemo(() => catalog?.find((item) => item.name === toolName) ?? null, [catalog, toolName])

  const prepare = async () => {
    if (!selected || !deviceId) return
    setState('preparing')
    setError('')
    setExecution(null)
    try {
      const parameters =
        selected.name === 'update_config'
          ? Object.fromEntries(CONFIG_FIELDS.map((field) => [field.key, Number(configValues[field.key])]))
          : {}
      const created = await proposeTool(ticketId, { toolName: selected.name, deviceId, parameters }, token)
      setProposal(created)
      setState('proposed')
    } catch (caught) {
      setState('idle')
      setError(caught instanceof TicketsApiError ? caught.message : 'The action could not be prepared.')
    }
  }

  const confirm = async () => {
    if (!proposal) return
    setState('executing')
    setError('')
    try {
      const result = await confirmTool(ticketId, proposal.id, proposal.confirmation_id, token)
      setExecution(result)
      setProposal(null)
      setDialogOpen(false)
      setState('done')
    } catch (caught) {
      setState('proposed')
      setDialogOpen(false)
      setError(caught instanceof TicketsApiError ? caught.message : 'The action could not be executed.')
    }
  }

  const reset = () => {
    setState('idle')
    setProposal(null)
    setExecution(null)
    setError('')
  }

  return (
    <Card className="panel" aria-labelledby="actions-heading">
      <p className="section-label">AGENT ACTIONS</p>
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
        <div className="action-form">
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
        </div>
      )}

      {proposal && state !== 'done' && (
        <ActionProposal
          proposal={proposal}
          onReview={() => setDialogOpen(true)}
          busy={state === 'executing'}
        />
      )}

      {dialogOpen && proposal && (
        <ActionApprovalDialog
          title="Approve device action"
          description={`${proposal.summary} This runs a simulated change on the demo device.`}
          confirmLabel="Approve and run"
          busy={state === 'executing'}
          onConfirm={() => void confirm()}
          onCancel={() => setDialogOpen(false)}
        />
      )}

      {state === 'done' && execution && <ToolExecutionResult execution={execution} onRunAnother={reset} />}
    </Card>
  )
}
