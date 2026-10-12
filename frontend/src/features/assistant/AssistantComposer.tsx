import { useState, type FormEvent } from 'react'
import { Button } from '../../components/ui/button'
import { Label } from '../../components/ui/label'
import { Textarea } from '../../components/ui/textarea'

type AssistantComposerProps = {
  onSubmit: (question: string) => void
  disabled: boolean
  isSearching?: boolean
}

export function AssistantComposer({ onSubmit, disabled, isSearching = false }: AssistantComposerProps) {
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
        <Label htmlFor="assistant-question">Ask about this ticket</Label>
        <Textarea
          id="assistant-question"
          name="question"
          rows={3}
          maxLength={1000}
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          disabled={disabled}
          aria-describedby="composer-hint"
           onKeyDown={(event) => {
             if (event.key === 'Enter' && (event.metaKey || event.ctrlKey) && !event.nativeEvent.isComposing) {
               event.preventDefault()
               event.currentTarget.form?.requestSubmit()
             }
           }}
          placeholder="Describe what you see and what you need to fix."
        />
      </div>
      <div className="composer-footer">
      <p id="composer-hint">Enter adds a line · Ctrl / ⌘ + Enter sends{isSearching ? ' · You can ask a follow-up while the assistant responds' : ''}</p>
      <Button
        className="process-button assistant-submit"
        type="submit"
        disabled={disabled || question.trim().length === 0}
      >
        {disabled ? 'Assistant unavailable' : 'Send question'}
      </Button>
      </div>
    </form>
  )
}
