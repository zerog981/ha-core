"""The Eurotronic Comet WiFi integration."""

from __future__ import annotations

from asyncio import sleep

from comet_wifi_communicator.thermostat import Thermostat

from homeassistant.const import CONF_MAC, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr

from .const import (
    CONF_MQTT_HOST,
    CONF_MQTT_PORT,
    DOMAIN,
    FETCH_DATA_TIMEOUT,
    MANUFACTURER,
    MODEL,
)
from .coordinator import CometWiFiConfigEntry, CometWiFiDataCoordinator

_PLATFORMS: list[Platform] = [Platform.CLIMATE]


async def async_setup_entry(hass: HomeAssistant, entry: CometWiFiConfigEntry) -> bool:
    """Set up Eurotronic Comet WiFi from a config entry."""

    mac = entry.data[CONF_MAC]

    client = Thermostat(
        mqtt_host=entry.data[CONF_MQTT_HOST],
        mqtt_port=entry.data[CONF_MQTT_PORT],
        mac=mac,
    )

    await client.connect()
    await sleep(FETCH_DATA_TIMEOUT)

    if not client.connected:
        raise ConfigEntryNotReady

    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, mac)},
        name=f"{mac}",
        manufacturer=MANUFACTURER,
        model=MODEL,
    )

    coordinator = CometWiFiDataCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: CometWiFiConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
