import { useEffect, useMemo, useRef, useState, type ComponentType } from 'react'
import {
  ReactFlow,
  Handle, Position, Controls, useReactFlow, useStore,
  type Edge,
  type Node as FlowNode,
  type NodeProps,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import {
  Camera,
  Circuitry,
  Desktop,
  DeviceMobile,
  DeviceTablet,
  GameController,
  HardDrives,
  Laptop,
  Printer,
  SpeakerHigh,
  Television,
  WifiHigh,
  Globe,
  type IconProps,
} from '@phosphor-icons/react'
import type { TopologyEdge, TopologyNode } from '../../lib/api/topology'
import type { EntityFact } from '../../lib/api/tickets'
import { TopologyInspector } from './TopologyInspector'
import { PacketEdge } from './PacketEdge'
import type { IncidentStage } from '../work/IncidentTrace'
import { useReducedMotion } from 'framer-motion'

type IconComponent = ComponentType<IconProps>

function deviceIcon(deviceType: string): IconComponent {
  switch (deviceType.trim().toLowerCase()) {
    case 'internet':
      return Globe
    case 'router':
    case 'ap':
    case 'access point':
    case 'mesh':
    case 'extender':
    case 'gateway':
      return WifiHigh
    case 'olt':
    case 'switch':
      return HardDrives
    case 'onu':
    case 'ont':
      return Globe
    case 'phone':
    case 'mobile':
    case 'smartphone':
      return DeviceMobile
    case 'laptop':
      return Laptop
    case 'desktop':
    case 'computer':
    case 'pc':
      return Desktop
    case 'tablet':
      return DeviceTablet
    case 'tv':
    case 'television':
    case 'iptv':
    case 'streaming':
      return Television
    case 'camera':
    case 'cam':
      return Camera
    case 'speaker':
    case 'smart speaker':
      return SpeakerHigh
    case 'printer':
      return Printer
    case 'console':
    case 'gaming':
    case 'game console':
      return GameController
    default:
      return Circuitry
  }
}

function deviceKindLabel(deviceType: string): string {
  const labels: Record<string, string> = {
    router: 'Router',
    ap: 'Access point',
    'access point': 'Access point',
    mesh: 'Mesh node',
    extender: 'Extender',
    gateway: 'Gateway',
    olt: 'OLT',
    internet: 'Internet',
    onu: 'Internet',
    ont: 'Internet',
    switch: 'Switch',
    phone: 'Phone',
    mobile: 'Phone',
    smartphone: 'Phone',
    laptop: 'Laptop',
    desktop: 'Desktop',
    computer: 'Computer',
    pc: 'Computer',
    tablet: 'Tablet',
    tv: 'TV',
    television: 'TV',
    iptv: 'IPTV box',
    camera: 'Camera',
    speaker: 'Speaker',
    printer: 'Printer',
    console: 'Console',
    gaming: 'Console',
  }
  return labels[deviceType.trim().toLowerCase()] ?? deviceType.replace(/_/g, ' ')
}

function deviceStatusLabel(status: string): string {
  switch (status.toLowerCase()) {
    case 'online':
      return 'Online'
    case 'offline':
      return 'Offline'
    case 'unreachable':
      return 'Unreachable'
    case 'degraded':
      return 'Degraded'
    case 'unknown':
      return 'Unknown'
    default:
      return status.replace(/_/g, ' ')
  }
}

function statusTone(status: string): 'ok' | 'warn' | 'down' {
  const normalized = status.trim().toLowerCase()
  if (normalized === 'offline' || normalized === 'unreachable') return 'down'
  if (normalized === 'online') return 'ok'
  return 'warn'
}

function isBrokenStatus(status: string): boolean {
  return statusTone(status) === 'down'
}

// Relation-driven layout: BFS depth from the head of the path gives the column,
// order within the column keeps the recorded sequence. Disconnected devices get their own columns.
function layoutPositions(nodes: TopologyNode[], edges: TopologyEdge[]) {
  const adjacency = new Map<string, string[]>(nodes.map((node) => [node.device_id, []]))
  for (const edge of edges) {
    adjacency.get(edge.source_device_id)?.push(edge.target_device_id)
    adjacency.get(edge.target_device_id)?.push(edge.source_device_id)
  }
  const incoming = new Set(edges.map((edge) => edge.target_device_id))
  const seeds = [...nodes.filter((node) => !incoming.has(node.device_id)), ...nodes]
  const depth = new Map<string, number>()
  let offset = 0
  for (const seed of seeds) {
    if (depth.has(seed.device_id)) continue
    depth.set(seed.device_id, offset)
    const queue = [seed.device_id]
    let furthest = offset
    for (let head = 0; head < queue.length; head += 1) {
      const current = queue[head]
      const currentDepth = depth.get(current) ?? offset
      furthest = Math.max(furthest, currentDepth)
      for (const next of adjacency.get(current) ?? []) {
        if (depth.has(next)) continue
        depth.set(next, currentDepth + 1)
        queue.push(next)
      }
    }
    offset = furthest + 1
  }

  const columns = new Map<number, string[]>()
  for (const node of nodes) {
    const column = depth.get(node.device_id) ?? 0
    columns.set(column, [...(columns.get(column) ?? []), node.device_id])
  }
  const positions = new Map<string, { x: number; y: number }>()
  for (const [column, ids] of columns) {
    ids.forEach((id, row) => {
      const angle = ids.length > 2 ? Math.PI * row / (ids.length - 1) : 0
      positions.set(id, ids.length > 2
        ? { x: Math.cos(angle) * Math.max(280, ids.length * 55), y: column * 190 - 90 + Math.sin(angle) * 180 }
        : { x: (row - (ids.length - 1) / 2) * 210, y: column * 190 })
    })
  }
  return positions
}

type DeviceData = {
  name: string
  deviceRef: string
  deviceType: string
  status: string
  selected: boolean
  active: boolean
  outcome?: 'complete' | 'blocked'
}
type DeviceFlowNode = FlowNode<DeviceData, 'device'>

function DeviceNode({ data }: NodeProps<DeviceFlowNode>) {
  const Icon = deviceIcon(data.deviceType)
  const tone = statusTone(data.status)
  return (
    <div className={`network-device network-device--${tone}${data.selected ? ' is-selected' : ''}${data.active ? ' is-active' : ''}${data.outcome ? ` outcome-${data.outcome}` : ''}`}>
      <Handle type="target" position={Position.Top} />
      <div className="network-device__equipment">
        <span className="network-device__pulse" />
        {data.deviceType.toLowerCase() === 'router' ? <svg width="72" height="68" viewBox="0 0 72 68" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <rect x="9" y="39" width="54" height="18" rx="4" /><path d="M16 39V18a2 2 0 0 1 4 0v21M52 39V18a2 2 0 0 1 4 0v21M17 49h3m5 0h5M15 62h7m28 0h7M28 24a12 12 0 0 1 16 0m-12 5a6 6 0 0 1 8 0" /><circle cx="36" cy="34" r="1" />
        </svg> : <Icon size={58} weight="regular" aria-hidden="true" />}
      </div>
      <strong>{data.name}</strong>
      <span className="network-device__state">{deviceStatusLabel(data.status)}</span>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

function FitCanvas() {
  const { fitView } = useReactFlow()
  const width = useStore((state) => state.width)
  const height = useStore((state) => state.height)
  useEffect(() => {
    if (width && height) void fitView({ padding: 0.25, duration: 0 })
  }, [width, height, fitView])
  return null
}

const nodeTypes = { device: DeviceNode }
const edgeTypes = { packet: PacketEdge }

type TopologyPathProps = {
  nodes: TopologyNode[]
  edges: TopologyEdge[]
  serviceRef: string | null
  facts?: EntityFact[]
  selectedDeviceId?: string
  onSelectDevice?: (id: string) => void
  onClearSelection?: () => void
  actionStage?: IncidentStage
  actionDeviceId?: string
}

export function TopologyPath({ nodes, edges, serviceRef, facts = [], selectedDeviceId, onSelectDevice, onClearSelection, actionStage, actionDeviceId }: TopologyPathProps) {
  const reducedMotion = Boolean(useReducedMotion())
  const [hoveredDeviceId, setHoveredDeviceId] = useState<string>()
  const [paused, setPaused] = useState(false)
  const hoverTimer = useRef<ReturnType<typeof setTimeout>>()
  useEffect(() => () => clearTimeout(hoverTimer.current), [])
  const inspect = (id: string) => { clearTimeout(hoverTimer.current); setHoveredDeviceId(id) }
  const leave = () => { hoverTimer.current = setTimeout(() => setHoveredDeviceId(undefined), 180) }
  // The HTTP execution contract has no start acknowledgement; request latency is not running telemetry.
  const actionRunning = false
  const inspectedId = hoveredDeviceId ?? selectedDeviceId
  const nodeById = useMemo(() => new Map(nodes.map((node) => [node.device_id, node])), [nodes])
  const drawableEdges = useMemo(
    () => edges.filter((edge) => nodeById.has(edge.source_device_id) && nodeById.has(edge.target_device_id)),
    [edges, nodeById],
  )

  const flowNodes = useMemo<DeviceFlowNode[]>(() => {
    const positions = layoutPositions(nodes, drawableEdges)
    return nodes.map((node) => ({
      id: node.device_id,
      type: 'device',
      position: positions.get(node.device_id) ?? { x: 0, y: 0 },
      data: {
        name: node.name,
        deviceRef: node.device_ref,
        deviceType: node.device_type,
        status: node.status,
        selected: node.device_id === inspectedId,
        active: Boolean(!paused && !reducedMotion && actionRunning && node.device_id === actionDeviceId),
        outcome: node.device_id === actionDeviceId && (actionStage?.state === 'complete' || actionStage?.state === 'blocked') ? actionStage.state : undefined,
      },
      draggable: false,
      selectable: false,
      focusable: false,
    }))
  }, [nodes, drawableEdges, inspectedId, actionRunning, actionDeviceId, actionStage?.state, paused, reducedMotion])

  const flowEdges = useMemo<Edge[]>(() => drawableEdges.map((edge, index) => {
    const source = nodeById.get(edge.source_device_id)
    const target = nodeById.get(edge.target_device_id)
    const broken = isBrokenStatus(source?.status ?? '') || isBrokenStatus(target?.status ?? '')
    const highlighted = selectedDeviceId === edge.source_device_id || selectedDeviceId === edge.target_device_id
    return {
      id: `link-${index}`,
      source: edge.source_device_id,
      target: edge.target_device_id,
      type: 'packet',
      data: { broken, paused: paused || reducedMotion, active: Boolean(actionRunning && (actionDeviceId === edge.source_device_id || actionDeviceId === edge.target_device_id)) },
      label: edge.service_ref ?? undefined,
      animated: false,
      focusable: false,
      style: {
        stroke: broken ? '#9b2828' : highlighted ? '#1559a6' : '#334454',
        strokeWidth: highlighted ? 2.5 : 1.5,
        strokeDasharray: broken ? '6 6' : undefined,
      },
      labelStyle: { fill: '#5c6370', fontSize: 11, fontFamily: 'ui-monospace, SFMono-Regular, monospace' },
      labelBgStyle: { fill: '#ffffff' },
      labelBgPadding: [6, 3],
    }
  }), [drawableEdges, nodeById, selectedDeviceId, reducedMotion, paused, actionRunning, actionDeviceId])

  if (nodes.length === 0) {
    return (
      <div className="state-panel">
        <p>No topology is recorded for this service path.</p>
      </div>
    )
  }

  const selectedNode = nodeById.get(inspectedId ?? '')
  const selectedDeviceIsInPath = nodeById.has(selectedDeviceId ?? '')
  const linkSummary = drawableEdges.map((edge) => {
    const source = nodeById.get(edge.source_device_id)?.name ?? edge.source_device_id
    const target = nodeById.get(edge.target_device_id)?.name ?? edge.target_device_id
    return `${source} → ${target}${edge.service_ref ? ` via ${edge.service_ref}` : ''}`
  })

  return (
    <figure className="topology" onKeyDown={(event) => { if (event.key === 'Escape') { clearTimeout(hoverTimer.current); setHoveredDeviceId(undefined); onClearSelection?.() } }}>
      {selectedDeviceId && !selectedDeviceIsInPath && (
        <div className="topology-selection-notice" role="status">
          <p>The selected device is not present in this service path.</p>
          {onClearSelection && <button type="button" className="inline-link" onClick={onClearSelection}>Clear device selection</button>}
        </div>
      )}

      <div className="topology-layout">
        <div className="topology-graph">
          <div className="network-canvas-heading"><span>Service path</span><span>{serviceRef ?? 'Recorded topology'}</span></div>
          <div className="network-canvas-hint">Hover to inspect · Select to pin · Drag to pan</div>
          <ReactFlow
            nodes={flowNodes}
            edges={flowEdges}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            onNodeMouseEnter={(_, node) => inspect(node.id)}
            onNodeMouseLeave={leave}
            onPaneClick={() => { setHoveredDeviceId(undefined); onClearSelection?.() }}
            onNodeClick={(_, node) => onSelectDevice?.(node.id)}
            fitView
            fitViewOptions={{ padding: 0.3 }}
            minZoom={0.2}
            maxZoom={1.5}
            nodesDraggable={false}
            nodesConnectable={false}
            nodesFocusable={false}
            edgesFocusable={false}
            zoomOnScroll={false}
            proOptions={{ hideAttribution: true }}
          ><FitCanvas /><Controls showInteractive={false} /></ReactFlow>
          {selectedNode && <TopologyInspector node={selectedNode} edges={drawableEdges} facts={facts}
            onPointerEnter={() => clearTimeout(hoverTimer.current)}
            onPointerLeave={leave}
            onClose={() => { setHoveredDeviceId(undefined); onClearSelection?.() }} />}
          <div className="network-canvas-footer">
            <span><i /> Online <i className="is-interrupted" /> Interrupted</span>
            <button type="button" onClick={() => setPaused((value) => !value)} aria-pressed={paused}>{paused ? 'Resume packets' : 'Pause packets'}</button>
          </div>
          <p className="network-simulation-label">Packet animation illustrates recorded links, not live traffic.</p>
        </div>
      </div>
      {actionStage && actionStage.state !== 'upcoming' && <div className={`network-operation network-operation--${actionStage.state}`} role="status">
        <span className="network-operation__indicator" />
        <div><strong>{actionStage.state === 'current' ? 'Device action' : actionStage.state === 'complete' ? 'Action completed' : 'Action needs attention'}</strong><p>{actionStage.detail}</p></div>
        {actionDeviceId && <span>{nodeById.get(actionDeviceId)?.name ?? 'Target outside this path'}</span>}
      </div>}

      <div className="topology-devices">
        <p className="section-label">Devices</p>
        <ol className="topology-device-list" aria-label="Devices">
          {nodes.map((node) => {
            const selected = selectedDeviceId === node.device_id
            const Icon = deviceIcon(node.device_type)
            return (
              <li key={node.device_id} className={`topology-device is-${statusTone(node.status)}`}>
                {(() => {
                  const content = <>
                    <span className="topology-device__icon" aria-hidden="true"><Icon size={20} weight="duotone" /></span>
                    <span className="topology-device__text">
                      <span className="topology-device__name">{node.name}</span>
                      <span className="topology-device__meta">{deviceKindLabel(node.device_type)} · <span className="tabular">{node.device_ref}</span></span>
                    </span>
                    <span className="topology-device__status">{deviceStatusLabel(node.status)}</span>
                  </>
                  return onSelectDevice ? (
                    <button type="button" className="topology-device__button" aria-pressed={selected}
                      onFocus={() => setHoveredDeviceId(node.device_id)} onBlur={() => setHoveredDeviceId(undefined)} onClick={() => onSelectDevice(node.device_id)}>{content}</button>
                  ) : <div className="topology-device__button">{content}</div>
                })()}
              </li>
            )
          })}
        </ol>
      </div>

      {drawableEdges.length > 0 ? (
        <>
          <ul aria-label="Connections" className="sr-only topology-connections">
            {linkSummary.map((summary) => <li key={summary}>{summary}</li>)}
          </ul>

        </>
      ) : (
        <p className="muted-note">No connections are recorded.</p>
      )}
      <figcaption className="sr-only">
        {`Topology: ${nodes.length} devices, ${drawableEdges.length} connections.${serviceRef ? ` Carried over ${serviceRef}.` : ''}`}
      </figcaption>
    </figure>
  )
}
