import { CheckCircle, Clock, MagnifyingGlass, WarningCircle, XCircle, Wrench } from '@phosphor-icons/react'

export type OperationStatus = 'queued' | 'searching' | 'running' | 'needs-approval' | 'completed' | 'no-evidence' | 'failed' | 'unknown' | 'rejected'
export const operationLabels: Record<OperationStatus, string> = {
  queued: 'Queued', searching: 'Checking evidence', running: 'Running', 'needs-approval': 'Needs approval',
  completed: 'Completed', 'no-evidence': 'No matching evidence', failed: 'Failed', unknown: 'Outcome not confirmed', rejected: 'Not approved',
}
export function OperationStatusLabel({ status }: { status: OperationStatus }) {
  const Icon = status === 'completed' ? CheckCircle : status === 'failed' || status === 'unknown' ? WarningCircle : status === 'rejected' ? XCircle : status === 'searching' ? MagnifyingGlass : status === 'running' ? Wrench : Clock
  return <span className={`operation-status operation-status--${status}`}><Icon size={18} aria-hidden="true" />{operationLabels[status]}</span>
}
