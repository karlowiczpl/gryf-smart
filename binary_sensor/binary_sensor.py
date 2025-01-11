from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.restore_state import RestoreEntity

from ..const import DOOR_DEVICE_CLASS , WINDOW_DEVICE_CLASS

class BinarySensorEntity(BinarySensorEntity, RestoreEntity):
    def __init__(self, name: str, door_id, pin):
        self._name = name
        self._is_open = False
        self._pin = pin
        self._id = door_id

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_open = last_state.state == "on"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_open

    def change_state(self, array):
        if array[0] == str(self._id):
            if array[self._pin] == str(1):
                self.turn_close()
            else:
                self.turn_open()

    def turn_open(self):
        self._is_open = True
        self.schedule_update_ha_state()

    def turn_close(self):
        self._is_open = False
        self.schedule_update_ha_state()

class DoorSensor(BinarySensorEntity):
    @property
    def device_class(self):
        return DOOR_DEVICE_CLASS

class WindowSensor(BinarySensorEntity):
    @property
    def device_class(self):
        return WINDOW_DEVICE_CLASS
