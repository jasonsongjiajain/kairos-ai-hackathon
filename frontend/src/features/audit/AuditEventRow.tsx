import type { AuditEvent } from '../../lib/api/audit'
import { OperationStatusLabel } from '../../components/ai/status'
export function AuditEventStatus({ event }: { event: AuditEvent }) {
  if (event.event_type === 'tool_proposed') return <OperationStatusLabel status="needs-approval" />
  if (event.event_type !== 'tool_executed') return null
  return <OperationStatusLabel status={event.details.outcome === 'succeeded' ? 'completed' : event.details.outcome === 'failed' ? 'failed' : 'unknown'} />
}
