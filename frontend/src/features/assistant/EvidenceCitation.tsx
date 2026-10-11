import type { AssistantCitation } from '../../lib/api/assistant'

type EvidenceCitationProps = {
  citation: AssistantCitation
  index: number
}

export function EvidenceCitation({ citation, index }: EvidenceCitationProps) {
  return (
    <li className="citation-item">
      <details className="citation-details">
        <summary className="citation-summary">
          <span className="citation-index">Evidence {index + 1}</span>
          <span className="citation-title">{citation.document_title}</span>
          <span className="citation-section">{citation.section}</span>
        </summary>
        <div className="citation-body">
          <p className="citation-content">{citation.content}</p>
          <p className="citation-meta">
            Source: {citation.source_type} ({citation.chunk_id})
          </p>
        </div>
      </details>
    </li>
  )
}
