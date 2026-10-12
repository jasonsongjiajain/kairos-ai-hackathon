kb-optical-loss-v1
Optical Loss Triage
1.0
## Validate alarm scope
Confirm alarm time, affected service, and whether neighbouring endpoints share the same loss condition on the same splitter. Treat a single-endpoint alarm differently from a segment-wide event. Establish whether the condition is intermittent or continuous.
## Collect optical measurements
Record the OLT receive level, the ONU receive level, and the expected window for the deployment. Compare against the commissioning baseline rather than an absolute figure. Note any change in patch leads or splitters since commissioning.
## Field inspection
Inspect connectors and cable routing for contamination, strain, or tight bends. Clean connectors only with approved materials and use an approved ferrule cleaner. Re-test after cleaning before replacing any assembly.
## Interpreting loss thresholds
A loss within a few decibels of baseline is usually acceptable. A drop beyond the design margin, or a receive level below the receiver sensitivity, indicates a dirty connector, a damaged drop cable, or a fault at the splitter. Do not adjust provider-side optics without authorization.
## Record and route
Record measured receive level, equipment identifiers, and actions taken. Escalate persistent or shared-path loss to the network team with the measurements attached. Re-test the service from the customer end after any physical intervention.
