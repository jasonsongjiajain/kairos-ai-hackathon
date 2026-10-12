import { useEffect, type ReactNode } from 'react'
import { motion, useAnimationControls, useReducedMotion } from 'framer-motion'
import type { TopologyEdge, TopologyNode } from '../../lib/api/topology'
import { Badge } from '../../components/ui/badge'
import { motionDuration, prefersReducedMotion, transitionFor } from '../../lib/motion'

function PathItem({ children, className, delay, emphasis, reducedMotion }: {
  children: ReactNode
  className: string
  delay: number
  emphasis?: string
  reducedMotion: boolean
}) {
  const emphasisControls = useAnimationControls()
  useEffect(() => {
    if (reducedMotion || !emphasis) {
      emphasisControls.stop()
      emphasisControls.set({ boxShadow: 'inset 0 0 0 0px #181818' })
      return
    }
    void emphasisControls.start({
      boxShadow: ['inset 0 0 0 0px #181818', 'inset 0 0 0 3px #181818', 'inset 0 0 0 0px #181818'],
      transition: transitionFor(false, motionDuration.sequence),
    })
    return () => emphasisControls.stop()
  }, [emphasis, reducedMotion, emphasisControls])

  return (
    <motion.li className={className}
      initial={{ opacity: reducedMotion ? 1 : 0 }}
      animate={{ opacity: 1 }}
      transition={{ ...transitionFor(reducedMotion), delay: reducedMotion ? 0 : delay }}
    >
      <motion.div className="topology-item-content" animate={emphasisControls}>{children}</motion.div>
    </motion.li>
  )
}

function modifier(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-')
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

function statusMarker(status: string): string {
  switch (status.toLowerCase()) {
    case 'online':
      return 'OK'
    case 'offline':
      return 'DOWN'
    case 'unreachable':
      return 'NO LINK'
    case 'degraded':
      return 'DEGRADED'
    default:
      return 'STATUS'
  }
}

type TopologyPathProps = {
  nodes: TopologyNode[]
  edges: TopologyEdge[]
  serviceRef: string | null
  selectedDeviceId?: string
  onSelectDevice?: (id: string) => void
  onClearSelection?: () => void
}

export function TopologyPath({ nodes, edges, serviceRef, selectedDeviceId, onSelectDevice, onClearSelection }: TopologyPathProps) {
  const motionPreference = useReducedMotion()
  const reducedMotion = Boolean(motionPreference) || prefersReducedMotion()
  if (nodes.length === 0) {
    return (
      <div className="state-panel">
        <p>No topology is recorded for this service path.</p>
      </div>
    )
  }

  const nodeById = new Map(nodes.map((node) => [node.device_id, node]))
  const selectedDeviceIsInPath = nodes.some((node) => node.device_id === selectedDeviceId)
  const nodeOrder = new Map(nodes.map((node, index) => [node.device_id, index]))
  const revealDelay = (position: number) => Math.max(position, 0) / (nodes.length * 2) * motionDuration.sequence
  const pathText = `Service path: ${nodes
    .map((node) => `${node.name} (${deviceStatusLabel(node.status)})`)
    .join(', ')}.${serviceRef ? ` Carried over ${serviceRef}.` : ''}`

  return (
    <figure className="topology-figure">
      {selectedDeviceId && !selectedDeviceIsInPath && (
        <div className="topology-selection-notice" role="status">
          <p>The selected device is not present in this service path.</p>
          {onClearSelection && <button type="button" className="inline-link" onClick={onClearSelection}>Clear device selection</button>}
        </div>
      )}
      <div className="topology-diagram">
        <ol className="topology-nodes" aria-label="Devices">
          {nodes.map((node, index) => {
            const selected = selectedDeviceId === node.device_id
            const content = <>
                <span className="topology-marker" aria-hidden="true">{statusMarker(node.status)}</span>
                <span className="topology-node-name">{node.name}</span>
                <span className="topology-node-meta">
                  {node.device_type} <span className="tabular">{node.device_ref}</span>
                </span>
                <Badge className={`status-pill status-${modifier(node.status)}`}>
                  {deviceStatusLabel(node.status)}
                </Badge>
              </>
            return (
              <PathItem className={`topology-node is-${modifier(node.status)}${selected ? ' is-selected' : ''}`}
                key={node.device_id} delay={revealDelay(index * 2)} reducedMotion={reducedMotion}
                emphasis={selected ? selectedDeviceId : undefined}>
                {onSelectDevice ? <button type="button" className="topology-select"
                  aria-pressed={selected} onClick={() => onSelectDevice(node.device_id)}>
                  {content}
                </button> : <div className="topology-static">{content}</div>}
              </PathItem>
            )
          })}
        </ol>
        {edges.length ? <ul aria-label="Connections" className="topology-connections">
          {edges.map((edge) => (
            <PathItem className="topology-connector" key={JSON.stringify([edge.source_device_id, edge.target_device_id, edge.service_id])}
              delay={revealDelay(Math.max(nodeOrder.get(edge.source_device_id) ?? 0, nodeOrder.get(edge.target_device_id) ?? 0) * 2 - 1)}
              reducedMotion={reducedMotion}
              emphasis={selectedDeviceId === edge.source_device_id || selectedDeviceId === edge.target_device_id ? selectedDeviceId : undefined}>
              <span className="topology-connection-line" aria-hidden="true" />
              <span className="topology-connection-label">
                {`${nodeById.get(edge.source_device_id)?.name ?? edge.source_device_id} → ${nodeById.get(edge.target_device_id)?.name ?? edge.target_device_id}${edge.service_ref ? ` via ${edge.service_ref}` : ''}`}
              </span>
            </PathItem>
          ))}
        </ul> : <p className="muted-note">No connections are recorded.</p>}
      </div>
      <figcaption className="sr-only">{pathText}</figcaption>
    </figure>
  )
}
