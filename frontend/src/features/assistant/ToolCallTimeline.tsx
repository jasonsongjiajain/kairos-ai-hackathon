import type { ReactNode } from 'react'
export function ToolCallTimeline({ children }: { children: ReactNode }) {
  return <div className="tool-call-timeline" aria-label="Tool-call timeline">{children}</div>
}
