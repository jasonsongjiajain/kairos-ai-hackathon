import { render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, expect, it, vi } from 'vitest'
import type { AuditEvent } from '../../lib/api/audit'
import { AuditTimeline } from './AuditTimeline'

const events: AuditEvent[] = [
  { id: 'audit-1', event_type: 'event_processed', actor_id: null, actor_name: null,
    ticket_id: 'ticket-1', created_at: '2026-10-11T09:30:00Z', details: { severity: 'high' } },
  { id: 'audit-2', event_type: 'tool_executed', actor_id: 'tech-1', actor_name: 'Test technician',
    ticket_id: 'ticket-1', created_at: '2026-10-11T10:30:00Z',
    details: { device_ref: 'DEV-1', tool_name: 'restart_router', outcome: 'success', message: 'Restart confirmed' } },
]
afterEach(() => vi.unstubAllGlobals())

it('preserves recorded chronology, actors, timestamps and actual outcome', () => {
  render(<AuditTimeline events={events} />)
  const list = screen.getByRole('list', { name: 'Recorded activity' })
  expect(list.tagName).toBe('OL')
  const rows = Array.from(list.children)
  expect(rows[0]).toHaveTextContent('Event processed into a ticket')
  expect(rows[0]).toHaveTextContent('System')
  expect(rows[1]).toHaveTextContent('Device action executed')
  expect(rows[1]).toHaveTextContent('Test technician')
  expect(rows[1]).toHaveTextContent('Device: DEV-1')
  expect(rows[1]).toHaveTextContent('Outcome: success')
  expect(rows[1]).toHaveTextContent('Restart confirmed')
  expect(Array.from(list.querySelectorAll('time')).map(time => time.dateTime))
    .toEqual(['2026-10-11T09:30:00Z', '2026-10-11T10:30:00Z'])
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
})

it('shows an honest empty history without claiming live updates', () => {
  render(<AuditTimeline events={[]} />)
  expect(screen.getByText(/No recorded activity/)).toBeInTheDocument()
  expect(screen.queryByText(/as they happen|live|polling/i)).not.toBeInTheDocument()
})

it('reveals loaded history once without replaying existing rows on new data', async () => {
  const { rerender } = render(<AuditTimeline events={[]} />)
  rerender(<AuditTimeline events={[events[0]]} />)
  const list = screen.getByRole('list', { name: 'Recorded activity' })
  const row = list.firstElementChild
  await waitFor(() => expect(row).toHaveStyle({ opacity: '1' }))
  rerender(<AuditTimeline events={events.map(event => ({ ...event }))} />)
  expect(list.firstElementChild).toBe(row)
  expect(row).toHaveStyle({ opacity: '1' })
  expect(within(list).getByText('Restart confirmed')).toBeInTheDocument()
})

it('renders all records immediately with reduced motion', () => {
  vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: true, addListener: vi.fn(), removeListener: vi.fn() })))
  render(<AuditTimeline events={events} />)
  const list = screen.getByRole('list', { name: 'Recorded activity' })
  for (const row of list.children) expect(row).toHaveStyle({ opacity: '1' })
})
