import { z } from 'zod'
import {
  TicketsApiError,
  customerSchema,
  customerSummarySchema,
  deviceSchema,
  routerSchema,
} from './tickets'

const networkCustomerSchema = z.object({
  customer: customerSchema,
  devices: z.array(deviceSchema),
  routers: z.array(routerSchema),
  summary: customerSummarySchema.nullable().optional(),
})

export type NetworkCustomer = z.infer<typeof networkCustomerSchema>

export async function fetchNetworkCustomers(
  token: string,
  signal?: AbortSignal,
): Promise<NetworkCustomer[]> {
  let response: Response
  try {
    response = await fetch('/customers', {
      headers: { Authorization: `Bearer ${token}` },
      signal,
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new TicketsApiError('The customer network directory could not be reached. Check your connection and retry.')
  }
  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new TicketsApiError('Your account cannot view the customer network directory.', response.status)
    }
    throw new TicketsApiError('The customer network directory could not be loaded. Retry in a moment.', response.status)
  }
  const parsed = z.array(networkCustomerSchema).safeParse(await response.json().catch(() => null))
  if (!parsed.success) {
    throw new TicketsApiError('The customer network directory returned an unexpected response.')
  }
  return parsed.data
}
