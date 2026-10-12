import { Fragment, useCallback, useEffect, useRef, useState } from 'react'
import { motion, useReducedMotion } from 'framer-motion'
import { reveal } from '../../lib/motion'
import { Button } from '../../components/ui/button'
import { TicketsApiError } from '../../lib/api/tickets'
import type { Device } from '../../lib/api/tickets'
import { askAssistantWithStream, type AssistantAnswer } from '../../lib/api/assistant'
import { AgentSuggestedAction } from './AgentSuggestedAction'
import { NextBestActionPanel } from '../work/NextBestActionPanel'
import { AssistantComposer } from './AssistantComposer'
import { ChatMessage } from './ChatMessage'
import { EvidenceCitation } from './EvidenceCitation'
import { ToolActivity, type ToolActivityState } from './ToolActivity'
import type { IncidentStage } from '../work/IncidentTrace'
import type { ToolExecution } from '../../lib/api/tools'

type TurnState = 'pending' | 'answered' | 'error'

type Turn = {
  id: number
  question: string
  state: TurnState
  answer?: AssistantAnswer
  message?: string
  activity: ToolActivityState
}

type TroubleshootingAssistantProps = {
  ticketId: string
  token: string
  devices: Device[]
  onSelectDevice?: (deviceId: string) => void
  onEvidenceProgress?: (stage: IncidentStage) => void
  onEvidenceStart?: () => NonNullable<TroubleshootingAssistantProps['onEvidenceProgress']>
  onActionProgress?: (stage: IncidentStage, outcome?: ToolExecution) => void
  onActionStart?: () => NonNullable<TroubleshootingAssistantProps['onActionProgress']>
}

function AssistantAnswerBody({ answer }: { answer: AssistantAnswer }) {
  const reducedMotion = Boolean(useReducedMotion())
  return (
    <motion.div className="assistant-answer" variants={reveal} initial="hidden" animate="visible" custom={reducedMotion}>
      <p className="assistant-answer-text">{answer.answer}</p>
      {answer.uncertainty && <p className="assistant-uncertainty">{answer.uncertainty}</p>}
      {!answer.has_evidence && (
        <p className="no-evidence-note">
          No knowledge document matched this question, so this answer has no cited source.
        </p>
      )}
      {answer.citations.length > 0 && (
        <div className="citation-block">
          <h4>Retrieved evidence</h4>
          <ul className="citation-list">
            {answer.citations.map((citation, index) => (
              <EvidenceCitation key={citation.chunk_id} citation={citation} index={index} />
            ))}
          </ul>
        </div>
      )}
      {answer.next_best_action && (
        <NextBestActionPanel action={answer.next_best_action} citations={answer.citations} />
      )}
    </motion.div>
  )
}

export function TroubleshootingAssistant(props: TroubleshootingAssistantProps) {
  return <AssistantSession key={`${props.ticketId}:${props.token}`} {...props} />
}

function AssistantSession({ ticketId, token, devices, onSelectDevice, onEvidenceProgress, onEvidenceStart, onActionProgress, onActionStart }: TroubleshootingAssistantProps) {
  const [turns, setTurns] = useState<Turn[]>([])
  const [nextId, setNextId] = useState(1)
  const active = useRef(true)
  const latestRequest = useRef(0)
  useEffect(() => { active.current = true; return () => { active.current = false } }, [])

  const run = useCallback(
    async (id: number, question: string) => {
      const request = ++latestRequest.current
      const reportEvidence = onEvidenceStart?.() ?? onEvidenceProgress
      setTurns((current) =>
        current.map((turn) => (turn.id === id ? { ...turn, state: 'pending', activity: 'pending', message: undefined } : turn)),
      )
      try {
        const answer = await askAssistantWithStream(ticketId, question, token, (message) => {
          if (!active.current) return
          setTurns((current) => current.map((turn) => (turn.id === id ? { ...turn, message } : turn)))
          if (request === latestRequest.current || onEvidenceStart) reportEvidence?.({ id: 'evidence', label: 'Evidence', state: 'current', detail: message })
        })
        if (!active.current) return
        setTurns((current) =>
          current.map((turn) => (turn.id === id ? { ...turn, state: 'answered', activity: answer.has_evidence ? 'completed' : 'no-evidence', answer } : turn)),
        )
        if (request === latestRequest.current || onEvidenceStart) reportEvidence?.({ id: 'evidence', label: 'Evidence', state: answer.has_evidence ? 'complete' : 'blocked', detail: answer.has_evidence ? 'Evidence returned' : 'No matching evidence returned' })
      } catch (error) {
        if (!active.current) return
        if (request === latestRequest.current || onEvidenceStart) reportEvidence?.({ id: 'evidence', label: 'Evidence', state: 'blocked', detail: 'Assistant request failed' })
        setTurns((current) =>
          current.map((turn) =>
            turn.id === id
              ? {
                  ...turn,
                  state: 'error',
                  activity: 'failed',
                  message:
                    error instanceof TicketsApiError
                      ? error.message
                      : 'The assistant could not answer this question.',
                }
              : turn,
          ),
        )
      }
    },
    [ticketId, token, onEvidenceProgress],
  )

  const ask = (question: string) => {
    const id = nextId
    setNextId(id + 1)
    setTurns((current) => [...current, { id, question, state: 'pending', activity: 'pending' }])
    void run(id, question)
  }

  const isSearching = turns.some((turn) => turn.state === 'pending')

  return (
    <section className="panel assistant-panel" aria-labelledby="assistant-heading">
      <header className="assistant-heading">
        <div>
          <p className="section-label">Troubleshooting assistant</p>
          <h3 id="assistant-heading">A clearer path to resolution.</h3>
        </div>
        <span className="assistant-context-label">Ticket context included</span>
      </header>

      {turns.length === 0 ? (
        <div className="assistant-empty">
          <p className="assistant-empty-title">Investigate the service<br /><em>one question at a time.</em></p>
          <p className="muted-note">Ask about the ticket, network path, or next checks. Answers can include ticket evidence and inspectable sources.</p>
          <div className="assistant-starters" aria-label="Suggested questions">
            {['What should I check first?', 'Why is the service down?', 'Summarize this ticket'].map((question) => (
              <Button key={question} variant="secondary" type="button" onClick={() => ask(question)}>{question}</Button>
            ))}
          </div>
        </div>
      ) : (
        <ul className="chat-thread" tabIndex={0} aria-label="Ticket conversation" aria-live="polite" aria-relevant="additions text">
          {turns.map((turn) => (
            <Fragment key={turn.id}>
              <ChatMessage role="user" label="You asked">
                <p>{turn.question}</p>
              </ChatMessage>

              <ChatMessage role="assistant" label="Assistant">
                <ToolActivity state={turn.activity} label="Ticket evidence"
                  description={turn.state === 'answered'
                    ? turn.answer?.has_evidence ? 'Evidence returned with the answer.' : 'No matching evidence returned.'
                    : turn.message ?? 'Waiting for the assistant response.'} />
              {turn.state === 'error' && (
                <>
                  <p className="form-error" role="alert">
                    {turn.message}
                  </p>
                  <Button
                    className="process-button"
                    type="button"
                    onClick={() => void run(turn.id, turn.question)}
                  >
                    Retry this question
                  </Button>
                </>
              )}

              {turn.state === 'answered' && turn.answer && (
                <>
                  <AssistantAnswerBody answer={turn.answer} />
                  {turn.answer.has_evidence && (
                    <AgentSuggestedAction
                      ticketId={ticketId}
                      token={token}
                      question={turn.question}
                      devices={devices}
                      onSelectDevice={onSelectDevice}
                      onActionProgress={onActionProgress}
                      onActionStart={onActionStart}
                    />
                  )}
                </>
              )}
              </ChatMessage>
            </Fragment>
          ))}
        </ul>
      )}

      <AssistantComposer onSubmit={ask} disabled={false} isSearching={isSearching} />
    </section>
  )
}
