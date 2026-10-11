import { useState, type FormEvent } from 'react'

type AssistantComposerProps = {
  onSubmit: (question: string) => void
  disabled: boolean
}

export function AssistantComposer({ onSubmit, disabled }: AssistantComposerProps) {
  const [question, setQuestion] = useState('')

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const trimmed = question.trim()
    if (!trimmed || disabled) return
    onSubmit(trimmed)
    setQuestion('')
  }

  return (
    <form className="assistant-composer" onSubmit={handleSubmit}>
      <div className="form-field">
        <label htmlFor="assistant-question">Ask about this ticket</label>
        <textarea
          id="assistant-question"
          name="question"
          rows={3}
          maxLength={1000}
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={disabled}
          placeholder="Describe what you see and what you need to fix."
        />
      </div>
      <button
        className="process-button assistant-submit"
        type="submit"
        disabled={disabled || question.trim().length === 0}
      >
        {disabled ? 'Searching service guidance' : 'Ask the assistant'}
      </button>
    </form>
  )
}
