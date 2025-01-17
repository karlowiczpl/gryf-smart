from homeassistant.components.lock import LockEntity, LockEntityFeature

from enum import Enum

from .send import send_command

class States(Enum):
    LOCK = 1
    LOCKING = 2
    UNLOCK = 3
    UNLOCKING = 4

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([GryfLock("test" , 3 , 1 , 1 , 1)])

class GryfLock(LockEntity):

    def __init__(self, name, id_o, pin_o , id_i , pin_i):
        self._name = name
        self._is_on = False
        self._id = id_o  
        self._pin = pin_o
        self._id_i = id_i
        self._pin_i = pin_i
        self._attr_supported_features = LockEntityFeature.OPEN
        self._state = 1

    # async def async_added_to_hass(self):
    #     await super().async_added_to_hass()
    #     if (last_state := await self.async_get_last_state()) is not None:
    #         self._is_on = last_state.state == "on"
    
    async def async_lock(self):
        self.create_command("1")

    async def async_unlock(self):
        self.create_command("1")

    async def async_open(self):
        pass

    async def feedback(self, parsed_states):
        pass

    @property
    def is_locked(self):
        return self._state == States.LOCK
    
    @property
    def is_locking(self):
        return self._state == States.LOCKING

    @property
    def is_unlocking(self):
        return self._state == States.UNLOCKING

    @property
    def is_opening(self):
        return False

    @property
    def is_open(self):
        return self._open

    @property
    def name(self):
        return self._name

    def create_command(self , state):
        if self._pin > 6:
            states_list = ["0", "0", "0", "0", "0", "0" , "0" , "0"]
        else:
            states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = state
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        send_command(command)
    # @property
    # def suported_features(self):
    #     return SUPPORT_OPEN
