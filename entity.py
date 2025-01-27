"Base Entity for GryfSmart"

from __future__ import annotations

from .const import CONF_NAME
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from pygryfsmart.api import GryfApi
from pygryfsmart.const import DriverFunctions
from .device import _GryfDevice , _GryfOutput

import logging

_LOGGER = logging.getLogger(__name__)

class _GryfSmartEntityBase(Entity):
    _attr_should_poll = False
    _api: GryfApi

    @property
    def name(self) -> str:
        """Returns the name of Gryf Smart device"""
        return self._device.name

    # @property
    # def available(self) -> bool:
    #     return self._api.data

    # async def async_added_to_hass(self) -> None:

class GryfYamlEntity(_GryfSmartEntityBase):

    def __init__(self , device: _GryfDevice , api: GryfApi):
        self._api = api
        self._device = device
        

