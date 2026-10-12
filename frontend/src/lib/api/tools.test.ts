import { afterEach, describe, expect, it, vi } from 'vitest'
import { confirmTool, proposeAgentTool, proposeTool } from './tools'

const proposal = { id: 'p1', ticket_id: 't1', tool_name: 'reboot_router', device_id: 'd1', device_ref: 'R1', kind: 'stateful', requires_confirmation: true, parameters: {}, status: 'proposed', summary: 'Reboot', confirmation_id: 'c1', created_at: '2026-10-12T12:00:00Z' }
afterEach(() => vi.unstubAllGlobals())
describe.each(['catalog', 'agent'])('%s proposal validation', (endpoint) => {
  it.each([
    { kind: 'stateful', requires_confirmation: true, status: 'proposed' },
    { kind: 'stateful', requires_confirmation: true, status: 'succeeded' },
    { kind: 'stateful', requires_confirmation: true, status: 'failed' },
    { kind: 'read_only', requires_confirmation: false, status: 'succeeded' },
    { kind: 'read_only', requires_confirmation: false, status: 'failed' },
  ])('accepts supported combination %j', async (changes) => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...proposal, ...changes }))))
    const request = endpoint === 'catalog'
      ? proposeTool('t1', { toolName: 'reboot_router', deviceId: 'd1' }, 'token')
      : proposeAgentTool('t1', { question: 'Check router', deviceId: 'd1' }, 'token')
    await expect(request).resolves.toMatchObject(changes)
  })
  it.each([
    { status: 'pending' },
    { kind: 'read_only', requires_confirmation: false },
    { kind: 'read_only', requires_confirmation: true },
    { kind: 'stateful', requires_confirmation: false, status: 'succeeded' },
    { kind: 'unknown' },
  ])('rejects unsupported combination %j', async (changes) => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...proposal, ...changes }))))
    const request = endpoint === 'catalog'
      ? proposeTool('t1', { toolName: 'reboot_router', deviceId: 'd1' }, 'token')
      : proposeAgentTool('t1', { question: 'Check router', deviceId: 'd1' }, 'token')
    await expect(request).rejects.toThrow('The action service returned an unexpected response.')
  })
})
it('rejects nonterminal confirmation response', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...proposal, status: 'pending', message: '', correlation_id: 'c1', executed_at: proposal.created_at }))))
  await expect(confirmTool('t1', 'p1', 'c1', 'token')).rejects.toThrow('The action service returned an unexpected response.')
})
