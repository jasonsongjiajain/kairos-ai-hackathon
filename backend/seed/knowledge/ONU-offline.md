kb-onu-offline-v1
ONU Offline Field Checks
1.0
## Confirm service impact
Check whether the reported loss affects one endpoint or multiple endpoints on the same PON segment. Compare the service status with the latest network event before dispatch. A single ONU down usually points to the drop or the customer premises, while several ONUs down on the same port points upstream.
## Inspect optical path
Verify the patch lead is seated at both the ONU and the wall outlet, and inspect for visible bends, kinks, or damage. Use approved optical test equipment and follow site safety practices. Never look into a live fibre end. Do not disconnect shared plant to test a single endpoint.
## Verify ONU power and indicators
Confirm the ONU has stable power and that the PON and LAN indicators match expected states. A red or extinguished PON light with a lit power light indicates loss of the optical signal rather than a power fault. Record the indicator pattern and the ONU serial number.
## Check the upstream access node
Confirm the serving OLT port is up and that no maintenance window overlaps the reported time. Compare the ONU reference, the OLT shelf and port, and the optical splitter ratio against the provisioning record.
## Record findings and escalate
If the ONU remains offline after local connection checks, record optical readings, indicator state, serial number, and access-node reference, then escalate through the network operations process. Do not factory-reset customer equipment as an initial diagnostic step.
