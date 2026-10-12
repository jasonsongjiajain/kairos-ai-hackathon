import { motion, useReducedMotion } from 'framer-motion'
import { arrive, reveal } from '../../lib/motion'

export type ToolActivityState = 'pending' | 'completed' | 'needs-approval' | 'no-evidence' | 'failed'

const labels: Record<ToolActivityState, string> = {
  pending: 'Pending', completed: 'Completed', 'needs-approval': 'Needs approval',
  'no-evidence': 'No evidence', failed: 'Failed',
}

export function ToolActivity({ state, label, description }: {
  state: ToolActivityState
  label: string
  description: string
}) {
  const reducedMotion = Boolean(useReducedMotion())
  return (
    <motion.div className={`tool-activity tool-activity--${state}`} role="status" aria-live="polite" aria-atomic="true"
      variants={arrive} initial="hidden" animate="visible" custom={reducedMotion}>
      <motion.span className="tool-activity__state" variants={reveal}
        initial="hidden" animate="visible" custom={reducedMotion}>
        {state === 'pending' && <span className="tool-activity__pending" aria-hidden="true" />}
        {labels[state]}
      </motion.span>
      <div><strong>{label}</strong><p>{description}</p></div>
    </motion.div>
  )
}
