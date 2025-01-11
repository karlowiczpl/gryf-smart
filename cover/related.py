# from homeassistant.components.cover import SUPPORT_SET_POSITION , ATTR_POSITION , STATE_OPENING, STATE_CLOSING
from homeassistant.const import STATE_CLOSED, STATE_OPEN
from homeassistant.components.cover import CoverEntityFeature

import asyncio
from .cover import Cover

from ..send import send_command


class Ha_position_cover(Cover):

    _attr_supported_features = CoverEntityFeature.SET_POSITION

    def __init__(self, name, cover_id, pin, time):
        self._name = name
        self._pin = pin
        self._id = cover_id
        self._state = STATE_CLOSED
        self._is_opening = False
        self._is_closing = False
        self._position = 0
        self._time = time
        
        self._timer_en = False
        self._new_position = 0

    async def async_set_cover_position(self, **kwargs):
        self._new_position = kwargs.get(ATTR_POSITION)
        if self._new_position is None:
            return

        if not self._timer_en:
            self._timer_en = True
            await self.set_start_command()
            await self.start_timer()

        
    async def start_timer(self):
        one_interwal_position = 100 / self._time
        tolerance = 0.1

        while abs(self._new_position - self._position) > tolerance:
            await asyncio.sleep(0.1)

            delta = abs(self._new_position - self._position)
            step = min(delta, one_interwal_position)

            if self._new_position > self._position:
                self._position += step
            else:
                self._position -= step

            self.schedule_update_ha_state()
                
        self._timer_en = False
        self._is_opening = False
        self._is_closing = False
        self._state = STATE_OPEN if self._position > 10 else STATE_CLOSED

        states = [0, 0, 0, 0]
        states[self._pin - 1] = 3
        control = self._id + sum(states)
        command = f"AT+SetRol={self._id},0,{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()


    async def set_start_command(self):
        states = [0, 0, 0, 0]

        if self._new_position > self._position:
            states[self._pin - 1] = 2
            self._is_opening = False
            self._is_closing = True
        else:
            self._is_opening = True
            self._is_closing = False
            states[self._pin - 1] = 1
        
        t1 = self._time
        control = self._id + t1 + sum(states)
        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()

    @property
    def position(self):
        return self._position

    @property
    def current_cover_position(self):
        return self._position

    async def changeRolState(self, parsed_states):

        if parsed_states[self._pin] == "2":
            self._state = STATE_CLOSING
            self._is_opening = False
            self._is_closing = True

        elif parsed_states[self._pin] == "1":
            self._state = STATE_OPENING
            self._is_opening = True
            self._is_closing = False

        self.async_write_ha_state()
