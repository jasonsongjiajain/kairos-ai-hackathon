import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { ToolActivity, type ToolActivityState } from './ToolActivity'

vi.mock('framer-motion', async (importOriginal) => {
  const original = await importOriginal<typeof import('framer-motion')>()
  return { ...original, useReducedMotion: () => true }
})

describe('ToolActivity', () => {
  it('keeps one polite status through real state changes, with immediate reduced motion', () => {
    const { rerender } = render(<ToolActivity state="pending" label="Retrieving evidence" description="Searching ticket evidence and service guidance..." />)
    const status = screen.getByRole('status')
    const liveText = status.querySelector('.tool-activity__state')
    expect(screen.getAllByRole('status')).toHaveLength(1)
    expect(status).toHaveAttribute('aria-live', 'polite')
    expect(status).toHaveTextContent('Pending')
    expect(status.querySelector('.tool-activity__track')).toBeInTheDocument()
    expect(status).toHaveTextContent('Retrieving evidence')
    expect(status).toHaveTextContent('Searching ticket evidence and service guidance...')
    expect(status).toHaveStyle({ opacity: '1' })
    for (const [state, text] of Object.entries({ completed: 'Completed', 'needs-approval': 'Needs approval', 'no-evidence': 'No evidence', failed: 'Failed' })) {
      rerender(<ToolActivity state={state as ToolActivityState} label="Ticket evidence" description="Service response received" />)
      expect(screen.getByRole('status')).toBe(status)
      expect(status.querySelector('.tool-activity__state')).toBe(liveText)
      expect(status).toHaveTextContent(text)
      expect(status).not.toHaveTextContent('Pending')
      expect(status.querySelector('.tool-activity__track')).not.toBeInTheDocument()
      expect(status).toHaveStyle({ opacity: '1' })
    }
  })
})
