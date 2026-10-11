import { z } from 'zod'
import { TicketsApiError } from './tickets'

const citationSchema = z.object({
  chunk_id: z.string().min(1),
  document_id: z.string().min(1),
  document_title: z.string(),
  section: z.string(),
  source_type: z.string(),
  content: z.string(),
  score: z.number(),
})

const nextBestActionSchema = z.object({
  remediation: z.string().nullable(),
  dispatch_required: z.boolean(),
  suggestion: z.string().nullable(),
  evidence: z.array(z.string()),
  suggestion_evidence: z.array(z.string()),
})

const assistantAnswerSchema = z.object({
  session_id: z.string().min(1),
  answer: z.string(),
  uncertainty: z.string(),
  has_evidence: z.boolean(),
  citations: z.array(citationSchema),
  next_best_action: nextBestActionSchema.nullable(),
})

export type AssistantCitation = z.infer<typeof citationSchema>
export type NextBestAction = z.infer<typeof nextBestActionSchema>
export type AssistantAnswer = z.infer<typeof assistantAnswerSchema>

export async function askAssistant(
  ticketId: string,
  question: string,
  token: string,
  signal?: AbortSignal,
): Promise<AssistantAnswer> {
  let response: Response
  try {
    response = await fetch(`/tickets/${encodeURIComponent(ticketId)}/assistant/messages`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
      signal,
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new TicketsApiError('The assistant could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 403 || response.status === 404) {
      throw new TicketsApiError(
        'The assistant is not available for this assigned ticket.',
        response.status,
      )
    }
    if (response.status === 401) {
      throw new TicketsApiError('Your session has expired. Sign in again.', response.status)
    }
    throw new TicketsApiError(
      'The assistant could not answer this question. Retry in a moment.',
      response.status,
    )
  }
  const parsed = assistantAnswerSchema.safeParse(await response.json().catch(() => null))
  if (!parsed.success) {
    throw new TicketsApiError('The assistant service returned an unexpected response.')
  }
  return parsed.data
}
