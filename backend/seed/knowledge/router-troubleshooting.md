kb-router-troubleshooting-v1
Router Troubleshooting Field Checks
1.0
## Confirm router reachability
Check whether the home router answers management probes from the access segment. Compare its reachability with the reported service impact before dispatch. A router that is unreachable while its ONU is online points to the LAN side or the router itself.
## Inspect LAN and Wi-Fi
Verify power, uplink cable seating, and Wi-Fi broadcast state. Confirm the subscriber can reach the local gateway before changing any radio settings. Note the firmware version and the number of connected clients.
## Check the WAN and uplink
Confirm the WAN interface has an address and that the router can reach the first provider hop. Verify the uplink port negotiates at the expected speed and that no link-flap events are present in the last hour.
## Wi-Fi performance review
Review channel utilisation, neighbour access-point count, and retry rate on both bands before recommending a channel change. Prefer the 5 GHz band for high-throughput clients and reserve 2.4 GHz for range and legacy devices.
## Factory reset decision
Treat a factory reset as a last resort. Record the current configuration, confirm the customer accepts the reset, and re-provision the service afterward. Re-test throughput and Wi-Fi coverage once the router is back online.
