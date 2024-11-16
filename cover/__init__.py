from .cover import Cover


covers = []

STATE_PAUSED = "zatrzymano"

async def new_rols_command(parsed_states):
    if covers:
        for i in range(len(covers)):
            if str(covers[i].get_id) == parsed_states[0]:
                await covers[i].changeRolState(parsed_states)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global covers

    cover_config = discovery_info or []

    for cover in cover_config:
        name = cover.get("name")
        cover_id = cover.get("id")
        pin = cover.get("pin")
        time = cover.get("time")
        covers.append(Cover(name, cover_id, pin, time))

    async_add_entities(covers)