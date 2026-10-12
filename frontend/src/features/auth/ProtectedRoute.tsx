import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from './AuthProvider'
import { SignInForm } from './SignInForm'

export type WorkspaceRole = 'operator' | 'supervisor' | 'technician' | 'customer'

export function landingPath(role: string): string {
  if (role === 'customer') return '/portal'
  if (role === 'technician') return '/work'
  if (role === 'operator' || role === 'supervisor') return '/operations'
  return '/sign-in'
}

export function ProtectedRoute({ allowedRoles, signInPath = '/sign-in' }: { allowedRoles: readonly WorkspaceRole[]; signInPath?: string }) {
  const { session } = useAuth()
  if (!session) return <Navigate to={signInPath} replace />
  if (!allowedRoles.includes(session.role as WorkspaceRole)) {
    return <Navigate to={landingPath(session.role)} replace />
  }
  return <Outlet />
}

export function SignInRoute() {
  const { session } = useAuth()
  if (session) return <Navigate to={landingPath(session.role)} replace />
  return (
    <main className="app-shell sign-in-shell">
      <header className="app-header">
        <p className="app-context">FIELD OPERATIONS</p>
        <h1>Field Force Incident Assistant</h1>
      </header>
      <section className="sign-in-panel" aria-labelledby="sign-in-heading">
        <div className="sign-in-intro">
          <p className="section-label">WORKSPACE ACCESS</p>
          <h2 id="sign-in-heading">Sign in to your field workspace</h2>
          <p>Use your work account to continue to assigned operations.</p>
        </div>
        <SignInForm />
      </section>
    </main>
  )
}
