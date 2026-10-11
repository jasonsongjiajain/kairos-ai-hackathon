import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from '../features/auth/AuthProvider'
import { ProtectedRoute, SignInRoute } from '../features/auth/ProtectedRoute'
import { EventIntakeQueue } from '../features/intake/EventIntakeQueue'
import { AssignedWorkList } from '../features/work/AssignedWorkList'
import { TicketPage } from '../features/work/TicketPage'

function Workspace() {
  const { signOut } = useAuth()
  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-context">FIELD OPERATIONS</p>
        <h1>Field Force Incident Assistant</h1>
        <p className="section-label">TECHNICIAN</p>
        <button className="text-button" type="button" onClick={signOut}>Sign out</button>
      </header>
      <AssignedWorkList />
    </main>
  )
}

function OperationsWorkspace() {
  const { session, signOut } = useAuth()
  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-context">FIELD OPERATIONS</p>
        <h1>Field Force Incident Assistant</h1>
        <p className="section-label">{session?.role === 'supervisor' ? 'SUPERVISOR' : 'OPERATOR'}</p>
        <button className="text-button" type="button" onClick={signOut}>Sign out</button>
      </header>
      <EventIntakeQueue />
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
            <Route path="/work" element={<Workspace />} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={['operator', 'supervisor']} />}>
            <Route path="/operations" element={<OperationsWorkspace />} />
          </Route>
          <Route
            element={<ProtectedRoute allowedRoles={['technician', 'operator', 'supervisor']} />}
          >
            <Route path="/tickets/:ticketId" element={<TicketPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/sign-in" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
