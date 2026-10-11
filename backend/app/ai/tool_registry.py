"""Allowlisted agent tools.

The assistant may *propose* a tool, but nothing here executes anything on its
own. Each tool declares the roles that may use it, whether explicit
confirmation is required, and a Pydantic parameter model so model-supplied
arguments are treated as untrusted input.
"""

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field, field_validator

ToolKind = Literal["read_only", "stateful"]

# Only these configuration keys may be changed, with inclusive integer bounds.
CONFIG_BOUNDS: dict[str, tuple[int, int]] = {
    "wifi_channel": (1, 13),
    "tx_power_dbm": (0, 30),
}

TECHNICIAN_ROLES = ("technician",)
ANY_WORK_ROLES = ("technician", "operator", "supervisor")


class DeviceTargetParams(BaseModel):
    device_id: str = Field(min_length=1, max_length=64)


class UpdateConfigParams(BaseModel):
    device_id: str = Field(min_length=1, max_length=64)
    settings: dict[str, int]

    @field_validator("settings")
    @classmethod
    def _validate_settings(cls, value: dict[str, int]) -> dict[str, int]:
        if not value:
            raise ValueError("At least one configuration setting is required")
        for key, setting in value.items():
            if key not in CONFIG_BOUNDS:
                raise ValueError(f"Unsupported configuration key: {key}")
            if isinstance(setting, bool) or not isinstance(setting, int):
                raise ValueError(f"{key} must be an integer")
            low, high = CONFIG_BOUNDS[key]
            if not low <= setting <= high:
                raise ValueError(f"{key} must be between {low} and {high}")
        return value


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    kind: ToolKind
    allowed_roles: tuple[str, ...]
    requires_confirmation: bool
    device_type: str | None
    params: type[BaseModel]


TOOL_SPECS: dict[str, ToolSpec] = {
    "get_device_status": ToolSpec(
        name="get_device_status",
        description="Read the current simulated status of a customer device.",
        kind="read_only",
        allowed_roles=ANY_WORK_ROLES,
        requires_confirmation=False,
        device_type=None,
        params=DeviceTargetParams,
    ),
    "reboot_router": ToolSpec(
        name="reboot_router",
        description="Simulate a reboot of the customer's home router.",
        kind="stateful",
        allowed_roles=TECHNICIAN_ROLES,
        requires_confirmation=True,
        device_type="router",
        params=DeviceTargetParams,
    ),
    "update_config": ToolSpec(
        name="update_config",
        description="Simulate a bounded configuration change on the home router.",
        kind="stateful",
        allowed_roles=TECHNICIAN_ROLES,
        requires_confirmation=True,
        device_type="router",
        params=UpdateConfigParams,
    ),
}


def get_tool_spec(name: str) -> ToolSpec | None:
    return TOOL_SPECS.get(name)


def catalog_for_role(role: str) -> list[ToolSpec]:
    return [spec for spec in TOOL_SPECS.values() if role in spec.allowed_roles]
