import asyncio
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.switch import SwitchEntity

from ..update_states import update_states
from ..send import send_command

from .switch import Switch
from .const import RESET_ICON

class ResetEntity(SwitchEntity , RestoreEntity):

    def __init__(self, name, button_id, pin):
        """initialisation light and lock entity"""
        self._name = name
        self._is_on = False
        self._id = button_id  
        self._pin = pin

    async def async_added_to_hass(self):
        """restoring last state."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_on = last_state.state == "on"

    @property
    def name(self):
        """returning entity name"""
        return self._name

    @property
    def is_on(self):
        """returning entity state"""
        return self._is_on

    @property
    def icon(self):
        """setting entity icon"""
        return RESET_ICON

    async def feedback(self , states):
        """update state using feedback"""
        pass
    async def async_turn_on(self, **kwargs):

        self._is_on = 1
        self.async_write_ha_state()

        command = "AT+RST=0"
        send_command(command)
        await asyncio.sleep(2)

        self._is_on = 0
        self.async_write_ha_state()
        await update_states()

    async def async_turn_off(self, **kwargs):
        pass

    async def async_toggle(self, **kwargs):
        pass

    async def send_our_state(self):
        pass

    async def create_command(self , state):
        """creating and sending command"""
        if self._pin > 6:
            states_list = ["0", "0", "0", "0", "0", "0" , "0" , "0"]
        else:
            states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = state
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        send_command(command)