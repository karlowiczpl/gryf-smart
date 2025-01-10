import serial
import logging
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

ser = None
sensorEntity = []
tcp_client = None

def set_tcp_client(tcp):
    global tcp_client
    tcp_client = tcp

def setupPlatform(async_add_entities):
    global sensorEntity

    sensorEntity.append(SendSensor())

    async_add_entities(sensorEntity)

def setup_serial(port):
    global ser
    
    ser = serial.Serial(port, 115200, timeout=1)

def send_command(command):
    full_command = command + "\r\n"
    _LOGGER.debug("Logger: %s", command)
    if ser: 
        try:
            ser.write(full_command.encode('utf-8'))
            sensorEntity[0].set_new_state(command)
        except Exception as e:
            print(f"Error sending command: {e}")
    if tcp_client:
        tcp_client.send_data(full_command)

class SendSensor(SensorEntity):

    def __init__(self) -> None:
        self._state = None
        self._name = "Gryf OUT"

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def get_id(self):
        return self._id
    
    @property
    def get_pin(self):
        return self._pin

    def set_new_state(self, state) -> None:
        self._state = state
        self.schedule_update_ha_state()