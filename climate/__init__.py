from .climate import Climate

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
        name = climate.get("name")
        t_id = climate.get("t_id")
        t_pin = climate.get("t_pin")
        o_id = climate.get("o_id")
        o_pin = climate.get("o_pin")
        climates.append(Climate(name, t_id, t_pin, o_id, o_pin))

    async_add_entities(climates)