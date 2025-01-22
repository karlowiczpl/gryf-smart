from homeassistant.components.light import LightEntity

import logging

from .const import CONF_NAME
from .devices.output import _GryfOutput

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    cf = {
        "id" : 1,
        "pin" : 1,
        "name" : "sdjahsjd",
    }

    async_add_entities([myLamp(cf)])

class myLamp(LightEntity , _GryfOutput):
    def __init__(self , conf) -> None:
        _GryfOutput.__init__(self , conf)
        self._name = conf.get(CONF_NAME)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        _LOGGER.warning("Task timed out while handling event %s" , self.get_state)
        if _GryfOutput.get_state == 1:
            _LOGGER.warning("Task timed out while handling event %s" , self.get_state)
            return "on"
        else:
            return "off"

    async def async_turn_on(self):
        _GryfOutput.set_out(self , "1")
    async def async_turn_off(self):
        _GryfOutput.set_out(self , "2")

    async def async_update(self):
        self.async_write_ha_state()

