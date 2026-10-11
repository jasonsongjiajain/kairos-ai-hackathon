import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TroubleshootingAssistant } from './TroubleshootingAssistant'
import { askAssistantWithStream } from '../../lib/api/assistant'

const CITED_ANSWER = {
  session_id: 'session-1',
  answer: 'Recommendation: inspect the optical path before dispatch.',
  uncertainty: 'Field conditions vary.',
  has_evidence: true,
  citations: [
    {
      chunk_id: 'kb-onu-offline-v1:1.0:inspect-optical-path',
      document_id: 'kb-onu-offline-v1',
      document_title: 'ONU Offline Field Checks',
      section: 'Inspect optical path',
      source_type: 'curated_procedure',
      content: 'Verify the patch lead is seated and inspect for visible bends or damage.',
      score: 0.82,
    },
  ],
  next_best_action: {
    remediation: 'Reseat the patch lead and recheck.',
    dispatch_required: false,
    suggestion: null,
    evidence: ['kb-onu-offline-v1:1.0:inspect-optical-path'],
    suggestion_evidence: [],
  },
}

const NO_EVIDENCE_ANSWER = {
  session_id: 'session-2',
  answer: 'No service guidance matched this question, so there is no cited procedure to rely on.',
  uncertainty: '',
  has_evidence: false,
  citations: [],
  next_best_action: null,
}

const DEVICES = [
  {
    id: 'device-router',
    device_ref: 'DEV-RTR-1',
    device_type: 'router',
    name: 'Customer router',
    status: 'unreachable',
    credential_available: false,
  },
]

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('TroubleshootingAssistant', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('renders a cited answer with an evidence panel after asking', async () => {
    vi.mocked(fetch).mockResolvedValue(jsonResponse(CITED_ANSWER))
    const user = userEvent.setup()
    render(<TroubleshootingAssistant ticketId="ticket-1" token="token" devices={DEVICES} />)

    await user.type(screen.getByLabelText('Ask about this ticket', { selector: 'textarea' }), 'Why is the ONU offline?')
    await user.click(screen.getByRole('button', { name: 'Ask the assistant' }))

    expect(
      await screen.findByText('Recommendation: inspect the optical path before dispatch.'),
    ).toBeInTheDocument()
    expect(screen.getByText('Retrieved evidence')).toBeInTheDocument()
    expect(screen.getByText('ONU Offline Field Checks')).toBeInTheDocument()
    expect(screen.getByText('Reseat the patch lead and recheck.')).toBeInTheDocument()
  })

  it('shows an explicit no-evidence response without a citation list', async () => {
    vi.mocked(fetch).mockResolvedValue(jsonResponse(NO_EVIDENCE_ANSWER))
    const user = userEvent.setup()
    render(<TroubleshootingAssistant ticketId="ticket-1" token="token" devices={DEVICES} />)

    await user.type(screen.getByLabelText('Ask about this ticket', { selector: 'textarea' }), 'A question with no matching guidance')
    await user.click(screen.getByRole('button', { name: 'Ask the assistant' }))

    expect(
      await screen.findByText('No service guidance matched this question, so there is no cited procedure to rely on.'),
    ).toBeInTheDocument()
    expect(screen.getByText(/no cited source/)).toBeInTheDocument()
    expect(screen.queryByText('Retrieved evidence')).not.toBeInTheDocument()
  })

  it('shows a retryable error when the assistant request fails', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response('', { status: 502 }))
    const user = userEvent.setup()
    render(<TroubleshootingAssistant ticketId="ticket-1" token="token" devices={DEVICES} />)

    await user.type(screen.getByLabelText('Ask about this ticket', { selector: 'textarea' }), 'Why is the ONU offline?')
    await user.click(screen.getByRole('button', { name: 'Ask the assistant' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'The assistant could not answer this question.',
    )
    expect(screen.getByRole('button', { name: 'Retry this question' })).toBeInTheDocument()
  })

  it('lets the agent propose an action and requires confirmation before state changes', async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(jsonResponse(CITED_ANSWER))
      .mockResolvedValueOnce(
        jsonResponse({
          id: 'proposal-1',
          ticket_id: 'ticket-1',
          tool_name: 'reboot_router',
          device_id: 'device-router',
          device_ref: 'DEV-RTR-1',
          kind: 'stateful',
          requires_confirmation: true,
          parameters: { device_id: 'device-router' },
          status: 'proposed',
          summary: 'Reboot the customer router',
          confirmation_id: 'confirm-1',
          created_at: '2026-05-20T12:00:00Z',
        }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          id: 'proposal-1',
          ticket_id: 'ticket-1',
          tool_name: 'reboot_router',
          device_id: 'device-router',
          device_ref: 'DEV-RTR-1',
          status: 'succeeded',
          message: 'Customer router rebooted and is back online.',
          correlation_id: 'confirm-1',
          executed_at: '2026-05-20T12:01:00Z',
        }),
      )
    const user = userEvent.setup()
    render(<TroubleshootingAssistant ticketId="ticket-1" token="token" devices={DEVICES} />)

    await user.type(screen.getByLabelText('Ask about this ticket', { selector: 'textarea' }), 'The router is unreachable')
    await user.click(screen.getByRole('button', { name: 'Ask the assistant' }))
    await user.click(await screen.findByRole('button', { name: 'Ask agent to select an action' }))

    expect(await screen.findByText('Reboot the customer router')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Review and approve' }))
    expect(screen.getByRole('dialog')).toHaveTextContent('Review the target and effect')
    await user.click(screen.getByRole('button', { name: 'Approve and run' }))

    expect(await screen.findByText('Customer router rebooted and is back online.')).toBeInTheDocument()
    expect(fetch).toHaveBeenCalledTimes(3)
  })

  it('uses the assistant WebSocket and reports retrieval progress', async () => {
    class StubSocket extends EventTarget {
      readyState = 0

      constructor() {
        super()
        queueMicrotask(() => {
          this.readyState = 1
          this.dispatchEvent(new Event('open'))
          this.dispatchEvent(new MessageEvent('message', { data: JSON.stringify({ type: 'ready' }) }))
        })
      }

      send(message: string) {
        expect(JSON.parse(message)).toEqual({ question: 'Why is the ONU offline?' })
        this.dispatchEvent(new MessageEvent('message', { data: JSON.stringify({ type: 'retrieval_started' }) }))
        this.dispatchEvent(new MessageEvent('message', { data: JSON.stringify({ type: 'answer', data: CITED_ANSWER }) }))
      }

      close() {
        this.readyState = 3
        this.dispatchEvent(new Event('close'))
      }
    }
    vi.stubGlobal('WebSocket', StubSocket)
    const progress: string[] = []

    const answer = await askAssistantWithStream(
      'ticket-1',
      'Why is the ONU offline?',
      'token',
      (message) => progress.push(message),
    )

    expect(answer.answer).toBe(CITED_ANSWER.answer)
    expect(progress).toContain('Connecting to the ticket assistant...')
    expect(progress).toContain('Searching ticket evidence and service guidance...')
    expect(fetch).not.toHaveBeenCalled()
  })
})
