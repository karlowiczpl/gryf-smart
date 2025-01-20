from .send import send_command

from homeassistant.helpers.entity import Entity
from homeassistant.components.light import LightEntity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([gryf_light(3 , 1)])

class _gryf_output():
    def __init__(self , id , pin) -> None:
        self._id = id
        self._pin = pin
    
    def set_on(self):
        self.create_command("1")

    def set_off(self):
        self.create_command("2")

    def set_toggle(self):
        self.create_command("3")

    def create_command(self , state):
        if self._pin > 6:
            states_list = ["0", "0", "0", "0", "0", "0" , "0" , "0"]
        else:
            states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = state
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        send_command(command)

class gryf_light(LightEntity , _gryf_output):
    def __init__(self, id, pin) -> None:
        super().__init__(id, pin)
        self._name = "tescior"

    @property
    def name(self):
        return self._name

    async def async_turn_on(self):
        self.set_on()

    async def async_turn_off(self):
        self.set_off()

    async def assync_toggle(self):
        self.set_toggle()
