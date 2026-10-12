"""Simulated tool execution.

Each executor mutates the in-database simulated device state and returns a
result the caller can persist and audit. They never touch real hardware. The
dispatch table keeps the service layer free of per-tool branching.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from app.domain.models import NetworkDevice


@dataclass(frozen=True)
class SimulationResult:
    succeeded: bool
    message: str
    device_status: str | None = None
    details_updates: dict = field(default_factory=dict)


def get_device_status(device: NetworkDevice) -> SimulationResult:
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} reports status '{device.status}'.",
    )


def list_connected_clients(device: NetworkDevice) -> SimulationResult:
    clients = _client_refs(device)
    if not clients:
        return SimulationResult(
            succeeded=True,
            message=f"{device.name} reports no simulated clients attached.",
        )
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} reports {len(clients)} connected client(s): {', '.join(clients)}.",
    )


def run_speed_test(device: NetworkDevice) -> SimulationResult:
    download = float(device.details.get("download_mbps", 480.0) or 480.0)
    upload = float(device.details.get("upload_mbps", 95.0) or 95.0)
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} throughput test: {download:.1f} Mbps down / {upload:.1f} Mbps up.",
    )


def run_optical_diagnostics(device: NetworkDevice) -> SimulationResult:
    rx = device.details.get("rx_power_db", "unknown")
    los = device.details.get("los_status", "unknown")
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} optical read: rx_power_db={rx}, los_status={los}.",
    )


def reboot_router(device: NetworkDevice) -> SimulationResult:
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} rebooted and is back online.",
        device_status="online",
    )


def reboot_ont(device: NetworkDevice) -> SimulationResult:
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} power-cycled and re-established the PON link.",
        device_status="online",
        details_updates={"los_status": "OK"},
    )


def refresh_ont_registration(device: NetworkDevice) -> SimulationResult:
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} re-registered with the OLT.",
        device_status="online",
        details_updates={"los_status": "OK", "registered": True},
    )


def reset_optical_port(device: NetworkDevice) -> SimulationResult:
    baseline = device.details.get("baseline_rx_power_db", -21.4)
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} optical port reset; receive power re-baselined to {baseline} dBm.",
        details_updates={"rx_power_db": baseline, "los_status": "OK"},
    )


def update_config(device: NetworkDevice, settings: dict[str, int]) -> SimulationResult:
    applied = ", ".join(f"{key}={value}" for key, value in sorted(settings.items()))
    return SimulationResult(
        succeeded=True,
        message=f"Applied configuration on {device.name}: {applied}.",
        details_updates={"settings": dict(settings)},
    )


def set_wifi_ssid(device: NetworkDevice, ssid_2g: str | None, ssid_5g: str | None) -> SimulationResult:
    updates: dict[str, object] = {}
    changed: list[str] = []
    if ssid_2g is not None:
        updates["ssid_2g"] = ssid_2g
        changed.append(f"2.4G={ssid_2g}")
    if ssid_5g is not None:
        updates["ssid_5g"] = ssid_5g
        changed.append(f"5G={ssid_5g}")
    return SimulationResult(
        succeeded=True,
        message=f"Renamed Wi-Fi network on {device.name}: {', '.join(changed)}.",
        details_updates=updates,
    )


def set_wifi_channel(device: NetworkDevice, band: str, channel: int) -> SimulationResult:
    key = "channel_2g" if band == "2.4" else "channel_5g"
    return SimulationResult(
        succeeded=True,
        message=f"Moved {band} GHz radio on {device.name} to channel {channel}.",
        details_updates={key: channel},
    )


def flush_dns_cache(device: NetworkDevice) -> SimulationResult:
    return SimulationResult(
        succeeded=True,
        message=f"Resolver cache flushed on {device.name}.",
        details_updates={"dns_cache": "flushed"},
    )


def restart_service(device: NetworkDevice, service: str) -> SimulationResult:
    return SimulationResult(
        succeeded=True,
        message=f"Restarted the {service.upper()} service stack on {device.name}.",
        details_updates={f"{service}_restarted": True},
    )


def block_client(device: NetworkDevice, client_mac: str) -> SimulationResult:
    blocked = list(device.details.get("blocked_clients", []) or [])
    if client_mac not in blocked:
        blocked.append(client_mac)
    return SimulationResult(
        succeeded=True,
        message=f"Quarantined client {client_mac} on {device.name}.",
        details_updates={"blocked_clients": blocked},
    )


def set_dhcp_reservation(device: NetworkDevice, client_mac: str, ip_address: str) -> SimulationResult:
    reservations = dict(device.details.get("dhcp_reservations", {}) or {})
    reservations[client_mac] = ip_address
    return SimulationResult(
        succeeded=True,
        message=f"Reserved {ip_address} for {client_mac} on {device.name}.",
        details_updates={"dhcp_reservations": reservations},
    )


def _client_refs(device: NetworkDevice) -> list[str]:
    return [str(ref) for ref in (device.details.get("connected_clients", []) or [])]


Executor = Callable[..., SimulationResult]

EXECUTORS: dict[str, Executor] = {
    "get_device_status": get_device_status,
    "list_connected_clients": list_connected_clients,
    "run_speed_test": run_speed_test,
    "run_optical_diagnostics": run_optical_diagnostics,
    "reboot_router": reboot_router,
    "reboot_ont": reboot_ont,
    "refresh_ont_registration": refresh_ont_registration,
    "reset_optical_port": reset_optical_port,
    "update_config": update_config,
    "set_wifi_ssid": set_wifi_ssid,
    "set_wifi_channel": set_wifi_channel,
    "flush_dns_cache": flush_dns_cache,
    "restart_service": restart_service,
    "block_client": block_client,
    "set_dhcp_reservation": set_dhcp_reservation,
}


def run(tool_name: str, device: NetworkDevice, params) -> SimulationResult:
    """Dispatch a tool to its simulator using validated parameters."""
    executor = EXECUTORS.get(tool_name)
    if executor is None:
        raise KeyError(tool_name)
    if tool_name == "update_config":
        return executor(device, params.settings)
    if tool_name == "set_wifi_ssid":
        return executor(device, params.ssid_2g, params.ssid_5g)
    if tool_name == "set_wifi_channel":
        return executor(device, params.band, params.channel)
    if tool_name == "restart_service":
        return executor(device, params.service)
    if tool_name == "block_client":
        return executor(device, params.client_mac)
    if tool_name == "set_dhcp_reservation":
        return executor(device, params.client_mac, params.ip_address)
    return executor(device)
