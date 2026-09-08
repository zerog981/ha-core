"""Base entity for the Comet WiFi integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import CometWiFiDataCoordinator


class CometWiFiEntity(CoordinatorEntity[CometWiFiDataCoordinator]):
    """Base entity for Comet WiFi thermostats."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CometWiFiDataCoordinator) -> None:
        """Initialize the Comet WiFi entity."""
        super().__init__(coordinator)

        # Device info added in __init__.py
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.mac)}
        )

    @property
    def available(self) -> bool:
        """Returns the current availability state."""
        return self.coordinator.data.is_connected
