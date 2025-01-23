from homeassistant.core import callback

import logging
import asyncio
import serial
import serial_asyncio

_LOGGER = logging.getLogger(__name__)

class GryfSmartApi:
    """Class to communicate with GryfSmart devices"""

    def __init__(
            self,
            port: str,
            hass,
    ) -> None:
        self.port = port
        self._serial_loop_task = None
        self.hass = hass
        self.data = {"OUT": {} , "IN": {} , "TEMP": {}} 

        if self._serial_loop_task:
            _LOGGER.warning("Serial read task already running. Skipping initialization.")
            return
        self._serial_loop_task = self.hass.loop.create_task(self.read_from_serial())
        _LOGGER.info("Serial read task started.")

    async def custom_readline(self, reader):
        try:
            buffer = await reader.readuntil(b'\n')
            return buffer.strip()
        except asyncio.IncompleteReadError as e:
            _LOGGER.error("Incomplete read error: %s", e)
            return b''
        except Exception as e:
            _LOGGER.error("Unexpected error in custom_readline: %s", e)
            return b''

    async def read_from_serial(self):
        """Pętla odczytu danych z portu szeregowego."""
        while True:
            try:
                _LOGGER.debug("Opening serial connection on %s", self.port)
                reader, _ = await serial_asyncio.open_serial_connection(
                    url=self.port,
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    xonxoff=False,
                    rtscts=False,
                    dsrdtr=False
                )
                _LOGGER.info("Serial connection opened on %s", self.port)
                while True:
                    try:
                        line = await self.custom_readline(reader)
                        _LOGGER.debug("Received line: %s", line)

                        line = line.decode("utf-8").strip()
                        _LOGGER.debug("Decoded line: %s", line)
                        self._state = line
                        _LOGGER.debug("State updated to: %s", self._state)

                        self.parse_data(line)
                        

                    except serial.SerialException as e:
                        _LOGGER.error("SerialException during read: %s", e)
                        await self._handle_error()
                        continue

                    except asyncio.CancelledError:
                        _LOGGER.debug("Serial read task cancelled")
                        break

                    except Exception as e:
                        _LOGGER.error("Unexpected error during read: %s", e)
                        await self._handle_error()
                        break

            except serial.SerialException as err:
                _LOGGER.error("Failed to open serial connection: %s", err)
                await self._handle_error()
            except asyncio.CancelledError:
                _LOGGER.debug("Serial read task cancelled during connection setup")
                break 
            except Exception as e:
                _LOGGER.error("Unexpected error while opening serial connection: %s", e)
                await self._handle_error()
    @callback
    def stop_serial_read(self, event):
        if self._serial_loop_task and not self._serial_loop_task.done():
            try:
                _LOGGER.debug("Stopping serial read task")
                self._serial_loop_task.cancel()
            except asyncio.CancelledError:
                _LOGGER.debug("Serial read task already cancelled")

    def parse_data(self, data):
        try:
            parts = data.split('=')
            parsed_states = parts[1].split(',')
            last_state = parsed_states[-1].split(';')
            parsed_states[-1] = last_state[0]

            if parts[0] == "I":
                for i in range(1, len(parsed_states)):
                    self.data["IN"][f"{parsed_states[0]}{i}"] = int(parsed_states[i])

            if parts[0] == "O":
                for i in range(1, len(parsed_states)):
                    self.data["OUT"][f"{parsed_states[0]}{i}"] = int(parsed_states[i])

            if parts[0] == "T":
                self.data["TEMP"][f"{parsed_states[0]}{parsed_states[1]}"] = float(f"{parsed_states[2]}.{parsed_states[3]}")
        except Exception as e:
            _LOGGER.error("Error parsing data: %s", e)
    async def _handle_error(self):
        _LOGGER.warning("Handling error and retrying connection...")
        await asyncio.sleep(5)

        
