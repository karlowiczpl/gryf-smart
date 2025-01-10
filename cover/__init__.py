from ..const import CONF_ID, CONF_NAME, CONF_PIN, CONF_TIME, CONF_HARMONOGRAM
from .cover import Cover
from .related import Ha_position_cover

from ..harmonogram import setup_date_time

covers = []

STATE_PAUSED = "zatrzymano"

async def new_rols_command(parsed_states):
    if covers:
        for i in range(len(covers)):
            if str(covers[i].get_id) == parsed_states[0]:
                await covers[i].changeRolState(parsed_states)

async def setup_entities(config , clas, hass):
    global covers

    for item in config:
        entity = clas(item.get(CONF_NAME) , item.get(CONF_ID) , item.get(CONF_PIN) , item.get(CONF_TIME))
        if item.get(CONF_HARMONOGRAM) is not None:
            await setup_date_time(hass , item.get(CONF_NAME) , entity , item.get(CONF_HARMONOGRAM))
        covers.append(entity)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global covers

    cover_config = discovery_info[0] or []
    p_cover_config = discovery_info[1] or []

    await setup_entities(cover_config , Cover , hass);
    await setup_entities(p_cover_config , Ha_position_cover , hass);

    async_add_entities(covers)
