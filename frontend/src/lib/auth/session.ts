import { z } from 'zod'

const storedSessionSchema = z.object({
  accessToken: z.string().min(1),
  userId: z.string().min(1),
  role: z.string().min(1),
  expiresAt: z.number().finite(),
}).strict()

export type AuthSession = z.infer<typeof storedSessionSchema>

const storageKey = 'field-force-auth-session'

export function readSession(now = Date.now()): AuthSession | null {
  try {
    const raw = window.sessionStorage.getItem(storageKey)
    if (!raw) return null
    const parsed = storedSessionSchema.safeParse(JSON.parse(raw))
    if (!parsed.success || !Number.isFinite(parsed.data.expiresAt) || parsed.data.expiresAt <= now) {
      window.sessionStorage.removeItem(storageKey)
      return null
    }
    return parsed.data
  } catch {
    return null
  }
}

export function writeSession(session: AuthSession): void {
  const parsed = storedSessionSchema.parse(session)
  window.sessionStorage.setItem(storageKey, JSON.stringify(parsed))
}

export function clearSession(): void {
  window.sessionStorage.removeItem(storageKey)
}

export function isSessionExpired(session: AuthSession, now = Date.now()): boolean {
  return session.expiresAt <= now
}
