from homeassistant.components.cover import CoverEntity
from homeassistant.const import STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_CLOSING
from homeassistant.components.cover import CoverDeviceClass
from homeassistant.helpers.restore_state import RestoreEntity  

from ..send import send_command
import logging


class Cover(CoverEntity, RestoreEntity):  
    def __init__(self, name, cover_id, pin, time):
        self._name = name
        self._pin = pin
        self._id = cover_id
        self._state = STATE_CLOSED
        self._is_opening = False
        self._is_closing = False
        self._position = None
        self._time = time

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._position = last_state.attributes.get("position", self._position)
            self._state = last_state.state if last_state.state in [STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_CLOSING] else self._state
            self._is_opening = last_state.attributes.get("is_opening", self._is_opening)
            self._is_closing = last_state.attributes.get("is_closing", self._is_closing)
            self.async_write_ha_state()

    @property
    def name(self):
        return self._name

    @property
    def is_opening(self):
        return self._is_opening

    def turn_on(self):
        await self.async_open_cover()

    def turn_off(self):
        await self.async_close_cover()
    @property
    def is_closing(self):
        return self._is_closing

    @property
    def is_closed(self):
        return self._state == STATE_CLOSED

    @property
    def device_class(self):
        return CoverDeviceClass.SHUTTER

    @property
    def state(self):
        return self._state

    @property
    def get_id(self):
        return self._id

    @property
    def get_pin(self):
        return self._pin

    async def changeRolState(self, parsed_states):
        if parsed_states[self._pin] == "0":
            if self._is_opening:
                self._state = STATE_OPEN
            elif self._is_closing:
                self._state = STATE_CLOSED
            elif self._state != STATE_OPEN and self._state != STATE_CLOSED:
                self._state = None  
            self._is_opening = False
            self._is_closing = False

        elif parsed_states[self._pin] == "2":
            self._state = STATE_CLOSING
            self._is_opening = False
            self._is_closing = True

        elif parsed_states[self._pin] == "1":
            self._state = STATE_OPENING
            self._is_opening = True
            self._is_closing = False

        self.async_write_ha_state()
    async def async_open_cover(self):
        self.open_cover()

    async def async_close_cover(self):
        self.close_cover()

    def open_cover(self):
        self._is_opening = True
        self._is_closing = False
        states = [0, 0, 0, 0]
        states[self._pin - 1] = 2
        t1 = self._time
        control = self._id + t1 + sum(states)
        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()

    def close_cover(self):
        self._is_opening = False
        self._is_closing = True
        states = [0, 0, 0, 0]
        states[self._pin - 1] = 1
        t1 = self._time
        control = self._id + t1 + sum(states)
        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()

    async def async_stop_cover(self):
        self._is_opening = False
        self._is_closing = False
        self._state = None
        states = [0, 0, 0, 0]
        states[self._pin - 1] = 3
        control = self._id + sum(states)
        command = f"AT+SetRol={self._id},0,{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()
