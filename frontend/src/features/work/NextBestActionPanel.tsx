import type { AssistantCitation, NextBestAction } from '../../lib/api/assistant'
import { Plan, PlanContent, PlanDescription, PlanHeader, PlanTitle, PlanTrigger } from '@/components/ai/plan'

type NextBestActionPanelProps = {
  action: NextBestAction
  citations: AssistantCitation[]
}

function evidenceLabels(ids: string[], citations: AssistantCitation[]): string[] {
  return ids.map((id) => {
    const citation = citations.find((item) => item.chunk_id === id)
    return citation ? `${citation.document_title}, ${citation.section}` : id
  })
}

export function NextBestActionPanel({ action, citations }: NextBestActionPanelProps) {
  return (
    <Plan defaultOpen className="nba-panel" aria-label="Next best action">
      <PlanHeader>
        <div className="nba-heading">
          <PlanTitle>Next best action</PlanTitle>
          <PlanDescription>
            {action.dispatch_required
              ? 'Dispatch or escalation is indicated for this ticket.'
              : 'This looks remotely resolvable with the guidance below.'}
          </PlanDescription>
        </div>
        <PlanTrigger />
      </PlanHeader>
      <PlanContent className="nba-content">
        {action.remediation && (
          <div className="nba-advice">
            <p className="nba-advice-label">Recommended remediation</p>
            <p className="nba-advice-text">{action.remediation}</p>
            <p className="nba-evidence">
              Evidence: {evidenceLabels(action.evidence, citations).join('; ')}
            </p>
          </div>
        )}
        {action.suggestion && (
          <div className="nba-advice">
            <p className="nba-advice-label">Service suggestion</p>
            <p className="nba-advice-text">{action.suggestion}</p>
            <p className="nba-evidence">
              Evidence: {evidenceLabels(action.suggestion_evidence, citations).join('; ')}
            </p>
          </div>
        )}
      </PlanContent>
    </Plan>
  )
}
