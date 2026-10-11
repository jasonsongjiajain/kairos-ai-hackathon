import { useState } from 'react'
import { Button } from '../../components/ui/button'
import { EventsApiError, processEventWithUpdates, type ProcessEventResult } from '../../lib/api/events'

type ProcessEventButtonProps = {
  eventId: string
  token: string
  onProcessed: (result: ProcessEventResult) => void
}

export function ProcessEventButton({ eventId, token, onProcessed }: ProcessEventButtonProps) {
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState('')

  const submit = async () => {
    if (submitting) return
    setSubmitting(true)
    setError('')
    setProgress('')
    try {
      const result = await processEventWithUpdates(eventId, token, setProgress)
      onProcessed(result)
    } catch (caught) {
      setError(caught instanceof EventsApiError ? caught.message : 'The event could not be processed. Retry.')
    } finally {
      setSubmitting(false)
      setProgress('')
    }
  }

  return (
    <div className="process-actions">
      <Button
        className="process-button"
        type="button"
        onClick={submit}
        disabled={submitting}
        aria-busy={submitting}
      >
        {submitting ? progress || 'Processing event' : 'Process event'}
      </Button>
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
