from .binary_sensor import DoorSensor , WindowSensor

from ..const import CONF_PIN , CONF_NAME , CONF_ID

binary_sensor = []

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global binary_sensor
    
    doors_config = discovery_info[0] or []
    windows_config = discovery_info[1] or []

    for door in doors_config:
        binary_sensor.append(DoorSensor(door.get(CONF_NAME), door.get(CONF_ID), door.get(CONF_PIN)))

    for window in windows_config:
        binary_sensor.append(WindowSensor(window.get(CONF_NAME), window.get(CONF_ID), window.get(CONF_PIN)))

    async_add_entities(binary_sensor)

async def updateAllStates(array):
    if binary_sensor:
        for sensor in binary_sensor:
            sensor.change_state(array)
