import asyncio

from .switch import Switch
from .const import LOCK_ON_ICON , LOCK_OFF_ICON , LIGHT_ON_ICON , LIGHT_OFF_ICON, GATE_ICON , RESET_ICON
from .gryf import setEnabled

from ..send import send_command

class LightEntity(Switch):
    @property
    def icon(self):
        """setting entity icon"""
        return LIGHT_ON_ICON if self._is_on else LIGHT_OFF_ICON

class LockEntity(Switch):
    @property
    def icon(self):
        """setting entity icon"""
        return LOCK_ON_ICON if self._is_on else LOCK_OFF_ICON

class GateEntity(Switch):
    @property
    def icon(self):
        """setting entity icon"""
        return GATE_ICON
        
    async def async_turn_on(self, **kwargs):
        await self.create_command("1")
        await asyncio.sleep(1)
        await self.create_command("2")

    async def async_turn_off(self, **kwargs):
        pass

    async def async_toggle(self, **kwargs):
        pass

class Connection_switch(Switch):
    @property
    def icon(self):
        """setting entity icon"""
        return GATE_ICON

    async def async_added_to_hass(self):
        setEnabled(False)
        self._is_on = False
        self.async_write_ha_state()
        
    async def async_turn_on(self, **kwargs):
        setEnabled(True)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        setEnabled(False)
        self._is_on = False
        self.async_write_ha_state()

    async def async_toggle(self, **kwargs):
        pass