
from homeassistant.helpers.entity import Entity
from homeassistant.components.light import LightEntity
from enum import Enum

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the custom alarm control panel."""
    
    cw = {
        "id": 1,
        "pin": 1,
        "name": "entity_light"
    }
    add_entities([MyLightEntity(cw)])

class device_types(Enum):
    classic_schema = 0
    cover_schema = 1
    climate_schema = 2

class __device:
    def __init__(self , config , schema: device_types) -> None:
        self._schema = schema

        if schema == device_types.classic_schema:
            self._id = config.get("id")
            self._pin = config.get("pin")
            self._name = config.get("name")

    @property
    def name(self):
        return self._name
    
    @property
    def pin(self):
        return self._pin

    @property
    def id(self):
        return self._id

class MyBaseEntity(Entity):
    def __init__(self , config) -> None:
        # Inicjalizowanie _device w konstruktorze klasy bazowej
        self._device = __device(config, device_types.classic_schema)
    
    @property
    def name(self):
        return self._device.name

    def update_custom_state(self, state):
        """Method to update the state of the entity."""
        self._state = state

class MyLightEntity(LightEntity, MyBaseEntity):
    def __init__(self, config):
        # Wywołanie konstruktora klasy bazowej
        super().__init__(config)
        self._is_on = False

    @property
    def is_on(self):
        """Return the state of the light."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        self._is_on = True
        self.update_custom_state("light is on")

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        self._is_on = False
        self.update_custom_state("light is off")
