# Network workspace implementation plan

Goal: Replace boxed topology and stacked ticket UI with a connected network canvas and adjacent evidence-led conversation.
Architecture: Retain React Flow and API state. Add GSAP packet edges and independent action-target state. Keep existing authorization, proposal confirmation, and conversation persistence.
Tech stack: React, React Flow, GSAP, existing assistant components.

1. Replace device-card markup with outline icons; lay out relation depths vertically, exposing recorded facts on hover, focus, and selection.
2. Add packet edge animations with pause/reduced-motion support; distinguish interrupted links and actual action lifecycle feedback.
3. Place topology and AI chat side by side; move secondary context below; replace redundant assistant progress with one expandable evidence trace and formatted answers.
4. Run the frontend test suite and production build. Inspect desktop/mobile UI in the browser and repair regressions.

Design: Use the supplied dark network reference, green online equipment, amber degraded equipment, muted red interrupted equipment. White conversation surface preserves reading contrast. Motion communicates connections and action state, not invented telemetry.
