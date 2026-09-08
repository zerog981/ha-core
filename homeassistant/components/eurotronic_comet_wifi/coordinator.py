"""Data update coordinator for CometWiFi energy monitors."""

from __future__ import annotations

from asyncio import sleep
from dataclasses import dataclass
from datetime import timedelta

from comet_wifi_communicator.thermostat import Thermostat

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, FETCH_DATA_TIMEOUT, LOGGER, POLL_INTERVAL

type CometWiFiConfigEntry = ConfigEntry[CometWiFiDataCoordinator]


@dataclass
class CometWiFiData:
    """Data from Comet WiFi device."""

    temperature_setpoint: float
    temperature_ambient: float
    is_heating: bool
    is_connected: bool


class CometWiFiDataCoordinator(DataUpdateCoordinator[CometWiFiData]):
    """Class to manage fetching Comet WiFi data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: CometWiFiConfigEntry,
        client: Thermostat,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=LOGGER,
            name=f"{DOMAIN} {client.mac}",
            update_interval=timedelta(seconds=POLL_INTERVAL),
            config_entry=config_entry,
        )
        self.client = client
        self.mac = client.mac

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
