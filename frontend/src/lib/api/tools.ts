import { z } from 'zod'
import { TicketsApiError } from './tickets'

const catalogItemSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),
  kind: z.string().min(1),
  requires_confirmation: z.boolean(),
})

const proposalSchema = z.object({
  id: z.string().min(1),
  ticket_id: z.string().min(1),
  tool_name: z.string().min(1),
  device_id: z.string().min(1),
  device_ref: z.string().min(1),
  kind: z.string().min(1),
  requires_confirmation: z.boolean(),
  parameters: z.record(z.unknown()),
  status: z.string().min(1),
  summary: z.string(),
  confirmation_id: z.string().min(1),
  created_at: z.string(),
})

const executionSchema = z.object({
  id: z.string().min(1),
  ticket_id: z.string().min(1),
  tool_name: z.string().min(1),
  device_id: z.string().min(1),
  device_ref: z.string().min(1),
  status: z.string().min(1),
  message: z.string(),
  correlation_id: z.string().min(1),
  executed_at: z.string(),
})

export type ToolCatalogItem = z.infer<typeof catalogItemSchema>
export type ToolProposal = z.infer<typeof proposalSchema>
export type ToolExecution = z.infer<typeof executionSchema>

async function post(path: string, token: string, body: unknown): Promise<Response> {
  try {
    return await fetch(path, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  } catch {
    throw new TicketsApiError('The action service could not be reached. Check your connection and retry.')
  }
}

export async function fetchToolCatalog(ticketId: string, token: string): Promise<ToolCatalogItem[]> {
  let response: Response
  try {
    response = await fetch(`/tickets/${encodeURIComponent(ticketId)}/tools/catalog`, {
      headers: { Authorization: `Bearer ${token}` },
    })
  } catch {
    throw new TicketsApiError('The action catalog could not be reached.')
  }
  if (!response.ok) {
    throw new TicketsApiError('The action catalog could not be loaded.', response.status)
  }
  const parsed = z.array(catalogItemSchema).safeParse(await response.json().catch(() => null))
  if (!parsed.success) {
    throw new TicketsApiError('The action catalog returned an unexpected response.')
  }
  return parsed.data
}

export async function proposeTool(
  ticketId: string,
  input: { toolName: string; deviceId: string; parameters?: Record<string, number> },
  token: string,
): Promise<ToolProposal> {
  const response = await post(`/tickets/${encodeURIComponent(ticketId)}/tools/propose`, token, {
    tool_name: input.toolName,
    device_id: input.deviceId,
    parameters: input.parameters ?? {},
  })
  if (!response.ok) {
    if (response.status === 403) {
      throw new TicketsApiError('This action is not permitted here.', response.status)
    }
    if (response.status === 422) {
      throw new TicketsApiError('The action details were rejected. Check the values and retry.', response.status)
    }
    if (response.status === 404) {
      throw new TicketsApiError('This action target is not available for your assigned work.', response.status)
    }
    throw new TicketsApiError('The action could not be prepared. Retry in a moment.', response.status)
  }
  const parsed = proposalSchema.safeParse(await response.json().catch(() => null))
  if (!parsed.success) {
    throw new TicketsApiError('The action service returned an unexpected response.')
  }
  return parsed.data
}

export async function proposeAgentTool(
  ticketId: string,
  input: { question: string; deviceId: string },
  token: string,
): Promise<ToolProposal> {
  const response = await post(`/tickets/${encodeURIComponent(ticketId)}/tools/agent-propose`, token, {
    question: input.question,
    device_id: input.deviceId,
  })
  if (!response.ok) {
    if (response.status === 403 || response.status === 404) {
      throw new TicketsApiError('This action is not available for your assigned ticket.', response.status)
    }
    if (response.status === 422) {
      const body = await response.json().catch(() => null)
      throw new TicketsApiError(
        body && typeof body.detail === 'string'
          ? body.detail
          : 'The agent could not ground a safe action in the retrieved procedure.',
        response.status,
      )
    }
    throw new TicketsApiError('The agent could not prepare an action. Retry in a moment.', response.status)
  }
  const parsed = proposalSchema.safeParse(await response.json().catch(() => null))
  if (!parsed.success) {
    throw new TicketsApiError('The action service returned an unexpected response.')
  }
  return parsed.data
}

export async function confirmTool(
  ticketId: string,
  proposalId: string,
  confirmationId: string,
  token: string,
): Promise<ToolExecution> {
  const response = await post(
    `/tickets/${encodeURIComponent(ticketId)}/tools/${encodeURIComponent(proposalId)}/confirm`,
    token,
    { confirmation_id: confirmationId },
  )
  if (!response.ok) {
    if (response.status === 403 || response.status === 404) {
      throw new TicketsApiError('This action cannot be confirmed here.', response.status)
    }
    throw new TicketsApiError('The action could not be executed. Retry in a moment.', response.status)
  }
  const parsed = executionSchema.safeParse(await response.json().catch(() => null))
  if (!parsed.success) {
    throw new TicketsApiError('The action service returned an unexpected response.')
  }
  return parsed.data
}
