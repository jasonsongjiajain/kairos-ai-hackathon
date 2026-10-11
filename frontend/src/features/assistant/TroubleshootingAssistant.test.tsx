import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { TroubleshootingAssistant } from './TroubleshootingAssistant'

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
    render(<TroubleshootingAssistant ticketId="ticket-1" token="token" />)

    await user.type(screen.getByLabelText('Ask about this ticket'), 'Why is the ONU offline?')
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
    render(<TroubleshootingAssistant ticketId="ticket-1" token="token" />)

    await user.type(screen.getByLabelText('Ask about this ticket'), 'A question with no matching guidance')
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
    render(<TroubleshootingAssistant ticketId="ticket-1" token="token" />)

    await user.type(screen.getByLabelText('Ask about this ticket'), 'Why is the ONU offline?')
    await user.click(screen.getByRole('button', { name: 'Ask the assistant' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'The assistant could not answer this question.',
    )
    expect(screen.getByRole('button', { name: 'Retry this question' })).toBeInTheDocument()
  })
})
