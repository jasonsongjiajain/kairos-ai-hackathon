import { cleanup, render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { IncidentTrace, type IncidentStage } from './IncidentTrace'

const stages: IncidentStage[] = [
  { id: 'event', label: 'Event', state: 'complete', detail: 'Source event: event-1' },
  { id: 'ticket', label: 'Ticket', state: 'current' },
  { id: 'topology', label: 'Topology', state: 'blocked', detail: 'Service path unavailable' },
  { id: 'evidence', label: 'Evidence', state: 'upcoming' },
  { id: 'action', label: 'Action', state: 'upcoming' },
]

afterEach(() => { cleanup(); vi.unstubAllGlobals() })

describe('IncidentTrace', () => {
  it('exposes ordered stages, current context, blocked detail and unknown states', () => {
    render(<IncidentTrace stages={stages} />)
    const list = screen.getByRole('list', { name: 'Incident trace' })
    expect(list.tagName).toBe('OL')
    const items = within(list).getAllByRole('listitem')
    expect(items.map(item => within(item).getByRole('heading').textContent))
      .toEqual(['Event', 'Ticket', 'Topology', 'Evidence', 'Action'])
    expect(items[0]).toHaveTextContent('Complete')
    expect(items[1]).toHaveAttribute('aria-current', 'step')
    expect(items[1]).toHaveTextContent('Current')
    expect(items[2]).toHaveTextContent('Blocked')
    expect(items[2]).toHaveTextContent('Service path unavailable')
    expect(items[3]).toHaveTextContent('Upcoming')
    expect(items[4]).toHaveTextContent('Upcoming')
    expect(list.querySelectorAll('[aria-current="step"]')).toHaveLength(1)
  })

  it('requires a caller-confirmed outcome before presenting action completion', () => {
    const completed = stages.map(stage => stage.id === 'action'
      ? { ...stage, state: 'complete' as const } : stage)
    const { rerender } = render(<IncidentTrace stages={completed} />)
    const action = () => screen.getAllByRole('listitem')[4]
    expect(action()).toHaveTextContent('Upcoming')
    expect(action()).not.toHaveTextContent('Complete')
    rerender(<IncidentTrace stages={completed} confirmedActionOutcome="  " />)
    expect(action()).toHaveTextContent('Upcoming')
    rerender(<IncidentTrace stages={completed} confirmedActionOutcome="Router restart confirmed" />)
    expect(action()).toHaveTextContent('Complete')
    expect(action()).toHaveTextContent('Router restart confirmed')
  })

  it('renders the full trace immediately when reduced motion is requested', () => {
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: true, addListener: vi.fn(), removeListener: vi.fn(),
    })))
    const { container } = render(<IncidentTrace stages={stages} />)
    const marks = container.querySelectorAll('[aria-hidden="true"]')
    expect(marks.length).toBeGreaterThan(0)
    for (const mark of marks) {
      expect(mark).toHaveStyle({ opacity: '1', transform: 'none' })
    }
    expect(screen.getAllByRole('listitem')[4]).toHaveTextContent('Upcoming')
  })

  it('settles once without restarting when stage data rerenders', async () => {
    const { container, rerender } = render(<IncidentTrace stages={stages} />)
    const marks = Array.from(container.querySelectorAll('[aria-hidden="true"]'))
    await waitFor(() => {
      for (const mark of marks) expect(mark).toHaveStyle({ opacity: '1', transform: 'none' })
    }, { timeout: 2500 })
    rerender(<IncidentTrace stages={stages.map(stage => ({ ...stage, detail: 'Updated context' }))} />)
    expect(Array.from(container.querySelectorAll('[aria-hidden="true"]'))).toEqual(marks)
    for (const mark of marks) expect(mark).toHaveStyle({ opacity: '1', transform: 'none' })
  })
})
