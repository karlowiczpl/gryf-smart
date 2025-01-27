from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
import voluptuous as vol
import logging
import asyncio

from .const import CONF_MODULE_COUNT, DOMAIN , CONF_LIGHTS , CONF_BUTTON , CONF_NAME , CONF_ID , CONF_PIN , CONF_SERIAL , CONF_DOORS , CONF_WINDOW , CONF_TEMPERATURE , CONF_COVER , CONF_TIME , CONF_LOCK , CONF_PWM , CONF_CLIMATE , CONF_T_ID , CONF_O_ID , CONF_T_PIN , CONF_O_PIN , CONF_ID_COUNT , CONF_GATE , CONF_P_COVER , CONF_IP , CONF_STATES_UPDATE , CONF_HARMONOGRAM , CONF_TILT , CONF_MODULE_COUNT

from pygryfsmart.api import GryfApi 

first = True
conf = None

_LOGGER = logging.getLogger(__name__)

STANDARD_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_ID): cv.positive_int,
    vol.Required(CONF_PIN): cv.positive_int,
})
SENSOR_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_ID): cv.positive_int,
    vol.Required(CONF_PIN): cv.positive_int,
})
COVER_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_ID): cv.positive_int,
    vol.Required(CONF_PIN): cv.positive_int,
    vol.Required(CONF_TIME): cv.positive_int,
    vol.Optional(CONF_TILT): cv.positive_int
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
        vol.Optional(CONF_BUTTON): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
        vol.Optional(CONF_DOORS): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
        vol.Optional(CONF_WINDOW): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
        vol.Optional(CONF_TEMPERATURE): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
        vol.Optional(CONF_COVER): vol.All(cv.ensure_list, [COVER_SCHEMA]),
        vol.Optional(CONF_P_COVER): vol.All(cv.ensure_list, [COVER_SCHEMA]),
        vol.Optional(CONF_LOCK): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_PWM): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_GATE): vol.All(cv.ensure_list, [STANDARD_SCHEMA]),
        vol.Optional(CONF_CLIMATE): vol.All(cv.ensure_list, [CLIMATE_SCHEMA]),
        vol.Required(CONF_SERIAL): cv.string,
        vol.Optional(CONF_MODULE_COUNT): cv.positive_int,
        vol.Optional(CONF_STATES_UPDATE): cv.positive_int,
    })
}, extra=vol.ALLOW_EXTRA)

async def su(state):
    _LOGGER.debug(f"state: {state}")

async def async_setup(hass: HomeAssistant, config: dict):
    port = config[DOMAIN].get(CONF_SERIAL)
    update_states = config[DOMAIN].get(CONF_STATES_UPDATE)
    module_count = config[DOMAIN].get(CONF_MODULE_COUNT , None)

    lights_config = config[DOMAIN].get(CONF_LIGHTS, [])
    lock_config = config[DOMAIN].get(CONF_LOCK, [])
    
    api = GryfApi(port)
    await api.start_connection()

    hass.data[DOMAIN] = api

    if update_states == True and module_count != None:
        api.start_update_interval(3)

    await async_load_platform(hass , 'light', DOMAIN, lights_config , config)
    await async_load_platform(hass , 'lock', DOMAIN, lock_config , config)

    # hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, coordinator.stop_serial_read)

    # conf = config
    #
    # if DOMAIN not in config:
    #     return True
    #
    # lights_config = config[DOMAIN].get(CONF_LIGHTS, [])
    # buttons_config = config[DOMAIN].get(CONF_BUTTON, [])
    # doors_config = config[DOMAIN].get(CONF_DOORS, [])
    # window_config = config[DOMAIN].get(CONF_WINDOW, [])
    # port_config = config[DOMAIN].get(CONF_SERIAL, None)
    # temperature_config = config[DOMAIN].get(CONF_TEMPERATURE , [])
    # cover_config = config[DOMAIN].get(CONF_COVER , [])
    # lock_conf = config[DOMAIN].get(CONF_LOCK , [])
    # pwm_config = config[DOMAIN].get(CONF_PWM , [])
    # climate_config = config[DOMAIN].get(CONF_CLIMATE , [])
    # gate_config = config[DOMAIN].get(CONF_GATE , [])
    # p_cover_config = config[DOMAIN].get(CONF_P_COVER , [])
    # ip_config = config[DOMAIN].get(CONF_IP , None)
    #
    # sensor_config = [buttons_config , port_config , temperature_config , ip_config]
    # binary_sensor_config = [doors_config , window_config]
    # switch_config = [lights_config , lock_conf , gate_config]

    return True
