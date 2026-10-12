import { motion, useReducedMotion } from 'framer-motion'
import { prefersReducedMotion, reveal } from '../../lib/motion'
import { Button } from '../../components/ui/button'

type ProcessEventButtonProps = {
  submitting: boolean
  error: string
  onProcess: () => void
}

export function ProcessEventButton({ submitting, error, onProcess }: ProcessEventButtonProps) {
  const reducedMotion = useReducedMotion() || prefersReducedMotion()

  return (
    <div className="process-actions">
      <Button
        className="process-button"
        type="button"
        onClick={onProcess}
        disabled={submitting}
        aria-busy={submitting}
      >
        {submitting ? 'Processing event' : error ? 'Retry processing event' : 'Process event'}
      </Button>
      <p role="status" aria-live="polite" aria-atomic="true" className="process-status">
        {submitting && <motion.span initial="hidden" animate="visible" variants={reveal} custom={reducedMotion}>Processing event. Waiting for the ticket result.</motion.span>}
      </p>
      {error && (
        <motion.p initial="hidden" animate="visible" variants={reveal} custom={reducedMotion} className="form-error" role="alert">
          {error}
        </motion.p>
      )}
    </div>
  )
}
