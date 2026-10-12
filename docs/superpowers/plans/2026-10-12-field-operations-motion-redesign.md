# Field Operations Motion Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the field operations frontend as a distinctive white-and-black shadcn-style workspace whose motion clarifies incident progress, topology, assistant tool calls, and results.

**Architecture:** Preserve the React/Vite routes, API contracts, authorization behavior, and existing feature components. Add a shared motion language and semantic visual tokens, then apply them in vertical slices: workspace shell, incident trace, topology selection/reveal, assistant tool lifecycle, and action outcomes. Use the existing Framer Motion dependency for component transitions and add GSAP only if a coordinated SVG sequence cannot be implemented cleanly with the existing library.

**Tech Stack:** React 18, TypeScript, Vite, Tailwind CSS, Radix/shadcn-style primitives, Framer Motion, optional GSAP for bounded SVG choreography, Phosphor icons, Vitest, React Testing Library.

---

## Product and interaction constraints

- Keep the app light-only for this brief: white/near-white surfaces, near-black text, neutral borders, and semantic status colors only. Do not add a theme toggle.
- Keep the product flow real: operator intake, assigned work, ticket investigation, real topology, grounded answers/citations, proposed actions, explicit approval, execution result, and audit.
- Tool states must be driven by actual request/backend states. Never animate or label an action completed before its response confirms completion.
- The current assistant endpoint streams retrieval progress and a final structured answer, not token deltas. Animate only the reported progress and actual final response.
- Respect `prefers-reduced-motion`, keyboard operation, WCAG AA contrast, mobile layout, and existing empty/loading/error/denied states.
- Motion dials: **ENERGY 2 / RHYTHM 2 / MOTION 3 for explicitly choreographed incident/tool/topology moments**, while ordinary controls remain restrained. This is a motion-forward interface, not a continuously animated one.
- Motion decisions: incident trace reveals workflow sequence; topology path reveal teaches spatial relationships; tool lifecycle animation communicates request/result state; result entrance establishes resolution. No ambient loops, fake telemetry, simulated tool stages, or decorative movement.

## File map

| File | Responsibility |
|---|---|
| `frontend/src/styles.css` | Existing global/application styles; replace conflicting legacy color/radius rules with the new white/black tokens and responsive visual system. |
| `frontend/src/lib/motion.ts` | Shared durations, easings, reduced-motion-aware transition helpers, and variant definitions used across features. |
| `frontend/src/features/work/IncidentTrace.tsx` | Real incident workflow path from event through ticket, topology, evidence, and action/result. |
| `frontend/src/features/work/IncidentTrace.test.tsx` | Workflow rendering, current/completed state semantics, and reduced-motion checks. |
| `frontend/src/features/work/TicketPage.tsx` | Mount trace in ticket context and coordinate selected topology entity from assistant references where available. |
| `frontend/src/features/topology/TopologyPath.tsx` | Accessible topology rendering, stable node identity, node selection, and real path emphasis. |
| `frontend/src/features/topology/TopologyPath.test.tsx` | Topology sequence, selection, text alternative, and reduced-motion behavior. |
| `frontend/src/features/assistant/TroubleshootingAssistant.tsx` | Extend turn model to represent real retrieval/tool activity and render result transitions in place. |
| `frontend/src/features/assistant/ToolActivity.tsx` | Inline, accessible tool activity row with pending, completed, needs-approval, no-evidence, and failed states. |
| `frontend/src/features/assistant/ToolActivity.test.tsx` | State semantics, announcements, and motion preference behavior. |
| `frontend/src/features/assistant/ChatMessage.tsx` | Consistent message entrance treatment and stable message layout. |
| `frontend/src/features/assistant/ActionProposal.tsx` | Distinct entrance and hierarchy for proposal details and approval affordance. |
| `frontend/src/features/assistant/ToolExecutionResult.tsx` | In-place result reveal for confirmed execution outcome. |
| `frontend/src/features/assistant/AgentActionsPanel.tsx` | Animate proposal/execution lifecycle using actual state transitions. |
| `frontend/src/features/intake/EventIntakeQueue.tsx` | Queue state transitions and ticket-created confirmation motion. |
| `frontend/src/features/intake/ProcessEventButton.tsx` | Processing-state visual transition tied to request lifecycle. |
| `frontend/src/features/work/AssignedWorkList.tsx` | Queue-to-ticket navigation continuity and list empty/loading/error presentation. |
| `frontend/src/features/audit/AuditTimeline.tsx` | Subtle insertion/reveal of actual audit records. |
| `frontend/src/features/audit/AuditTimeline.test.tsx` | Audit entry order/content and reduced-motion reveal behavior. |
| `frontend/src/app/App.tsx` | Workspace shell navigation/layout and route transitions without changing route semantics. |
| `frontend/src/app/App.test.tsx` | Route/shell regression coverage if shell behavior changes. |
| `frontend/src/features/assistant/TroubleshootingAssistant.test.tsx` | Retrieval, answer, no-evidence, retry, and tool activity lifecycle coverage. |
| `frontend/src/features/intake/EventIntakeQueue.test.tsx` | Intake lifecycle transition regression coverage. |
| `docs/ui-design.md` | Replace prior visual direction with approved white/black system and motion rationale. |

Create tests beside the components following the existing feature test convention. Do not generate logos, avatars, people, or PNG/SVG artwork as part of the implementation without explicit approval. Use the real topology visualization as the visual asset.

---

## Task 1: Establish the white/black visual and motion foundation

**Files:** Modify `frontend/src/styles.css`, `frontend/tailwind.config.ts`, `docs/ui-design.md`; create `frontend/src/lib/motion.ts`.

- [ ] **Step 1: Record the current frontend baseline**

Run from `frontend/`:

```bash
npm test -- --run
npm run build
```

Expected: existing tests pass and the production build succeeds before visual changes.

- [ ] **Step 2: Define shared motion constants and variants**

Create `frontend/src/lib/motion.ts` with typed timing and easing constants. Include short control feedback, state transitions, and bounded choreographed sequences. Export helpers that return immediate transitions when `window.matchMedia('(prefers-reduced-motion: reduce)').matches` is true; guard `window` for test/SSR safety.

Required exports: `motionDuration`, `motionEase`, `prefersReducedMotion()`, `transitionFor(reducedMotion, duration)`, and reusable variants for `arrive`, `reveal`, and `settle`. Avoid infinite/repeating variants.

- [ ] **Step 3: Define semantic monochrome tokens**

Update Tailwind/theme tokens and CSS variables for page background, surface, elevated surface, primary/secondary text, border, focus, and semantic success/warning/error states. Use white or warm-white canvas, near-black foreground, and neutral grays. Keep severity colors semantic and pair them with text. Do not retain deep green as a general brand/action accent from the old direction.

- [ ] **Step 4: Replace conflicting legacy styles**

Refactor `styles.css` token values and remove appended overrides that contradict the new visual language. Preserve current component selectors and working layouts while standardizing radius, focus ring, spacing, and transition values. Ensure no normal-text pair falls below 4.5:1 and large text pairs meet 3:1.

- [ ] **Step 5: Document the direction and reasons**

Rewrite `docs/ui-design.md` to state the white/black direction, the incident-trace identity motif, motion dials, and the purpose of each major motion sequence. Record that the product is light-only for this brief and that no logo/image assets are assumed.

- [ ] **Step 6: Verify foundation**

Run `npm test -- --run && npm run build` from `frontend/`.

Expected: tests and build pass; current routes and API behavior remain unchanged.

---

## Task 2: Add the incident trace motion motif

**Files:** Create `frontend/src/features/work/IncidentTrace.tsx`, `frontend/src/features/work/IncidentTrace.test.tsx`; modify `frontend/src/features/work/TicketPage.tsx` and `frontend/src/styles.css`.

- [ ] **Step 1: Write failing rendering tests**

Test that the trace renders the real sequence labels (Event, Ticket, Topology, Evidence, Action), marks the current/available states with accessible text, and does not assert decorative implementation details. Test that completed action state is not shown until the caller passes a confirmed outcome.

- [ ] **Step 2: Implement the trace component**

Define a typed stage model with `id`, `label`, `state` (`complete | current | upcoming | blocked`), and optional `detail`. Render semantic ordered-list markup. Current ticket detail begins with event/ticket context available and later stages reflect evidence/action state supplied by the parent. Do not imply evidence or action completion merely because the screen loaded.

- [ ] **Step 3: Animate the trace as a one-time bounded sequence**

Use Framer Motion to draw/reveal the connector and stage markers in reading order on first mount. Completed/current/upcoming styles remain distinct after entrance. Skip entrance sequencing for reduced motion. Do not replay the sequence on every rerender.

- [ ] **Step 4: Mount trace in ticket workflow**

Add `IncidentTrace` to `TicketPage.tsx` near the ticket heading and before detailed investigation surfaces. Feed only real ticket/event state already present in loaded detail. Where evidence/action data is not yet known, label the stage as upcoming rather than inventing progress.

- [ ] **Step 5: Verify trace behavior**

Run `npm test -- --run src/features/work/IncidentTrace.test.tsx` and `npm run build`.

Expected: state labels and order pass, no false-completion state is rendered, and reduced motion removes the staged entrance.

---

## Task 3: Make network topology a meaningful animated interaction

**Files:** Modify `frontend/src/features/topology/TopologyPath.tsx`, `frontend/src/features/work/TicketPage.tsx`, and `frontend/src/styles.css`; create or update `frontend/src/features/topology/TopologyPath.test.tsx`.

- [ ] **Step 1: Add tests for actual topology and interaction**

Test the service path text alternative, all real node names/statuses, selectable node behavior, selected-state accessibility, and stable rendering when selection changes. Test that the non-animated/reduced-motion path exposes identical data.

- [ ] **Step 2: Add stable selection and path mapping**

Add optional controlled props `selectedDeviceId?: string` and `onSelectDevice?: (deviceId: string) => void` to `TopologyPath`. Keep existing usage valid. Make nodes keyboard-operable buttons only when selection is enabled; otherwise preserve static semantic list items. Associate each connection with its real source/target edge.

- [ ] **Step 3: Add a one-time topology reveal**

Use Framer Motion for a short sequential node/link reveal in the actual path order. Build connections from actual edges; do not fabricate a path when edge data is missing. Keep positions fixed and stop all entrance motion after initial reveal. Reduced-motion mode renders the final diagram immediately.

- [ ] **Step 4: Add focus-to-node emphasis**

When `selectedDeviceId` changes due to a user selection or a real assistant/tool reference, transition only that node and its connected path. Use a temporary emphasis that settles without a pulse or loop. Expose selection in text/ARIA state, not solely with color or animation.

- [ ] **Step 5: Integrate topology selection with ticket context**

Pass selected device state from `TicketPage` to `TopologyPath`. Keep selection stable while switching focus between context and assistant; do not change actual topology/backend data.

- [ ] **Step 6: Verify topology**

Run `npm test -- --run src/features/topology/TopologyPath.test.tsx` and `npm run build`.

Expected: selection and text alternative tests pass, topology state is real-data-driven, and reduced motion preserves the full diagram.

---

## Task 4: Give assistant tool calls and results a clear motion lifecycle

**Files:** Create `frontend/src/features/assistant/ToolActivity.tsx` and test; modify `TroubleshootingAssistant.tsx`, `ChatMessage.tsx`, `AgentActionsPanel.tsx`, `ActionProposal.tsx`, `ToolExecutionResult.tsx`, assistant tests, and `styles.css`.

- [ ] **Step 1: Inspect current assistant stream event contract**

Read `frontend/src/lib/api/assistant.ts` and existing tests. Use only event names/data actually emitted by the current API. Record the currently supported retrieval-progress message and final answer shape in the implementation. Do not add fake model/tool phases to presentation state.

- [ ] **Step 2: Test `ToolActivity` state rendering**

Create tests for pending, completed, needs-approval, no-evidence, and failed labels, accessible live status, and nonanimated reduced-motion output. Keep states typed; do not infer completion from elapsed time.

- [ ] **Step 3: Implement inline tool activity component**

Build an inline activity row with an actual state label, tool/action description, and compact progress affordance only while pending. Animate entry and state transition in place using shared motion helpers. Add `aria-live="polite"` to status text; avoid announcing every decorative frame.

- [ ] **Step 4: Connect current assistant progress honestly**

Extend the assistant turn model so the actual retrieval progress event renders in the activity row. The final structured answer transitions the same row to a completed result and reveals the answer beneath it. No token-stream imitation. If a future API emits tool events, add a typed adapter from those real frames; until then, do not render tool names as if execution occurred.

- [ ] **Step 5: Animate answer and citations as one result unit**

Use an in-place reveal for the response, citations, and next-best-action. Keep citation expansion user-controlled. Avoid cascading entrances for every paragraph or citation. Preserve retries and the original question on error.

- [ ] **Step 6: Animate action proposal and confirmed execution**

Use real `AgentActionsPanel` states (`preparing`, `proposed`, `executing`, `done`) as the animation source. Reveal the proposal only after API success, preserve it if execution fails, transition to executing only after user confirms, and show result only after `confirmTool` resolves. Do not present a success animation on error or dialog cancel.

- [ ] **Step 7: Verify assistant lifecycle**

Run `npm test -- --run src/features/assistant/ToolActivity.test.tsx src/features/assistant/TroubleshootingAssistant.test.tsx` and `npm run build`.

Expected: actual progress, result, error, retry, proposal, approval, and execution states pass with no fabricated intermediate stages.

---

## Task 5: Apply state-aware motion to event intake, work list, and audit

**Files:** Modify `frontend/src/features/intake/EventIntakeQueue.tsx`, `ProcessEventButton.tsx`, `frontend/src/features/work/AssignedWorkList.tsx`, `frontend/src/features/audit/AuditTimeline.tsx`, related tests, and `styles.css`.

- [ ] **Step 1: Add/adjust tests for intake transition outcomes**

Cover idle-to-processing, confirmed ticket creation, duplicate/already-processed response, and failure. Assert labels and real destination links, not animation frame timing.

- [ ] **Step 2: Animate event processing in place**

Change the event row/button from idle to labeled processing without moving unrelated queue content. On API success, reveal the actual ticket confirmation and link. On failure, reveal retry/error in place. Respect reduced motion.

- [ ] **Step 3: Preserve work-list spatial continuity**

Apply restrained entrance/exit transitions to actual ticket rows when data loads or filters change. Keep keyboard focus stable; do not animate rows on every rerender. Empty/loading/error states remain visible and specific.

- [ ] **Step 4: Reveal real audit entries without implying live activity**

Use a one-time, short transition when actual audit data loads. No polling indicator, fake activity, looping animation, or invented actor/event. Preserve chronology and screen-reader order.

- [ ] **Step 5: Verify cross-screen states**

Run `npm test -- --run src/features/intake/EventIntakeQueue.test.tsx src/features/work/AssignedWorkList.test.tsx src/features/audit/AuditTimeline.test.tsx`. Create assigned-work and audit timeline test files if absent, following the component contracts described above. Then run all frontend tests and build.

Expected: real server states map to visible outcomes; reduced-motion behavior remains complete.

---

## Task 6: Finish app shell and shadcn visual consistency

**Files:** Modify `frontend/src/app/App.tsx`, `frontend/src/styles.css`, shared components under `frontend/src/components/ui/`, and relevant app tests.

- [ ] **Step 1: Audit routes and interaction destinations**

Keep current route structure and role access. Ensure each shell navigation item maps to an existing route, and do not invent pages or sections.

- [ ] **Step 2: Establish the operations shell hierarchy**

Apply a restrained white/black header and workspace frame. Prioritize app identity, role/context, active workspace, and sign-out. Use text labels with icons only when useful. Maintain clear responsive navigation and minimum 44px touch targets.

- [ ] **Step 3: Normalize shared primitives**

Bring Button, Input, Textarea, Select, Badge, Card, and Dialog into token alignment: consistent focus-visible treatment, semantic variants, restrained radius, high-contrast disabled/error states, and predictable hover/active behavior. Preserve Radix accessibility behavior.

- [ ] **Step 4: Add route transition only if it preserves context**

Use a short crossfade for route content where it does not disrupt browser navigation or focus. Do not animate the persistent shell or delay content. Ensure reduced-motion routes render immediately.

- [ ] **Step 5: Verify shell and primitives**

Run `npm test -- --run src/app/App.test.tsx` and full `npm test -- --run && npm run build`.

Expected: no route/role regressions; keyboard focus and navigation remain functional.

---

## Task 7: Accessibility, responsive, and motion verification

**Files:** Tests and adjustments across `frontend/src/features/**`, `frontend/src/app/**`, and `frontend/src/styles.css`; update `docs/ui-design.md` verification notes.

- [ ] **Step 1: Verify reduced motion**

Run component tests with `matchMedia` reporting reduced motion. Confirm no essential status or relationship depends on animation and all final states render immediately.

- [ ] **Step 2: Verify keyboard behavior**

Use Testing Library user-event to tab through shell, topology node selection, assistant composer, citations, action proposal, dialog confirmation/cancel, and audit links. Confirm visible focus and Enter/Space/Escape behavior.

- [ ] **Step 3: Verify responsive layouts in browser**

Run the app and inspect at 320px, 375px, 768px, and desktop width. Check no horizontal overflow, clipped identifiers, obscured composer, or topology node collision. Confirm controls meet 44px minimum where touchable.

- [ ] **Step 4: Verify contrast and status semantics**

Use the project contrast checker or a WCAG contrast calculator against every semantic token pair. Confirm status text remains understandable without color and citations/focus indicators are visible.

- [ ] **Step 5: Click through actual motion-bearing workflows**

Record results for: event processing start/success/error; ticket opening and incident trace; topology selection/reference focus; assistant retrieval pending/final answer/no-evidence/error/retry; proposal preparation; approval cancel; confirmed execution success/failure; audit navigation. Confirm browser console has no errors and animations do not gate interaction.

- [ ] **Step 6: Run delivery checks**

From `frontend/`, run:

```bash
npm test -- --run
npm run build
```

Expected: all tests pass and production build succeeds. Update `docs/ui-design.md` with verified scope and any browser-only checks performed.

---

## Plan self-review

- **Scope coverage:** visual white/black direction, shadcn consistency, signature incident trace, topology reveal/selection, assistant progress/tool lifecycle, animated results, action approval/execution, intake, work list, audit, responsive behavior, keyboard accessibility, reduced motion, and build/test verification are covered.
- **Honesty:** animation is tied to actual API/request states; the current stream contract is specifically called out to prevent fake tool phases or token streaming.
- **Assets:** no unapproved logo/avatar/illustration generation. Topology is rendered from real data. Custom logo or PNG/SVG creation requires product-owner approval before implementation.
- **File paths:** new files are explicit. Existing component tests should follow repository conventions; where no named test currently exists, create the test at the listed path before implementation.
- **Dependency scope:** Framer Motion is already installed. GSAP is optional and should be added only if a concrete SVG sequence cannot be maintained with the current library.
