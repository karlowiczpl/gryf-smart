from __future__ import annotations

import asyncio
import logging
import time

from serial import SerialException
import serial_asyncio_fast as serial_asyncio

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

class SerialSensor(SensorEntity):
    _attr_should_poll = False

    def __init__(self, port):
        self._name = "Gryf IN"
        self._state = None
        self._port = port
        self._serial_loop_task = None
        self._template = None
        self._attributes = None

    async def async_added_to_hass(self) -> None:
        _LOGGER.debug("Adding SerialSensor to Home Assistant")
        self._serial_loop_task = self.hass.loop.create_task(
            self.serial_read()
        )

    async def custom_readline(self, reader):
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
        pass
        # while True:
        #     try:
        #         _LOGGER.debug("Opening serial connection on %s", self._port)
        #         reader, _ = await serial_asyncio.open_serial_connection(
        #             url=self._port,
        #             baudrate=115200,
        #             bytesize=serial_asyncio.serial.EIGHTBITS,
        #             parity=serial_asyncio.serial.PARITY_NONE,
        #             stopbits=serial_asyncio.serial.STOPBITS_ONE,
        #             xonxoff=False,
        #             rtscts=False,
        #             dsrdtr=False
        #         )
        #     except SerialException as e:
        #         _LOGGER.error("SerialException: %s", e)
        #         await self._handle_error()
        #     else:
        #         while True:
        #             try:
        #                 line = await self.custom_readline(reader)
        #                 _LOGGER.debug("Received line: %s", line)
        #             except SerialException as e:
        #                 _LOGGER.error("SerialException during read: %s", e)
        #                 await self._handle_error()
        #                 break
        #             else:
        #                 line = line.decode("utf-8").strip()
        #                 _LOGGER.debug("Decoded line: %s", line)
        #                 self._state = line
        #                 _LOGGER.debug("State updated to: %s", self._state)
        #                 self.async_write_ha_state()

    async def _handle_error(self):
        self._state = None
        _LOGGER.debug("Resetting state and attributes due to an error")
        self.async_write_ha_state()
        await asyncio.sleep(5)

    @callback
    def stop_serial_read(self, event):
        if self._serial_loop_task:
            try:
                _LOGGER.debug("Stopping serial read task")
                self._serial_loop_task.cancel()
            except asyncio.CancelledError:
                _LOGGER.debug("Serial read task already cancelled")

    @property
    def name(self):
        return "Gryf IN"

    @property
    def native_value(self):
        return self._state
