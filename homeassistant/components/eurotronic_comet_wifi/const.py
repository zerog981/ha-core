"""Constants for the Eurotronic Comet WiFi integration."""

import logging

DOMAIN = "eurotronic_comet_wifi"
MANUFACTURER = "Eurotronic"
MODEL = "Euroronic Comet WiFi"

LOGGER = logging.getLogger(__package__)

CONF_MQTT_HOST = "mqtt_host"
CONF_MQTT_PORT = "mqtt_port"

DEFAULT_MQTT_HOST = "localhost"
DEFAULT_MQTT_PORT = 1883

POLL_INTERVAL = 900  # seconds
FETCH_DATA_TIMEOUT = 5  # seconds

UNIQUE_ID_SUFFIX_CLIMATE = "climate"
