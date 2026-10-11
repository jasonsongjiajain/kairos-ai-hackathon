# Field Force Incident Assistant: Design

**Status:** Draft for product-owner review
**Target:** 24-hour hackathon MVP
**Product direction:** Mobile-first technician companion with a rugged field-tool character

## 1. Product goal

Build an authenticated workforce assistant that helps a technician understand and resolve an assigned customer connectivity issue without an unnecessary site visit. The system demonstrates an end-to-end incident journey: a supervisor processes a seeded network event, an assigned ticket is created, the technician reviews customer topology and service data, asks a retrieval-grounded assistant for help, and may approve a constrained remediation tool call. After troubleshooting, the assistant can suggest an appropriate solution or upsell for FF/EC/NextGen.

The hackathon differentiator is not a generic chat window. It is a grounded agent that can combine ticket, customer, topology, and knowledge-base evidence, explain its reasoning in concise operational terms, and perform explicitly authorized actions with traceable outcomes.

## 2. MVP boundaries

### In scope

- Seeded operational data for one representative incident type and a small set of staff/customer records.
- Authentication with role-aware access for supervisor/operator and technician.
- Assignment-scoped ticket access. A technician can only view tickets assigned to them.
- One operator-triggered, deterministic event intake path that creates and assigns a ticket automatically.
- Customer and service context: address, Granite/service identifier, ONU details, HSI details, VoBB details, and customer topology. Sensitive values use demo credentials and are accessible only within the authorized work context.
- RAG over a small set of troubleshooting documents and service knowledge, with source citations.
- Agentic tool calling for a small allowlist of simulated actions, such as router reboot and a narrowly defined configuration change.
- Explicit action confirmation, backend authorization, execution result, and audit event for all state-changing tools.
- Contextual solution or upsell advice, labeled as a recommendation and grounded in available service/customer data.
- Responsive mobile-first UI with empty, loading, error, denied, pending-approval, success, and failure states.

### Out of scope for the 24-hour build

- Live TMF, NTT, OSS/BSS, router, or ONU integration.
- Broad event taxonomy, production-grade correlation, configurable routing policies, and generalized ticket lifecycle automation.
- Real network configuration changes or real customer secrets.
- Production identity federation, multi-tenant administration, or claims of enterprise certification.
- A fully generalized connector framework for every database/vendor. Database access must be configurable, but a working PostgreSQL path is the target.

## 3. Personas and permissions

| Capability | Supervisor/operator | Assigned technician |
|---|---:|---:|
| Sign in and view own role | Yes | Yes |
| View incoming seeded events | Yes | No, unless separately assigned a relevant work item |
| Process event and create/assign ticket | Yes | No |
| View ticket and customer context | Operational scope | Assigned tickets only |
| Ask assistant about an authorized ticket | Yes, if in scope | Yes, for assigned ticket |
| Reveal a sensitive field credential | No by default | Only when authorized for the assigned work context |
| Request/approve a network action | Policy-dependent | Explicit confirmation required; tool policy still enforced server-side |
| View audit history | Operational scope | Events relevant to their assigned work |

Role checks and assignment checks are enforced by FastAPI on every relevant endpoint, not only by hiding UI controls. The model does not grant access. It can request tools, but the backend validates user, role, assignment, action allowlist, parameters, and approval state.

## 4. End-to-end experience

### A. Operator intake

1. Operator signs in and sees an incoming-event queue containing clearly identified seeded data.
2. Operator opens an event to inspect its source, detected symptom, and affected service/device reference.
3. Operator selects **Process event**. The system validates the event and idempotency key, creates one ticket, applies the single predefined assignment rule, and records the event-to-ticket transition.
4. The operator sees the created ticket and assigned technician. Reprocessing the same event does not create a duplicate.

### B. Technician workflow

1. Technician signs in and opens **My work**. The list contains only assigned tickets.
2. Technician opens the new ticket and sees a prioritized issue summary, current status, customer service context, and recommended next step.
3. The topology view shows the relevant service path and equipment, with the suspect or unreachable segment visually distinguished by an actual device/service state rather than decoration.
4. HSI and VoBB details appear in labeled sections. Address and service identifiers are available for field verification. Sensitive demo credentials are revealed only through a deliberate, authorized reveal action, and reveal access is audited. Raw secrets are not copied into the assistant transcript or ticket narrative.
5. Technician asks a question. The assistant uses authorized ticket/customer context plus indexed knowledge documents. Answers cite sources and separate observed data from inference or recommendation.
6. When a tool is appropriate, the assistant presents the action, target, expected impact, and evidence. The technician confirms. The backend validates permission and parameters, runs the simulator, then displays a success/failure result and audit entry.
7. The assistant recommends whether the issue appears remotely resolvable or whether a site visit/device replacement is indicated. It may offer relevant FF/EC/NextGen service advice only when the supplied data supports it.

## 5. Demo narrative and simulation behavior

The product should behave like a working operations system, not a pre-scripted animation. Seeded data makes it repeatable; the operator deliberately processes an event to start the workflow. Backend state changes drive the UI.

Suggested walkthrough:

1. Sign in as supervisor and process the seeded optical-loss or ONU-offline event.
2. Show the created ticket, assignment, and event correlation record.
3. Sign in as the assigned technician, or use a clearly labeled role-switch demo account flow if time requires it. Avoid silently impersonating a user.
4. Open the job and inspect customer topology and service details.
5. Ask a troubleshooting question such as why this customer may be offline and what checks should happen before dispatch.
6. Show cited retrieval evidence and customer/topology facts supporting the response.
7. Request a simulated router reboot or approved configuration action. Show the confirmation gate, execution state, outcome, and audit record.
8. Ask for the next best action and show a grounded resolution/field-dispatch recommendation plus a relevant service suggestion when supported.

No looping activity feed or fake live metrics are needed. All displayed events and values come from seeded records and are identifiable as demo data where a user could mistake them for live production data.

## 6. Recommended technology stack

| Layer | Recommendation | Rationale and scope |
|---|---|---|
| Web client | React + TypeScript + Vite | Fast iteration, mature ecosystem, simple deployment, and a straightforward fit for a mobile-first single-page workforce app. |
| UI primitives | shadcn/ui with Radix UI primitives | Accessible, composable controls that can be styled to the product direction rather than shipping an unmodified generic dashboard. Use only the components the workflow needs. |
| Styling | Tailwind CSS | Rapid responsive layout and token-driven styling during a short hackathon. Define semantic design tokens rather than scattering arbitrary colors. |
| Icons | Phosphor Icons, selected by meaning and weight | Use only where an icon improves recognition, such as network equipment, location, ticket, or action state. Labels remain visible; no decorative AI glyphs. |
| Motion | Framer Motion, used selectively | Animate meaningful state transitions such as ticket creation, retrieval progress, approval, and tool result. Respect reduced-motion preferences; no perpetual pulses. |
| Server-state client | TanStack Query | Caching, loading/error handling, query invalidation after actions, and predictable state for tickets, topology, chat sessions, and tool runs. |
| Forms and validation | React Hook Form + Zod | Typed form handling and consistent client-side validation for event processing, approvals, and configuration parameters. Backend validation remains authoritative. |
| API client | OpenAPI-generated TypeScript client, or a small typed fetch wrapper if generation is too costly | Keep API contracts aligned with FastAPI. Prefer generated types once the endpoints stabilize. |
| Backend | Python 3.12 + FastAPI + Pydantic | Async API, request validation, automatic OpenAPI schema, and direct ecosystem fit for LLM/RAG libraries. |
| Relational database | PostgreSQL | Store users, roles, assignments, events, tickets, customers, topology, service records, tool executions, and audit events. Configure via `DATABASE_URL`. |
| Vector retrieval | pgvector extension in PostgreSQL | Keeps hackathon operations simple and provides semantic retrieval beside relational context. Define a `VectorStore` boundary so another provider can replace it if pgvector is unavailable. |
| ORM/migrations | SQLAlchemy 2 + Alembic | Explicit persistence layer and repeatable schema changes. Keep repositories and domain services separate from HTTP routes. |
| LLM integration | Provider adapter using the available hosted model API | Keep model selection configurable. Tool schemas and response validation belong in the application, not in provider-specific UI code. Exact provider is selected based on available credentials and network access. |
| RAG orchestration | Thin application-owned retrieval pipeline; optionally LlamaIndex only if it materially speeds ingestion | For this bounded dataset, explicit chunking, embeddings, metadata filters, retrieval, and citations are easier to reason about than adding orchestration complexity. |
| Authentication | FastAPI OAuth2 password flow for local demo accounts, signed short-lived JWT access tokens, password hashing with Argon2id | Keep secrets in environment variables. A company identity provider can replace the local provider later. Never store plaintext passwords. |
| Authorization | Backend role-based checks plus ticket-assignment and customer-scope checks | Apply to every read and action endpoint. Sensitive-field reveal and tool execution are separately permission-checked and audited. |
| Background work | FastAPI background task or a small explicit worker for event ingestion/indexing | Avoid Redis/Celery unless the deployed environment requires durable asynchronous jobs. Keep the MVP operationally small. |
| Local environment | Docker Compose for API and PostgreSQL/pgvector, with frontend dev server | Gives the team a repeatable local setup and a path to hosted PostgreSQL. |
| Testing | Pytest + HTTPX for backend contracts and permissions; Vitest + React Testing Library for key UI behavior | Prioritize auth/assignment boundaries, idempotent ticket creation, retrieval citations, approval gates, and tool audit outcomes. |

### Database provider and client compatibility

The application connects to a database using its driver and connection URL. DBeaver is a database client, not a database server or provider. phpMyAdmin is primarily a MySQL/MariaDB administration client and does not make a MySQL database compatible with PostgreSQL. The MVP targets PostgreSQL because relational data and pgvector fit the use case. If the company-hosted database is MySQL/MariaDB, the team must confirm whether a separate PostgreSQL instance is allowed or explicitly change the vector-store and schema design; compatibility cannot be assumed solely because the database is accessible through DBeaver/phpMyAdmin.

### Suggested repository boundaries

```text
frontend/
  src/app/                 routes, auth/session boundary
  src/features/auth/       sign-in, role/session handling
  src/features/intake/     incoming event review and processing
  src/features/work/       assigned ticket list and job details
  src/features/topology/   customer/service topology view
  src/features/assistant/  chat, citations, action proposal/approval
  src/features/audit/      event/action history
  src/components/ui/       shared primitives and app-specific controls

backend/
  app/api/                 HTTP routes and dependencies
  app/auth/                authentication, roles, authorization policies
  app/domain/              incident, ticket, customer, topology, action rules
  app/services/            event processing, ticket assignment, assistant flow
  app/ai/                  ingestion, retrieval, prompt/context assembly, tools
  app/integrations/        model and vector-store provider interfaces
  app/repositories/        PostgreSQL persistence adapters
  app/audit/               append-only audit event writing/querying
  migrations/              Alembic migrations
```

## 7. RAG and agent design

### Knowledge ingestion

- Seed a small, curated set of troubleshooting procedures, service/device references, and operational FAQs.
- Store document ID, title, source type, version, and section metadata with each chunk.
- Chunk by meaningful headings/steps rather than arbitrary character windows where possible.
- Generate embeddings through the selected model provider and store vectors in pgvector.
- Make ingestion repeatable and idempotent using a stable document/version key.
- Treat customer-specific topology and current ticket state as structured operational context, not as a substitute for knowledge-document retrieval.

### Answer path

1. Verify the signed-in user and ticket assignment.
2. Build a bounded context from authorized ticket, service, topology, and customer fields.
3. Retrieve relevant knowledge chunks, applying metadata filters where available.
4. Ask the model to answer from supplied evidence, identify uncertainty, and return structured source references.
5. Validate source references against retrieved chunks and render citations with document/section labels.
6. Do not expose secrets in chat context unless a specific, authorized workflow truly requires them. The password reveal workflow is separate from ordinary RAG/chat.

### Tool-calling path

The model can propose, but cannot execute directly. A tool registry defines name, schema, allowed roles, required permission, confirmation requirement, and simulator implementation. The backend validates the proposal against the current user, ticket, target device, and action policy. State-changing calls require explicit technician confirmation. Store an audit record containing actor, ticket, tool name, normalized parameters with secrets redacted, approval timestamp, outcome, and correlation ID.

Initial tools should be limited to:

- Read-only device/service status lookup.
- Simulated router reboot.
- One constrained configuration update, with enumerated safe parameters and validated bounds.
- Ticket note/status update if time permits.

No unrestricted shell, arbitrary URL, arbitrary SQL, or model-generated code execution.

## 8. UI and UX specification

### Visual direction

Reading this as: **a mobile-first field workforce tool for technicians and supervisors, in a rugged operational style, dial ENERGY 2 / RHYTHM 2 / MOTION 2.**

- **ENERGY 2:** clear emphasis at incidents and actions without a marketing-style visual treatment.
- **RHYTHM 2:** consistent operational structure with variation where the task changes, such as a queue list, topology canvas, and conversational troubleshooting view.
- **MOTION 2:** transitions communicate state changes and system progress; no idle animation.
- Use a compact, high-legibility sans-serif selected for field readability. Use tabular numerals only for identifiers/status values where scanning benefits. Avoid oversized monospace headings.
- Use a restrained neutral base and one operational accent; reserve severity colors for actual severity/status meanings. Final brand tokens can be replaced with TM brand values if supplied.
- Status color never carries meaning alone. Pair it with text and/or a relevant icon; preserve WCAG AA text contrast and visible keyboard focus.
- Use solid surfaces for most content. Elevation is reserved for overlays and an action-confirmation dialog. No page-wide glass effects, glow, or decorative grid.
- Responsive behavior begins at phone width: a bottom-level navigation or compact header, full-width task content, touch targets at least 44px, and no horizontal overflow. On larger screens, the same task hierarchy can use a persistent work list beside the selected job.

### Primary navigation

Only implemented destinations appear:

- **My work** for technicians, showing assigned tickets.
- **Event intake** for supervisors/operators, showing seeded incoming events.
- **Audit** for authorized roles, showing relevant ticket/action history.

The selected ticket detail is a route/state under My work rather than a dead navigation destination. Chat is embedded in the ticket workflow so it inherits its authorized context.

### Core screens and components

| Screen/component | Job it supports | Key behavior |
|---|---|---|
| `SignInForm` | Authenticate the user | Validates credentials, announces errors accessibly, redirects according to role. Demo accounts are explicitly labeled as seeded/demo accounts. |
| `RoleAwareShell` | Keep navigation and scope understandable | Shows current role and user identity. Navigation links are permission-filtered and all APIs independently enforce access. |
| `EventIntakeQueue` | Let an operator inspect pending events | Shows event source/type, device/service reference, received time from seeded data, and processing state. Includes a useful empty state. |
| `EventReviewPanel` | Establish why an event will create work | Shows relevant event payload fields and target customer/device references. Sensitive fields are omitted. |
| `ProcessEventButton` + `ProcessingState` | Trigger deterministic event handling | Prevents repeat submission, reports progress, and presents duplicate/error outcomes. |
| `TicketCreatedConfirmation` | Confirm automation result | Shows ticket ID, assignment, event correlation, and a direct route to the ticket. |
| `AssignedWorkList` | Help technician choose the next job | Prioritizes status and symptom, supports empty/loading/error states, and excludes unassigned records. |
| `TicketHeader` | Summarize issue and current state | Displays ticket status, severity, customer reference, assignment, and event source. |
| `CustomerServiceSummary` | Give field context quickly | Groups address, Granite/service identifier, HSI, and VoBB fields into scannable labeled rows. |
| `SensitiveCredentialReveal` | Reveal an authorized ONU credential when needed | Requires deliberate user action and backend permission; records audit event; uses demo-only secrets; avoids clipboard/transcript leakage by default. |
| `TopologyPath` | Explain where the customer service path runs | Shows device/service nodes and their real seeded state. Supports small screens via vertical flow and larger screens via horizontal/diagram layout. Includes a text equivalent for assistive technology. |
| `TroubleshootingAssistant` | Ask questions with ticket context | Supports citations, explicit uncertainty, streaming or pending state, retry, and an error state. Keeps the chat context bound to the authorized ticket. |
| `EvidenceCitation` | Let staff verify an answer | Opens the referenced document/section or a compact evidence panel; does not claim a citation that was not retrieved. |
| `ActionProposal` | Review a proposed tool call | Shows action, target, parameters, reason/evidence, and expected effect before any execution. |
| `ActionApprovalDialog` | Confirm a state-changing action | Keyboard accessible, closable with Escape before execution, clear confirm/cancel actions, and clear irreversible/impact wording. |
| `ToolExecutionResult` | Explain the outcome | Shows success/failure, simulator result, timestamp, and link to relevant audit entry. Supports retry only where idempotency/policy permits. |
| `NextBestActionPanel` | Support field resolution and relevant advice | Distinguishes fix/dispatch recommendation from optional upsell advice and cites the underlying service/customer evidence. |
| `AuditTimeline` | Make system and staff actions accountable | Lists event processing, assignment, sensitive reveal, approval, tool execution, and outcome. Redacts secrets. |
| `FeedbackNotice` | Communicate request status and errors | Uses accessible live regions for async completion/failure; does not rely on color alone. |

### Motion and state transitions

- Event processing: button changes to a labeled processing state, then ticket confirmation appears when the backend completes.
- RAG request: show a compact “Searching service guidance” progress state and then render the answer with citations. If retrieval returns no useful evidence, say so rather than inventing confidence.
- Tool request: proposal appears as a reviewable state. No action animation starts before explicit confirmation.
- Tool execution: show pending, success, and failure with status text; update ticket/device state only after API response.
- Topology state changes: transition only the node whose backend state changed, so the user can track impact.
- Respect reduced-motion preferences and provide an immediate non-animated state change.

### Required UI states

- Empty work list: explain that no assigned jobs are available and how new assignments arrive.
- Empty event queue: explain that no pending seeded events are waiting.
- Loading: name the data being loaded, such as ticket, topology, or assistant evidence.
- Error: name the failed operation and provide a retry or return path where appropriate.
- Permission denied: explain the scope restriction without revealing whether another customer's record exists.
- No RAG evidence: distinguish knowledge not found from a service/device failure.
- Tool denied: explain that the action is unavailable for this user/context and preserve no misleading success state.
- Tool failure: show failure and retain the proposal for an allowed next step.

## 9. Data model outline

Core relational entities:

- `users`, `roles`, and role assignments.
- `customers` and service records for Granite, HSI, and VoBB.
- `network_devices` and `topology_edges`.
- `network_events` with stable source/event identifiers and processing state.
- `tickets` with customer, service, assigned technician, severity, status, and source event.
- `knowledge_documents` and vectorized `knowledge_chunks` with source/version metadata.
- `assistant_sessions` and `assistant_messages`, with sensitive data excluded/redacted.
- `tool_executions` and `audit_events`.

Seeded names, addresses, identifiers, and credentials must be synthetic and clearly designated as demo data. Never use real customer credentials in a hackathon seed file.

## 10. Security and operational requirements

- Enforce authorization server-side on every customer, ticket, topology, secret reveal, and tool operation.
- Use synthetic customer data and credentials only.
- Keep model keys, database credentials, and signing secrets in environment variables. Do not commit them.
- Redact secrets from logs, LLM prompts unless strictly necessary, assistant history, ticket notes, and audit payloads.
- Bind tool execution to a user, assigned ticket, explicit confirmation, allowed action, and validated parameters.
- Make event processing idempotent and audit its outcome.
- Use parameterized database operations and validated payload schemas.
- Keep a record of why the assistant recommended an action using source references and structured observations, not hidden chain-of-thought.
- Do not claim the prototype is production-certified or connected to TMF/NTT unless those integrations are actually implemented and verified.

## 11. Verification strategy

### Backend checks

- Unauthenticated requests are rejected.
- Technician cannot list or read another technician's ticket/customer/topology.
- Operator can process an allowed seeded event; duplicate processing does not create duplicate tickets.
- Event processing creates a ticket and applies the expected assignment rule.
- Sensitive credential reveal is denied outside the authorized assignment and creates an audit record when allowed.
- RAG response citations refer only to retrieved documents and authorized context.
- Tool calls are denied for invalid role, ticket assignment, action, or parameters.
- State-changing actions require explicit approval and record the result with secret redaction.

### Frontend checks

- Sign-in, role navigation, assigned work, event intake, ticket details, topology, assistant, citations, action confirmation, and audit links work end to end.
- Empty, loading, error, denied, no-evidence, approval, success, and failure states are understandable.
- Keyboard navigation and focus indicators work; dialogs close with Escape before execution.
- Phone and desktop layouts have no horizontal overflow; buttons meet touch target requirements.
- Reduced-motion setting removes nonessential transitions.

### End-to-end demo acceptance

An operator signs in, processes one seeded event, and sees the assigned ticket created once. The assigned technician signs in, sees that ticket, reads topology/service context, obtains a cited RAG response, confirms one permitted simulated tool action, sees its outcome and audit record, and receives a grounded next-best-action recommendation. Unauthorized access and duplicate event processing are demonstrated or verified by automated checks.

## 12. Decisions and reasons

| Decision | Reason |
|---|---|
| Narrow one-event ticket automation | Preserves a credible incident origin while protecting the 24-hour focus on RAG and agentic AI. |
| React + TypeScript + Vite | Fast feedback and a broad component ecosystem for a small responsive app. |
| FastAPI + PostgreSQL | Strong Python AI ecosystem plus a reliable relational store for permissions, assignments, and audit history. |
| PostgreSQL + pgvector | Keeps relational context and semantic retrieval in one hackathon-friendly database when the extension is available. |
| shadcn/ui + Radix + Tailwind | Accessible primitives with enough styling control to create a field-specific visual identity quickly. |
| TanStack Query | Keeps server state and async states predictable without building custom caching behavior. |
| Framer Motion, selectively | Makes event/action transitions legible while avoiding decorative or continuous animation. |
| Ticket assignment as an authorization boundary | Operational customer data must be scoped to the staff member's job. |
| Explicit approval for network actions | The model can recommend an operation, but staff and backend policy retain execution authority. |
| Audited secret reveal | Supports real technician workflow while making sensitive access deliberate and attributable. |
| Synthetic seed data | Enables a realistic repeatable demo without exposing real customer or credential data. |
