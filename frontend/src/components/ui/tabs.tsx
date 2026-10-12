import { useId, useRef, type ReactNode } from 'react'

export type WorkspaceTab = { id: string; label: string; content: ReactNode }
export function Tabs({ tabs, value, onValueChange, label }: { tabs: WorkspaceTab[]; value: string; onValueChange: (id: string) => void; label: string }) {
  const prefix = useId()
  const buttons = useRef<(HTMLButtonElement | null)[]>([])
  return <div className="workspace-tabs">
    <div className="workspace-tablist" role="tablist" aria-label={label}>
      {tabs.map((tab, index) => <button key={tab.id} ref={(node) => { buttons.current[index] = node }} type="button" role="tab"
        id={`${prefix}-tab-${tab.id}`} aria-controls={`${prefix}-panel-${tab.id}`} aria-selected={value === tab.id} tabIndex={value === tab.id ? 0 : -1}
        onClick={() => onValueChange(tab.id)} onKeyDown={(event) => {
          const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : event.key === 'ArrowRight' ? (index + 1) % tabs.length : event.key === 'ArrowLeft' ? (index + tabs.length - 1) % tabs.length : undefined
          if (next === undefined) return
          event.preventDefault(); onValueChange(tabs[next].id); buttons.current[next]?.focus()
        }}>{tab.label}</button>)}
    </div>
    {tabs.map((tab) => <div key={tab.id} role="tabpanel" id={`${prefix}-panel-${tab.id}`} aria-labelledby={`${prefix}-tab-${tab.id}`} hidden={value !== tab.id} tabIndex={0}>{tab.content}</div>)}
  </div>
}
