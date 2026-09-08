"""Config flow for the Eurotronic Comet WiFi integration."""

from __future__ import annotations

from asyncio import sleep
import logging
from typing import Any

from comet_wifi_communicator.thermostat import MQTTConnectError, Thermostat
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_MAC, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_MQTT_HOST,
    CONF_MQTT_PORT,
    DEFAULT_MQTT_HOST,
    DEFAULT_MQTT_PORT,
    DOMAIN,
    FETCH_DATA_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_MAC): str,
        vol.Optional(CONF_MQTT_HOST, default=DEFAULT_MQTT_HOST): str,
        vol.Optional(CONF_MQTT_PORT, default=DEFAULT_MQTT_PORT): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    client = Thermostat(
        mqtt_host=data[CONF_MQTT_HOST],
        mqtt_port=data[CONF_MQTT_PORT],
        mac=data[CONF_MAC],
    )
    try:
        await client.connect()
        await sleep(FETCH_DATA_TIMEOUT)
    except MQTTConnectError as err:
        raise CannotConnect from err
    except Exception as err:
        raise CannotConnect from err

    if not client.connected:
        raise CannotConnect

    await client.disconnect()

    # Return info to be stored in the config entry.
    return {"title": data[CONF_NAME], "mac": client.mac}


class CometWiFiConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eurotronic Comet WiFi."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info["mac"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
