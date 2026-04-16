"""Data update coordinator for CometWiFi energy monitors."""

from __future__ import annotations

from asyncio import sleep
from dataclasses import dataclass
from datetime import timedelta

from comet_wifi_communicator.thermostat import Thermostat

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_MQTT_HOST,
    CONF_MQTT_PORT,
    DOMAIN,
    FETCH_DATA_TIMEOUT,
    LOGGER,
    POLL_INTERVAL,
)


@dataclass
class CometWiFiData:
    """Data from Comet WiFi device."""

    temperature_setpoint: float
    temperature_ambient: float
    is_heating: bool
    is_connected: bool


class CometWiFiDataCoordinator(DataUpdateCoordinator[CometWiFiData]):
    """Class to manage fetching Comet WiFi data."""

    mac: str

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=POLL_INTERVAL),
            config_entry=config_entry,
        )
        self.client = Thermostat(
            mqtt_host=config_entry.data[CONF_MQTT_HOST],
            mqtt_port=config_entry.data[CONF_MQTT_PORT],
            mac=config_entry.data[CONF_MAC],
        )

    async def _async_setup(self) -> None:
        try:
            await self.client.connect()
            self.mac = self.client.mac
        except Exception as err:
            raise ConfigEntryError from err

    async def _async_update_data(self) -> CometWiFiData:
        """Fetch data from Comet WiFi device."""
        try:
            await self.client.update_heating_values()
            await sleep(FETCH_DATA_TIMEOUT)  # Wait for reply
            is_heating = self.client.is_heating
            temperature_setpoint = self.client.setpoint
            temperature_ambient = self.client.temperature_ambient
            is_connected = self.client.connected
        except Exception as err:
            # will raise ConfigEntryAuthFailed once reauth is implemented
            raise ConfigEntryError("Error fetching device info: {err}") from err
        # except ConnectError as err:
        #    raise UpdateFailed(f"Error fetching device info: {err}") from err

        return CometWiFiData(
            temperature_setpoint, temperature_ambient, is_heating, is_connected
        )
