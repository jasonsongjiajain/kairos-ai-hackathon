import { z } from 'zod'

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

const assignedTicketSchema = ticketSchema.extend({
  customer_ref: z.string().min(1),
  customer_name: z.string().min(1),
  service_type: z.string().nullable(),
  service_ref: z.string().nullable(),
})

const customerSchema = z.object({
  id: z.string().min(1),
  customer_ref: z.string().min(1),
  name: z.string().min(1),
  address: z.string().min(1),
  is_demo: z.boolean(),
})

const serviceSchema = z.object({
  id: z.string().min(1),
  service_type: z.string().min(1),
  service_ref: z.string().min(1),
  status: z.string().min(1),
  details: z.record(z.unknown()),
})

const deviceSchema = z.object({
  id: z.string().min(1),
  device_ref: z.string().min(1),
  device_type: z.string().min(1),
  name: z.string().min(1),
  status: z.string().min(1),
  credential_available: z.boolean(),
})

const ticketDetailSchema = z.object({
  ticket: ticketSchema,
  assigned_technician_name: z.string(),
  customer: customerSchema,
  services: z.array(serviceSchema),
  devices: z.array(deviceSchema),
})

const credentialRevealSchema = z.object({
  device_id: z.string().min(1),
  device_ref: z.string().min(1),
  credential_type: z.string().min(1),
  credential: z.string().min(1),
})

export type AssignedTicket = z.infer<typeof assignedTicketSchema>
export type TicketDetail = z.infer<typeof ticketDetailSchema>
export type Customer = z.infer<typeof customerSchema>
export type ServiceDetail = z.infer<typeof serviceSchema>
export type Device = z.infer<typeof deviceSchema>
export type CredentialReveal = z.infer<typeof credentialRevealSchema>

export class TicketsApiError extends Error {
  readonly status: number | null

  constructor(message: string, status: number | null = null) {
    super(message)
    this.name = 'TicketsApiError'
    this.status = status
  }
}

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

function isAbort(error: unknown): boolean {
  return error instanceof DOMException && error.name === 'AbortError'
}

export async function fetchMyTickets(token: string, signal?: AbortSignal): Promise<AssignedTicket[]> {
  let response: Response
  try {
    response = await fetch('/tickets/mine', { headers: authHeaders(token), signal })
  } catch (error) {
    if (isAbort(error)) throw error
    throw new TicketsApiError('The assigned work list could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new TicketsApiError('Your account cannot view assigned work.', response.status)
    }
    throw new TicketsApiError('The assigned work list could not be loaded. Retry in a moment.', response.status)
  }
  const parsed = z.array(assignedTicketSchema).safeParse(await readJson(response))
  if (!parsed.success) {
    throw new TicketsApiError('The assigned work service returned an unexpected response.')
  }
  return parsed.data
}

export async function fetchTicket(
  ticketId: string,
  token: string,
  signal?: AbortSignal,
): Promise<TicketDetail> {
  let response: Response
  try {
    response = await fetch(`/tickets/${encodeURIComponent(ticketId)}`, {
      headers: authHeaders(token),
      signal,
    })
  } catch (error) {
    if (isAbort(error)) throw error
    throw new TicketsApiError('The ticket could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 403 || response.status === 404) {
      throw new TicketsApiError('This ticket is not part of your assigned work.', response.status)
    }
    if (response.status === 401) {
      throw new TicketsApiError('Your session has expired. Sign in again.', response.status)
    }
    throw new TicketsApiError('The ticket could not be loaded. Retry in a moment.', response.status)
  }
  const parsed = ticketDetailSchema.safeParse(await readJson(response))
  if (!parsed.success) {
    throw new TicketsApiError('The ticket service returned an unexpected response.')
  }
  return parsed.data
}

export async function revealDeviceCredential(
  ticketId: string,
  deviceId: string,
  token: string,
): Promise<CredentialReveal> {
  let response: Response
  try {
    response = await fetch(
      `/tickets/${encodeURIComponent(ticketId)}/devices/${encodeURIComponent(deviceId)}/credential`,
      { headers: authHeaders(token) },
    )
  } catch {
    throw new TicketsApiError('The credential could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 403 || response.status === 404) {
      throw new TicketsApiError('This credential is not available for your assigned work.', response.status)
    }
    throw new TicketsApiError('The credential could not be revealed. Retry in a moment.', response.status)
  }
  const parsed = credentialRevealSchema.safeParse(await readJson(response))
  if (!parsed.success) {
    throw new TicketsApiError('The credential service returned an unexpected response.')
  }
  return parsed.data
}
