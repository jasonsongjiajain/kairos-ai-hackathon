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
  return submitEvent(eventId, token)
}

export async function processEventWithUpdates(
  eventId: string,
  token: string,
  onProgress: (message: string) => void,
): Promise<ProcessEventResult> {
  let runId: string
  try {
    const runResponse = await fetch('/events/runs', {
      method: 'POST',
      headers: { ...authHeaders(token), 'Content-Type': 'application/json' },
      body: '{}',
    })
    const run = z.object({ run_id: z.string().uuid() }).safeParse(await readJson(runResponse))
    if (!runResponse.ok || !run.success) return submitEvent(eventId, token)
    runId = run.data.run_id
  } catch {
    return submitEvent(eventId, token)
  }

  const controller = new AbortController()
  let streamResponse: Response
  try {
    streamResponse = await fetch(`/events/runs/${encodeURIComponent(runId)}/events`, {
      headers: authHeaders(token),
      signal: controller.signal,
    })
    if (!streamResponse.ok || !streamResponse.body) {
      controller.abort()
      return submitEvent(eventId, token)
    }
  } catch {
    controller.abort()
    return submitEvent(eventId, token)
  }

  const streamFinished = readEventUpdates(streamResponse, onProgress)
  try {
    const result = await submitEvent(eventId, token, runId)
    await streamFinished
    return result
  } catch (error) {
    controller.abort()
    await streamFinished.catch(() => undefined)
    throw error
  } finally {
    controller.abort()
  }
}

async function submitEvent(eventId: string, token: string, runId?: string): Promise<ProcessEventResult> {
  let response: Response
  try {
    const suffix = runId ? `?run_id=${encodeURIComponent(runId)}` : ''
    response = await fetch(`/events/${encodeURIComponent(eventId)}/process${suffix}`, {
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

async function readEventUpdates(
  response: Response,
  onProgress: (message: string) => void,
): Promise<void> {
  const reader = response.body?.getReader()
  if (!reader) throw new EventsApiError('The event progress stream could not be read.')
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { value, done } = await reader.read()
    buffer += decoder.decode(value, { stream: !done })
    const blocks = buffer.split(/\r?\n\r?\n/)
    buffer = blocks.pop() ?? ''
    for (const block of blocks) {
      const eventName = block.match(/^event:\s*(.+)$/m)?.[1]
      const data = block.match(/^data:\s*(.+)$/m)?.[1]
      if (eventName === 'processing') onProgress('Assigning the incident to a technician...')
      if (eventName === 'ticket_created') onProgress('Ticket created and assigned.')
      if (eventName === 'failed') throw new EventsApiError('The event could not be processed. Retry in a moment.')
      if (data) JSON.parse(data)
    }
    if (done) return
  }
}
