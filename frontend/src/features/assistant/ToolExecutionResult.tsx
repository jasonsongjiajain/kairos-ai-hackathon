import type { ToolExecution } from '../../lib/api/tools'
import { Button } from '../../components/ui/button'
import { motion, useReducedMotion } from 'framer-motion'
import { reveal, settle } from '../../lib/motion'

type ToolExecutionResultProps = {
  execution: ToolExecution
  onRunAnother?: () => void
  runAnotherLabel?: string
  onSelectDevice?: (deviceId: string) => void
}

export function ToolExecutionResult({ execution, onRunAnother, onSelectDevice, runAnotherLabel = 'Prepare another action' }: ToolExecutionResultProps) {
  const reducedMotion = Boolean(useReducedMotion())
  const succeeded = execution.status === 'succeeded'
  return (
    <motion.div className={`execution-result ${succeeded ? 'is-success' : 'is-failure'}`} role="status" aria-live="polite"
      variants={succeeded ? settle : reveal} initial="hidden" animate="visible" custom={reducedMotion}>
      <p className={`execution-status ${succeeded ? 'is-success' : 'is-failure'}`}>
        <span aria-hidden="true">{succeeded ? 'OK' : 'FAILED'}</span>{' '}
        {succeeded ? 'Action completed' : 'Action failed'}
      </p>
      <p>{execution.message}</p>
      <dl className="proposal-details">
        <div>
          <dt>Device</dt>
          <dd>{execution.device_ref}</dd>
        </div>
        <div>
          <dt>Action</dt>
          <dd>{execution.tool_name}</dd>
        </div>
        <div>
          <dt>Recorded</dt>
          <dd>{new Date(execution.executed_at).toLocaleString()}</dd>
        </div>
      </dl>
      {onSelectDevice && <Button variant="quiet" type="button" onClick={() => onSelectDevice(execution.device_id)}>
        Show {execution.device_ref} in topology
      </Button>}
      {onRunAnother && <Button className="text-button" variant="quiet" type="button" onClick={onRunAnother}>
        {runAnotherLabel}
      </Button>}
    </motion.div>
  )
}
