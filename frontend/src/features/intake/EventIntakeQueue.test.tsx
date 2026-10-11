import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { AuthProvider } from '../auth/AuthProvider'
import { EventIntakeQueue } from './EventIntakeQueue'

const PENDING_EVENTS = [
  {
    id: 'event-1',
    source_event_id: 'EVT-1',
    event_type: 'ONU_OFFLINE',
    device_id: 'device-1',
    device_ref: 'DEV-1',
    device_name: 'Test ONU',
    device_status: 'offline',
    service_id: 'service-1',
    service_ref: 'SVC-1',
    payload: { signal_state: 'no_link' },
    received_at: '2026-10-11T09:30:00Z',
  },
]

const PROCESS_RESULT = {
  ticket: {
    id: 'ticket-1',
    source_event_id: 'event-1',
    customer_id: 'customer-1',
    service_id: 'service-1',
    assigned_technician_id: 'technician-1',
    severity: 'high',
    status: 'open',
    summary: 'ONU_OFFLINE reported for Test ONU',
  },
  created: true,
  duplicate: false,
  source_event_id: 'EVT-1',
  assigned_technician_name: 'Test Technician',
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

function renderQueue() {
  return render(
    <AuthProvider>
      <MemoryRouter initialEntries={['/operations']}>
        <Routes>
          <Route path="/operations" element={<EventIntakeQueue />} />
          <Route path="/tickets/:ticketId" element={<h1>Ticket workspace</h1>} />
        </Routes>
      </MemoryRouter>
    </AuthProvider>,
  )
}

describe('EventIntakeQueue', () => {
  beforeEach(() => {
    window.sessionStorage.clear()
    window.sessionStorage.setItem(
      'field-force-auth-session',
      JSON.stringify({
        accessToken: 'operator-token',
        userId: 'operator-1',
        role: 'operator',
        expiresAt: Date.now() + 60_000,
      }),
    )
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    window.sessionStorage.clear()
  })

  it('shows a loading state and then the labeled seeded event', async () => {
    let resolveFetch: (value: Response) => void = () => {}
    vi.stubGlobal(
      'fetch',
      vi.fn(
        () =>
          new Promise<Response>((resolve) => {
            resolveFetch = resolve
          }),
      ),
    )
    renderQueue()

    expect(screen.getByText('Loading pending events.')).toBeInTheDocument()

    await act(async () => {
      resolveFetch(jsonResponse(PENDING_EVENTS))
    })
    expect(await screen.findByRole('button', { name: /ONU OFFLINE/ })).toBeInTheDocument()
    expect(screen.getByText('Seeded demo event')).toBeInTheDocument()
    expect(screen.getAllByText('EVT-1').length).toBeGreaterThan(0)
  })

  it('shows an empty state when no events are pending', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse([])))
    renderQueue()

    expect(await screen.findByRole('heading', { name: 'No pending events' })).toBeInTheDocument()
  })

  it('shows an error state and reloads on retry', async () => {
    const user = userEvent.setup()
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(jsonResponse({ detail: 'boom' }, 500))
      .mockResolvedValueOnce(jsonResponse(PENDING_EVENTS))
    vi.stubGlobal('fetch', fetchMock)
    renderQueue()

    expect(await screen.findByRole('alert')).toHaveTextContent('The event queue could not be loaded.')
    await user.click(screen.getByRole('button', { name: 'Retry loading events' }))

    expect(await screen.findByRole('button', { name: /ONU OFFLINE/ })).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })

  it('disables the submit while processing and links to the created ticket', async () => {
    const user = userEvent.setup()
    let resolveProcess: (value: Response) => void = () => {}
    const fetchMock = vi.fn((input: RequestInfo | URL) => {
      if (String(input).includes('/process')) {
        return new Promise<Response>((resolve) => {
          resolveProcess = resolve
        })
      }
      return Promise.resolve(jsonResponse(PENDING_EVENTS))
    })
    vi.stubGlobal('fetch', fetchMock)
    renderQueue()

    const eventButton = await screen.findByRole('button', { name: /ONU OFFLINE/ })
    await user.click(eventButton)
    await user.click(screen.getByRole('button', { name: 'Process event' }))

    const pendingButton = await screen.findByRole('button', { name: 'Processing event' })
    expect(pendingButton).toBeDisabled()

    await act(async () => {
      resolveProcess(jsonResponse(PROCESS_RESULT))
    })
    expect(await screen.findByRole('heading', { name: 'Ticket created' })).toBeInTheDocument()
    expect(screen.getByText('Test Technician')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Open ticket' })).toHaveAttribute('href', '/tickets/ticket-1')
    await waitFor(() => expect(screen.queryByRole('button', { name: /Process event/ })).not.toBeInTheDocument())
  })

  it('reports a duplicate result without creating a second ticket', async () => {
    const user = userEvent.setup()
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL) =>
        Promise.resolve(
          String(input).includes('/process')
            ? jsonResponse({ ...PROCESS_RESULT, created: false, duplicate: true })
            : jsonResponse(PENDING_EVENTS),
        ),
      ),
    )
    renderQueue()

    await user.click(await screen.findByRole('button', { name: /ONU OFFLINE/ }))
    await user.click(screen.getByRole('button', { name: 'Process event' }))

    expect(await screen.findByRole('heading', { name: 'Ticket already exists' })).toBeInTheDocument()
  })
})
