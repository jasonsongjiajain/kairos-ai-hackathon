import { useCallback, useEffect, useMemo, useState } from 'react'
import { Button } from '../../components/ui/button'
import { TicketsApiError } from '../../lib/api/tickets'
import { fetchToolCatalog, type ToolCatalogItem } from '../../lib/api/tools'
import {
  Agent,
  AgentContent,
  AgentHeader,
  AgentInstructions,
  AgentTool,
  AgentTools,
} from '../../components/ai/agent'

type CatalogState = 'loading' | 'ready' | 'error'

const INSTRUCTIONS =
  'Ground every answer in the retrieved procedure and the authorized ticket context, then rank grounded actions from low to high impact. Read-only checks run on request; state-changing actions run only after explicit approval and are recorded in the audit timeline.'

const CATEGORY_LABEL: Record<ToolCatalogItem['category'], string> = {
  diagnostics: 'Diagnostics (read-only)',
  wifi: 'Wi-Fi configuration',
  optical: 'Optical / PON',
  service: 'Customer services',
  network: 'Network policy',
}

const RISK_LABEL: Record<ToolCatalogItem['risk'], string> = {
  low: 'low risk',
  medium: 'needs approval',
  high: 'high impact',
}

function toolSchema(tool: ToolCatalogItem) {
  return {
    type: 'object',
    properties: {
      tool: { const: tool.name, description: tool.description },
      title: { const: tool.title },
      kind: { const: tool.kind, description: 'read_only runs on request; stateful needs approval' },
      category: { const: tool.category },
      risk: { const: tool.risk, description: RISK_LABEL[tool.risk] },
      requires_confirmation: { const: tool.requires_confirmation },
      target_device_types: { const: tool.target_device_types },
    },
  }
}

type AgentCapabilityPanelProps = {
  ticketId: string
  token: string
  modelName?: string
}

export function AgentCapabilityPanel({ ticketId, token, modelName }: AgentCapabilityPanelProps) {
  const [tools, setTools] = useState<ToolCatalogItem[]>([])
  const [state, setState] = useState<CatalogState>('loading')
  const [error, setError] = useState('')

  const load = useCallback(async (signal?: AbortSignal) => {
    setState('loading')
    setError('')
    try {
      const catalog = await fetchToolCatalog(ticketId, token)
      if (signal?.aborted) return
      setTools(catalog)
      setState('ready')
    } catch (caught) {
      if (signal?.aborted || (caught instanceof DOMException && caught.name === 'AbortError')) return
      setState('error')
      setError(caught instanceof TicketsApiError ? caught.message : 'The action catalog could not be loaded.')
    }
  }, [ticketId, token])

  useEffect(() => {
    const controller = new AbortController()
    void load(controller.signal)
    return () => controller.abort()
  }, [load])

  const grouped = useMemo(() => {
    const order: ToolCatalogItem['category'][] = ['diagnostics', 'wifi', 'optical', 'service', 'network']
    return order
      .map((category) => ({ category, items: tools.filter((tool) => tool.category === category) }))
      .filter((group) => group.items.length > 0)
  }, [tools])

  return (
    <section className="panel agent-panel" aria-labelledby="agent-capability-heading">
      <h3 id="agent-capability-heading">What the assistant can do here</h3>

      {state === 'loading' && (
        <p className="muted-note" role="status">Loading the permitted actions for this ticket.</p>
      )}

      {state === 'error' && (
        <div className="state-panel">
          <p className="form-error" role="alert">{error}</p>
          <Button className="process-button" type="button" onClick={() => void load()}>
            Retry loading actions
          </Button>
        </div>
      )}

      {state === 'ready' && tools.length === 0 && (
        <div className="state-panel">
          <p>No device actions are available for your role on this ticket.</p>
        </div>
      )}

      {state === 'ready' && tools.length > 0 && (
        <Agent className="agent-block">
          <AgentHeader name="Device action agent" model={modelName} />
          <AgentContent>
            <AgentInstructions>{INSTRUCTIONS}</AgentInstructions>
            {grouped.map((group) => (
              <div key={group.category} className="agent-category">
                <p className="agent-category__label">{CATEGORY_LABEL[group.category]}</p>
                <ul className="agent-category__tools">
                  {group.items.map((tool) => (
                    <li key={tool.name} className="agent-category__item">
                      <span className="agent-category__title">{tool.title}</span>
                      <span className={`risk-badge risk-badge--${tool.risk}`}>{RISK_LABEL[tool.risk]}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
            <AgentTools>
              {tools.map((tool) => (
                <AgentTool key={tool.name} value={tool.name} tool={{ description: tool.description, jsonSchema: toolSchema(tool) }} />
              ))}
            </AgentTools>
          </AgentContent>
        </Agent>
      )}
    </section>
  )
}
