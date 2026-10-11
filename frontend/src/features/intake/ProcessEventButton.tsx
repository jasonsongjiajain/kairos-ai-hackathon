import { useState } from 'react'
import { EventsApiError, processEvent, type ProcessEventResult } from '../../lib/api/events'

type ProcessEventButtonProps = {
  eventId: string
  token: string
  onProcessed: (result: ProcessEventResult) => void
}

export function ProcessEventButton({ eventId, token, onProcessed }: ProcessEventButtonProps) {
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const submit = async () => {
    if (submitting) return
    setSubmitting(true)
    setError('')
    try {
      const result = await processEvent(eventId, token)
      onProcessed(result)
    } catch (caught) {
      setError(caught instanceof EventsApiError ? caught.message : 'The event could not be processed. Retry.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="process-actions">
      <button
        className="process-button"
        type="button"
        onClick={submit}
        disabled={submitting}
        aria-busy={submitting}
      >
        {submitting ? 'Processing event' : 'Process event'}
      </button>
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
