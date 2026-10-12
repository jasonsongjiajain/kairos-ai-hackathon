import { motion, useReducedMotion } from 'framer-motion'
import { motionDuration, prefersReducedMotion, transitionFor } from '../../lib/motion'

export type IncidentStage = {
  id: 'event' | 'ticket' | 'topology' | 'evidence' | 'action'
  label: string
  state: 'complete' | 'current' | 'upcoming' | 'blocked'
  detail?: string
}

type IncidentTraceProps = {
  stages: readonly IncidentStage[]
  /** Supply only an actual confirmed execution result, never a proposal or approval. */
  confirmedActionOutcome?: string
}

const stateLabels = { complete: 'Complete', current: 'Current', upcoming: 'Upcoming', blocked: 'Blocked' }
const settled = { opacity: 1, scale: 1 }

export function IncidentTrace({ stages, confirmedActionOutcome }: IncidentTraceProps) {
  const preference = useReducedMotion()
  const reducedMotion = Boolean(preference) || prefersReducedMotion()
  const outcome = confirmedActionOutcome?.trim()

  return (
    <ol className="incident-trace" role="list" aria-label="Incident trace">
      {stages.map((stage, index) => {
        const state = stage.id === 'action' && stage.state === 'complete' && !outcome
          ? 'upcoming' : stage.state
        const entrance = (step: number) => ({
          ...transitionFor(reducedMotion, motionDuration.state),
          delay: reducedMotion ? 0 : step * motionDuration.control,
        })
        return (
          <li key={stage.id} className={`incident-trace__stage incident-trace__stage--${state}`}
            aria-current={state === 'current' ? 'step' : undefined}>
            {index < stages.length - 1 && <motion.span className="incident-trace__connector" aria-hidden="true"
              initial={reducedMotion ? false : { opacity: 0, scale: 0 }} animate={settled}
              transition={entrance(index * 2 + 1)} />}
            <motion.span className="incident-trace__marker" aria-hidden="true"
              initial={reducedMotion ? false : { opacity: 0, scale: 0.8 }} animate={settled}
              transition={entrance(index * 2)}>
              {state === 'complete' ? '✓' : state === 'blocked' ? '!' : index + 1}
            </motion.span>
            <div className="incident-trace__content">
              <h3>{stage.label}</h3>
              <p className="incident-trace__state">{stateLabels[state]}</p>
              {stage.detail && <p className="incident-trace__detail">{stage.detail}</p>}
              {stage.id === 'action' && state === 'complete' && outcome &&
                <p className="incident-trace__detail">{outcome}</p>}
            </div>
          </li>
        )
      })}
    </ol>
  )
}
