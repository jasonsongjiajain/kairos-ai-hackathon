import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { AuthProvider, useAuth } from '../features/auth/AuthProvider'
import { ProtectedRoute, SignInRoute } from '../features/auth/ProtectedRoute'
import { EventIntakeQueue } from '../features/intake/EventIntakeQueue'
import { AssignedWorkList } from '../features/work/AssignedWorkList'
import { TicketPage } from '../features/work/TicketPage'
import { AuditPage } from '../features/audit/AuditPage'
import { CustomerChatPage } from '../features/portal/CustomerChatPage'
import { ReportCheckerPage } from '../features/portal/ReportCheckerPage'
import { PortalSignInPage } from '../features/portal/PortalSignInPage'

function Workspace() {
  const { signOut } = useAuth()
  return (
    <main className="app-shell">
      <header className="app-header">
        <p className="app-context">FIELD OPERATIONS</p>
        <h1>Field Force Incident Assistant</h1>
        <p className="section-label">TECHNICIAN</p>
        <Button className="text-button" variant="quiet" type="button" onClick={signOut}>Sign out</Button>
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
        <Button className="text-button" variant="quiet" type="button" onClick={signOut}>Sign out</Button>
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
          <Route path="/portal/sign-in" element={<PortalSignInPage />} />
          <Route path="/admin/sign-in" element={<PortalSignInPage checker />} />
          <Route element={<ProtectedRoute allowedRoles={['customer']} signInPath="/portal/sign-in" />}>
            <Route path="/portal" element={<CustomerChatPage />} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={['technician']} />}>
            <Route path="/work" element={<Workspace />} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={['operator', 'supervisor']} />}>
            <Route path="/operations" element={<OperationsWorkspace />} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={['operator', 'supervisor']} signInPath="/admin/sign-in" />}>
            <Route path="/admin/check" element={<ReportCheckerPage />} />
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
