import { z } from 'zod'
import { assistantAnswerSchema } from '../api/assistant'

const activitySchema = z.enum(['pending', 'completed', 'needs-approval', 'no-evidence', 'failed'])
const planSuggestionSchema = z.object({
  tool_name: z.string(), title: z.string(), description: z.string(), kind: z.enum(['read_only', 'stateful']),
  category: z.enum(['diagnostics', 'wifi', 'optical', 'service', 'network']), risk: z.enum(['low', 'medium', 'high']), requires_confirmation: z.boolean(),
  device_id: z.string(), device_ref: z.string(), device_type: z.string(), parameters: z.record(z.unknown()),
  rationale: z.string(), steps: z.array(z.string()), evidence: z.array(z.string()), confidence: z.number(),
})
const planSchema = z.object({ ticket_id: z.string(), question: z.string(), device_id: z.string(), summary: z.string(), suggestions: z.array(planSuggestionSchema) })
const proposalSchema = z.object({
  id: z.string(), ticket_id: z.string(), tool_name: z.string(), device_id: z.string(), device_ref: z.string(),
  kind: z.enum(['read_only', 'stateful']), requires_confirmation: z.boolean(), parameters: z.record(z.unknown()),
  status: z.enum(['proposed', 'succeeded', 'failed']), summary: z.string(), confirmation_id: z.string(), created_at: z.string(),
})
const executionSchema = z.object({
  id: z.string(), ticket_id: z.string(), tool_name: z.string(), device_id: z.string(), device_ref: z.string(),
  status: z.enum(['succeeded', 'failed']), message: z.string(), correlation_id: z.string(), executed_at: z.string(),
})
const actionStateSchema = z.object({
  plan: planSchema.nullable(), proposal: proposalSchema.nullable(), execution: executionSchema.nullable(),
  rejected: z.boolean(), attempts: z.array(z.object({ proposal: proposalSchema.nullable(), execution: executionSchema })),
})
const turnSchema = z.object({
  id: z.number().int().positive(),
  question: z.string(),
  state: z.enum(['pending', 'answered', 'error']),
  answer: assistantAnswerSchema.optional(),
  message: z.string().optional(),
  activity: activitySchema,
  action: actionStateSchema.optional(),
})

export type StoredConversationTurn = z.infer<typeof turnSchema>
export type StoredActionState = z.infer<typeof actionStateSchema>

function storageKey(userId: string, ticketId: string) {
  return `field-force-chat-history:v1:${encodeURIComponent(userId)}:${encodeURIComponent(ticketId)}`
}

export function readConversation(userId: string, ticketId: string): StoredConversationTurn[] {
  try {
    const stored = window.sessionStorage.getItem(storageKey(userId, ticketId))
    if (!stored) return []
    const parsed = z.array(turnSchema).safeParse(JSON.parse(stored))
    if (!parsed.success) return []
    return parsed.data.map((turn) => turn.state === 'pending'
      ? { ...turn, state: 'error', activity: 'failed', message: 'This reply did not finish. Retry the question to continue.' }
      : turn)
  } catch {
    return []
  }
}

export function writeConversation(userId: string, ticketId: string, turns: StoredConversationTurn[]) {
  try {
    window.sessionStorage.setItem(storageKey(userId, ticketId), JSON.stringify(turns))
  } catch {
    // Storage can be unavailable or full; the live conversation remains usable.
  }
}
