import type { ReactNode } from 'react'
import { BrowserRouter, NavLink, Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { AuthProvider, useAuth } from '../features/auth/AuthProvider'
import { ProtectedRoute, SignInRoute } from '../features/auth/ProtectedRoute'
import { EventIntakeQueue } from '../features/intake/EventIntakeQueue'
import { AssignedWorkList } from '../features/work/AssignedWorkList'
import { TicketPage } from '../features/work/TicketPage'
import { AuditPage } from '../features/audit/AuditPage'

function WorkspaceShell({ children }: { children: ReactNode }) {
  const { session, signOut } = useAuth()
  const navigate = useNavigate()
  const isTechnician = session?.role === 'technician'
  const roleLabel = isTechnician ? 'TECHNICIAN' : session?.role === 'supervisor' ? 'SUPERVISOR' : 'OPERATOR'
  const workspaceLabel = isTechnician ? 'Assigned work' : 'Event intake'

  function handleSignOut() {
    signOut()
    navigate('/sign-in', { replace: true })
  }

  return (
    <main className="app-shell">
      <header className="app-header">
        <div className="app-brand">
          <p className="app-context">FIELD OPERATIONS</p>
          <h1>Field Force Incident Assistant</h1>
        </div>
        <nav className="workspace-nav" aria-label="Workspace">
          <NavLink to={isTechnician ? '/work' : '/operations'} aria-current="page">{workspaceLabel}</NavLink>
        </nav>
        <div className="app-account">
          <span className="workspace-role">{roleLabel}</span>
          <Button className="text-button" variant="quiet" type="button" onClick={handleSignOut}>Sign out</Button>
        </div>
      </header>
      {children}
    </main>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/sign-in" element={<SignInRoute />} />
          <Route element={<ProtectedRoute allowedRoles={['technician']} />}>
            <Route path="/work" element={<WorkspaceShell><AssignedWorkList /></WorkspaceShell>} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={['operator', 'supervisor']} />}>
            <Route path="/operations" element={<WorkspaceShell><EventIntakeQueue /></WorkspaceShell>} />
          </Route>
          <Route
            element={<ProtectedRoute allowedRoles={['technician', 'operator', 'supervisor']} />}
          >
            <Route path="/tickets/:ticketId" element={<TicketPage />} />
            <Route path="/tickets/:ticketId/audit" element={<AuditPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/sign-in" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
