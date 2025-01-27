from typing import Any

from homeassistant import config_entries
from .const import DOMAIN
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import (
    CONF_LATITUDE,
    CONF_LOCATION,
    CONF_LONGITUDE,
    CONF_MAC,
    CONF_RADIUS,
    UnitOfLength,
)

class GryfSmartConfigFlow(config_entries.ConfigFlow , domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:

        self._longitude = 0.0
        self._latitude = 0.0
        self._radius = 0.0
        self._stations: dict[str, dict[str, Any]] = {}

async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step to select the location."""


