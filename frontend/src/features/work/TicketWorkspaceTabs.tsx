import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Tabs } from '../../components/ui/tabs'
import type { TicketDetail, EntityFact, Device } from '../../lib/api/tickets'
import { fetchTicketAudit, type AuditEvent } from '../../lib/api/audit'
import { AuditTimeline } from '../audit/AuditTimeline'
import { CustomerServiceSummary } from './CustomerServiceSummary'
import { SensitiveCredentialReveal } from './SensitiveCredentialReveal'

const TM_EQUIPMENT = new Set(['router', 'rg', 'onu', 'ont', 'iptv', 'iptv box', 'streaming'])

function isTmEquipment(device: Device): boolean {
  const type = device.device_type.trim().toLowerCase()
  return TM_EQUIPMENT.has(type) || /\b(router|rg|onu|ont|iptv)\b/i.test(`${device.name} ${type}`)
}

function equipmentLabel(device: Device): string {
  const value = `${device.device_type} ${device.name}`.toLowerCase()
  if (/iptv|streaming/.test(value)) return 'IPTV box'
  if (/onu|ont/.test(value)) return 'ONU'
  if (/router|\brg\b/.test(value)) return 'Router (RG)'
  return device.device_type
}

export function TicketWorkspaceTabs({ detail, facts, token, onSelectDevice }: { detail: TicketDetail; facts: EntityFact[]; token: string; onSelectDevice: (id: string) => void }) {
  const [tab, setTab] = useState('customer')
  const [events, setEvents] = useState<AuditEvent[]>([])
  const [auditState, setAuditState] = useState('idle')
  const [revision, setRevision] = useState(0)
  useEffect(() => {
    if (tab !== 'audit') return
    const controller = new AbortController()
    setAuditState('loading')
    void fetchTicketAudit(detail.ticket.id, token, controller.signal).then((result) => { setEvents(result); setAuditState('ready') }).catch(() => { if (!controller.signal.aborted) setAuditState('error') })
    return () => controller.abort()
  }, [tab, detail.ticket.id, token, revision])
  const equipment = detail.devices.filter(isTmEquipment)
  return <section className="ticket-context-tabs" aria-label="Ticket context"><h3>Ticket context</h3><Tabs label="Ticket context" value={tab} onValueChange={setTab} tabs={[
    { id: 'customer', label: 'Customer', content: <CustomerServiceSummary customer={detail.customer} services={[]} devices={[]} routers={detail.routers} customerSummary={detail.customer_summary} showDevices={false} /> },
    { id: 'services', label: 'Services', content: <><CustomerServiceSummary customer={detail.customer} services={detail.services} devices={[]} routers={detail.routers} customerSummary={detail.customer_summary} showDevices={false} /><SensitiveCredentialReveal ticketId={detail.ticket.id} token={token} devices={detail.devices} services={detail.services} /></> },
    { id: 'devices', label: 'Devices', content: <section className="panel"><h4>TM equipment</h4>{equipment.length ? <ul className="workspace-device-list">{equipment.map((device) => { const deviceFacts = facts.filter((fact) => fact.entity_type === 'device' && fact.entity_id === device.id && !fact.is_sensitive); const warranty = deviceFacts.find((fact) => /warranty|coverage/i.test(`${fact.field_key} ${fact.label}`)); return <li key={device.id}><div><strong>{device.name}</strong><p>{equipmentLabel(device)} · <span className="tabular">{device.device_ref}</span> · {device.status}</p>{warranty && <p className="device-warranty"><span>Warranty</span> {warranty.value_text ?? warranty.value_number ?? 'Not recorded'}</p>}</div><button type="button" className="process-button" onClick={() => onSelectDevice(device.id)}>View details</button></li> })}</ul> : <p>No TM equipment is recorded for this customer.</p>}</section> },
    { id: 'audit', label: 'Audit', content: <section className="panel"><h4>Audit history</h4>{auditState === 'loading' && <p role="status">Loading audit history.</p>}{auditState === 'error' && <p role="alert">Audit history could not be loaded or is unavailable for this ticket.</p>}{auditState === 'ready' && <AuditTimeline events={events} />}<button type="button" className="process-button" onClick={() => setRevision((value) => value + 1)} disabled={auditState === 'loading'}>Refresh audit history</button><Link className="inline-link" to={`/tickets/${detail.ticket.id}/audit`}>View audit history</Link></section> },
  ]} /></section>
}
