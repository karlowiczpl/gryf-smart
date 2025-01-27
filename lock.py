from homeassistant.components.lock import LockEntity

from .device import _GryfOutput
from .entity import GryfYamlEntity

class GryfLock(GryfYamlEntity , LockEntity):

    def __init__(self, device: _GryfOutput):
        self._device = device
        self._device.set_update_function(self.update)

    async def update(self , data):
        self._is_locked = data
        self.async_write_ha_state()

    @property
    def is_locked(self):
        return self._is_locked

    async def async_turn_on(self, **kwargs):
        await self._device.turn_on()

    async def async_turn_off(self, **kwargs):
        await self._device.turn_off()

    async def async_toggle(self , **kwargs):
        await self._device.toggle()
