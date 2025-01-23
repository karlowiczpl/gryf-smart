from typing import reveal_type
from homeassistant.components.light import LightEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass,
    config: dict,
    async_add_entities,
    discovery_info=None,
):
    """Konfiguracja platformy light z YAML."""
    coordinator = hass.data.get("gryf_smart")

    # Zakładając, że urządzenia są przechowywane w słowniku
    # devices = coordinator.data.keys()

    # Tworzenie encji
    lights = [RS232Light(coordinator, "test")]
    async_add_entities(lights)

class RS232Light(CoordinatorEntity, LightEntity):
    """Encja światła obsługiwana przez RS232."""

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id

    @property
    def name(self):
        """Zwraca nazwę encji."""
        return f"RS232 Light {self.device_id}"

    @property
    def is_on(self):
        """Zwraca stan włączenia/wyłączenia."""
        
        _LOGGER.warning("Task timed out while handling event: %s", self.coordinator.data)
        return 1

    async def async_turn_on(self, **kwargs):
        """Włącz światło."""
        await self.send_command("TURN_ON", self.device_id)

    async def async_turn_off(self, **kwargs):
        """Wyłącz światło."""
        await self.send_command("TURN_OFF", self.device_id)

    async def send_command(self, command, device_id):
        """Wysyła komendę do urządzenia."""
        self.async_write_ha_state()
