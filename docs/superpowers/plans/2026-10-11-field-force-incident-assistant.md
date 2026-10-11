# Field Force Incident Assistant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an authenticated field-force app that turns one operator-processed seeded network event into an assigned ticket, then helps the assigned technician diagnose it with cited RAG and permission-checked simulated actions.

**Architecture:** React/TypeScript/Vite client calls a FastAPI API. PostgreSQL stores operational records and audit history; pgvector stores knowledge embeddings. Backend domain services enforce assignment/role policy and mediate model-proposed tools. The UI is mobile-first and ticket-contextual.

**Tech Stack:** React, TypeScript, Vite, shadcn/ui, Radix UI, Tailwind CSS, TanStack Query, React Hook Form, Zod, FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL + pgvector, pytest, HTTPX, Vitest, React Testing Library, Docker Compose.

---

## Implementation boundaries

Build the vertical slice in dependency order. Keep one event type, deterministic assignment, seeded synthetic records, a small curated knowledge set, and simulated network tools. Live TMF/NTT/device integration is out of scope. Do not commit real credentials or use real customer data.

## File map

The repository currently has no application scaffold. Create these files as the plan progresses; keep modules narrow and add files only for the agreed feature boundaries.

```text
frontend/
  package.json                  frontend scripts and dependencies
  vite.config.ts                Vite configuration
  tailwind.config.ts            semantic theme tokens and breakpoints
  src/main.tsx                  React entry point
  src/app/App.tsx               route composition
  src/app/router.tsx            route definitions and protected route boundary
  src/app/query-client.ts       TanStack Query configuration
  src/features/auth/            login form and session state
  src/features/intake/          supervisor event queue and processing
  src/features/work/            assigned ticket list and job view
  src/features/topology/        customer network topology view
  src/features/assistant/       chat, citations, proposal, approval, results
  src/features/audit/           audit timeline
  src/components/ui/            shadcn/Radix shared primitives
  src/lib/api/                  typed API functions and generated/manual types
  src/lib/auth/                 session helpers
  src/styles/                   global styles and tokens
  tests/                        Vitest and Testing Library tests

backend/
  pyproject.toml                Python dependencies and test tooling
  Dockerfile                    API image
  alembic.ini                   migration configuration
  app/main.py                   FastAPI app and lifespan
  app/config.py                 environment-backed settings
  app/api/                      route modules and dependency wiring
  app/auth/                     password verification, token, and access policy
  app/domain/                   entities, schemas, and rules
  app/repositories/             SQLAlchemy persistence adapters
  app/services/                 event, ticket, customer, and assistant workflows
  app/ai/                       ingestion, retrieval, context, tools, model adapter
  app/audit/                    redacted append-only audit writing/querying
  app/db/                        engine, session, base model
  migrations/                   Alembic revisions
  seed/                         synthetic demo records and knowledge documents
  tests/                         pytest unit/API/integration tests

compose.yaml                    PostgreSQL + pgvector and API local environment
.env.example                   variable names only, with no real secrets
```

## Task 1: Establish the local app skeleton

**Files:** Create root `compose.yaml`, `.env.example`; create `backend/pyproject.toml`, `backend/Dockerfile`, `backend/app/main.py`, `backend/app/config.py`; create `frontend/package.json`, `frontend/vite.config.ts`, `frontend/src/main.tsx`, `frontend/src/app/App.tsx`.

- [ ] Create a compose service for `pgvector/pgvector:pg16` with a named volume, health check, and development-only credentials read from `.env`.
- [ ] Add `.env.example` with `DATABASE_URL`, `JWT_SECRET`, `MODEL_API_KEY`, `MODEL_NAME`, `EMBEDDING_MODEL`, and `VITE_API_BASE_URL`; use conspicuous local-only example values.
- [ ] Set backend dependencies to FastAPI, Uvicorn, Pydantic Settings, SQLAlchemy 2, psycopg, Alembic, PyJWT, Argon2-cffi, HTTPX, pytest, and pytest-asyncio. Add optional model SDK dependency only after choosing the available provider.
- [ ] Add frontend dependencies and scripts for React, TypeScript, Vite, TanStack Query, React Router, React Hook Form, Zod, Tailwind, shadcn/Radix prerequisites, Phosphor icons, Framer Motion, Vitest, jsdom, and Testing Library.
- [ ] Add minimal `GET /health` in `backend/app/main.py` and a React shell that renders a named app heading.
- [ ] Run `docker compose up -d db`, `cd backend && python -m pytest`, and `cd frontend && npm run build` after creating the initial passing health/render tests. Expected: database healthy, backend tests pass, frontend production build succeeds.

## Task 2: Define persistence schema and synthetic seed data

**Files:** Create `backend/app/db/{base.py,engine.py,session.py}`, `backend/app/domain/{models.py,schemas.py}`, `backend/app/repositories/`, `backend/migrations/env.py`, `backend/seed/{demo_data.py,knowledge/}`, `backend/tests/test_seed.py`.

- [ ] Define SQLAlchemy models for users, roles, customers, services, network devices, topology edges, network events, tickets, documents, chunks, assistant sessions/messages, tool executions, and audit events.
- [ ] Define foreign keys and uniqueness constraints, including unique source event ID and one ticket per processed event.
- [ ] Configure SQLAlchemy from `DATABASE_URL`; enable pgvector extension through an Alembic migration and declare vector column dimensions from config.
- [ ] Create an Alembic initial migration and run `alembic upgrade head` against local PostgreSQL.
- [ ] Add synthetic operator/technician users with Argon2id hashes, one customer and services for Granite/HSI/VoBB, topology nodes, one unprocessed ONU-offline or optical-loss event, and a synthetic ONU credential.
- [ ] Add a small curated troubleshooting knowledge corpus with stable document IDs, titles, versions, and sections. Do not use real customer information or credentials.
- [ ] Add a seed command that is idempotent and verifies it produces exactly one pending event and known demo accounts. Run it twice; expected: counts remain unchanged.

## Task 3: Authentication and server-side access policy

**Files:** Create `backend/app/auth/{passwords.py,tokens.py,policy.py,dependencies.py}`, `backend/app/api/auth.py`, `backend/tests/test_auth.py`, `backend/tests/test_authorization.py`; frontend `src/features/auth/{SignInForm.tsx,AuthProvider.tsx,ProtectedRoute.tsx}`, `src/lib/auth/session.ts`.

- [ ] Write API tests for valid login, invalid password, missing token, expired token, and password hashes not containing plaintext.
- [ ] Implement login using Argon2id verification and signed short-lived JWT access tokens. Return user ID and role, not password hash.
- [ ] Implement an authenticated-user dependency and policy functions for role access, assigned-ticket access, and audit scope.
- [ ] Write policy tests proving a technician cannot read a different technician's ticket or customer through direct ID access.
- [ ] Implement frontend session state, sign-in form validation with Zod, protected route behavior, visible login errors, and role-aware redirect.
- [ ] Add API and component tests. Run `cd backend && pytest tests/test_auth.py tests/test_authorization.py -q` and `cd frontend && npm test -- --run`; expected: all pass.

## Task 4: Event intake and idempotent ticket creation

**Files:** Create `backend/app/api/events.py`, `backend/app/domain/event_rules.py`, `backend/app/services/event_processing.py`, `backend/app/repositories/events.py`, `backend/app/repositories/tickets.py`, `backend/tests/test_event_processing.py`; frontend `src/features/intake/{EventIntakeQueue.tsx,EventReviewPanel.tsx,ProcessEventButton.tsx}`, API functions under `frontend/src/lib/api/events.ts`.

- [ ] Write service tests for operator-only event processing, assignment rule, ticket creation, repeat processing, unknown event, and database failure rollback.
- [ ] Implement `GET /events/pending` limited to authorized operator role.
- [ ] Implement `POST /events/{event_id}/process` in a transaction. Lock/check event status, enforce unique source event, create ticket using the predefined assignment rule, update event state, and write audit event.
- [ ] Return the existing ticket on a repeated idempotent request instead of creating a duplicate.
- [ ] Implement the event queue/review UI with labeled seeded data, process confirmation, disabled duplicate submit, loading state, empty state, error retry, and created-ticket link.
- [ ] Run `cd backend && pytest tests/test_event_processing.py -q` and `cd frontend && npm test -- --run`; expected: duplicate event creates one ticket and UI reflects API outcomes.

## Task 5: Assigned tickets and customer/topology detail

**Files:** Create `backend/app/api/tickets.py`, `backend/app/api/customers.py`, `backend/app/services/ticket_queries.py`, `backend/tests/test_ticket_access.py`, `backend/tests/test_sensitive_reveal.py`; frontend `src/features/work/{AssignedWorkList.tsx,TicketPage.tsx,TicketHeader.tsx,CustomerServiceSummary.tsx,SensitiveCredentialReveal.tsx}`, `src/features/topology/{TopologyPath.tsx,TopologyPath.test.tsx}`, API modules under `frontend/src/lib/api/`.

- [ ] Write API tests for technician assigned-work list, direct access denial for another technician's ticket, customer/service scope, and no credential in normal ticket response.
- [ ] Implement `GET /tickets/mine`, `GET /tickets/{id}`, `GET /tickets/{id}/topology` with assignment/role checks in service or policy layer.
- [ ] Implement a dedicated credential reveal endpoint that checks assigned-work permission, records an audit event, returns only the requested demo credential, and uses no-store response headers.
- [ ] Ensure ticket/customer serializers redact password fields by default; add regression test asserting no secret in ticket response.
- [ ] Implement mobile-first assigned list, issue summary, grouped Granite/HSI/VoBB/address details, credential reveal control, and topology path. Use text alternative and status labels alongside visual topology state.
- [ ] Add loading, empty, error, denied, and reveal-success states. Verify narrow viewport layout and 44px controls.
- [ ] Run `cd backend && pytest tests/test_ticket_access.py tests/test_sensitive_reveal.py -q` and `cd frontend && npm test -- --run`; expected: access boundaries and reveal audit behavior pass.

## Task 6: Knowledge ingestion and cited retrieval

**Files:** Create `backend/app/ai/{ports.py,ingestion.py,chunking.py,retrieval.py,context.py}`, `backend/app/integrations/{embeddings.py,model_provider.py}`, `backend/app/api/knowledge.py`, `backend/tests/test_ingestion.py`, `backend/tests/test_retrieval.py`.

- [ ] Define provider interfaces for embedding and chat completion so tests can use deterministic fakes and deployment can configure an available provider.
- [ ] Write tests for repeatable ingestion, chunk metadata retention, retrieval relevance against a small fixed corpus, metadata filters, and empty retrieval.
- [ ] Implement heading-aware chunking for seeded documents and stable versioned chunk IDs.
- [ ] Implement embedding generation and pgvector persistence; make ingestion idempotent by document/version/chunk key.
- [ ] Implement retrieval that returns chunk text, document ID/title/section, and relevance score; apply the service-category metadata filter from the authorized ticket when present, and allow globally applicable documents.
- [ ] Implement bounded context assembly from authorized ticket/customer/topology fields. Exclude secrets and redact credential-shaped values.
- [ ] Seed or index knowledge with a CLI command; run twice and confirm chunk count is unchanged.
- [ ] Run `cd backend && pytest tests/test_ingestion.py tests/test_retrieval.py -q`; expected: citation metadata always maps back to indexed documents.

## Task 7: Assistant answers, citations, and next-best-action

**Files:** Create `backend/app/services/assistant.py`, `backend/app/api/assistant.py`, `backend/app/domain/assistant_schemas.py`, `backend/tests/test_assistant.py`; frontend `src/features/assistant/{TroubleshootingAssistant.tsx,ChatMessage.tsx,EvidenceCitation.tsx,AssistantComposer.tsx}`, `src/features/work/NextBestActionPanel.tsx`, API module `frontend/src/lib/api/assistant.ts`.

- [ ] Write tests using a fake model provider for authorized question flow, cited answer, no evidence response, invalid citation rejection, and unauthorized ticket denial.
- [ ] Implement `POST /tickets/{id}/assistant/messages`: verify assignment, assemble context, retrieve evidence, call model with structured response schema, validate citations against retrieved chunk IDs, persist redacted user/assistant messages, and return answer plus citations.
- [ ] Define prompt instructions to distinguish observed ticket/customer data, retrieved procedural evidence, inference, and recommendation; do not request or reveal hidden chain-of-thought.
- [ ] Implement assistant UI embedded in TicketPage with cited evidence panel, loading/searching state, retryable errors, no-evidence response, and keyboard-accessible message form.
- [ ] Implement next-best-action output with separate fields for remediation/dispatch recommendation and optional FF/EC/NextGen suggestion. Require evidence references for each advice item; omit unsupported upsell advice.
- [ ] Run `cd backend && pytest tests/test_assistant.py -q` and `cd frontend && npm test -- --run`; expected: unsupported claims/citations do not render as sourced facts.

## Task 8: Permissioned agent tools and audit timeline

**Files:** Create `backend/app/ai/{tool_registry.py,tool_executor.py}`, `backend/app/api/tools.py`, `backend/app/services/tool_execution.py`, `backend/tests/test_tool_permissions.py`, `backend/tests/test_tool_execution.py`, `backend/app/api/audit.py`, `backend/tests/test_audit.py`; frontend `src/features/assistant/{ActionProposal.tsx,ActionApprovalDialog.tsx,ToolExecutionResult.tsx}`, `src/features/audit/{AuditTimeline.tsx,AuditPage.tsx}`, `frontend/src/lib/api/tools.ts`.

- [ ] Define typed allowlisted tools: read-only device status, simulated router reboot, and one configuration update restricted to enumerated keys and ranges.
- [ ] Write tests that reject unknown tools, forbidden roles, unassigned tickets, mismatched device IDs, invalid config bounds, missing approval, and replayed confirmation IDs.
- [ ] Implement tool proposal generation from structured model tool calls. Treat model arguments as untrusted input and validate with Pydantic schemas.
- [ ] Implement two-phase action flow: create proposal, display details, receive explicit confirmation, revalidate current authorization/parameters, simulate action, persist result, update simulated device state only after success.
- [ ] Record audit fields: actor, ticket, action, normalized redacted parameters, approval, outcome, timestamp, correlation ID. Never store secrets in audit payloads.
- [ ] Implement audit endpoint with role and assignment scope; implement timeline UI for event, assignment, credential reveal, approval, and tool outcomes.
- [ ] Implement accessible confirmation dialog with visible target/effect, confirm/cancel, Escape before execution, focus management, and no execution on dialog dismissal.
- [ ] Run `cd backend && pytest tests/test_tool_permissions.py tests/test_tool_execution.py tests/test_audit.py -q` and frontend tests. Expected: all execution paths are authorized and auditable.

## Task 9: Visual system, responsive polish, and resilient states

**Files:** Create/modify `frontend/tailwind.config.ts`, `frontend/src/styles/{tokens.css,global.css}`, `frontend/src/components/ui/`, feature state components and tests.

- [ ] Define semantic color, typography, spacing, radius, focus, and state tokens for the rugged field-tool direction. Use TM brand values only if supplied and verified.
- [ ] Add shadcn/Radix primitives only as needed: button, input, dialog, alert, tabs, separator, toast/live region. Keep every interactive primitive functional.
- [ ] Add Phosphor icons only when they improve recognition and keep visible text labels for state/action.
- [ ] Add selective Framer Motion transitions for event processing, RAG progress/results, topology state update, and tool result. Respect `prefers-reduced-motion` and avoid infinite animation.
- [ ] Add mobile and desktop component tests or Playwright viewport checks for no horizontal overflow, logical keyboard order, visible focus, and minimum tap target sizes.
- [ ] Verify WCAG AA text contrast for chosen tokens with a contrast checker; adjust foreground/background pairs that fail.
- [ ] Verify component states including loading, empty, failed, denied, pending approval, success, and failure at phone and desktop widths.

## Task 10: End-to-end walkthrough and delivery checks

**Files:** Create `backend/tests/test_demo_flow.py`, `frontend/tests/demo-flow.test.tsx` or Playwright test, `README.md`, `compose.yaml`, `.env.example`.

- [ ] Add one integrated API test: seed, authenticate operator, process event, verify one assigned ticket, authenticate assigned technician, retrieve ticket/topology, ask assistant with citations, confirm simulated action, and inspect redacted audit history.
- [ ] Add UI end-to-end walkthrough using seeded accounts and a fake deterministic model provider, covering operator processing and technician investigation/action.
- [ ] Add README setup instructions with exact prerequisites, environment variables, migration, seed, ingestion, run, test, and demo-account steps. Clearly label all values as synthetic demo data.
- [ ] Run `docker compose up --build -d`, `docker compose exec api alembic upgrade head`, `docker compose exec api python -m app.seed.demo_data`, and the knowledge ingestion command documented in README.
- [ ] Run backend suite with `docker compose exec api pytest -q`; run frontend suite and production build with `cd frontend && npm test -- --run && npm run build`.
- [ ] Perform click-through at phone and desktop sizes: sign-in, event process, ticket navigation, topology, credential reveal, assistant citations, proposed action approval/cancel, action result, audit, empty/error states, and keyboard navigation. Record results and browser console status.
- [ ] Confirm no real credentials, customer data, or provider keys appear in repository files, logs, chat history, seed data, or audit records.

## Self-review against the design spec

- Event intake and automatic ticket creation: Tasks 2 and 4.
- Authentication, role and assignment authorization: Task 3 and cross-cutting API checks in Tasks 4-8.
- Customer, service, topology, and controlled credential reveal: Task 5.
- RAG ingestion, retrieval, citations, and missing-evidence behavior: Tasks 6 and 7.
- Agent tool allowlist, approval, simulation, and audit: Task 8.
- UI library, mobile-first screens, animation, accessibility, and states: Tasks 1, 5, 7-10.
- Next-best-action and FF/EC/NextGen advice: Task 7.
- PostgreSQL/pgvector setup, configurable connection, provider adapter, and repeatable local environment: Tasks 1, 2, and 6.
- Demo acceptance and run/test instructions: Task 10.

The plan intentionally excludes live TMF/NTT and device integrations, generalized routing, and unbounded agent capabilities as specified. No placeholders such as TBD or TODO are required for execution. Before Task 6, select the available LLM and embedding provider, then implement its adapter behind the provider interfaces defined in that task.
