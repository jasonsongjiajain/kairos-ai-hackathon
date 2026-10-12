import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { AgentCapabilityPanel } from './AgentCapabilityPanel'

const CATALOG = [
  { name: 'get_device_status', title: 'Read device status', description: 'Read the current simulated status of a customer device.', kind: 'read_only', category: 'diagnostics', risk: 'low', requires_confirmation: false, target_device_types: null },
  { name: 'reboot_router', title: 'Reboot home router', description: 'Simulate a reboot of the customer home router.', kind: 'stateful', category: 'diagnostics', risk: 'medium', requires_confirmation: true, target_device_types: ['router'] },
]
const json = (body: unknown) => new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json' } })
afterEach(() => vi.unstubAllGlobals())

describe('AgentCapabilityPanel', () => {
  it('lists the permitted actions with their descriptions from the catalog', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => json(CATALOG)))
    render(<AgentCapabilityPanel ticketId="t1" token="token" />)

    expect(await screen.findByText('Device action agent')).toBeInTheDocument()
    expect(screen.getByText('Read the current simulated status of a customer device.')).toBeInTheDocument()
    expect(screen.getByText('Simulate a reboot of the customer home router.')).toBeInTheDocument()
    expect(fetch).toHaveBeenCalledWith('/tickets/t1/tools/catalog', expect.objectContaining({ headers: { Authorization: 'Bearer token' } }))
  })

  it('expands a tool to reveal its schema, including the confirmation requirement', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => json(CATALOG)))
    const user = userEvent.setup()
    render(<AgentCapabilityPanel ticketId="t1" token="token" />)

    await user.click(await screen.findByRole('button', { name: 'Simulate a reboot of the customer home router.' }))
    const panel = screen.getByRole('region', { name: 'What the assistant can do here' })
    expect(panel).toHaveTextContent('stateful')
    expect(panel).toHaveTextContent('requires_confirmation')
    expect(panel).toHaveTextContent('true')
  })

  it('shows an empty state when the role has no available actions', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => json([])))
    render(<AgentCapabilityPanel ticketId="t1" token="token" />)
    expect(await screen.findByText('No device actions are available for your role on this ticket.')).toBeInTheDocument()
  })

  it('shows an error state that can retry', async () => {
    const fetcher = vi.fn()
      .mockResolvedValueOnce(new Response('nope', { status: 500 }))
      .mockResolvedValueOnce(json(CATALOG))
    vi.stubGlobal('fetch', fetcher)
    const user = userEvent.setup()
    render(<AgentCapabilityPanel ticketId="t1" token="token" />)

    expect(await screen.findByRole('alert')).toHaveTextContent('The action catalog could not be loaded.')
    await user.click(screen.getByRole('button', { name: 'Retry loading actions' }))
    expect(await screen.findByText('Device action agent')).toBeInTheDocument()
  })
})
