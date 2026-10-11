import type { ToolProposal } from '../../lib/api/tools'
import { Button } from '../../components/ui/button'

type ActionProposalProps = {
  proposal: ToolProposal
  onReview: () => void
  busy?: boolean
}

function parameterLines(proposal: ToolProposal): string[] {
  const entries: string[] = []
  for (const [key, value] of Object.entries(proposal.parameters)) {
    if (key === 'device_id') continue
    if (key === 'settings' && value && typeof value === 'object') {
      for (const [setting, settingValue] of Object.entries(value as Record<string, unknown>)) {
        entries.push(`${setting} = ${String(settingValue)}`)
      }
      continue
    }
    entries.push(`${key} = ${String(value)}`)
  }
  return entries
}

export function ActionProposal({ proposal, onReview, busy = false }: ActionProposalProps) {
  const lines = parameterLines(proposal)
  return (
    <article className="proposal-card" aria-label={`Proposed action ${proposal.tool_name}`}>
      <header className="proposal-header">
        <p className="section-label">PROPOSED ACTION</p>
        <h4>{proposal.summary}</h4>
      </header>
      <dl className="proposal-details">
        <div>
          <dt>Target device</dt>
          <dd>{proposal.device_ref}</dd>
        </div>
        <div>
          <dt>Type</dt>
          <dd>{proposal.kind === 'read_only' ? 'Read-only check' : 'State-changing action'}</dd>
        </div>
        {lines.length > 0 && (
          <div>
            <dt>Parameters</dt>
            <dd>{lines.join(', ')}</dd>
          </div>
        )}
      </dl>
      {proposal.requires_confirmation ? (
        <p className="muted-note">
          This action changes the device. Review the target and effect, then approve to execute the
          simulated change.
        </p>
      ) : (
        <p className="muted-note">This is a read-only check and makes no changes.</p>
      )}
      <Button className="process-button" type="button" onClick={onReview} disabled={busy}>
        {proposal.requires_confirmation ? 'Review and approve' : 'Run check'}
      </Button>
    </article>
  )
}
