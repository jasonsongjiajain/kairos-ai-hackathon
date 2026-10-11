import { useState } from 'react'
import { Button } from '../../components/ui/button'
import { TicketsApiError, revealDeviceCredential, type Device } from '../../lib/api/tickets'

type RevealResult = {
  state: 'revealing' | 'revealed' | 'error'
  credential?: string
  credentialType?: string
  message?: string
}

type SensitiveCredentialRevealProps = {
  ticketId: string
  token: string
  devices: Device[]
}

export function SensitiveCredentialReveal({ ticketId, token, devices }: SensitiveCredentialRevealProps) {
  const [results, setResults] = useState<Record<string, RevealResult>>({})
  const revealable = devices.filter((device) => device.credential_available)

  const reveal = async (device: Device) => {
    setResults((current) => ({ ...current, [device.id]: { state: 'revealing' } }))
    try {
      const result = await revealDeviceCredential(ticketId, device.id, token)
      setResults((current) => ({
        ...current,
        [device.id]: {
          state: 'revealed',
          credential: result.credential,
          credentialType: result.credential_type,
        },
      }))
    } catch (error) {
      setResults((current) => ({
        ...current,
        [device.id]: {
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
      <p className="section-label">SENSITIVE FIELD DATA</p>
      <h3 id="credential-heading">Credential reveal</h3>
      <p className="muted-note">
        Demo credentials only. Revealing records an audit event and is never written into ticket notes
        or the assistant conversation.
      </p>

      {revealable.length === 0 ? (
        <div className="state-panel">
          <p>No demo credential is on file for this customer's equipment.</p>
        </div>
      ) : (
        <ul className="credential-list">
          {revealable.map((device) => {
            const result = results[device.id]
            return (
              <li className="credential-item" key={device.id}>
                <div className="credential-head">
                  <span className="device-name">{device.name}</span>
                  <span className="device-ref tabular">{device.device_ref}</span>
                </div>
                <Button
                  className="process-button"
                  type="button"
                  onClick={() => void reveal(device)}
                  disabled={result?.state === 'revealing'}
                  aria-busy={result?.state === 'revealing'}
                >
                  {result?.state === 'revealing'
                    ? 'Revealing credential'
                    : `Reveal credential for ${device.name}`}
                </Button>

                {result?.state === 'revealed' && (
                  <output className="credential-result" aria-live="polite">
                    <span className="credential-label">
                      {result.credentialType?.replace(/_/g, ' ')} (demo)
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
