"""Gryf SMART integration"""

from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change_event
import voluptuous as vol
import logging

from .sensor import input_state_relaod , ps_state_reload , pl_state_reload , temp_reload
from .binary_sensor import updateAllStates
from .switch import new_switch_command
from .cover import new_rols_command
from .send import setup_serial
from .const import DOMAIN , CONF_LIGHTS , CONF_BUTTON , CONF_NAME , CONF_ID , CONF_PIN , CONF_SERIAL , CONF_DOORS , CONF_WINDOW , CONF_TEMPERATURE , CONF_COVER , CONF_TIME , CONF_LOCK , CONF_PWM , CONF_CLIMATE
from .climate import new_climate_temp , new_climate_out

from .update_states import setup_update_states

import logging

first = True
conf = None

_LOGGER = logging.getLogger(__name__)

CONF_T_ID = "t_id"
CONF_O_ID = "o_id"
CONF_T_PIN = "t_pin"
CONF_O_PIN = "o_pin"
CONF_ID_COUNT = "id"
CONF_GATE = "gate"
CONF_P_COVER = "p_covers"

_LOGGER = logging.getLogger(__name__)

STANDARD_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_ID): cv.positive_int,
    vol.Required(CONF_PIN): cv.positive_int,
})
COVER_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_ID): cv.positive_int,
    vol.Required(CONF_PIN): cv.positive_int,
    vol.Required(CONF_TIME): cv.positive_int,
})
CLIMATE_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_T_ID): cv.positive_int,
    vol.Required(CONF_O_ID): cv.positive_int,
    vol.Required(CONF_T_PIN): cv.positive_int,
    vol.Required(CONF_O_PIN): cv.positive_int,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_LIGHTS): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_BUTTON): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_DOORS): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_WINDOW): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_TEMPERATURE): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_COVER): vol.All(cv.ensure_list, [COVER_SCHEMA]),
        vol.Optional(CONF_P_COVER): vol.All(cv.ensure_list, [COVER_SCHEMA]),
        vol.Optional(CONF_LOCK): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_PWM): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_GATE): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_CLIMATE): vol.All(cv.ensure_list, [CLIMATE_SCHEMA]),
        vol.Required(CONF_SERIAL): cv.string,
        vol.Optional(CONF_ID_COUNT): cv.positive_int,
    })
}, extra=vol.ALLOW_EXTRA)

async def sensor_state_changed(event):
    global first

    data = event.data.get('new_state')
    data = str(data)

    parts = data.split('=')
    parsed_states = parts[2].split(',')
    last_state = parsed_states[-1].split(';')
    parsed_states[-1] = last_state[0]
    
    if first:
        first = False
        await setup_update_states(conf[DOMAIN].get(CONF_ID_COUNT, 0))


    if str(parts[1]) == "O":
        await new_switch_command(parsed_states)
        await new_climate_out(parsed_states)
    
    if str(parts[1]) == "I":
        await input_state_relaod(parsed_states)
        await updateAllStates(parsed_states)

    if str(parts[1]) == "PL":
        await pl_state_reload(parsed_states)

    if str(parts[1]) == "PS":
        await ps_state_reload(parsed_states)

    if str(parts[1]) == "T":
        await temp_reload(parsed_states)
        await new_climate_temp(parsed_states)

    if str(parts[1]) == "R":
        await new_rols_command(parsed_states)


async def async_setup(hass: HomeAssistant, config: dict):
    global conf

    conf = config

    if DOMAIN not in config:
        return True

    lights_config = config[DOMAIN].get(CONF_LIGHTS, [])
    buttons_config = config[DOMAIN].get(CONF_BUTTON, [])
    doors_config = config[DOMAIN].get(CONF_DOORS, [])
    window_config = config[DOMAIN].get(CONF_WINDOW, [])
    port_config = config[DOMAIN].get(CONF_SERIAL, [])
    temperature_config = config[DOMAIN].get(CONF_TEMPERATURE , [])
    cover_config = config[DOMAIN].get(CONF_COVER , [])
    lock_conf = config[DOMAIN].get(CONF_LOCK , [])
    pwm_config = config[DOMAIN].get(CONF_PWM , [])
    climate_config = config[DOMAIN].get(CONF_CLIMATE , [])
    gate_config = config[DOMAIN].get(CONF_GATE , [])
    p_cover_config = config[DOMAIN].get(CONF_P_COVER , [])

    setup_serial(port_config)
    sensor_config = [buttons_config , port_config , temperature_config]
    binary_sensor_config = [doors_config , window_config]
    switch_config = [lights_config , lock_conf , port_config , gate_config]
    cover_conf = [cover_config , p_cover_config]

    await hass.helpers.discovery.async_load_platform('sensor', DOMAIN, sensor_config, config)
    await hass.helpers.discovery.async_load_platform('binary_sensor', DOMAIN, binary_sensor_config , config)
    await hass.helpers.discovery.async_load_platform('switch', DOMAIN, switch_config , config)
    await hass.helpers.discovery.async_load_platform('cover', DOMAIN, cover_conf , config)
    await hass.helpers.discovery.async_load_platform('number', DOMAIN, pwm_config , config)
    await hass.helpers.discovery.async_load_platform('climate', DOMAIN, climate_config , config)

    async_track_state_change_event(hass, 'sensor.gryf_in', sensor_state_changed)

    return True