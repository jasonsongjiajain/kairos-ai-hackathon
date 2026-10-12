import type { TopologyNode, TopologyEdge } from '../../lib/api/topology'
import type { EntityFact } from '../../lib/api/tickets'
import { EntityFactsPanel } from '../work/EntityFactsPanel'

export function TopologyInspector({ node, edges, facts, onClose, onPointerEnter, onPointerLeave }: { node: TopologyNode; edges: TopologyEdge[]; facts: EntityFact[]; onClose?: () => void; onPointerEnter?: () => void; onPointerLeave?: () => void }) {
  const status = node.status.charAt(0).toUpperCase() + node.status.slice(1).replace(/_/g, ' ')
  const deviceFacts = facts.filter((fact) => fact.entity_type === 'device' && fact.entity_id === node.device_id && !fact.is_sensitive)
  const services = [...new Set([node.service_ref, ...edges.filter((edge) => edge.source_device_id === node.device_id || edge.target_device_id === node.device_id).map((edge) => edge.service_ref)].filter(Boolean))]
  return <aside className="topology-inspector" aria-label="Device details" onPointerEnter={onPointerEnter} onPointerLeave={onPointerLeave}>
    {onClose && <button type="button" className="network-inspector-close" aria-label="Close device details" onClick={onClose}>×</button>}
    <p className="section-label">Selected device</p><h4>{node.name}</h4>
    <dl className="data-list"><div className="data-row"><dt>Reference</dt><dd>{node.device_ref}</dd></div><div className="data-row"><dt>Type</dt><dd>{node.device_type}</dd></div><div className="data-row"><dt>Status</dt><dd>{status}</dd></div><div className="data-row"><dt>Connected services</dt><dd>{services.join(', ') || 'Not recorded'}</dd></div></dl>
    {[...new Set(deviceFacts.map((fact) => fact.group_key))].map((group) => <EntityFactsPanel key={group} facts={deviceFacts} groupKey={group} />)}
  </aside>
}
