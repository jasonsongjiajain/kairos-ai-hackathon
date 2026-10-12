import { useEffect, useRef, useState } from 'react'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader } from '../../components/ui/card'
import { Label } from '../../components/ui/label'
import { Select, SelectItem } from '../../components/ui/select'
import type { Device } from '../../lib/api/tickets'
import { TicketsApiError } from '../../lib/api/tickets'
import { confirmTool, executionFromProposal, proposeAgentTool, type ToolExecution, type ToolProposal } from '../../lib/api/tools'
import { ActionApprovalDialog } from './ActionApprovalDialog'
import { ActionProposal } from './ActionProposal'
import { ToolActivity } from './ToolActivity'
import { ToolExecutionResult } from './ToolExecutionResult'
import type { IncidentStage } from '../work/IncidentTrace'

type AgentSuggestedActionProps = {
  ticketId: string
  token: string
  question: string
  devices: Device[]
  onSelectDevice?: (deviceId: string) => void
  onActionProgress?: (stage: IncidentStage, outcome?: ToolExecution) => void
  onActionStart?: () => NonNullable<AgentSuggestedActionProps['onActionProgress']>
}

export function AgentSuggestedAction(props: AgentSuggestedActionProps) {
  return <SuggestedActionSession key={`${props.ticketId}:${props.token}:${props.question}`} {...props} />
}

function SuggestedActionSession({ ticketId, token, question, devices, onSelectDevice, onActionProgress, onActionStart }: AgentSuggestedActionProps) {
  const active = useRef(true)
  useEffect(() => { active.current = true; return () => { active.current = false } }, [])
  const [deviceId, setDeviceId] = useState(devices[0]?.id ?? '')
  const [proposal, setProposal] = useState<ToolProposal | null>(null)
  const [execution, setExecution] = useState<ToolExecution | null>(null)
  const [attempts, setAttempts] = useState<{ proposal: ToolProposal | null; execution: ToolExecution }[]>([])
  const [busy, setBusy] = useState(false)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [error, setError] = useState('')

  const prepare = async () => {
    if (!deviceId || busy) return
    const report = onActionStart?.() ?? onActionProgress
    setBusy(true)
    report?.({ id: 'action', label: 'Action', state: 'current', detail: 'Preparing proposal' })
    setError('')
    if (execution) setAttempts((current) => [...current, { proposal, execution }])
    setProposal(null)
    setExecution(null)
    try {
      const result = await proposeAgentTool(ticketId, { question, deviceId }, token)
      if (!active.current) return
      setProposal(result)
      const outcome = executionFromProposal(result)
      setExecution(outcome)
      if (outcome) {
        report?.({ id: 'action', label: 'Action', state: outcome.status === 'succeeded' ? 'complete' : 'blocked', detail: outcome.message }, outcome)
      } else {
        report?.({ id: 'action', label: 'Action', state: 'current', detail: 'Proposal ready for review' })
      }
    } catch (caught) {
      if (!active.current) return
      report?.({ id: 'action', label: 'Action', state: 'blocked', detail: 'Proposal request failed' })
      setError(caught instanceof TicketsApiError ? caught.message : 'The agent could not prepare an action.')
    } finally {
      if (active.current) setBusy(false)
    }
  }

  const confirm = async () => {
    if (!proposal || execution || !proposal.requires_confirmation || proposal.status !== 'proposed' || busy) return
    const report = onActionStart?.() ?? onActionProgress
    setBusy(true)
    setExecution(null)
    report?.({ id: 'action', label: 'Action', state: 'current', detail: 'Executing approved action' })
    setError('')
    try {
      const result = await confirmTool(ticketId, proposal.id, proposal.confirmation_id, token)
      if (!active.current) return
      setExecution(result)
      if (result.status === 'succeeded') setProposal(null)
      report?.({ id: 'action', label: 'Action', state: result.status === 'succeeded' ? 'complete' : 'blocked', detail: result.message }, result)
      setDialogOpen(false)
    } catch (caught) {
      if (!active.current) return
      report?.({ id: 'action', label: 'Action', state: 'blocked', detail: 'Execution request failed' })
      setError(caught instanceof TicketsApiError ? caught.message : 'The action could not be executed.')
      setDialogOpen(false)
    } finally {
      if (active.current) setBusy(false)
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
              {busy ? 'Preparing proposal...' : 'Ask agent to select an action'}
            </Button>
          </>
        )}

        {error && (
          <p className="form-error" role="alert">
            {error}
          </p>
        )}

        {(busy || proposal || execution || error) && <ToolActivity
          state={error || (execution && execution.status !== 'succeeded') ? 'failed' : busy ? 'pending' : execution ? 'completed' : 'needs-approval'}
          label={busy ? proposal ? 'Executing action' : 'Preparing proposal' : 'Device action'}
          description={error || proposal?.tool_name || execution?.tool_name || 'Requesting a grounded action proposal.'} />}
        {proposal && !execution && <ActionProposal proposal={proposal} onReview={() => setDialogOpen(true)} busy={busy} onSelectDevice={onSelectDevice} />}
        {execution?.status === 'failed' && proposal && proposal.requires_confirmation && <ActionProposal proposal={proposal} onSelectDevice={onSelectDevice} />}
        {execution && <ToolExecutionResult key={execution.id} execution={execution} onSelectDevice={onSelectDevice}
          runAnotherLabel={execution.status === 'failed' ? 'Retry with new proposal' : undefined}
          onRunAnother={execution.status === 'failed' ? () => void prepare() : () => {
            setAttempts((current) => [...current, { proposal, execution }])
            setExecution(null); setProposal(null); setError('')
          }} />}
        {attempts.map((attempt) => <section key={attempt.execution.id} aria-label="Previous action attempt">
          {attempt.proposal?.requires_confirmation && <ActionProposal proposal={attempt.proposal} onSelectDevice={onSelectDevice} />}
          <ToolExecutionResult execution={attempt.execution} onSelectDevice={onSelectDevice} />
        </section>)}

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
