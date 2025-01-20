from homeassistant.helpers.entity import Entity
from homeassistant.components.light import LightEntity

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the custom alarm control panel."""
    add_entities([MyLightEntity("entity_light")])
# Klasa bazowa dziedzicząca z Entity
class MyBaseEntity(Entity):
    def __init__(self, name):
        self._name = name
        self._custom_state = "default"

    @property
    def name(self):
        """Zwraca nazwę encji."""
        return self._name

    @property
    def custom_state(self):
        """Zwraca niestandardowy stan."""
        return self._custom_state

    def update_custom_state(self, new_state):
        """Aktualizuje niestandardowy stan."""
        self._custom_state = new_state

# Klasa specyficzna dziedzicząca z LightEntity i MyBaseEntity
class MyLightEntity(LightEntity, MyBaseEntity):
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
