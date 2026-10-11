import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from '../features/auth/AuthProvider'
import { ProtectedRoute, SignInRoute } from '../features/auth/ProtectedRoute'

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
            <Route path="/operations" element={<Workspace />} />
          </Route>
          <Route path="*" element={<Navigate to="/sign-in" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
