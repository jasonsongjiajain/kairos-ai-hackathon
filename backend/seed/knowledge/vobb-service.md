kb-vobb-service-v1
VoBB Voice Service Checks
1.0
## Validate voice registration
Check whether the voice adapter registers with the softswitch and whether dial tone is present. Confirm the impact is limited to voice before dispatch. Record the registration status and the last successful registration time.
## Check power and cabling
Verify adapter power, phone cabling, and the data connection the voice service depends on. A voice-only fault on a healthy data link usually stays local. Confirm the adapter is not sharing an overloaded power strip.
## Review signalling responses
Note the response codes seen on registration attempts. A timeout (408) usually indicates a path or firewall problem, while an authentication failure points to credentials or provisioning. Do not change credentials without authorization.
## Test the call path
Place a test call to a known number and confirm two-way audio. Check the adapter priority marking if supported and confirm the service VLAN or priority settings match the provisioning record.
## Escalate to voice team
If registration still fails after local checks, record the adapter identifiers, signalling codes, and test-call results, then escalate through the voice operations process.
