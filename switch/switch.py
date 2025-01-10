from homeassistant.components.switch import SwitchEntity
import serial
import time
from homeassistant.helpers.restore_state import RestoreEntity

from ..send import send_command

class Switch(SwitchEntity , RestoreEntity):

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
    def get_pin(self):
        return self._pin

    @property
    def get_id(self):
        return self._id

    @property
    def is_on(self):
        """returning entity state"""
        return self._is_on

    async def feedback(self , states):
        """update state using feedback"""
        if states[0] == str(self._id):
            self._is_on = int(states[self._pin])
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        self.create_command("1")

    async def async_turn_off(self, **kwargs):
        self.create_command("2")

    async def async_toggle(self, **kwargs):
        self.create_command("3")

    def turn_on(self):
        self.create_command("1")

    def turn_off(self):
        self.create_command("2")

    async def send_our_state(self):
        if self.state == "on":
            await self.create_command("1")
        else:
            await self.create_command("0")

    def create_command(self , state):
        """creating and sending command"""
        if self._pin > 6:
            states_list = ["0", "0", "0", "0", "0", "0" , "0" , "0"]
        else:
            states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = state
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        send_command(command)