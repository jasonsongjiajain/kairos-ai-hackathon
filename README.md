# Customer Incident Assistant

An authenticated customer-operations app that turns one processed network event into an assigned
ticket, then helps the customer diagnose it with retrieval-grounded answers and
permission-checked device actions.

**Status:** 24-hour hackathon MVP. All customer, device, and credential data is synthetic demo data.
No live TMF/NTT/OSS or real device integration is included.

The customer portal also supports a bounded model-directed agent and confirmed
router reboot/VLAN restoration simulations. See [Customer agent showcase](docs/customer-agent-showcase.md)
for the walkthrough, file changes, new tables, and safety boundaries.

## What it does

1. An operator processes a seeded network event. The backend creates and assigns exactly one ticket
   (idempotent: reprocessing returns the existing ticket).
2. The assigned technician opens the ticket and sees the customer service context (Granite, HSI,
   VoBB, address) and the customer topology path.
3. The technician reveals a sensitive ONU credential only through a deliberate, audited action.
4. The technician asks the assistant a question. Answers are grounded in retrieved knowledge and
   the authorized ticket context, and every citation is validated against the retrieved chunks.
5. The assistant can propose an allowlisted device action (status check, router reboot, bounded
   config change). State-changing actions run only after explicit approval, and every run is
   recorded in an audit timeline.

The agent can select an allowlisted action from a grounded request with
`POST /tickets/{ticket_id}/tools/agent-propose` using `{ "question": "...", "device_id": "..." }`.
The backend checks the assigned ticket, retrieved procedure, device/customer scope, tool allowlist,
and typed arguments. A selected read-only check runs immediately; state-changing actions are returned
as proposals and require the separate `/confirm` call. Evidence chunk IDs are recorded in the audit event.

Event intake supports an optional authenticated SSE run stream. Create an event run, connect to its
event stream, then process the event with the returned `run_id`:

```text
POST /events/runs
GET  /events/runs/{run_id}/events
POST /events/{event_id}/process?run_id={run_id}
GET  /events/runs/{run_id}
```

The stream emits `processing`, then `ticket_created` or `failed`. Reconnect with the
`Last-Event-ID` header to replay events after the last received event. Run state is held in API
process memory for this single-process MVP; a restart clears run history.

Ticket troubleshooting also exposes an authenticated WebSocket endpoint:

```text
WS /tickets/{ticket_id}/assistant/stream?token={access_token}
```

Send `{"question":"..."}` after the `ready` frame. The server sends `retrieval_started`, then an
`answer` frame containing the same validated citations and recommendations as the HTTP endpoint,
followed by `complete`. The HTTP `POST /tickets/{ticket_id}/assistant/messages` remains available
for clients that do not support WebSockets. The current chat provider returns complete structured
answers, so this stream reports retrieval progress and the final answer rather than token deltas.

## Architecture

Customer-scoped, read-only diagnostics are available at `GET /portal/me/diagnostics`.
See [customer diagnostic setup and file explanations](docs/customer-diagnostics.md)
for customer demo-login provisioning, measurement freshness and model settings.

For hosted Qwen embeddings, see [the 1024-dimensional migration guide](docs/qwen-embedding-migration.md).

Customer complaint triage is available at `POST /portal/me/chat/messages`, with
saved history and a customer-only `/portal` frontend. See [customer chatbot setup,
diagnostic rules and file explanations](docs/customer-chat.md). It asks follow-up
questions, offers self-help, and can record/route local customer trouble tickets.
It does not operate equipment or dispatch real Unifi teams. The desktop customer
portal and separate read-only checker are documented in [Customer portal](docs/customer-portal.md).
Evidence-based mesh/plan suggestions and conflict-safe appointments are documented
in [Customer support workflows](docs/customer-support-workflows.md).
The migration preserves original vectors; activate hosted retrieval only after
gateway probing, re-indexing and verification succeed.

- **Frontend:** React + TypeScript + Vite, Tailwind, Radix primitives, TanStack Query-ready API layer.
- **Backend:** FastAPI + Pydantic + SQLAlchemy 2 + Alembic.
- **Data:** PostgreSQL with the `pgvector` extension for both relational records and knowledge
  embeddings. PostgreSQL is required (see "Database notes" below).
- **AI:** provider-port design. Defaults to a deterministic local embedding + chat provider so the
  demo runs without external API keys; hosted OpenAI-compatible providers are selectable by setting.

## Prerequisites

- Docker Desktop (for PostgreSQL + the API).
- Node.js 20+ and npm (for the frontend dev server).

## Setup

```bash
cp .env.example .env
```

Edit `.env` if a port is already in use. To run the demo with the built-in sample data, set:

```
DEMO_SEED_ENABLED=true
```

All example values are local-only placeholders. Do not reuse them anywhere shared.

## Run the backend (Docker Compose)

```bash
docker compose up -d db
docker compose run --rm api alembic upgrade head
docker compose run --rm api python -m app.seed.demo_data     # requires DEMO_SEED_ENABLED=true
docker compose run --rm api python -m app.ai.ingestion       # fills knowledge embeddings
docker compose up -d api
```

The API is then available at `http://localhost:8000` (health: `GET /health`, docs: `/docs`).

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server proxies `/auth`, `/events`, `/tickets`, and `/audit` to `http://localhost:8000`
(override with `VITE_API_PROXY_TARGET`).

## Demo accounts (synthetic)

| Role | Email | Password |
|---|---|---|
| Operator | `operator@demo.invalid` | `Demo-Operator-Only-2026!` |
| Technician | `technician@demo.invalid` | `Demo-Technician-Only-2026!` |

These accounts exist only when `DEMO_SEED_ENABLED=true`. They are demo-only and must never be
enabled in a shared or production environment.

## Demo walkthrough

For a larger fictional dataset with 20 customers, Wi-Fi configuration, measurement
history and assigned tickets, see [Dummy data and PostgreSQL](docs/dummy-data-and-postgres.md).
That guide also covers DBeaver connections and how pgvector shares the existing database.

1. Sign in as the operator and open **Event intake**. Process the seeded ONU-offline event.
2. Confirm the created ticket and its assignment.
3. Sign out and sign in as the technician. Open **My work** and the assigned ticket.
4. Review the service details and the customer topology path.
5. Deliberately reveal the ONU credential (this writes an audit entry).
6. Ask the assistant why the service is down and what to check before dispatch; review the cited
   evidence and the next-best-action panel.
7. Open **Run a device action**, prepare a router reboot (or a bounded config change), and approve it.
8. Open **View audit history** to see the event, credential reveal, proposal, and execution.

## Test and build commands

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test -- --run
npm run build
```

## Database notes

The app connects using `DATABASE_URL`. DBeaver is a database client, not a provider, and phpMyAdmin
targets MySQL/MariaDB, so neither makes a non-PostgreSQL database compatible with this schema. The
MVP targets PostgreSQL because relational records and `pgvector` embeddings live in one database.
Knowledge storage supports separate 1536-dimensional local and 1024-dimensional
hosted vector columns. Other sizes require a migration; changing models requires
re-indexing and matching model provenance.

## Security notes

- Authorization is enforced server-side on every customer, ticket, topology, credential-reveal, and
  tool endpoint. Assignment scope is checked in the service layer, not only the UI.
- Credentials are revealed only inside an authorized assigned-work context and are never written to
  the assistant transcript, ticket narrative, or audit payloads.
- The assistant may propose tools, but the backend validates role, assignment, device, parameters,
  and confirmation before anything executes. Replayed confirmations are idempotent.
- No secrets are committed. Real customer data and real credentials must never be used with this
  demo.

## Out of scope

Live TMF/NTT/device integration, broad event taxonomy, configurable routing, production identity
federation, and real network configuration changes.
