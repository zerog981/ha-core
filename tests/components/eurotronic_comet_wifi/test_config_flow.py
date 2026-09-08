"""Test the Eurotronic Comet WiFi config flow."""

from unittest.mock import AsyncMock

from homeassistant import config_entries
from homeassistant.components.eurotronic_comet_wifi.const import (
    CONF_MQTT_HOST,
    CONF_MQTT_PORT,
    DOMAIN,
)
from homeassistant.const import CONF_MAC, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_form(
    hass: HomeAssistant, mock_setup_entry: AsyncMock, mock_thermostat: AsyncMock
) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_NAME: "test-thermostat",
            CONF_MAC: "AABBCCDDEEFF",
            CONF_MQTT_HOST: "192.168.0.2",
            CONF_MQTT_PORT: 3333,
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "test-thermostat"
    assert result["data"] == {
        CONF_NAME: "test-thermostat",
        CONF_MAC: "AABBCCDDEEFF",
        CONF_MQTT_HOST: "192.168.0.2",
        CONF_MQTT_PORT: 3333,
    }
    assert len(mock_setup_entry.mock_calls) == 1


# async def test_form_cannot_connect(
#     hass: HomeAssistant, mock_setup_entry: AsyncMock
# ) -> None:
#     """Test we handle cannot connect error."""
#     result = await hass.config_entries.flow.async_init(
#         DOMAIN, context={"source": config_entries.SOURCE_USER}
#     )

#     with patch(
#         "homeassistant.components.eurotronic_comet_wifi.config_flow.PlaceholderHub.authenticate",
#         side_effect=CannotConnect,
#     ):
#         result = await hass.config_entries.flow.async_configure(
#             result["flow_id"],
#             {
#                 CONF_HOST: "1.1.1.1",
#                 CONF_USERNAME: "test-username",
#                 CONF_PASSWORD: "test-password",
#             },
#         )

#     assert result["type"] is FlowResultType.FORM
#     assert result["errors"] == {"base": "cannot_connect"}

#     # Make sure the config flow tests finish with either an
#     # FlowResultType.CREATE_ENTRY or FlowResultType.ABORT so
#     # we can show the config flow is able to recover from an error.

#     with patch(
#         "homeassistant.components.eurotronic_comet_wifi.config_flow.PlaceholderHub.authenticate",
#         return_value=True,
#     ):
#         result = await hass.config_entries.flow.async_configure(
#             result["flow_id"],
#             {
#                 CONF_HOST: "1.1.1.1",
#                 CONF_USERNAME: "test-username",
#                 CONF_PASSWORD: "test-password",
#             },
#         )
#         await hass.async_block_till_done()

#     assert result["type"] is FlowResultType.CREATE_ENTRY
#     assert result["title"] == "Name of the device"
#     assert result["data"] == {
#         CONF_HOST: "1.1.1.1",
#         CONF_USERNAME: "test-username",
#         CONF_PASSWORD: "test-password",
#     }
#     assert len(mock_setup_entry.mock_calls) == 1
