import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { clearSession, isSessionExpired, readSession, writeSession, type AuthSession } from '../../lib/auth/session'

type AuthContextValue = {
  session: AuthSession | null
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)
const MAX_TIMEOUT_MS = 2_147_483_647
const SIGN_IN_STORAGE_ERROR = 'This browser could not save the sign-in session. Enable session storage and try again.'

type LoginResponse = {
  access_token: string
  expires_at: string
  user_id: string
  role: string
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(() => readSession())

  useEffect(() => {
    if (!session) return
    let timeoutId: number | undefined
    let cancelled = false
    const scheduleExpiryCheck = () => {
      const remaining = session.expiresAt - Date.now()
      if (remaining <= 0) {
        clearSession()
        setSession((current) => current?.accessToken === session.accessToken ? null : current)
        return
      }
      timeoutId = window.setTimeout(scheduleExpiryCheck, Math.min(remaining, MAX_TIMEOUT_MS))
    }
    const checkExpiry = () => {
      if (!cancelled) scheduleExpiryCheck()
    }
    timeoutId = window.setTimeout(checkExpiry, Math.min(Math.max(0, session.expiresAt - Date.now()), MAX_TIMEOUT_MS))
    return () => {
      cancelled = true
      if (timeoutId !== undefined) window.clearTimeout(timeoutId)
    }
  }, [session])

  const signIn = useCallback(async (email: string, password: string) => {
    const body = new URLSearchParams({ username: email, password })
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    })
    if (!response.ok) {
      throw new Error(response.status === 401 ? 'Email or password is incorrect.' : 'Sign-in is unavailable. Try again.')
    }
    const result = await response.json() as LoginResponse
    const expiresAt = Date.parse(result.expires_at)
    if (!Number.isFinite(expiresAt) || expiresAt <= Date.now()) {
      throw new Error('Sign-in returned an invalid session. Try again.')
    }
    const nextSession: AuthSession = {
      accessToken: result.access_token,
      userId: result.user_id,
      role: result.role,
      expiresAt,
    }
    if (!writeSession(nextSession)) throw new Error(SIGN_IN_STORAGE_ERROR)
    setSession(nextSession)
  }, [])

  const signOut = useCallback(() => {
    clearSession()
    setSession(null)
  }, [])

  const value = useMemo(() => ({ session, signIn, signOut }), [session, signIn, signOut])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const value = useContext(AuthContext)
  if (!value) throw new Error('useAuth must be used within AuthProvider')
  return value
}
