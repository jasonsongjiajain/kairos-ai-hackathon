# AI Operations Workspace UI/UX Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the Field Force Incident Assistant into a clear, evidence-led operations workspace with a slate foundation, blue investigation language, orange action emphasis, a complete AI chat experience, inspectable tool calls, realtime status feedback, and purposeful motion.

**Architecture:** Preserve existing API contracts, authorization, conversation persistence, topology data, audit history, redaction, and confirmed tool lifecycles. Recompose the ticket route around a task-first workspace with a dominant assistant, a connected topology view, and tabbed context panels. Extract tool-call and status presentation into reusable components so chat, topology, incident trace, and audit share one lifecycle vocabulary.

**Tech Stack:** React, TypeScript, Vite, Tailwind, existing Radix primitives, Framer Motion, `@xyflow/react`, Phosphor icons, current API clients, and `frontend/src/lib/motion.ts`.

---

## Design Read

Reading this as: a high-stakes field operations workbench for technicians and supervisors, in a calm instrument-panel visual language with slate surfaces, blue evidence signals, orange intervention signals, and motion dial `ENERGY 2 / RHYTHM 3 / MOTION 2`.

The product identity is the **incident signal path**: an issue moves from event, through ticket and topology evidence, into an assistant recommendation, then into an explicitly approved action and recorded result. Repeat that path in the layout, labels, color semantics, and transitions. Do not add generic AI decoration, fake metrics, avatars, illustrations, or ambient animated backgrounds.

## Non-Negotiable Principles

1. **Evidence before action.** Observed ticket and topology facts are visually distinct from assistant inference, recommendation, and executable action.
2. **One focal point per screen.** The active investigation is primary. Context is available without competing with the conversation.
3. **State is explicit.** Every async surface shows text plus an icon or structural cue for loading, empty, success, no evidence, approval, failure, and unknown state.
4. **No hidden execution.** A proposed write action is never represented as running until the backend confirms execution has started. A read-only call shows its returned result, not a fabricated progress story.
5. **Motion explains causality.** New evidence arrives into the evidence stream, the selected topology target connects to the action, and the final result settles only after the API response. No looping animation is decorative.
6. **Mobile is a deliberate mode.** The assistant remains first in reading order, topology and context become tabs or stacked sections, and the composer stays reachable above the mobile keyboard.

## Scope Map

### Create

- `frontend/src/components/ai/tool-call.tsx`: shared tool-call shell, lifecycle header, target, parameters, evidence, result, approval region, and retry affordance.
- `frontend/src/components/ai/status.tsx`: shared status icon and accessible status label primitives.
- `frontend/src/components/ui/tabs.tsx`: keyboard-accessible tabs, if an equivalent primitive is not already available.
- `frontend/src/features/work/TicketWorkspaceTabs.tsx`: ticket context tab model and panel composition.
- `frontend/src/features/assistant/ToolCallTimeline.tsx`: ordered tool-call timeline for a conversation turn.
- `frontend/src/features/assistant/AssistantEvidenceSummary.tsx`: observed, inferred, and recommended summary inside answers.
- `frontend/src/features/topology/TopologyInspector.tsx`: selected-device inspector with facts, relationship, state, and action linkage.
- `frontend/src/features/audit/AuditEventRow.tsx`: reusable audit event presentation aligned with tool-call states.
- `frontend/src/features/work/uiux-revamp.css`: scoped workspace layout and visual rules during migration.
- `frontend/src/features/work/uiux-revamp.test.tsx`: tab, lifecycle, and responsive-safe structure tests.

### Modify

- `frontend/src/styles.css`: slate, blue, and orange semantic tokens; preserve focus, density, and contrast guarantees.
- `frontend/src/lib/motion.ts`: lifecycle and tab transitions with reduced-motion support.
- `frontend/src/features/work/TicketPage.tsx`: new ticket shell, tabs, topology, assistant, context, and audit composition.
- `frontend/src/features/assistant/TroubleshootingAssistant.tsx`: complete conversation anatomy, evidence summary, tool timeline, and assistant states.
- `frontend/src/features/assistant/AgentActionPlan.tsx`: shared tool-call model while retaining permission and confirmation behavior.
- `frontend/src/features/assistant/ActionProposal.tsx`: action review hierarchy, target, risk, parameters, expected impact, and approval.
- `frontend/src/features/assistant/ToolActivity.tsx`: compact lifecycle row or shared timeline delegate.
- `frontend/src/features/assistant/ToolExecutionResult.tsx`: shared result, failure, retry, and immutable outcome language.
- `frontend/src/features/topology/TopologyPath.tsx`: selected-device inspector and action linkage.
- `frontend/src/features/work/IncidentTrace.tsx`: shared status semantics tied to real request ownership.
- `frontend/src/features/audit/AuditPage.tsx`: shared event row language.
- `frontend/src/features/work/CustomerServiceSummary.tsx`, `EntityFactsPanel.tsx`, and `SensitiveCredentialReveal.tsx`: context tabs, labels, grouping, and deliberate reveal feedback.
- Existing assistant, work, topology, and primitive tests: update composition expectations without weakening lifecycle assertions.

### Do not change in this UI pass

- Backend authorization, execution, audit persistence, retrieval, and assistant contracts.
- API request shapes unless a test exposes an existing contract mismatch.
- Conversation storage schema and sensitive-data redaction rules.

## Visual System

### Palette

Slate is the base, blue is evidence and navigation, and orange is intervention. These are semantic roles, not decoration.

| Token | Initial value | Use | Reason |
| --- | --- | --- | --- |
| `--canvas` | `#eef2f6` | app background | Separates the work plane from white content without texture. |
| `--surface` | `#ffffff` | chat, cards, inspectors | Maximizes reading contrast for dense operational content. |
| `--slate-950` | `#17212b` | shell, primary text, primary action | Grounds the workbench and creates hierarchy. |
| `--slate-700` | `#334454` | secondary text and dark labels | Keeps metadata legible without competing with task content. |
| `--slate-300` | `#b8c4cf` | borders and topology structure | Defines boundaries without making every surface float. |
| `--slate-100` | `#e8edf2` | muted fills and inactive tabs | Provides a neutral selected or disabled state. |
| `--blue-700` | `#1559a6` | evidence, active nav, links, selected topology | Blue means information that helps understand the incident. |
| `--blue-050` | `#edf5ff` | evidence surfaces | Gives citations and observations a stable field. |
| `--orange-700` | `#a94708` | action, approval, intervention | Orange marks a decision or change affecting the network. |
| `--orange-050` | `#fff3e8` | proposal surfaces | Separates intervention from evidence without implying failure. |
| existing success, warning, error tokens | verified current values | health and terminal outcomes | Retain their meanings and pair with text. |

Do not use blue and orange on every component. A screen has one dominant semantic accent at a time. Do not introduce gradients, glows, decorative dots, glassmorphism, or meaningless colored stripes.

### Typography and density

- Keep `Avenir Next` or `Segoe UI` for controls and operational text because the existing app is tuned for field legibility.
- Keep the editorial serif only for the ticket problem statement or sign-in statement, not data labels or tool names.
- Use sentence-case labels. Avoid wide-tracked all-caps except the existing small application context label.
- Use tabular numerals only for real IDs, timestamps, counts, and durations.
- Keep the existing 4/8/12/16/24/32/48px spacing scale, 12px panels, 6px controls, and 2px status markers.
- Use flat surfaces by default. Elevation belongs to dialogs, menus, and the mobile composer only.

### Status vocabulary

| State | Visible label | Meaning |
| --- | --- | --- |
| `queued` | Queued | Request exists but has not started. |
| `searching` | Checking evidence | Retrieval or planning is active. |
| `running` | Running | Backend tool execution is active. |
| `needs-approval` | Needs approval | Write proposal is ready and has not run. |
| `completed` | Completed | Backend returned a successful result. |
| `no-evidence` | No matching evidence | Request completed without a grounded source match. |
| `failed` | Failed | Backend returned a known failure. |
| `unknown` | Outcome not confirmed | Transport ended before the result was known. |
| `rejected` | Not approved | Technician declined the proposal. |

Never communicate these states with color alone.

## Information Architecture

### Application shell

1. Compact shell header: product context, workspace route, role, and sign-out.
2. Ticket header: incident title, severity, ticket status, assignment, source event, and audit link.
3. Incident path strip: Event, Ticket, Topology, Evidence, Action. Each stage reflects a real backend or user state.
4. Main workbench: assistant conversation as the primary pane, topology as a persistent secondary pane on wide screens.
5. Context tabs: `Overview`, `Services`, `Devices`, `Facts`, `Audit` below the workbench or in mobile reading order.

The ticket page must answer three questions in order: what is wrong, what evidence supports the diagnosis, and what can I safely do next?

### Tab behavior

- `Overview`: customer summary, incident synopsis, top evidence, and next recommended step.
- `Services`: HSI, VoBB, IPTV, Wi-Fi, and other service records with clear labels and status.
- `Devices`: device records and the same topology inspector used by the canvas.
- `Facts`: verified entity facts and source or timestamp when provided by the API.
- `Audit`: event processing, sensitive reveal, proposal, approval, execution, and outcomes.
- The active tab is a filled slate tab, not only an underline. A small blue indicator is allowed only on the active tab because it communicates location.
- Use native button semantics, `role=tablist`, `role=tab`, `aria-selected`, roving keyboard focus, and `role=tabpanel` with an accessible label.
- Keep selection local to the ticket session unless URL persistence already fits the route cleanly. Default to `Overview`.

### Responsive composition

- Wide: flexible grid, assistant 7 columns, topology 5 columns. Context remains below the active investigation.
- Intermediate: assistant and topology stack, with assistant first.
- Mobile: ticket header, incident path, assistant, topology, context tabs, audit link.
- On mobile, topology is bounded with a visible `Inspect device` action and inspector below the canvas. Never rely on hover.
- Context tabs wrap or use a contained horizontal tablist with visible focus and no page-level horizontal overflow.
- The composer uses safe-area bottom padding and scrolls into view when focused.
- All controls remain at least 44px high with at least 8px between adjacent targets.

## Complete AI Chat Experience

### Conversation anatomy

Each turn has this sequence:

1. User question, with a timestamp only when backend data provides one.
2. Assistant evidence header with state label.
3. Evidence trace showing retrieval, matched sources, or no evidence.
4. Answer sections: `Observed`, `Likely cause`, `Recommended next check`, and uncertainty only when returned data supports them.
5. Sources disclosure with citation title, section, and evidence reference.
6. Tool-call timeline when the assistant proposes or executes an action.
7. Next best action or follow-up prompt based on returned data.

Do not expose hidden chain-of-thought. Present concise, inspectable evidence and rationale only.

### States

- Empty: explain the assistant is scoped to the active ticket and offer three real starter questions tied to current incident data.
- Loading: show `Checking ticket evidence` and the current stream message. Keep the question visible.
- Error: identify request, stream, or validation failure. Keep the original question and provide `Retry this question`.
- No evidence: state that no indexed procedure matched. Never style an unsupported answer as verified.
- Closed or offline stream: show `Outcome not confirmed`, retain retry, and do not invent completion.

### Composer

- Multiline textarea helper: `Ask about this ticket, service, topology, or next check.`
- `Enter` inserts a newline. `Ctrl+Enter` and `Cmd+Enter` submit.
- Submit label changes from `Ask assistant` to `Checking evidence` while pending.
- Disable only for empty input, a request that cannot safely be concurrent, or known permission failure. Explain disabled state nearby when relevant.
- Suggested prompts are buttons in the empty state and disappear after the first question.

## Tool-Call Component System

### Shared anatomy

`ToolCall` has these regions:

- Header: relevant icon, human-readable title, lifecycle label, and correlation ID when available.
- Intent: why the call is relevant to the ticket.
- Target: device name, device reference, service reference, and `View in topology` when a real device ID exists.
- Parameters: labeled values, redacted where required, never raw secrets.
- Evidence: citations or structured observations supporting the call.
- Expected impact: read-only check versus state-changing action, with backend risk tier.
- Approval: `Approve and run`, `Decline`, or `Review proposal` only when confirmation is required.
- Result: returned status, message, updated device status when returned, and audit link when available.
- Retry: `Retry with new proposal` for a new attempt, never an implicit replay of a failed write.

### Variants

- `ToolCallCompact`: one-row status inside the assistant evidence stream.
- `ToolCallExpanded`: full review for proposals and completed actions.
- `ToolCallTimeline`: ordered collection for multiple calls in one turn.
- `ToolExecutionResult`: immutable terminal result linked to its proposal.
- `ToolCallInlineTarget`: topology-linked target that selects an actual device ID.

### Lifecycle rules

- Read-only: `queued` to `running` to `completed` or `failed` from actual API results.
- Write: `queued` to `needs-approval`, then `running` after approval, then `completed`, `failed`, or `unknown`.
- Failed and unknown results remain history. Retrying creates a new visible attempt.
- Proposal and execution IDs remain distinct where they help auditability.
- Do not show staged progress unless the backend emits those stages. Existing simulated stages must be labeled as backend-provided progress if retained; otherwise show one truthful `Running` state until response.
- A toast is never the only result channel. The result stays attached to its tool call and is announced in a live region.

## Realtime Tool-Call Motion

| Moment | Purpose | Implementation | Values |
| --- | --- | --- | --- |
| New call enters timeline | Spatial consistency | Framer Motion `arrive` on call shell | Existing 8px translate, 220ms ease-out. |
| Status changes | State indication | Opacity and color transition in status region | 120ms CSS transition, no layout animation. |
| Evidence expands | Prevent a jarring change | Disclosure behavior with opacity for content | 180ms maximum, instant under reduced motion. |
| Active topology target | State indication | Existing packet edge and target highlight tied to `running` | Only while real action is running; pause under reduced motion or user pause. |
| Successful result | State indication | `settle` after returned success | Existing 0.98 to 1 scale and opacity, 220ms. |
| Failed or unknown result | State indication | Neutral reveal | 220ms opacity only. |
| Tab selection | Spatial consistency | CSS active-state transition or small indicator transform | 120ms, never delays content. |

Use transform and opacity for motion. Do not animate width, margin, padding, top, left, box-shadow, or inherited CSS variables. Do not add perpetual pulses, typing simulations, fake token streaming, parallax, or animation on every message.

Reuse `useReducedMotion`, `transitionFor`, `arrive`, `reveal`, and `settle` from `frontend/src/lib/motion.ts`. Use CSS transitions for tabs and button feedback. Do not set React state from `requestAnimationFrame`. Verify the busiest state with browser performance tools or throttling and distinguish code evidence from browser evidence.

## Topology Experience

- Keep the real React Flow path and actual edge relationships.
- Use the same status labels and tones as tool calls.
- Selecting a device opens `TopologyInspector` with type, reference, status, connected services, facts, and linked action attempt.
- `View in topology` selects and focuses a real device ID. A document chunk ID never selects a device.
- Running actions highlight only the actual target node and adjacent real edges.
- Update a node only from returned execution outcome. Failure or unknown never optimistically marks it healthy.
- Keep `Pause network activity` as a real control for decorative packet movement, with a text label and reduced-motion behavior. Never present packet travel as telemetry.
- Empty topology explains no path is available. Loading names the service path. Error provides `Retry service path`.

## Labels and Copy

- Prefer: `Evidence`, `Observed`, `Recommended check`, `Target device`, `Expected impact`, `Needs approval`, `Execution result`, `Audit history`.
- Avoid generic AI marketing language, unexplained acronyms, decorative emoji, and claims absent from returned data.
- Risk labels describe consequence: `Read-only check`, `Changes device state`, `High impact`, not vague labels such as `Smart action`.
- Include the next meaningful action where one exists: `Needs approval: review target and parameters` or `Failed: retry with a new proposal`.

## Accessibility and Resilience

- Maintain WCAG AA text contrast and 3:1 non-text contrast for boundaries, focus, selected tabs, topology selection, and status icons. Run `/Users/adibo/.agents/skills/antislop-human/contrast-check.py` for every new token pairing.
- Keep `:focus-visible` at 3px with 3px offset. Test tabs, topology nodes, disclosures, dialogs, selects, composer, approval, decline, retry, and audit links with keyboard only.
- Pair every color with text, icon, or structure. Orange means intervention or approval, never error by itself.
- Give every data view empty, loading, error, permission-denied, and terminal states where applicable.
- Preserve redaction. Credentials never appear in chat history, tool parameters, citations, audit payloads, or logs.
- Support 200% text zoom without clipping. Avoid page-level `overflow: hidden`; bounded scrolling is limited to conversation and topology where necessary.
- Keep the composer above the mobile keyboard with safe-area padding.

## Task Breakdown

### Task 1: Establish design tokens and semantic primitives

**Files:** `frontend/src/styles.css`, `frontend/src/lib/motion.ts`, create `frontend/src/components/ai/status.tsx`, create `frontend/src/components/ui/tabs.tsx` if needed.

- [ ] Add slate, blue, and orange tokens plus verified neutral/status aliases. Remove ad hoc colors from redesigned selectors.
- [ ] Implement `Status` with text label, relevant Phosphor icon, and `role=status` only for live updates.
- [ ] Implement tabs with Radix keyboard semantics, focus behavior, and responsive overflow handling.
- [ ] Add lifecycle variants without breaking existing consumers.
- [ ] Add primitive tests for tab movement, selected state, panel association, and status visibility.
- [ ] Run `npm test -- --run src/components/ui/primitives.test.tsx src/features/work/uiux-revamp.test.tsx` from `frontend`.

### Task 2: Build the shared tool-call surface

**Files:** create `frontend/src/components/ai/tool-call.tsx`, create `frontend/src/features/assistant/ToolCallTimeline.tsx`, modify `ToolActivity.tsx`, `ActionProposal.tsx`, and `ToolExecutionResult.tsx`.

- [ ] Define a typed view model from existing proposal, execution, action state, target device, evidence, and callbacks without changing API types.
- [ ] Render compact and expanded states from one lifecycle mapping.
- [ ] Add labeled parameters, target linking, approval controls, terminal result, retry behavior, and redaction-safe rendering.
- [ ] Replace duplicated pending/result markup with the shared surface.
- [ ] Test read-only success/failure, write proposal, declined proposal, approved success, immutable failed write, unknown outcome, and retry-as-new-attempt.
- [ ] Run assistant action tests and confirm authorization and confirmation assertions remain green.

### Task 3: Recompose the assistant conversation

**Files:** `TroubleshootingAssistant.tsx`, create `AssistantEvidenceSummary.tsx`, create or modify `ToolCallTimeline.tsx`, relevant assistant CSS.

- [ ] Keep stored turns and stream ownership unchanged.
- [ ] Implement the conversation anatomy above with separate labels for evidence, answer, citations, and action.
- [ ] Preserve original-question retry, citation disclosure, credential separation, and late-response isolation.
- [ ] Add live announcements for retrieval start, terminal answer, tool result, and stream failure without duplicate announcements.
- [ ] Test empty, searching, evidence answer, no-evidence answer, answer failure, stream closure, citation expansion, and composer keyboard submission.

### Task 4: Build ticket tabs and context hierarchy

**Files:** `TicketPage.tsx`, create `TicketWorkspaceTabs.tsx`, `CustomerServiceSummary.tsx`, `EntityFactsPanel.tsx`, `SensitiveCredentialReveal.tsx`, `AuditPage.tsx`, scoped CSS.

- [ ] Move existing context content into five real tabs without duplicate fetching.
- [ ] Keep Overview default and give each tab meaningful empty/loading/error states.
- [ ] Keep sensitive credential reveal deliberate, audited, and outside the transcript.
- [ ] Make Audit use shared status and event vocabulary.
- [ ] Test selection, keyboard navigation, context rendering, denied content, and credential feedback.

### Task 5: Connect topology and tool-call targeting

**Files:** `TopologyPath.tsx`, create `TopologyInspector.tsx`, `TicketPage.tsx`, `PacketEdge.tsx`, topology tests.

- [ ] Add inspector for hover, keyboard focus, and persistent selection, with tap-first behavior on mobile.
- [ ] Wire tool-call target actions to `onSelectDevice` using actual device IDs.
- [ ] Tie active node and edge motion to real action ownership and lifecycle.
- [ ] Preserve pause, reduced motion, keyboard selection, disconnected edge treatment, and no optimistic success.
- [ ] Test selection, target linking, running, success, failure, and missing topology data.

### Task 6: Apply responsive composition and visual polish

**Files:** `frontend/src/styles.css`, create `frontend/src/features/work/uiux-revamp.css`, all touched components.

- [ ] Implement content-driven wide, intermediate, and narrow layouts.
- [ ] Verify assistant-first order, bounded topology, tab behavior, safe-area composer spacing, and no horizontal overflow.
- [ ] Use flat slate and white surfaces, limited shadows, semantic blue/orange accents, and no generic background decoration.
- [ ] Confirm labels wrap, IDs do not force width, dialogs/selects remain usable, and targets meet 44px minimums.
- [ ] Test 320px, 375px, 768px, 1024px, wide desktop, and 200% text zoom.

### Task 7: Verification and delivery gate

**Files:** all changed frontend files and tests.

- [ ] Run `npm test -- --run` from `frontend`.
- [ ] Run `npm run build` from `frontend`.
- [ ] Run `git diff --check` from repository root.
- [ ] Run `npx --no-install vite-node src/lib/motion.ts --check-motion` from `frontend`.
- [ ] Run contrast checks for all new slate, blue, orange, status, surface, border, and focus pairings.
- [ ] Complete keyboard click-through for tabs, disclosures, selects, topology, submit, retry, review, decline, approval, audit, credential reveal, and sign-out.
- [ ] Walk through empty, loading, no evidence, denied, stream failure, pending, approval, success, failed, unknown, and new-attempt retry states.
- [ ] Complete responsive walkthrough with no horizontal overflow and no composer occlusion.
- [ ] Record browser-tested findings separately from source/test-confirmed findings. Do not claim a visual browser PASS without a browser run.

## Acceptance Criteria

- The ticket screen has one focal point, the active assistant investigation, while topology and context remain easy to reach.
- Slate, blue, and orange have distinct meanings: slate anchors the workspace, blue identifies evidence/navigation, orange identifies intervention/approval.
- A technician can see the path from question to evidence to proposed tool call to returned result without a hidden workflow.
- Every tool call shows target, parameters, intent, impact, approval requirement, lifecycle, and terminal result when available.
- Realtime status is honest: no invented token stream, fake telemetry, optimistic recovery, or unknown outcome presented as success.
- Tabs improve scanning without hiding critical status or blocking the first investigation step.
- Topology selection and tool-call target selection stay synchronized through actual device IDs.
- All async/data views have informative empty, loading, error, permission, and terminal states.
- All interactions work with keyboard and touch, have visible focus, and meet contrast and target-size requirements.
- Motion is bounded, purposeful, reduced-motion aware, and limited to transform, opacity, and justified disclosure behavior.
- Existing authorization, audit, redaction, conversation persistence, and immutable execution behavior remain intact.

## Anti-Slop Delivery Gate

- [ ] No em dash in newly authored UI copy or documentation outside rule documentation.
- [ ] No generic gradients, full-page glows, decorative grids, glassmorphism, fake metrics, fake people, avatars, or generic illustrations.
- [ ] No dead navigation, dead controls, decorative status dots, or badges without a real status meaning.
- [ ] Every major design decision has a one-line purpose in this plan.
- [ ] Every interaction has real behavior and a test or click-through record.
- [ ] Every new number comes from real returned data or is omitted.
- [ ] Every new status is text plus a non-color cue.
- [ ] Every motion has a named purpose, bounded duration, and reduced-motion path.
- [ ] Mobile and 200% zoom behavior are verified before delivery.
- [ ] The final implementation is reviewed as a field operations product, not a generic AI dashboard.
