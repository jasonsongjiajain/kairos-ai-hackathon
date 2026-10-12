import { motion, useReducedMotion } from 'framer-motion'
import { arrive, reveal } from '../../lib/motion'
import { CheckCircle, WarningCircle, Wrench } from '@phosphor-icons/react'

export type ToolActivityState = 'pending' | 'completed' | 'needs-approval' | 'no-evidence' | 'failed'

const labels: Record<ToolActivityState, string> = {
  pending: 'Pending', completed: 'Completed', 'needs-approval': 'Needs approval',
  'no-evidence': 'No evidence', failed: 'Failed',
}

export function ToolActivity({ state, label, description, detail }: {
  state: ToolActivityState
  label: string
  description: string
  detail?: string
}) {
  const reducedMotion = Boolean(useReducedMotion())
  return (
    <motion.div className={`tool-activity tool-activity--${state}`} role="status" aria-live="polite" aria-atomic="true"
      variants={arrive} initial="hidden" animate="visible" custom={reducedMotion}>
      <span className="tool-activity__icon" aria-hidden="true">
        {state === 'completed' ? <CheckCircle size={22} /> : state === 'failed' ? <WarningCircle size={22} /> : <Wrench size={22} />}
      </span>
      <motion.span className="tool-activity__state" variants={reveal}
        initial="hidden" animate="visible" custom={reducedMotion}>
        {state === 'pending' && <span className="tool-activity__pending" aria-hidden="true" />}
        {labels[state]}
      </motion.span>
      <div className="tool-activity__copy"><strong>{label}</strong><p>{description}</p>{detail && <span className="tool-activity__detail">{detail}</span>}</div>
      {state === 'pending' && <span className="tool-activity__track" aria-hidden="true"><span /></span>}
    </motion.div>
  )
}
