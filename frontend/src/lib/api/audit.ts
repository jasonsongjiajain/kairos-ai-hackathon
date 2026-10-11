import { z } from 'zod'
import { TicketsApiError } from './tickets'

const auditEventSchema = z.object({
  id: z.string().min(1),
  event_type: z.string().min(1),
  actor_id: z.string().nullable(),
  actor_name: z.string().nullable(),
  ticket_id: z.string().nullable(),
  details: z.record(z.unknown()),
  created_at: z.string(),
})

export type AuditEvent = z.infer<typeof auditEventSchema>

export async function fetchTicketAudit(
  ticketId: string,
  token: string,
  signal?: AbortSignal,
): Promise<AuditEvent[]> {
  let response: Response
  try {
    response = await fetch(`/tickets/${encodeURIComponent(ticketId)}/audit`, {
      headers: { Authorization: `Bearer ${token}` },
      signal,
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new TicketsApiError('The audit history could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 403 || response.status === 404) {
      throw new TicketsApiError('Audit history is not available for this ticket.', response.status)
    }
    throw new TicketsApiError('The audit history could not be loaded. Retry in a moment.', response.status)
  }
  const parsed = z.array(auditEventSchema).safeParse(await response.json().catch(() => null))
  if (!parsed.success) {
    throw new TicketsApiError('The audit service returned an unexpected response.')
  }
  return parsed.data
}
