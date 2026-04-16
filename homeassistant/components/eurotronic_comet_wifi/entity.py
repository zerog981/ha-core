"""Base entity for the Comet WiFi integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import CometWiFiDataCoordinator


class CometWiFiEntity(CoordinatorEntity[CometWiFiDataCoordinator]):
    """Base entity for Comet WiFi thermostats."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CometWiFiDataCoordinator) -> None:
        """Initialize the Comet WiFi entity."""
        super().__init__(coordinator)

        mac = coordinator.mac
        # mac = coordinator.config_entry.data[CONF_MAC]
        # name = coordinator.config_entry.data[CONF_NAME]

        # Device info using coordinator's cached data
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, mac)},
            name=mac,
            manufacturer=MANUFACTURER,
            model=MODEL,
        )
