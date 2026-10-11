import type { TopologyEdge, TopologyNode } from '../../lib/api/topology'
import { Badge } from '../../components/ui/badge'

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
      return 'UNKNOWN'
  }
}

type TopologyPathProps = {
  nodes: TopologyNode[]
  edges: TopologyEdge[]
  serviceRef: string | null
}

export function TopologyPath({ nodes, edges, serviceRef }: TopologyPathProps) {
  if (nodes.length === 0) {
    return (
      <div className="state-panel">
        <p>No topology is recorded for this service path.</p>
      </div>
    )
  }

  const edgeByTarget = new Map(edges.map((edge) => [edge.target_device_id, edge]))
  const pathText = `Service path: ${nodes
    .map((node) => `${node.name} (${deviceStatusLabel(node.status)})`)
    .join(', then ')}.${serviceRef ? ` Carried over ${serviceRef}.` : ''}`

  return (
    <figure className="topology-figure">
      <div className="topology-diagram" aria-hidden="true">
        <ol className="topology-nodes">
          {nodes.map((node, index) => {
            const edge = edgeByTarget.get(node.device_id)
            return (
              <li className={`topology-node is-${modifier(node.status)}`} key={node.device_id}>
                {index > 0 && (
                  <span className="topology-connector">
                    {edge?.service_ref ? `via ${edge.service_ref}` : 'linked'}
                  </span>
                )}
                <span className="topology-marker">{statusMarker(node.status)}</span>
                <span className="topology-node-name">{node.name}</span>
                <span className="topology-node-meta">
                  {node.device_type} <span className="tabular">{node.device_ref}</span>
                </span>
                <Badge className={`status-pill status-${modifier(node.status)}`}>
                  {deviceStatusLabel(node.status)}
                </Badge>
              </li>
            )
          })}
        </ol>
      </div>
      <figcaption className="sr-only">{pathText}</figcaption>
    </figure>
  )
}
