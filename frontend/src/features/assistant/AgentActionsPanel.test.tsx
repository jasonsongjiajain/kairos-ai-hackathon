import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { AgentActionsPanel } from './AgentActionsPanel'

const devices = [{ id: 'router-1', device_ref: 'RTR-1', device_type: 'router', name: 'Router', status: 'offline', credential_available: false }]
const proposal = { id: 'p1', ticket_id: 't1', tool_name: 'reboot_router', device_id: 'router-1', device_ref: 'RTR-1', kind: 'stateful', requires_confirmation: true, parameters: {}, status: 'proposed', summary: 'Reboot router', confirmation_id: 'c1', created_at: '2026-10-12T12:00:00Z' }
const execution = { ...proposal, status: 'succeeded', message: 'Router restarted', correlation_id: 'c1', executed_at: '2026-10-12T12:01:00Z' }
const json = (body: unknown) => new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json' } })
const tool = (name: string, description: string, kind: 'read_only' | 'stateful', requires_confirmation: boolean) => ({
  name, title: description, description, kind, category: 'diagnostics', risk: 'medium', requires_confirmation, target_device_types: null,
})
function deferred() {
  let resolve!: (value: Response) => void
  const promise = new Promise<Response>((done) => { resolve = done })
  return { promise, resolve }
}
afterEach(() => vi.unstubAllGlobals())

describe.each(['catalog'] as const)('%s action lifecycle', (kind) => {
  const view = (ticketId = 't1', onSelectDevice = vi.fn(), onActionProgress = vi.fn()) =>
    <AgentActionsPanel ticketId={ticketId} token="token" devices={devices} onSelectDevice={onSelectDevice} onActionProgress={onActionProgress} />
  async function prepare(user: ReturnType<typeof userEvent.setup>) {
    if (kind === 'catalog') await user.click(screen.getByRole('button', { name: 'Load available actions' }))
    await user.click(await screen.findByRole('button', { name: kind === 'catalog' ? 'Prepare proposal' : 'Ask agent to select an action' }))
  }
  function setupFetch(pending: Promise<Response>) {
    const fetcher = vi.fn()
    if (kind === 'catalog') fetcher.mockResolvedValueOnce(json([tool('reboot_router', 'Reboot router', 'stateful', true)]))
    fetcher.mockReturnValueOnce(pending)
    vi.stubGlobal('fetch', fetcher)
    return fetcher
  }
  it('waits for proposal, approves, and waits for result', async () => {
    const preparing = deferred()
    const running = deferred()
    const fetcher = setupFetch(preparing.promise).mockReturnValueOnce(running.promise)
    const user = userEvent.setup()
    const select = vi.fn()
    render(view('t1', select))
    await prepare(user)
    expect(screen.getByRole('status')).toHaveTextContent('Preparing proposal')
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
    await act(async () => preparing.resolve(json(proposal)))
    expect(screen.getByRole('status')).toHaveTextContent('Needs approval')
    await user.click(screen.getByRole('button', { name: 'Show RTR-1 in topology' }))
    expect(select).toHaveBeenCalledWith('router-1')
    await user.click(screen.getByRole('button', { name: 'Approve and run' }))
    expect(screen.queryByText('Router restarted')).not.toBeInTheDocument()
    await act(async () => running.resolve(json(execution)))
    expect(screen.getByText('Router restarted')).toBeInTheDocument()
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
    expect(fetcher).toHaveBeenCalledTimes(kind === 'catalog' ? 3 : 2)
  })

  it('rejects a proposal without executing it', async () => {
    const fetcher = setupFetch(Promise.resolve(json(proposal)))
    const user = userEvent.setup()
    render(view())
    await prepare(user)
    expect(await screen.findByRole('article')).toHaveTextContent('Reboot router')
    await user.click(screen.getByRole('button', { name: 'Reject' }))
    expect(screen.queryByText('Router restarted')).not.toBeInTheDocument()
    expect(fetcher.mock.calls.some(([url]) => String(url).includes('/confirm'))).toBe(false)
  })

  it('preserves proposal on HTTP failure and permits confirmation replay', async () => {
    const fetcher = setupFetch(Promise.resolve(json(proposal)))
      .mockResolvedValueOnce(new Response('', { status: 502 }))
      .mockResolvedValueOnce(json(execution))
    const user = userEvent.setup()
    render(view())
    await prepare(user)
    await user.click(await screen.findByRole('button', { name: 'Approve and run' }))
    expect(await screen.findByRole('article')).toHaveTextContent('Reboot router')
    expect(screen.queryByText('Action completed')).not.toBeInTheDocument()
    expect(await screen.findByRole('button', { name: 'Approve and run' })).toBeEnabled()
    await user.click(screen.getByRole('button', { name: 'Approve and run' }))
    expect(await screen.findByText('Router restarted')).toBeInTheDocument()
    expect(fetcher).toHaveBeenCalledTimes(kind === 'catalog' ? 4 : 3)
  })

  it('retries recorded failure through a new proposal and new write approval', async () => {
    const failed = { ...execution, status: 'failed', message: 'Device unreachable' }
    const fetcher = setupFetch(Promise.resolve(json(proposal)))
    fetcher.mockImplementation(async (url) => {
      if (String(url).endsWith('/p1/confirm')) return json(failed)
      if (String(url).endsWith('/p2/confirm')) return json({ ...execution, id: 'p2', correlation_id: 'c2' })
      return json({ ...proposal, id: 'p2', confirmation_id: 'c2' })
    })
    const user = userEvent.setup()
    render(view())
    await prepare(user)
    await user.click(await screen.findByRole('button', { name: 'Approve and run' }))
    expect(await screen.findByText('Device unreachable')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Approve and run' })).not.toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Retry with new proposal' }))
    expect(await screen.findByRole('button', { name: 'Approve and run' })).toBeEnabled()
    expect(screen.getByText('Device unreachable')).toBeInTheDocument()
    expect(fetcher.mock.calls.filter(([url]) => String(url).endsWith('/p1/confirm'))).toHaveLength(1)
    expect(fetcher.mock.calls.some(([url]) => String(url).endsWith('/p2/confirm'))).toBe(false)
    await user.click(screen.getByRole('button', { name: 'Approve and run' }))
    expect(await screen.findByText('Router restarted')).toBeInTheDocument()
    expect(fetcher).toHaveBeenLastCalledWith('/tickets/t1/tools/p2/confirm', expect.objectContaining({ body: JSON.stringify({ confirmation_id: 'c2' }) }))
    expect(screen.getByText('Device unreachable')).toBeInTheDocument()
  })

  it.each(['succeeded', 'failed'])('renders read-only %s from propose without approval or confirm', async (status) => {
    const readOnly = { ...proposal, tool_name: 'get_device_status', kind: 'read_only', requires_confirmation: false, status, summary: 'Device check result' }
    const fetcher = vi.fn()
    if (kind === 'catalog') fetcher.mockResolvedValueOnce(json([tool('get_device_status', 'Check device', 'read_only', false)]))
    fetcher.mockResolvedValueOnce(json(readOnly))
      .mockResolvedValueOnce(json({ ...readOnly, id: 'p2', confirmation_id: 'c2', status: 'succeeded', summary: 'New device check result' }))
    vi.stubGlobal('fetch', fetcher)
    const progress = vi.fn()
    const user = userEvent.setup()
    render(view('t1', vi.fn(), progress))
    await prepare(user)
    expect(await screen.findByText('Device check result')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Review and approve' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Run check' })).not.toBeInTheDocument()
    expect(progress).toHaveBeenLastCalledWith(expect.objectContaining({ state: status === 'succeeded' ? 'complete' : 'blocked' }), expect.objectContaining({ id: 'p1', status, message: 'Device check result' }))
    if (status === 'failed') {
      await user.click(screen.getByRole('button', { name: 'Retry with new proposal' }))
      expect(await screen.findByText('New device check result')).toBeInTheDocument()
      expect(screen.getByText('Device check result')).toBeInTheDocument()
    }
    expect(fetcher.mock.calls.some(([url]) => String(url).includes('/confirm'))).toBe(false)
  })

  it('ignores late proposal after ticket switch', async () => {
    const pending = deferred()
    setupFetch(pending.promise)
    const user = userEvent.setup()
    const progress = vi.fn()
    const { rerender } = render(view('t1', vi.fn(), progress))
    await prepare(user)
    rerender(view('t2', vi.fn(), progress))
    progress.mockClear()
    await act(async () => pending.resolve(json(proposal)))
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
    expect(progress).not.toHaveBeenCalled()
  })

  if (kind === 'catalog') it('discards a proposal and permits changing action without confirmation', async () => {
    const scroll = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'scrollIntoView')
    Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', { configurable: true, value: vi.fn() })
    try {
    const fetcher = vi.fn().mockResolvedValueOnce(json([
      tool('reboot_router', 'Reboot router', 'stateful', true),
      tool('get_device_status', 'Check device', 'read_only', false),
    ])).mockResolvedValueOnce(json(proposal))
    vi.stubGlobal('fetch', fetcher)
    const user = userEvent.setup()
    render(view())
    await prepare(user)
    await user.click(await screen.findByRole('button', { name: 'Discard proposal' }))
    expect(screen.queryByRole('article')).not.toBeInTheDocument()
    const action = screen.getByRole('combobox', { name: 'Action' })
    expect(action).toBeEnabled()
    action.focus()
    await user.keyboard('{ArrowDown}')
    await user.click(await screen.findByRole('option', { name: 'Check device' }))
    expect(action).toHaveTextContent('Check device')
    expect(fetcher).toHaveBeenCalledTimes(2)
    } finally {
      if (scroll) Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', scroll)
      else Reflect.deleteProperty(HTMLElement.prototype, 'scrollIntoView')
    }
  })

  if (kind === 'catalog') it('resets the pending approval when the action state changes', async () => {
    const scrollIntoView = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'scrollIntoView')
    const pointerCapture = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'hasPointerCapture')
    Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', { configurable: true, value: vi.fn() })
    Object.defineProperty(HTMLElement.prototype, 'hasPointerCapture', { configurable: true, value: vi.fn(() => false) })
    const fetcher = vi.fn()
      .mockResolvedValueOnce(json([tool('reboot_router', 'Reboot router', 'stateful', true), tool('update_config', 'Update configuration', 'stateful', true)]))
      .mockResolvedValueOnce(json(proposal))
      .mockResolvedValueOnce(json({ ...proposal, id: 'p2', tool_name: 'update_config', summary: 'Update configuration', confirmation_id: 'c2' }))
    vi.stubGlobal('fetch', fetcher)
    const user = userEvent.setup()
    render(view())
    await prepare(user)
    await user.click(await screen.findByRole('button', { name: 'Discard proposal' }))
    const action = screen.getByRole('combobox', { name: 'Action' })
    await user.click(action)
    await user.click(await screen.findByRole('option', { name: 'Update configuration' }))
    await user.click(await screen.findByRole('button', { name: 'Prepare proposal' }))
    expect(screen.getByRole('article', { name: 'Proposed action update_config' })).toBeInTheDocument()
    expect(fetcher).toHaveBeenCalledTimes(3)
    if (scrollIntoView) Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', scrollIntoView)
    else Reflect.deleteProperty(HTMLElement.prototype, 'scrollIntoView')
    if (pointerCapture) Object.defineProperty(HTMLElement.prototype, 'hasPointerCapture', pointerCapture)
    else Reflect.deleteProperty(HTMLElement.prototype, 'hasPointerCapture')
  })

  it('ignores late execution after ticket switch', async () => {
    const pending = deferred()
    setupFetch(Promise.resolve(json(proposal))).mockReturnValueOnce(pending.promise)
    const user = userEvent.setup()
    const progress = vi.fn()
    const { rerender } = render(view('t1', vi.fn(), progress))
    await prepare(user)
    await user.click(await screen.findByRole('button', { name: 'Approve and run' }))
    rerender(view('t2', vi.fn(), progress))
    progress.mockClear()
    await act(async () => pending.resolve(json(execution)))
    expect(screen.queryByText('Router restarted')).not.toBeInTheDocument()
    expect(progress).not.toHaveBeenCalled()
  })
})
