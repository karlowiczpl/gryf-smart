from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from .serial import SerialSensor
from .sensor import Sensor , TemperaureSensor
from .tcp_sensor import TCPClientSensor

from ..send import setupPlatform, set_tcp_client
from ..const import CONF_NAME , CONF_ID , CONF_PIN

buttons = []
temp = []

async def input_state_relaod(parsed_states):
    if buttons:
        for i in range(len(buttons)):
            if str(buttons[i].get_id) == parsed_states[0]:
                pin = buttons[i].get_pin
                await buttons[i].set_new_state(parsed_states[pin])

async def pl_state_reload(parsed_states):
    if buttons:
        for i in range(len(buttons)):
            if str(buttons[i].get_id) == parsed_states[0] and str(buttons[i].get_pin) == parsed_states[1]:
                await buttons[i].set_new_state(3)

async def ps_state_reload(parsed_states):
    if buttons:
        for i in range(len(buttons)):
            if str(buttons[i].get_id) == parsed_states[0] and str(buttons[i].get_pin) == parsed_states[1]:
                await buttons[i].set_new_state(2)

async def temp_reload(parsed_states):
    if temp:
        for i in range(len(temp)):
            if str(temp[i].get_id) == parsed_states[0] and str(temp[i].get_pin) == parsed_states[1]:
                result_str = f"{parsed_states[2]}.{parsed_states[3]}"

                await temp[i].set_new_state(result_str)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global buttons
    global temp

    buttons_config = discovery_info[0] or []
    port_config = discovery_info[1] or None
    temperature_config = discovery_info[2] or []
    ip_config = discovery_info[3] or None

    for button in buttons_config:
        buttons.append(Sensor(button.get(CONF_NAME), button.get(CONF_ID), button.get(CONF_PIN)))

    for temperature in temperature_config:
        temp.append(TemperaureSensor(temperature.get(CONF_NAME), temperature.get(CONF_ID), temperature.get(CONF_PIN)))
    
    async_add_entities(buttons)
    async_add_entities(temp)

    sensor = None

    if port_config != None:
        sensor = SerialSensor(port_config)
    elif ip_config != None:
        sensor = TCPClientSensor(ip_config)
        set_tcp_client(sensor)


    async_add_entities([sensor], True)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, sensor.stop_serial_read)

    setupPlatform(async_add_entities)
