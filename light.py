from homeassistant.components.light import LightEntity

from .const import CONF_ID, CONF_NAME, CONF_PIN , DOMAIN
from .entity import GryfYamlEntity 
from .device import _GryfOutput

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass,
    config: dict,
    async_add_entities,
    discovery_info,
):
    lights = []

    for conf in discovery_info:
        device = _GryfOutput(
            conf.get(CONF_NAME),
            conf.get(CONF_ID),
            conf.get(CONF_PIN),
            hass.data[DOMAIN],
        )
        lights.append(GryfLight(device))

    async_add_entities(lights)

class GryfLight(GryfYamlEntity , LightEntity):

    def __init__(self , device):
        self._device = device
        self._device.set_update_function(self.update)
        self._is_on = False
        self._attr_unique_id = self._device.name + "lamp"

    async def update(self , state):
        self._is_on = state
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self._device.turn_on()

    async def async_turn_off(self, **kwargs):
        await self._device.turn_off()

