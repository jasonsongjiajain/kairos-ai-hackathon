"""Simulated tool execution.

These functions mutate the in-database simulated device state and return a
result the caller can persist and audit. They never touch real hardware.
"""

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


def reboot_router(device: NetworkDevice) -> SimulationResult:
    return SimulationResult(
        succeeded=True,
        message=f"{device.name} rebooted and is back online.",
        device_status="online",
    )


def update_config(device: NetworkDevice, settings: dict[str, int]) -> SimulationResult:
    applied = ", ".join(f"{key}={value}" for key, value in sorted(settings.items()))
    return SimulationResult(
        succeeded=True,
        message=f"Applied configuration on {device.name}: {applied}.",
        details_updates={"settings": dict(settings)},
    )
