from .binary_sensor import DoorSensor , WindowSensor

binary_sensor = []

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global binary_sensor
    
    doors_config = discovery_info[0] or []
    windows_config = discovery_info[1] or []

    for door in doors_config:
        name = door.get("name")
        door_id = door.get("id")
        pin = door.get("pin")
        binary_sensor.append(DoorSensor(name, door_id, pin))

    for window in windows_config:
        name = window.get("name")
        door_id = window.get("id")
        pin = window.get("pin")
        binary_sensor.append(WindowSensor(name, door_id, pin))

    async_add_entities(binary_sensor)

async def updateAllStates(array):
    if binary_sensor:
        for sensor in binary_sensor:
            sensor.change_state(array)