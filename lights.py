from homeassistant.helpers.entity import Entity
from homeassistant.components.light import LightEntity

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the custom alarm control panel."""
    add_entities([MyLightEntity("entity_light")])
    
class MyLightEntity(LightEntity):
    def __init__(self, name):
        # Wywołanie konstruktorów obu klas bazowych
        MyBaseEntity.__init__(self, name)
        self._is_on = False

    @property
    def is_on(self):
        """Zwraca stan światła."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Włącza światło."""
        self._is_on = True
        self.update_custom_state("light is on")  # Użycie metody z MyBaseEntity

    async def async_turn_off(self, **kwargs):
        """Wyłącza światło."""
        self._is_on = False
        self.update_custom_state("light is off")  # Użycie metody z MyBaseEntity
