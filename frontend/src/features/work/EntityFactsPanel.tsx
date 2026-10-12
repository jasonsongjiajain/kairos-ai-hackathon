import type { EntityFact } from '../../lib/api/tickets'

export const GROUP_LABELS: Record<string, string> = {
  router: 'Router details',
  optical: 'Optical signal',
  client: 'Client device',
  vobb: 'VoBB service',
  iptv: 'IPTV service',
  tmforce: 'Ticket operations',
}

export function factValue(fact: EntityFact): string {
  if (fact.value_number !== null && fact.value_number !== undefined) {
    return String(fact.value_number)
  }
  return fact.value_text ?? 'Not recorded'
}

type EntityFactsPanelProps = {
  facts: EntityFact[]
  groupKey: string
  heading?: string
}

export function EntityFactsPanel({ facts, groupKey, heading }: EntityFactsPanelProps) {
  const groupFacts = facts.filter((fact) => fact.group_key === groupKey)
  if (groupFacts.length === 0) return null
  const title = heading ?? GROUP_LABELS[groupKey] ?? groupKey

  return (
    <div className="facts-group">
      <h5 className="facts-heading">{title}</h5>
      <dl className="data-list">
        {groupFacts.map((fact) => (
          <div className="data-row" key={fact.field_key}>
            <dt>{fact.label}</dt>
            <dd className={fact.value_number !== null && fact.value_number !== undefined ? 'tabular' : undefined}>
              {factValue(fact)}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  )
}
