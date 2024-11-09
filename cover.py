from homeassistant.components.cover import CoverEntity
from homeassistant.const import STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_CLOSING
from homeassistant.components.cover import CoverEntityFeature , CoverDeviceClass


from .send import send_command

import logging

_LOGGER = logging.getLogger(__name__)

covers = []

STATE_PAUSED = "zatrzymano"

async def new_rols_command(parsed_states):
    if covers:
        for i in range(len(covers)):
            if str(covers[i].get_id) == parsed_states[0]:
                await covers[i].changeRolState(parsed_states)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global covers

    cover_config = discovery_info or []

    for cover in cover_config:
        name = cover.get("name")
        cover_id = cover.get("id")
        pin = cover.get("pin")
        time = cover.get("time")
        covers.append(Cover(name, cover_id, pin, time))

    async_add_entities(covers)

class Cover(CoverEntity):
    def __init__(self, name, cover_id, pin, time):
        self._name = name
        self._pin = pin
        self._id = cover_id
        self._state = STATE_CLOSED
        self._is_opening = False
        self._is_closing = False
        self._position = None 
        self._time = time
    @property
    def name(self):
        return self._name

    @property
    def current_cover_position(self):
        return self._position

    @property
    def is_opening(self):
        return self._is_opening

    @property
    def is_closing(self):
        return self._is_closing

    @property
    def get_id(self):
        return self._id

    @property
    def get_pin(self):
        return self._pin

    # @property
    # def supported_features(self):
    #     return CoverEntityFeature.SET_POSITION

    @property
    def is_closed(self):
        return self._state == STATE_CLOSED

    @property
    def device_class(self):
        return CoverDeviceClass.SHUTTER

    async def changeRolState(self , parsed_states):

        if parsed_states[self._pin] == "0":
            if self._is_opening:
                self._state = STATE_OPEN
            elif self._is_closing:
                self._state = STATE_CLOSED
            elif self._state != STATE_OPEN and self._state != STATE_CLOSED:
                self._state = STATE_PAUSED
                
            self._is_opening = False
            self._is_closing = False

        if parsed_states[self._pin] == "2":
            self._state = STATE_CLOSED
            self._is_opening = False
            self._is_closing = True
            self._state = STATE_CLOSING

        if parsed_states[self._pin] == "1":
            self._state = STATE_OPEN
            self._is_opening = True
            self._is_closing = False
            self._state = STATE_OPENING

        self.async_write_ha_state()
            
        

    async def async_open_cover(self, **kwargs):
        self._is_opening = False
        self._is_closing = False

        states = [0 , 0 , 0 , 0]
        states[self._pin - 1] = 2
        t1 = self._time
        control = self._id + t1 + sum(states)

        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()

    async def async_close_cover(self, **kwargs):
        self._is_opening = False
        self._is_closing = False

        states = [0 , 0 , 0 , 0]
        states[self._pin - 1] = 1
        t1 = self._time
        control = self._id + t1 + sum(states)

        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()

    async def async_stop_cover(self, **kwargs):
        self._is_opening = False
        self._is_closing = False
        self._state = None

        states = [0 , 0 , 0 , 0]
        states[self._pin - 1] = 3
        control = self._id + sum(states)

        command = f"AT+SetRol={self._id},0,{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)
        self.schedule_update_ha_state()

    def set_cover_position(self, position, **kwargs):
        pos = self.position - position
        pos = abs(pos)

        pos = self._time * (100/pos)

        if self.position > position:
            states = [0 , 0 , 0 , 0]
            states[self._pin - 1] = 2
        else:
            states = [0 , 0 , 0 , 0]
            states[self._pin - 1] = 1

        t1 = pos
        control = self._id + t1 + sum(states)

        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        send_command(command)

        self._position = position
        self.schedule_update_ha_state()

    @property
    def position(self):
        return self._position

    @property
    def state(self):
        return self._state
