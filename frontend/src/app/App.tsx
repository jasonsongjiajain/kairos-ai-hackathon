import { BrowserRouter, Link, Navigate, Route, Routes, useParams } from 'react-router-dom'
import { AuthProvider, useAuth } from '../features/auth/AuthProvider'
import { ProtectedRoute, SignInRoute } from '../features/auth/ProtectedRoute'
import { EventIntakeQueue } from '../features/intake/EventIntakeQueue'

function Workspace() {
  const { session, signOut } = useAuth()
  const destination = session?.role === 'technician' ? 'Assigned work' : 'Operations queue'
  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-context">FIELD OPERATIONS</p>
        <h1>Field Force Incident Assistant</h1>
      </header>
      <section className="welcome" aria-labelledby="workspace-heading">
        <p className="section-label">{session?.role === 'technician' ? 'TECHNICIAN' : 'OPERATOR'}</p>
        <h2 id="workspace-heading">{destination}</h2>
        <p>Your field workspace will appear here.</p>
        <button className="text-button" type="button" onClick={signOut}>Sign out</button>
      </section>
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

// TODO(Task 5): replace this placeholder with the real ticket workspace.
function TicketWorkspacePlaceholder() {
  const { ticketId } = useParams()
  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-context">FIELD OPERATIONS</p>
        <h1>Ticket workspace</h1>
      </header>
      <section className="welcome" aria-labelledby="ticket-heading">
        <p className="section-label">TICKET</p>
        <h2 id="ticket-heading">Ticket {ticketId}</h2>
        <p>The full ticket workspace is built in the next step.</p>
        <Link className="inline-link" to="/operations">Back to event intake</Link>
      </section>
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
            <Route path="/tickets/:ticketId" element={<TicketWorkspacePlaceholder />} />
          </Route>
          <Route path="*" element={<Navigate to="/sign-in" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
