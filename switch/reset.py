import asyncio
from homeassistant.components.switch import SwitchEntity

from ..entity import _GryfSmartEntityBase

from .const import RESET_ICON

class ResetEntity(SwitchEntity , _GryfSmartEntityBase):


    def __init__(self, name, button_id, pin):
        """initialisation light and lock entity"""
        self._name = name
        self._is_on = False
        self._id = button_id  
        self._pin = pin

    @property
    def icon(self):
        """setting entity icon"""
        return RESET_ICON

    async def async_turn_on(self):

        self._is_on = 1
        self.async_write_ha_state()

        command = "AT+RST=0"
        self.send_command(command)
        await asyncio.sleep(2)

        self._is_on = 0
        self.async_write_ha_state()
        # await update_states()

    async def async_turn_off(self, **kwargs):
        pass

    async def async_toggle(self, **kwargs):
        pass
