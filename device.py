from pygryfsmart.api import GryfApi
from pygryfsmart.const import DriverFunctions
from pygryfsmart.const import OUTPUT_STATES

import logging

_LOGGER = logging.getLogger(__name__)

class _GryfDevice:
    pass

class _GryfOutput(_GryfDevice):

    def __init__(self, 
                 name: str,
                 id: str,
                 pin: str,
                 api: GryfApi, 
                 ):
        self._name = name
        self._id = id
        self._pin = pin
        self._api = api
        self._update_fun_ptr = None

    def set_update_function(self , fun_ptr):
        self._api.subscribe(self._id , self._pin , "O" , fun_ptr)

    @property
    def name(self):
        return self._name

    async def turn_on(self):
        await self._api.set_out(self._id , self._pin , OUTPUT_STATES.ON)

    async def turn_off(self):
        await self._api.set_out(self._id , self._pin , OUTPUT_STATES.OFF)

    async def toggle(self):
        await self._api.set_out(self._id , self._pin , OUTPUT_STATES.TOGGLE)
