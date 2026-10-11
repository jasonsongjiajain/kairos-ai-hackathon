import { Fragment, useCallback, useState } from 'react'
import { Button } from '../../components/ui/button'
import { TicketsApiError } from '../../lib/api/tickets'
import type { Device } from '../../lib/api/tickets'
import { askAssistantWithStream, type AssistantAnswer } from '../../lib/api/assistant'
import { AgentSuggestedAction } from './AgentSuggestedAction'
import { NextBestActionPanel } from '../work/NextBestActionPanel'
import { AssistantComposer } from './AssistantComposer'
import { ChatMessage } from './ChatMessage'
import { EvidenceCitation } from './EvidenceCitation'

type TurnState = 'pending' | 'answered' | 'error'

type Turn = {
  id: number
  question: string
  state: TurnState
  answer?: AssistantAnswer
  message?: string
}

type TroubleshootingAssistantProps = {
  ticketId: string
  token: string
  devices: Device[]
}

function AssistantAnswerBody({ answer }: { answer: AssistantAnswer }) {
  return (
    <div className="assistant-answer">
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
    </div>
  )
}

export function TroubleshootingAssistant({ ticketId, token, devices }: TroubleshootingAssistantProps) {
  const [turns, setTurns] = useState<Turn[]>([])
  const [nextId, setNextId] = useState(1)

  const run = useCallback(
    async (id: number, question: string) => {
      setTurns((current) =>
        current.map((turn) => (turn.id === id ? { ...turn, state: 'pending', message: undefined } : turn)),
      )
      try {
        const answer = await askAssistantWithStream(ticketId, question, token, (message) => {
          setTurns((current) => current.map((turn) => (turn.id === id ? { ...turn, message } : turn)))
        })
        setTurns((current) =>
          current.map((turn) => (turn.id === id ? { ...turn, state: 'answered', answer } : turn)),
        )
      } catch (error) {
        setTurns((current) =>
          current.map((turn) =>
            turn.id === id
              ? {
                  ...turn,
                  state: 'error',
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
    [ticketId, token],
  )

  const ask = (question: string) => {
    const id = nextId
    setNextId(id + 1)
    setTurns((current) => [...current, { id, question, state: 'pending' }])
    void run(id, question)
  }

  const isSearching = turns.some((turn) => turn.state === 'pending')

  return (
    <section className="panel assistant-panel" aria-labelledby="assistant-heading">
      <p className="section-label">TROUBLESHOOTING ASSISTANT</p>
      <h3 id="assistant-heading">Ask about this ticket</h3>
      <p className="muted-note">
        Answers use the ticket context and retrieved service guidance. Every citation below was
        retrieved for your question; when no guidance matches, the assistant says so.
      </p>

      {turns.length === 0 ? (
        <p className="muted-note assistant-empty">
          No questions yet. Ask what to check first, or why the service is down.
        </p>
      ) : (
        <ul className="chat-thread">
          {turns.map((turn) => (
            <Fragment key={turn.id}>
              <ChatMessage role="user" label="You asked">
                <p>{turn.question}</p>
              </ChatMessage>

              {turn.state === 'pending' && (
                <ChatMessage role="assistant" label="Assistant">
                  <p className="searching-note" role="status">
                    {turn.message ?? 'Starting ticket investigation...'}
                  </p>
                </ChatMessage>
              )}

              {turn.state === 'error' && (
                <ChatMessage role="assistant" label="Assistant">
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
                </ChatMessage>
              )}

              {turn.state === 'answered' && turn.answer && (
                <ChatMessage role="assistant" label="Assistant">
                  <AssistantAnswerBody answer={turn.answer} />
                  {turn.answer.has_evidence && (
                    <AgentSuggestedAction
                      ticketId={ticketId}
                      token={token}
                      question={turn.question}
                      devices={devices}
                    />
                  )}
                </ChatMessage>
              )}
            </Fragment>
          ))}
        </ul>
      )}

      <AssistantComposer onSubmit={ask} disabled={isSearching} />
    </section>
  )
}
