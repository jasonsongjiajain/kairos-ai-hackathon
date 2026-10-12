import type { ReactNode } from 'react'
import { OperationStatusLabel, type OperationStatus } from './status'

export function ToolCall({ title, status, target, correlationId, children }: { title: string; status: OperationStatus; target?: ReactNode; correlationId?: string; children?: ReactNode }) {
  return <section className="tool-call-shell" aria-label={title}>
    <header className="tool-call-header"><strong>{title}</strong><OperationStatusLabel status={status} /></header>
    {target && <div className="tool-call-target">{target}</div>}
    {children}
    {correlationId && <p className="tool-call-correlation">Reference: {correlationId}</p>}
  </section>
}
