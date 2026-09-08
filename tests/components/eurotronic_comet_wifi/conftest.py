"""Common fixtures for the Eurotronic Comet WiFi tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.eurotronic_comet_wifi.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_thermostat() -> Generator[AsyncMock]:
    """Mock Thermostat."""
    with patch(
        "homeassistant.components.eurotronic_comet_wifi.config_flow.Thermostat"
    ) as mock_thermostat:
        mock_client = AsyncMock()
        mock_client.connected = True
        mock_client.mac = "AABBCCDDEEFF"
        mock_thermostat.return_value = mock_client
        yield mock_thermostat
