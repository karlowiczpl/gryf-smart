from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity , SensorDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.restore_state import RestoreEntity

class Sensor(SensorEntity , RestoreEntity):

    def __init__(self, name, button_id, pin) -> None:
        self._state = None
        self._name = name
        self._id = button_id
        self._pin = pin

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_on = last_state.state

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def get_id(self):
        return self._id
    
    @property
    def get_pin(self):
        return self._pin

    async def set_new_state(self, state) -> None:
        self._state = state
        self.async_write_ha_state()
    
class TemperaureSensor(Sensor):
    def __init__(self, name, button_id, pin) -> None:
        self._state = None
        self._name = name
        self._id = button_id
        self._pin = pin

        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS

    async def async_added_to_hass(self):
        pass
