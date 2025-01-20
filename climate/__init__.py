from .climate import Climate

from ..const import CONF_HARMONOGRAM, CONF_NAME , CONF_T_ID , CONF_T_PIN , CONF_O_PIN , CONF_O_ID , CONF_TILT
from ..harmonogram import setup_date_time

climates = []

async def new_climate_temp(parsed_states):
    if climates:
        for climate in climates:
            if str(climate.get_id) == parsed_states[0] and str(climate.get_pin) == parsed_states[1]:
                result_str = f"{parsed_states[2]}.{parsed_states[3]}"
                await climate.set_new_state(result_str)

async def new_climate_out(parsed_states):
    if climates:
        for climate in climates:
            if str(climate.get_o_id) == parsed_states[0]:
                await climate.update_out(parsed_states)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global climates

    climate_config = discovery_info or []

    for climate in climate_config:
        entity = (Climate(climate.get(CONF_NAME), climate.get(CONF_T_ID), climate.get(CONF_T_PIN), climate.get(CONF_O_ID), climate.get(CONF_O_PIN) , climate.get(CONF_TILT)))
        if climate.get(CONF_HARMONOGRAM) is not None:
            await setup_date_time(hass , climate.get(CONF_NAME) , entity , climate.get(CONF_HARMONOGRAM))
        climates.append(entity)

    async_add_entities(climates)
