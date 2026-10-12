import { render, screen, within } from '@testing-library/react'
import { useState } from 'react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { TopologyPath } from './TopologyPath'

const NODES = [
  { device_id: 'device-olt', device_ref: 'DEMO-OLT-001', device_type: 'OLT', name: 'Demo access node', status: 'online', service_id: 'service-granite', service_ref: 'DEMO-GR-001' },
  { device_id: 'device-onu', device_ref: 'DEMO-ONT-001', device_type: 'ONU', name: 'Demo optical network unit', status: 'offline', service_id: 'service-granite', service_ref: 'DEMO-GR-001' },
  { device_id: 'device-router', device_ref: 'DEMO-RTR-001', device_type: 'router', name: 'Demo home router', status: 'unreachable', service_id: 'service-hsi', service_ref: 'DEMO-HSI-001' },
]

const EDGES = [
  { source_device_id: 'device-olt', target_device_id: 'device-onu', service_id: 'service-granite', service_ref: 'DEMO-GR-001' },
  { source_device_id: 'device-onu', target_device_id: 'device-router', service_id: 'service-hsi', service_ref: 'DEMO-HSI-001' },
]

describe('TopologyPath', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('selects devices from the keyboard-operable device list and keeps focus on rerender', async () => {
    const user = userEvent.setup()
    const onSelectDevice = vi.fn()
    const props = { nodes: NODES, edges: EDGES, serviceRef: null, onSelectDevice }
    const { rerender } = render(<TopologyPath {...props} />)
    const list = screen.getByRole('list', { name: 'Devices' })
    const buttons = within(list).getAllByRole('button')
    expect(buttons).toHaveLength(3)

    await user.click(screen.getByRole('button', { name: 'Pause packets' }))
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
    expect(within(list).getAllByRole('button').map((button) => button === buttons[1])).toEqual([false, true, false])
    expect(buttons[1]).toHaveFocus()
  })

  it('shows and clears a selection that is not represented in the service path', async () => {
    function SelectionHarness() {
      const [selectedDeviceId, setSelectedDeviceId] = useState<string | undefined>('device-from-action')
      return <TopologyPath nodes={NODES} edges={EDGES} serviceRef={null} selectedDeviceId={selectedDeviceId}
        onSelectDevice={setSelectedDeviceId} onClearSelection={() => setSelectedDeviceId(undefined)} />
    }

    const user = userEvent.setup()
    render(<SelectionHarness />)
    expect(screen.getByRole('status')).toHaveTextContent('The selected device is not present in this service path.')
    await user.click(screen.getByRole('button', { name: 'Clear device selection' }))
    expect(screen.queryByRole('status')).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: /Demo optical network unit/ }))
    expect(screen.queryByText('The selected device is not present in this service path.')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Demo optical network unit/ })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('heading', { name: 'Demo optical network unit' })).toBeInTheDocument()
  })

  it('shows the inspector prompt until a device is selected', () => {
    render(<TopologyPath nodes={NODES} edges={EDGES} serviceRef={null} selectedDeviceId="device-router" />)
    expect(screen.getByRole('heading', { name: 'Demo home router' })).toBeInTheDocument()
    expect(screen.getByText('Unreachable', { selector: 'dd' })).toBeInTheDocument()
  })

  it('renders status labels for each device and a read-only list without handlers', () => {
    render(<TopologyPath nodes={NODES} edges={EDGES} serviceRef="DEMO-GR-001" />)

    const list = screen.getByRole('list', { name: 'Devices' })
    expect(within(list).getAllByRole('listitem')).toHaveLength(3)
    expect(within(list).queryByRole('button')).not.toBeInTheDocument()
    expect(within(list).getByText('Online')).toBeInTheDocument()
    expect(within(list).getByText('Offline')).toBeInTheDocument()
    expect(within(list).getByText('Unreachable')).toBeInTheDocument()
  })

  it('uses the device-type icon class for each equipment type', () => {
    const clients = [
      { device_id: 'd-rtr', device_ref: 'R1', device_type: 'router', name: 'Home router', status: 'online', service_id: null, service_ref: null },
      { device_id: 'd-ph', device_ref: 'P1', device_type: 'phone', name: 'Counter phone', status: 'online', service_id: null, service_ref: null },
      { device_id: 'd-tv', device_ref: 'T1', device_type: 'tv', name: 'Living room TV', status: 'online', service_id: null, service_ref: null },
      { device_id: 'd-lt', device_ref: 'L1', device_type: 'laptop', name: 'Work laptop', status: 'online', service_id: null, service_ref: null },
    ]
    render(<TopologyPath nodes={clients} edges={[]} serviceRef={null} />)

    const kinds = screen.getAllByRole('listitem').map((item) => item.textContent)
    expect(kinds[0]).toContain('Router')
    expect(kinds[1]).toContain('Phone')
    expect(kinds[2]).toContain('TV')
    expect(kinds[3]).toContain('Laptop')
    expect(within(screen.getByRole('list', { name: 'Devices' })).getByText('Counter phone')).toBeInTheDocument()
  })

  it('renders an unrecognized vendor status as readable text', () => {
    render(<TopologyPath nodes={[{ ...NODES[0], status: 'maintenance_window' }]} edges={[]} serviceRef={null} />)
    expect(screen.getByRole('list', { name: 'Devices' })).toHaveTextContent('maintenance window')
  })

  it('lists only real connections, including nonadjacent ones, and says so when none exist', () => {
    const { rerender } = render(<TopologyPath nodes={NODES} edges={[
      { ...EDGES[0], target_device_id: 'device-router' },
    ]} serviceRef={null} />)
    expect(screen.getByText('Demo access node → Demo home router via DEMO-GR-001')).toBeInTheDocument()
    expect(screen.queryByText(/Demo optical network unit →/)).not.toBeInTheDocument()
    rerender(<TopologyPath nodes={NODES} edges={[]} serviceRef={null} />)
    expect(screen.getByText('No connections are recorded.')).toBeInTheDocument()
  })

  it('shows an empty state when no topology is recorded', () => {
    render(<TopologyPath nodes={[]} edges={[]} serviceRef={null} />)
    expect(screen.getByText('No topology is recorded for this service path.')).toBeInTheDocument()
  })
})
