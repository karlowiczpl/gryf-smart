from homeassistant.components.lock import LockEntity, LockEntityFeature

from enum import Enum

from .send import send_command
from .const import CONF_HARMONOGRAM, CONF_NAME , CONF_PIN , CONF_ID 

locks = []

class States(Enum):
    LOCK = 0
    UNLOCK = 1
    LOCKING = 2
    UNLOCKING = 3

async def new_lock_command(parsed_states):
    if locks:
        for lock in locks:
            await lock.feedback(parsed_states)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    # async_add_entities([GryfLock("test" , 3 , 1 , 1 , 1)])
    global locks
    lock_config = discovery_info or []

    for item in lock_config:
        locks.append(GryfLock(item.get(CONF_NAME) , item.get(CONF_ID) , item.get(CONF_PIN) , 1 , 1))

    async_add_entities(locks)

class GryfLock(LockEntity):

    def __init__(self, name, id_o, pin_o , id_i , pin_i):
        self._name = name
        self._id = id_o  
        self._pin = pin_o
        self._id_i = id_i
        self._pin_i = pin_i
        self._attr_supported_features = LockEntityFeature.OPEN
        self._state = 1
        self._open = False

    # async def async_added_to_hass(self):
    #     await super().async_added_to_hass()
    #     if (last_state := await self.async_get_last_state()) is not None:
    #         self._is_on = last_state.state == "on"
    
    async def async_lock(self):
        self.create_command("1")
        self._state = States.LOCKING

    async def async_unlock(self):
        self.create_command("1")
        self._state = States.UNLOCKING

    async def async_open(self):
        pass

    async def feedback(self, parsed_states):
        if parsed_states[0] == str(self._id):
            self._state = int(parsed_states[self._pin])
            self.async_write_ha_state()

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
