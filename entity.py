from homeassistant.helpers.entity import Entity

from .send import send_command

class _GryfSmartEntityBase(Entity):
    
    @property
    def get_id(self):
        return self._id

    @property
    def get_pin(self):
        return self._pin

    def send_command(self , command):
        send_command(command)
    
    def async_turn_on(self):
        self.turn_on()

    def async_turn_off(self):
        self.turn_off()

    @property
    def name(self):
        return self._name;

