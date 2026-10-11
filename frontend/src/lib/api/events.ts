import { z } from 'zod'

const pendingEventSchema = z.object({
  id: z.string().min(1),
  source_event_id: z.string().min(1),
  event_type: z.string().min(1),
  device_id: z.string().min(1),
  device_ref: z.string().min(1),
  device_name: z.string().min(1),
  device_status: z.string().min(1),
  service_id: z.string().nullable(),
  service_ref: z.string().nullable(),
  payload: z.record(z.unknown()),
  received_at: z.string().min(1),
})

export type PendingEvent = z.infer<typeof pendingEventSchema>

const ticketSchema = z.object({
  id: z.string().min(1),
  source_event_id: z.string().min(1),
  customer_id: z.string().min(1),
  service_id: z.string().nullable(),
  assigned_technician_id: z.string().min(1),
  severity: z.string().min(1),
  status: z.string().min(1),
  summary: z.string().min(1),
})

export type CreatedTicket = z.infer<typeof ticketSchema>

const processEventResultSchema = z.object({
  ticket: ticketSchema,
  created: z.boolean(),
  duplicate: z.boolean(),
  source_event_id: z.string().min(1),
  assigned_technician_name: z.string(),
})

export type ProcessEventResult = z.infer<typeof processEventResultSchema>

export class EventsApiError extends Error {}

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Bearer ${token}` }
}

async function readJson(response: Response): Promise<unknown> {
  try {
    return await response.json()
  } catch {
    return null
  }
}

export function describeEventType(eventType: string): string {
  return eventType.replace(/_/g, ' ')
}

export async function fetchPendingEvents(token: string, signal?: AbortSignal): Promise<PendingEvent[]> {
  let response: Response
  try {
    response = await fetch('/events/pending', { headers: authHeaders(token), signal })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new EventsApiError('The event service could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new EventsApiError('Your account cannot view the event queue.')
    }
    throw new EventsApiError('The event queue could not be loaded. Retry in a moment.')
  }
  const parsed = z.array(pendingEventSchema).safeParse(await readJson(response))
  if (!parsed.success) {
    throw new EventsApiError('The event service returned an unexpected response.')
  }
  return parsed.data
}

export async function processEvent(eventId: string, token: string): Promise<ProcessEventResult> {
  let response: Response
  try {
    response = await fetch(`/events/${encodeURIComponent(eventId)}/process`, {
      method: 'POST',
      headers: authHeaders(token),
    })
  } catch {
    throw new EventsApiError('The event service could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 404) {
      throw new EventsApiError('This event is no longer available. Reload the queue.')
    }
    if (response.status === 401 || response.status === 403) {
      throw new EventsApiError('Your account cannot process events.')
    }
    if (response.status === 409) {
      throw new EventsApiError('This event cannot be turned into a ticket right now.')
    }
    throw new EventsApiError('The event could not be processed. Retry in a moment.')
  }
  const parsed = processEventResultSchema.safeParse(await readJson(response))
  if (!parsed.success) {
    throw new EventsApiError('The event service returned an unexpected response.')
  }
  return parsed.data
}
