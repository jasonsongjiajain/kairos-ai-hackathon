import { afterEach, expect, it, vi } from 'vitest'
import { processEvent } from './events'

afterEach(() => vi.unstubAllGlobals())

it('does not start setup or POST after cancellation', async () => {
  const fetchMock = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  controller.abort()
  await expect(processEvent('event-1', 'token', controller.signal)).rejects.toMatchObject({ name: 'AbortError' })
  expect(fetchMock).not.toHaveBeenCalled()
})

it('preserves AbortError when pending request is canceled', async () => {
  vi.stubGlobal('fetch', vi.fn((_input, init: RequestInit) => new Promise((_resolve, reject) => {
    init.signal?.addEventListener('abort', () => reject(init.signal?.reason), { once: true })
  })))
  const controller = new AbortController()
  const request = processEvent('event-1', 'token', controller.signal)
  controller.abort()
  await expect(request).rejects.toMatchObject({ name: 'AbortError' })
})

it('rejects late response data after cancellation without another request', async () => {
  let resolveJson!: (value: unknown) => void
  const fetchMock = vi.fn().mockResolvedValue({
    ok: true,
    json: () => new Promise(resolve => { resolveJson = resolve }),
  })
  vi.stubGlobal('fetch', fetchMock)
  const controller = new AbortController()
  const request = processEvent('event-1', 'token', controller.signal)
  await vi.waitFor(() => expect(resolveJson).toBeTypeOf('function'))
  controller.abort()
  resolveJson({})
  await expect(request).rejects.toMatchObject({ name: 'AbortError' })
  expect(fetchMock).toHaveBeenCalledOnce()
})
