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
        entity = clas(item.get("name") , item.get("id") , item.get("pin") , item.get("time"))
        if item.get("harmonogram") is not None:
            await setup_date_time(hass , item.get("name") , entity , item.get("harmonogram"))
        covers.append(entity)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global covers

    cover_config = discovery_info[0] or []
    p_cover_config = discovery_info[1] or []

    await setup_entities(cover_config , Cover , hass);
    await setup_entities(p_cover_config , Ha_position_cover , hass);

    # for cover in cover_config:
    #     name = cover.get("name")
    #     cover_id = cover.get("id")
    #     pin = cover.get("pin")
    #     time = cover.get("time")
    #     covers.append(Cover(name, cover_id, pin, time))
    #
    # for cover in p_cover_config:
    #     name = cover.get("name")
    #     cover_id = cover.get("id")
    #     pin = cover.get("pin")
    #     time = cover.get("time")
    #     covers.append(Ha_position_cover(name, cover_id, pin, time))

    async_add_entities(covers)
