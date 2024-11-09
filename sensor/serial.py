from __future__ import annotations

import asyncio
import json
import logging
import time

from serial import SerialException
import serial_asyncio_fast as serial_asyncio
import voluptuous as vol

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from ..const import BAUDRATE, GRYF_IN_NAME

_LOGGER = logging.getLogger(__name__)

class SerialSensor(SensorEntity):
    """Representation of a Serial sensor."""

    _attr_should_poll = False

    def __init__(self, port):
        """Initialize the Serial sensor."""
        self._name = GRYF_IN_NAME
        self._state = None
        self._port = port
        self._serial_loop_task = None
        self._template = None
        self._attributes = None

    async def async_added_to_hass(self) -> None:
        """Handle when an entity is about to be added to Home Assistant."""
        _LOGGER.debug("Adding SerialSensor to Home Assistant")
        self._serial_loop_task = self.hass.loop.create_task(
            self.serial_read()
        )

    async def custom_readline(self, reader):
        """Custom implementation of readline with a 1-second timeout after the first character."""
        buffer = b""
        start_time = None

        while True:
            char = await reader.read(1)
            if char == b'?':
                continue
            if start_time is None and char:
                start_time = time.monotonic()

            if char in [b"\n", b""] or (start_time and time.monotonic() - start_time > 1):
                buffer += char
                break

            buffer += char

        return buffer

    async def serial_read(self):
        """Read the data from the port."""
        while True:
            try:
                _LOGGER.debug("Opening serial connection on %s", self._port)
                reader, _ = await serial_asyncio.open_serial_connection(
                    url=self._port,
                    baudrate=BAUDRATE,
                    bytesize=serial_asyncio.serial.EIGHTBITS,
                    parity=serial_asyncio.serial.PARITY_NONE,
                    stopbits=serial_asyncio.serial.STOPBITS_ONE,
                    xonxoff=False,
                    rtscts=False,
                    dsrdtr=False
                )
            except SerialException as e:
                _LOGGER.error("SerialException: %s", e)
                await self._handle_error()
            else:
                while True:
                    try:
                        line = await self.custom_readline(reader)
                        _LOGGER.debug("Received line: %s", line)
                    except SerialException as e:
                        _LOGGER.error("SerialException during read: %s", e)
                        await self._handle_error()
                        break
                    else:
                        line = line.decode("utf-8").strip()
                        _LOGGER.debug("Decoded line: %s", line)
                        self._state = line
                        _LOGGER.debug("State updated to: %s", self._state)
                        self.async_write_ha_state()

    async def _handle_error(self):
        """Handle error for serial connection."""
        self._state = None
        _LOGGER.debug("Resetting state and attributes due to an error")
        self.async_write_ha_state()
        await asyncio.sleep(5)

    @callback
    def stop_serial_read(self, event):
        """Close resources."""
        if self._serial_loop_task:
            try:
                _LOGGER.debug("Stopping serial read task")
                self._serial_loop_task.cancel()
            except asyncio.CancelledError:
                _LOGGER.debug("Serial read task already cancelled")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state
