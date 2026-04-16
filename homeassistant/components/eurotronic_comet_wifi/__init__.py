"""The Eurotronic Comet WiFi integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import CometWiFiDataCoordinator

_PLATFORMS: list[Platform] = [Platform.CLIMATE]

type CometWiFiConfigEntry = ConfigEntry[CometWiFiDataCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: CometWiFiConfigEntry) -> bool:
    """Set up Eurotronic Comet WiFi from a config entry."""

    coordinator = CometWiFiDataCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: CometWiFiConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
