import type { Customer, Device, ServiceDetail } from '../../lib/api/tickets'
import { statusLabel } from './TicketHeader'

const GROUPED_TYPES = ['Granite', 'HSI', 'VoBB']

type CustomerServiceSummaryProps = {
  customer: Customer
  services: ServiceDetail[]
  devices: Device[]
}

function detailEntries(details: Record<string, unknown>): Array<[string, string]> {
  return Object.entries(details).map(([key, value]) => {
    const text =
      value === null ? 'none' : typeof value === 'string' ? value : JSON.stringify(value)
    return [key.replace(/_/g, ' '), text] as [string, string]
  })
}

function ServiceCard({ service }: { service: ServiceDetail }) {
  const entries = detailEntries(service.details)
  return (
    <article className="service-card">
      <div className="service-card-head">
        <h5>{service.service_type}</h5>
        <span className={`status-pill status-${service.status.toLowerCase()}`}>
          {statusLabel(service.status)}
        </span>
      </div>
      <dl className="data-list">
        <div className="data-row">
          <dt>Service reference</dt>
          <dd className="tabular">{service.service_ref}</dd>
        </div>
        {entries.map(([key, value]) => (
          <div className="data-row" key={key}>
            <dt>{key}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
    </article>
  )
}

export function CustomerServiceSummary({ customer, services, devices }: CustomerServiceSummaryProps) {
  const grouped = GROUPED_TYPES.map((type) => ({
    type,
    items: services.filter((service) => service.service_type === type),
  }))
  const other = services.filter((service) => !GROUPED_TYPES.includes(service.service_type))

  return (
    <section className="panel" aria-labelledby="service-summary-heading">
      <p className="section-label">CUSTOMER CONTEXT</p>
      <h3 id="service-summary-heading">{customer.name}</h3>
      <p className="customer-ref tabular">{customer.customer_ref}</p>

      <dl className="data-list">
        <div className="data-row">
          <dt>Service address</dt>
          <dd>{customer.address}</dd>
        </div>
      </dl>

      <div className="service-groups">
        {grouped.map((group) =>
          group.items.length > 0 ? (
            <div className="service-group" key={group.type}>
              <h4>{group.type}</h4>
              {group.items.map((service) => (
                <ServiceCard service={service} key={service.id} />
              ))}
            </div>
          ) : null,
        )}
        {other.length > 0 && (
          <div className="service-group">
            <h4>Other services</h4>
            {other.map((service) => (
              <ServiceCard service={service} key={service.id} />
            ))}
          </div>
        )}
      </div>

      <div className="device-block">
        <h4>Equipment</h4>
        {devices.length === 0 ? (
          <p className="muted-note">No equipment is recorded for this customer.</p>
        ) : (
          <ul className="device-list">
            {devices.map((device) => (
              <li className="device-item" key={device.id}>
                <span className="device-name">{device.name}</span>
                <span className="device-ref tabular">{device.device_ref}</span>
                <span className="device-type">{device.device_type}</span>
                <span className={`status-pill status-${device.status.toLowerCase()}`}>
                  {statusLabel(device.status)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}
