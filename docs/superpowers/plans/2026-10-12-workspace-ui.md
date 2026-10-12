# Field workspace UI implementation plan

**Goal:** Revamp every existing screen while preserving the light monochrome theme, real operational data, and approval workflows.

**Architecture:** Keep route and API contracts intact. Restyle the shared design system and page compositions, render actual topology edges, and add pending-only motion to shared tool and chat states.

**Tech stack:** React, TypeScript, CSS, Phosphor icons, existing Framer Motion.

## Design direction

User references: spacious chat composer, device network diagram, inspectable device details. Preserve existing Avenir/Georgia typography and monochrome palette. Dark topology canvas distinguishes physical infrastructure from the conversational workspace. Status colors carry device health only. ENERGY 3 / RHYTHM 3 / MOTION 2, with the user's explicit request for tool-call and generation animations overriding the no-loop default during pending operations. Respect reduced motion. No generated assets, fabricated telemetry, or new dependencies.

## Implementation

- [x] Reshape shared shell, sign-in, queue, work list, ticket metadata, audit and responsive layouts in `frontend/src/styles.css` and existing page components.
- [x] Update `TopologyPath.tsx` with actual edge geometry, device icons and a selected-device inspector using available fields only; preserve keyboard selection and text connections.
- [x] Update assistant heading, starters and composer; add response-generation indicator while requests are pending and shared tool animation until settlement.
- [x] Run `npm run build` and `npm test -- --run` from frontend. Verify topology selection and async state cleanup with focused tests.
- [x] Inspect rendered desktop and mobile screens, keyboard focus, overflow, pending/success/error states and reduced motion; record any environment limitation honestly.

## Verification

Production build succeeded; all 100 frontend tests passed. Tests verify pending animation elements are removed after error/success and restored on retry; existing reduced-motion and keyboard tests pass. Browser review covered sign-in, assigned tickets, topology selection, a real assistant request/answer, audit history, and intake empty state. Checked 390px, 768px, and 1440px layouts without page overflow. Fixed mobile composer overlap and changed narrow topology to a stacked device view with explicit connection descriptions. Dark-panel secondary text contrast measured 8.62:1 and 8.50:1.

Limitations: no pending events remained in the demo, so populated queue behavior was validated by existing component tests. Backend emits a complete answer, so animation covers generation and arrival rather than token streaming. Vite still reports the existing large bundle warning. Direct navigation to ticket URLs encounters the existing development proxy route overlap; in-app navigation works.
