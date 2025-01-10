import asyncio
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.switch import SwitchEntity

from ..send import send_command

from .const import RESET_ICON

class ResetEntity(SwitchEntity , RestoreEntity):

    def __init__(self, name, button_id, pin):
        self._name = name
        self._is_on = False
        self._id = button_id  
        self._pin = pin

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_on = last_state.state == "on"

    @property
    def name(self):
        return self._name

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
