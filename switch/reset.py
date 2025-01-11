import asyncio
from homeassistant.components.switch import SwitchEntity

from ..send import send_command

from .const import RESET_ICON , RESET_NAME

class ResetEntity(SwitchEntity):

    def __init__(self):
        self._is_on = False

    @property
    def name(self):
        return RESET_NAME

    @property
    def is_on(self):
        return self._is_on

    @property
    def icon(self):
        return RESET_ICON

    async def async_turn_on(self):

        self._is_on = 1
        self.async_write_ha_state()

        command = "AT+RST=0"
        send_command(command)
        await asyncio.sleep(2)

        self._is_on = 0
        self.async_write_ha_state()

    async def async_turn_off(self):
        pass

    async def async_toggle(self):
        pass
