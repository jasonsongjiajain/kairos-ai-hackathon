import { useState } from 'react'
import { Button } from '../../components/ui/button'
import {
  TicketsApiError,
  revealDeviceCredential,
  revealServiceCredential,
  type Device,
  type ServiceDetail,
} from '../../lib/api/tickets'

type RevealResult = {
  state: 'revealing' | 'revealed' | 'error'
  credential?: string
  credentialType?: string
  message?: string
}

type CredentialSubject = {
  id: string
  kind: 'device' | 'service'
  name: string
  reference: string
}

type SensitiveCredentialRevealProps = {
  ticketId: string
  token: string
  devices: Device[]
  services: ServiceDetail[]
}

export function SensitiveCredentialReveal({ ticketId, token, devices, services }: SensitiveCredentialRevealProps) {
  const [results, setResults] = useState<Record<string, RevealResult>>({})

  const subjects: CredentialSubject[] = [
    ...devices
      .filter((device) => device.credential_available)
      .map((device) => ({ id: device.id, kind: 'device' as const, name: device.name, reference: device.device_ref })),
    ...services
      .filter((service) => service.credential_available)
      .map((service) => ({
        id: service.id,
        kind: 'service' as const,
        name: `${service.service_type} credential`,
        reference: service.service_ref,
      })),
  ]

  const reveal = async (subject: CredentialSubject) => {
    setResults((current) => ({ ...current, [subject.id]: { state: 'revealing' } }))
    try {
      const result =
        subject.kind === 'device'
          ? await revealDeviceCredential(ticketId, subject.id, token)
          : await revealServiceCredential(ticketId, subject.id, token)
      setResults((current) => ({
        ...current,
        [subject.id]: {
          state: 'revealed',
          credential: result.credential,
          credentialType: result.credential_type,
        },
      }))
    } catch (error) {
      setResults((current) => ({
        ...current,
        [subject.id]: {
          state: 'error',
          message:
            error instanceof TicketsApiError
              ? error.message
              : 'The credential could not be revealed. Retry.',
        },
      }))
    }
  }

  return (
    <section className="panel" aria-labelledby="credential-heading">
      <h3 id="credential-heading">Credential reveal</h3>
      <p className="muted-note">
        Revealing records an audit event and is never written into ticket notes
        or the assistant conversation.
      </p>

      {subjects.length === 0 ? (
        <div className="state-panel">
          <p>No credential is on file for this customer's equipment or services.</p>
        </div>
      ) : (
        <ul className="credential-list">
          {subjects.map((subject) => {
            const result = results[subject.id]
            return (
              <li className="credential-item" key={subject.id}>
                <div className="credential-head">
                  <span className="device-name">{subject.name}</span>
                  <span className="device-ref tabular">{subject.reference}</span>
                </div>
                <Button
                  className="process-button"
                  type="button"
                  onClick={() => void reveal(subject)}
                  disabled={result?.state === 'revealing'}
                  aria-busy={result?.state === 'revealing'}
                >
                  {result?.state === 'revealing'
                    ? 'Revealing credential'
                    : `Reveal credential for ${subject.name}`}
                </Button>

                {result?.state === 'revealed' && (
                  <output className="credential-result" aria-live="polite">
                    <span className="credential-label">
                      {result.credentialType?.replace(/_/g, ' ')}
                    </span>
                    <code className="credential-value tabular">{result.credential}</code>
                    <span className="credential-note">
                      Revealed and recorded in the audit log. Keep this value on the task screen.
                    </span>
                  </output>
                )}

                {result?.state === 'error' && (
                  <p className="form-error" role="alert">
                    {result.message}
                  </p>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}
