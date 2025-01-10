import asyncio
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_HOST

from .const import PORT

_LOGGER = logging.getLogger(__name__)

class TCPClientSensor(SensorEntity):
    def __init__(self, host):
        self._host = host
        self._port = PORT
        self._state = None
        self._client_task = None
        self._tcp_socket = None

    @property
    def name(self):
        return "GRYF IN"

    @property
    def native_value(self):
        return self._state

    async def async_added_to_hass(self):
        _LOGGER.debug("Connecting to %s:%s", self._host, self._port)
        await self._connect_to_server()

    async def stop_serial_read(self):
        if self._client_task:
            self._client_task.cancel()
        if self._tcp_socket:
            self._tcp_socket[1].close()
            await self._tcp_socket[1].wait_closed()

    async def async_update(self):
        if self._tcp_socket is None:
            _LOGGER.error("TCP connection is not established. Reconnecting...")
            await self._connect_to_server()

    def send_data(self, message):
        if self._tcp_socket is None:
            _LOGGER.error("TCP connection is not established.")
            return
        try:
            writer = self._tcp_socket[1]
            writer.write(message.encode("utf-8"))
            writer.flush()  
            _LOGGER.debug("Logger: %s", message)
        except Exception as e:
            _LOGGER.error("Error while sending data: %s", e)

    async def _connect_to_server(self):
        self._tcp_socket = await asyncio.open_connection(self._host, self._port)
        self._client_task = asyncio.create_task(self._listen_for_data())

    async def _listen_for_data(self):

        if self._tcp_socket is None:
            return

        reader = self._tcp_socket[0]
        while True:
            try:
                data = await reader.read(1024)
                if not data:
                    break
                self._state = data.decode("utf-8").strip()
                _LOGGER.debug("Received data: %s", self._state)
                self.schedule_update_ha_state()
            except (asyncio.TimeoutError, OSError) as e:
                _LOGGER.error("Error receiving data from %s:%s - %s", self._host, self._port, e)
                self._state = "Error"
                break

def setup_platform(hass, config, add_entities, discovery_info=None):
    host = config[CONF_HOST]

    add_entities([TCPClientSensor(host)], True)
