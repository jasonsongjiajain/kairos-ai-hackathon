import { render, screen, waitFor, within } from '@testing-library/react'
import { useState } from 'react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { TopologyPath } from './TopologyPath'

const NODES = [
  {
    device_id: 'device-olt',
    device_ref: 'DEMO-OLT-001',
    device_type: 'OLT',
    name: 'Demo access node',
    status: 'online',
    service_id: 'service-granite',
    service_ref: 'DEMO-GR-001',
  },
  {
    device_id: 'device-onu',
    device_ref: 'DEMO-ONT-001',
    device_type: 'ONU',
    name: 'Demo optical network unit',
    status: 'offline',
    service_id: 'service-granite',
    service_ref: 'DEMO-GR-001',
  },
  {
    device_id: 'device-router',
    device_ref: 'DEMO-RTR-001',
    device_type: 'router',
    name: 'Demo home router',
    status: 'unreachable',
    service_id: 'service-hsi',
    service_ref: 'DEMO-HSI-001',
  },
]

const EDGES = [
  {
    source_device_id: 'device-olt',
    target_device_id: 'device-onu',
    service_id: 'service-granite',
    service_ref: 'DEMO-GR-001',
  },
  {
    source_device_id: 'device-onu',
    target_device_id: 'device-router',
    service_id: 'service-hsi',
    service_ref: 'DEMO-HSI-001',
  },
]

describe('TopologyPath', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('supports controlled keyboard selection without replacing devices or losing focus', async () => {
    const user = userEvent.setup()
    const onSelectDevice = vi.fn()
    const props = { nodes: NODES, edges: EDGES, serviceRef: null, onSelectDevice }
    const { rerender } = render(<TopologyPath {...props} />)
    const buttons = screen.getAllByRole('button')
    await waitFor(() => screen.getAllByRole('listitem').forEach((item) => {
      expect(item).toHaveStyle({ opacity: '1' })
    }))
    await user.tab()
    expect(buttons[0]).toHaveFocus()
    await user.keyboard('{Enter}')
    expect(onSelectDevice).toHaveBeenLastCalledWith('device-olt')
    expect(buttons[0]).toHaveAttribute('aria-pressed', 'false')
    rerender(<TopologyPath {...props} selectedDeviceId="device-olt" />)
    expect(buttons[0]).toHaveAttribute('aria-pressed', 'true')
    expect(buttons[0]).toHaveFocus()
    await user.tab()
    await user.keyboard(' ')
    expect(onSelectDevice).toHaveBeenLastCalledWith('device-onu')
    rerender(<TopologyPath {...props} selectedDeviceId="device-onu" />)
    screen.getAllByRole('button').forEach((button, index) => expect(button).toBe(buttons[index]))
    expect(buttons[0]).toHaveAttribute('aria-pressed', 'false')
    expect(buttons[1]).toHaveAttribute('aria-pressed', 'true')
    expect(buttons[1]).toHaveFocus()
    screen.getAllByRole('listitem').forEach((item) => expect(item).toHaveStyle({ opacity: '1' }))
  })

  it('shows and clears a selection that is not represented in the real service path', async () => {
    function SelectionHarness() {
      const [selectedDeviceId, setSelectedDeviceId] = useState<string | undefined>('device-from-action')
      return <TopologyPath nodes={NODES} edges={EDGES} serviceRef={null} selectedDeviceId={selectedDeviceId}
        onSelectDevice={setSelectedDeviceId} onClearSelection={() => setSelectedDeviceId(undefined)} />
    }

    const user = userEvent.setup()
    render(<SelectionHarness />)
    expect(screen.getByRole('status')).toHaveTextContent('The selected device is not present in this service path.')
    expect(within(screen.getByRole('list', { name: 'Devices' })).getAllByRole('listitem')).toHaveLength(NODES.length)
    await user.click(screen.getByRole('button', { name: 'Clear device selection' }))
    expect(screen.queryByRole('status')).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: /Demo optical network unit/ }))
    expect(screen.queryByText('The selected device is not present in this service path.')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Demo optical network unit/ })).toHaveAttribute('aria-pressed', 'true')
  })

  it('renders the complete final path immediately with reduced motion, including selection', () => {
    vi.stubGlobal('matchMedia', vi.fn(() => ({
      matches: true, addListener: vi.fn(), removeListener: vi.fn(),
      addEventListener: vi.fn(), removeEventListener: vi.fn(),
    })))
    const props = { nodes: NODES, edges: EDGES, serviceRef: null, onSelectDevice: vi.fn() }
    const { rerender } = render(<TopologyPath {...props} />)
    const items = screen.getAllByRole('listitem')
    expect(items).toHaveLength(5)
    items.forEach((item) => expect(item).toHaveStyle({ opacity: '1' }))
    expect(screen.getByText(/Service path:/)).toHaveTextContent('Demo home router (Unreachable)')
    rerender(<TopologyPath {...props} selectedDeviceId="device-onu" />)
    expect(screen.getAllByRole('button')[1]).toHaveAttribute('aria-pressed', 'true')
    items.forEach((item) => expect(item).toHaveStyle({ opacity: '1' }))
  })
  it('renders status labels next to each node', () => {
    render(<TopologyPath nodes={NODES} edges={EDGES} serviceRef="DEMO-GR-001" />)

    expect(screen.getByText('Demo access node')).toBeInTheDocument()
    expect(screen.getByText('Demo optical network unit')).toBeInTheDocument()
    expect(screen.getByText('Demo home router')).toBeInTheDocument()
    expect(screen.getByText('Online')).toBeInTheDocument()
    expect(screen.getByText('Offline')).toBeInTheDocument()
    expect(screen.getByText('Unreachable')).toBeInTheDocument()
    const nodes = within(screen.getByRole('list', { name: 'Devices' })).getAllByRole('listitem')
    expect(nodes).toHaveLength(3)
    expect(nodes[0]).toHaveTextContent('Demo access node')
    expect(nodes[1]).toHaveTextContent('Demo optical network unit')
    expect(nodes[2]).toHaveTextContent('Demo home router')
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })

  it('uses a neutral marker for an unrecognized vendor status', () => {
    render(<TopologyPath nodes={[{ ...NODES[0], status: 'maintenance_window' }]} edges={[]} serviceRef={null} />)
    const node = screen.getByRole('listitem')
    expect(node).toHaveTextContent('maintenance window')
    expect(node.querySelector('.topology-marker')).toHaveTextContent('STATUS')
    expect(node.querySelector('.topology-marker')).not.toHaveTextContent('UNKNOWN')
  })

  it('provides a text alternative describing the order and state of the path', () => {
    render(<TopologyPath nodes={NODES} edges={EDGES} serviceRef="DEMO-GR-001" />)

    expect(
      screen.getByText(
        'Service path: Demo access node (Online), Demo optical network unit (Offline), Demo home router (Unreachable). Carried over DEMO-GR-001.',
      ),
    ).toBeInTheDocument()
  })

  it('describes only real source and target connections, including nonadjacent edges', () => {
    const { rerender } = render(<TopologyPath nodes={NODES} edges={[
      { ...EDGES[0], target_device_id: 'device-router' },
    ]} serviceRef={null} />)
    expect(screen.getByText('Demo access node → Demo home router via DEMO-GR-001')).toBeInTheDocument()
    expect(screen.queryByText(/Demo optical network unit →/)).not.toBeInTheDocument()
    rerender(<TopologyPath nodes={NODES} edges={[]} serviceRef={null} />)
    expect(screen.queryByText(/→|linked|, then /)).not.toBeInTheDocument()
    expect(screen.getByText('No connections are recorded.')).toBeInTheDocument()
  })

  it('shows an empty state when no topology is recorded', () => {
    render(<TopologyPath nodes={[]} edges={[]} serviceRef={null} />)

    expect(screen.getByText('No topology is recorded for this service path.')).toBeInTheDocument()
  })
})
