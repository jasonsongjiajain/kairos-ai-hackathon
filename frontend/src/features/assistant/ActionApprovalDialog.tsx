import { useEffect, useRef, type ReactNode } from 'react'

type ActionApprovalDialogProps = {
  title: string
  description: string
  confirmLabel: string
  busy?: boolean
  onConfirm: () => void
  onCancel: () => void
  children?: ReactNode
}

export function ActionApprovalDialog({
  title,
  description,
  confirmLabel,
  busy = false,
  onConfirm,
  onCancel,
  children,
}: ActionApprovalDialogProps) {
  const confirmRef = useRef<HTMLButtonElement>(null)
  const previouslyFocused = useRef<Element | null>(null)

  useEffect(() => {
    previouslyFocused.current = document.activeElement
    confirmRef.current?.focus()
    return () => {
      const element = previouslyFocused.current
      if (element instanceof HTMLElement) element.focus()
    }
  }, [])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault()
        onCancel()
      }
    }
    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [onCancel])

  return (
    <div className="dialog-backdrop" role="presentation" onClick={onCancel}>
      <div
        className="dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="approval-dialog-title"
        aria-describedby="approval-dialog-description"
        onClick={(event) => event.stopPropagation()}
      >
        <h3 id="approval-dialog-title">{title}</h3>
        <p id="approval-dialog-description">{description}</p>
        {children}
        <div className="dialog-actions">
          <button className="text-button" type="button" onClick={onCancel} disabled={busy}>
            Cancel
          </button>
          <button
            ref={confirmRef}
            className="process-button"
            type="button"
            onClick={onConfirm}
            disabled={busy}
          >
            {busy ? 'Executing...' : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  )
}
