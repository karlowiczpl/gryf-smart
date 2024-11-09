from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity , SensorDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.restore_state import RestoreEntity

class Sensor(SensorEntity , RestoreEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, name, button_id, pin) -> None:
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._id = button_id
        self._pin = pin

    async def async_added_to_hass(self):
        """restoring last state."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            self._is_on = last_state.state

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def get_id(self):
        return self._id
    
    @property
    def get_pin(self):
        return self._pin

    async def set_new_state(self, state) -> None:
        """Fetch new state data for the sensor."""
        self._state = state
        self.async_write_ha_state()
    

class TemperaureSensor(Sensor):
    def __init__(self, hass: HomeAssistant, name, button_id, pin) -> None:
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._id = button_id
        self._pin = pin

        """set extra parametrs"""
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS

    async def async_added_to_hass(self):
        pass