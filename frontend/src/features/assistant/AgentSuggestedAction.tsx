import { useState } from 'react'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader } from '../../components/ui/card'
import { Label } from '../../components/ui/label'
import { Select, SelectItem } from '../../components/ui/select'
import type { Device } from '../../lib/api/tickets'
import { TicketsApiError } from '../../lib/api/tickets'
import { confirmTool, proposeAgentTool, type ToolExecution, type ToolProposal } from '../../lib/api/tools'
import { ActionApprovalDialog } from './ActionApprovalDialog'
import { ActionProposal } from './ActionProposal'

type AgentSuggestedActionProps = {
  ticketId: string
  token: string
  question: string
  devices: Device[]
}

export function AgentSuggestedAction({ ticketId, token, question, devices }: AgentSuggestedActionProps) {
  const [deviceId, setDeviceId] = useState(devices[0]?.id ?? '')
  const [proposal, setProposal] = useState<ToolProposal | null>(null)
  const [execution, setExecution] = useState<ToolExecution | null>(null)
  const [busy, setBusy] = useState(false)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [error, setError] = useState('')

  const prepare = async () => {
    if (!deviceId || busy) return
    setBusy(true)
    setError('')
    setProposal(null)
    setExecution(null)
    try {
      const result = await proposeAgentTool(ticketId, { question, deviceId }, token)
      setProposal(result)
      setBusy(false)
    } catch (caught) {
      setError(caught instanceof TicketsApiError ? caught.message : 'The agent could not prepare an action.')
      setBusy(false)
    }
  }

  const confirm = async () => {
    if (!proposal) return
    setBusy(true)
    setError('')
    try {
      const result = await confirmTool(ticketId, proposal.id, proposal.confirmation_id, token)
      setExecution(result)
      setProposal(null)
      setDialogOpen(false)
    } catch (caught) {
      setError(caught instanceof TicketsApiError ? caught.message : 'The action could not be executed.')
      setDialogOpen(false)
    } finally {
      setBusy(false)
    }
  }

  return (
    <Card className="agent-suggested-action" aria-label="Agent action suggestion">
      <CardHeader>
        <h4>Investigate with an action</h4>
      </CardHeader>
      <CardContent>
        {!proposal && !execution && (
          <>
            {devices.length > 0 ? (
              <Label className="field">
                <span>Device for the agent to inspect</span>
                <Select
                  value={deviceId}
                  onValueChange={setDeviceId}
                  disabled={busy}
                  aria-label="Device for the agent to inspect"
                >
                  {devices.map((device) => (
                    <SelectItem key={device.id} value={device.id}>
                      {device.device_ref} ({device.device_type})
                    </SelectItem>
                  ))}
                </Select>
              </Label>
            ) : (
              <p className="muted-note">There are no ticket devices available to inspect.</p>
            )}
            <Button
              className="process-button"
              type="button"
              onClick={() => void prepare()}
              disabled={busy || !deviceId}
            >
              {busy ? 'Checking the procedure...' : 'Ask agent to select an action'}
            </Button>
          </>
        )}

        {error && (
          <p className="form-error" role="alert">
            {error}
          </p>
        )}

        {proposal && proposal.requires_confirmation && (
          <ActionProposal proposal={proposal} onReview={() => setDialogOpen(true)} busy={busy} />
        )}
        {proposal && !proposal.requires_confirmation && (
          <p className="execution-result" role="status">
            {proposal.summary}
          </p>
        )}
        {execution && (
          <div className="execution-result" role="status">
            <strong>{execution.status === 'succeeded' ? 'Action completed' : 'Action failed'}</strong>
            <p>{execution.message}</p>
            <Button
              className="text-button"
              type="button"
              onClick={() => {
                setExecution(null)
                setProposal(null)
              }}
            >
              Suggest another action
            </Button>
          </div>
        )}

        {dialogOpen && proposal && (
          <ActionApprovalDialog
            title="Approve agent-proposed action"
            description={`${proposal.summary} Review the target and effect before running this simulated change.`}
            confirmLabel="Approve and run"
            busy={busy}
            onConfirm={() => void confirm()}
            onCancel={() => setDialogOpen(false)}
          />
        )}
      </CardContent>
    </Card>
  )
}
