# Field operations visual and motion foundation

Approved direction: light-only white/near-white workspace, near-black text, neutral boundaries, semantic status colors. Antislop applies during implementation. ENERGY 2 / RHYTHM 2 / MOTION 3, with choreography confined to incident, tool, and topology state changes.

## Identity and hierarchy

- Incident trace is the identity motif: follow actual event, ticket, topology, evidence, action, and confirmed result. Sequence and relationships supply character instead of a general colored accent. The trace component belongs to task 2; this foundation does not invent stages or completion.
- White surfaces on a near-white canvas keep incident evidence readable. Near-black actions establish priority; green is reserved for healthy/successful states, amber for uncertainty or warnings, red for errors or high severity. Open tickets and low severity remain neutral.
- Georgia editorial headings distinguish investigation prompts from dense evidence. Native Avenir Next / Segoe UI keeps controls readable without font downloads.
- Chat leads the ticket screen. Adjacent context keeps device facts available during investigation; mobile preserves one-column reading order. Ticket lists gain two columns at 600px; workbench and sign-in split at 900px. Short desktop viewports retain document scrolling so the composer remains reachable.
- Spacing uses 4/8/12/16/24/32/48px steps: broad entry spacing invites the first question, compact evidence groups support ongoing work. Radii use 4px for labels, 8px for controls, 12px for panels.
- Cards group actual tickets, evidence, and proposals. Shadows identify only overlapping selects/dialogs; composer boundaries identify its input area without elevation.
- Existing Button, Textarea, Card, Select, and Radix dialogs retain their behaviors. Suggested questions submit real requests. Ctrl/Cmd+Enter sends follow-ups; Enter remains available for newlines.
- No theme toggle, downloaded fonts, logo, illustration, avatar, or other new visual assets. Light-only is the approved field-work brief.

## Semantic tokens

CSS variables in `frontend/src/styles.css` are shared through `frontend/tailwind.config.ts`.

| Role | Value | Purpose |
| --- | --- | --- |
| Canvas | `#fafafa` | Separate workspace from content |
| Surface / elevated | `#ffffff` | Evidence, inputs, overlays |
| Primary text / focus | `#181818` | Reading priority and keyboard location |
| Secondary text | `#525252` | Readable metadata and placeholders |
| Border | `#858585` | Control boundaries, at least 3:1 against surfaces |
| Divider | `#dedede` | Noninteractive grouping only |
| Subtle | `#f2f2f2` | Neutral selection and user messages |
| Success / surface | `#21613b` / `#edf6ef` | Confirmed success or healthy state |
| Warning / surface | `#754900` / `#fff5df` | Uncertainty, degraded state, sensitive credentials |
| Error / surface | `#9b2828` / `#fff0ee` | Failure, offline state, high severity |

Computed WCAG contrast across all six neutral/status surfaces: primary minimum 15.86:1, secondary 6.98:1, success 6.61:1, warning 6.92:1, error 6.88:1. Border minimum 3.30:1. White text on near-black/error buttons also exceeds 4.5:1. Status text accompanies color; decorative dividers are not control boundaries.

Global focus uses a 3px near-black outline with 3px offset. Buttons, inputs, summaries, select items, and standalone navigation targets have 44px minimum dimensions. Long identifiers wrap; narrow data rows stack; dialogs and selects constrain scrolling to available space. No page-level clipping masks overflow.

## Motion contract

`frontend/src/lib/motion.ts` exports `motionDuration` (seconds: control 0.12, state 0.22, sequence 0.4), `motionEase`, `prefersReducedMotion()`, `transitionFor(reducedMotion, duration)`, and `arrive`, `reveal`, `settle` variants. Existing Framer Motion is the only motion dependency.

- `arrive`: small entrance for an actual incident/tool update, connecting new content to the current investigation.
- `reveal`: in-place visibility change for actual path/evidence data, keeping spatial relationships stable.
- `settle`: bounded result entrance, establishing a confirmed outcome without implying success before the response.
- Use `initial="hidden"`, `animate="visible"`, and `custom={Boolean(useReducedMotion())}`. Reduced-motion variants start in their final state; transitions have zero duration and zero delay. The preference helper safely handles absent `window` or `matchMedia`.
- Incident order, real topology links, tool lifecycle, and confirmed outcomes use returned application data. No stagger timers, simulated stages, fabricated telemetry, token-stream imitation, or ambient loops.
- Ordinary controls use 120ms color feedback. Legacy message CSS entrances and looping dots are removed; pending text remains. CSS reduced-motion rules remove transitions and animations immediately.

## Verification record

### Task 4: assistant and action lifecycle

- Supported assistant contract: WebSocket open reports connection progress; `ready` sends the question; `retrieval_started` reports “Searching ticket evidence and service guidance...”. `answer` supplies the complete validated answer, uncertainty, evidence flag, citations, and nullable next-best-action. `complete` alone does not establish an answer. Errors and premature close remain retryable. HTTP fallback has no retrieval-progress event.
- One activity row follows each request through pending, completed, no-evidence, or failed. Response, citations, and next action reveal together; native citation disclosure stays user-controlled. No token deltas, inferred model phases, timers, or invented tool execution.
- Proposal requests show preparing. Returned `proposed` writes become reviewable; approval starts execution. Read-only tools execute during propose: returned `succeeded`/`failed` status and summary supply the actual outcome without approval or confirmation. Proposal `confirmation_id` maps to execution correlation ID; `created_at` is the recorded timestamp used by backend execution records.
- Confirmed outcomes are immutable: replaying confirmation returns the same result. Recorded failure retains proposal details and outcome; “Retry with new proposal” explicitly requests a new proposal, archives the previous attempt, and requires new approval for writes. Read-only retry may execute during that new request. Transport failure has no known outcome, so confirmation replay remains available. Both catalog and assistant-suggested paths follow this contract.
- Tool responses carry `device_id` and `device_ref`; optional topology buttons use those IDs. Assistant document/chunk references are not device references. Incident evidence/action stages receive actual request/results only; unknown stages remain upcoming.
- Ticket/token-keyed sessions isolate local state; unmounted sessions ignore late progress/results before updating parent trace state. In-flight device execution is not represented as cancelled when leaving a ticket.
- Motion purpose: bounded message/proposal entry locates new information; in-place status transitions preserve request identity; answer-unit reveal keeps evidence attached; successful result settling occurs only after a returned execution outcome (propose for read-only, confirm for writes). Failure uses neutral reveal. Pending indicator is static, not looping. Shared variants render immediately for reduced motion.
- Presentation reuses approved type, spacing, neutral/status tokens. Wrapping activity rows preserve narrow layouts; native buttons retain focus and keyboard behavior. No new visual assets.
- Task 4 checks: 30 tests passed across ToolActivity, TroubleshootingAssistant, AgentActionsPanel (both action paths), IncidentTrace, and App. Build and `git diff --check` passed. React Router future-flag warnings and Vite's >500 kB chunk warning remain.
- Automated interaction evidence: starter and keyboard follow-up submit; citation disclosure opens on click; stream errors retain original-question retry; malformed/closed streams show failure; proposal waits for response; topology button emits real device ID; review opens dialog; cancel performs no execution; approval waits for resolution; HTTP/backend failures retain proposal; explicit retry succeeds; late proposal/execution/answer responses cannot populate another ticket.
- Delivery gate: state honesty, native controls, reduced-motion activity output, and bounded motion verified through tests/source review. Browser mobile/zoom layout and full manual click-through remain unverified; no full visual delivery-gate PASS claimed.
- Contract correction checks: 25 assistant/activity/action tests passed. Both action paths cover read-only success/failure without confirm, read-only retry through new propose, immutable failed write results, distinct proposal/confirmation IDs, fresh write approval, and retained failure history. Build passed; Vite chunk-size warning remains.
- Quality corrections: catalog “Discard proposal” clears only local pending proposal and unlocks action/target fields without confirmation. Every prepare/confirm request acquires a trace-owner generation; its reporter ignores updates after a newer operation starts. Local results remain visible regardless of trace ownership. Discard reports through its existing owner, never stealing ownership from another action.
- Tool response validation allows only `proposed`/`succeeded`/`failed` proposals and terminal execution statuses. Read-only requires no confirmation and a terminal status; stateful requires confirmation. Unknown kinds, pending statuses, and inconsistent combinations use existing unexpected-response errors.

- Historical baseline: the initial `npm test -- --run` run reported 4 files / 19 tests passed. This is superseded by the final verification below. Existing React Router v7 future-flag warnings were present.
- Existing automated coverage includes sign-in validation/routing, intake loading/errors/ticket creation, topology, cited and no-evidence answers, retry controls, action confirmation, suggested-question submission, and keyboard follow-up submission/clearing.
- Contrast: WCAG relative-luminance calculation checked primary/secondary/status colors and control borders against every neutral/status surface; all thresholds passed.
- Motion boundary check: `npx --no-install vite-node src/lib/motion.ts --check-motion` checks absent window/matchMedia, both preference values, zero-duration/zero-delay transitions, and final-state reduced-motion variants.
- Historical initial implementation verification: `npm test -- --run`, 4 files / 19 tests passed; `npm run build` passed; motion boundary check passed. Existing React Router warnings were present. Production CSS gzip size was 5.06 kB (baseline 5.24 kB); current CSS size is recorded below.
- Final verification (2026-10-12): `frontend/npm test -- --run` ran 13 files / 100 tests: 96 passed and 4 failed. Failures were in `TroubleshootingAssistant.test.tsx` for follow-up fetch counts, an unset mocked response resolver, and an unexpected fetch call. Running that file alone yielded 12 passed / 1 failed (pending follow-up fetch count); its WebSocket-focused cases passed in isolation. This indicates test/mock-order interaction and the suite is not green. React Router v7 future-flag warnings remain.
- `frontend/npm run build` passed TypeScript and Vite production compilation. Vite reports the JavaScript bundle at 560.98 kB minified (over the 500 kB warning threshold); CSS is 31.07 kB / 6.35 kB gzip. `git diff --check` passed.
- Route and interaction evidence is automated in jsdom: `App.test.tsx` covers unauthenticated direct-route redirect, technician/operator role redirects, role-specific active workspace navigation, and sign-out. `primitives.test.tsx` covers dialog Escape/focus return and keyboard select opening, selection, and close/focus return. Other feature tests cover intake processing/retry, ticket opening, topology keyboard selection, citation disclosure, and action proposal/approval lifecycle. These are not live-browser route checks.
- Responsive source audit: `styles.css` uses a single-column layout below 600px, two-column ticket lists from 600px, topology rearrangement from 720px, and ticket/sign-in split layouts from 900px. It also specifies wrapping, min-width protections, narrow-screen composer behavior, and scrolling dialogs/selects. This source inspection is not rendered viewport evidence.
- Browser verification unavailable: no browser automation namespace is available; no Chromium, Chrome, Firefox, or Playwright executable/package was found installed, and package scripts include only Vite/Vitest. Therefore actual rendering at 320px, 375px, 768px, and desktop, live app route/progress walkthrough, browser console inspection, and visual/200% zoom review were not performed. Do not treat automated jsdom tests or CSS inspection as a browser verification PASS.

### Ticket chat history and detail layout

- Conversation turns persist in `sessionStorage`, scoped by authenticated user and ticket. This keeps history through ticket navigation and refresh in the current tab without putting incident conversations into durable browser storage. Stored responses are schema-validated; a pending turn restored after interruption is marked retryable rather than replayed automatically.
- The chat panel has a viewport-bounded height, its message area owns scrolling, and the composer stays in the panel's flex layout. The scroll-to-latest control has an accessible label. This gives long multi-prompt sessions their own reading area while leaving the ticket page itself in normal document flow.
- Ticket heading and incident trace use open whitespace and hairline rules. Customer and operational context are separated by section rules instead of repeated panel boxes. The service topology keeps a clear graph boundary because its nodes and links need a defined visual field.
- Verification for this revision: frontend tests pass, 15 files / 111 tests; production build passes; scoped `git diff --check` passes. Vite continues to report the existing large JavaScript chunk warning. Browser viewport and click-through review remain unavailable, so no rendered-browser PASS is claimed.
