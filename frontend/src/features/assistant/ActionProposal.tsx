import type { ToolProposal } from '../../lib/api/tools'
import { Button } from '../../components/ui/button'
import { motion, useReducedMotion } from 'framer-motion'
import { arrive } from '../../lib/motion'

type ActionProposalProps = {
  proposal: ToolProposal
  onReview?: () => void
  busy?: boolean
  onSelectDevice?: (deviceId: string) => void
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

export function ActionProposal({ proposal, onReview, busy = false, onSelectDevice }: ActionProposalProps) {
  const reducedMotion = Boolean(useReducedMotion())
  const lines = parameterLines(proposal)
  return (
    <motion.article className="proposal-card" aria-label={`${onReview ? 'Proposed action' : 'Recorded proposal'} ${proposal.tool_name}`}
      variants={arrive} initial="hidden" animate="visible" custom={reducedMotion}>
      <header className="proposal-header">
        <p className="section-label">{onReview ? 'PROPOSED ACTION' : 'RECORDED PROPOSAL'}</p>
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
      {onSelectDevice && <Button variant="quiet" type="button" onClick={() => onSelectDevice(proposal.device_id)}>
        Show {proposal.device_ref} in topology
      </Button>}
      {onReview && (proposal.requires_confirmation ? (
        <p className="muted-note">
          This action changes the device. Review the target and effect, then approve to execute the
          simulated change.
        </p>
      ) : (
        <p className="muted-note">This is a read-only check and makes no changes.</p>
      ))}
      {onReview && <Button className="process-button" type="button" onClick={onReview} disabled={busy}>
        {proposal.requires_confirmation ? 'Review and approve' : 'Run check'}
      </Button>}
    </motion.article>
  )
}
