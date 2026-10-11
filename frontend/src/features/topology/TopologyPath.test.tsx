import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
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
  it('renders status labels next to each node', () => {
    render(<TopologyPath nodes={NODES} edges={EDGES} serviceRef="DEMO-GR-001" />)

    expect(screen.getByText('Demo access node')).toBeInTheDocument()
    expect(screen.getByText('Demo optical network unit')).toBeInTheDocument()
    expect(screen.getByText('Demo home router')).toBeInTheDocument()
    expect(screen.getByText('Online')).toBeInTheDocument()
    expect(screen.getByText('Offline')).toBeInTheDocument()
    expect(screen.getByText('Unreachable')).toBeInTheDocument()
  })

  it('provides a text alternative describing the order and state of the path', () => {
    render(<TopologyPath nodes={NODES} edges={EDGES} serviceRef="DEMO-GR-001" />)

    expect(
      screen.getByText(
        'Service path: Demo access node (Online), then Demo optical network unit (Offline), then Demo home router (Unreachable). Carried over DEMO-GR-001.',
      ),
    ).toBeInTheDocument()
  })

  it('shows an empty state when no topology is recorded', () => {
    render(<TopologyPath nodes={[]} edges={[]} serviceRef={null} />)

    expect(screen.getByText('No topology is recorded for this service path.')).toBeInTheDocument()
  })
})
