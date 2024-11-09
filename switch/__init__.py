from .switch import Switch
from .related import LightEntity , LockEntity , GateEntity
from .reset import ResetEntity

switches = []

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global switches

    light_config = discovery_info[0] or []
    lock_config = discovery_info[1] or []
    port = discovery_info[2] or []
    gate_config = discovery_info[3] or []

    for light in light_config:
        name = light.get("name")
        switch_id = light.get("id")
        pin = light.get("pin")
        switches.append(LightEntity(name, switch_id, pin))

    for lock in lock_config:
        name = lock.get("name")
        switch_id = lock.get("id")
        pin = lock.get("pin")
        switches.append(LockEntity(name, switch_id, pin))

    for gate in gate_config:
        name = gate.get("name")
        switch_id = gate.get("id")
        pin = gate.get("pin")
        switches.append(GateEntity(name, switch_id, pin))

    switches.append(ResetEntity("GRYF RST" , 0 , 0))

    async_add_entities(switches)

async def new_switch_command(parsed_states):
    if switches:
        for i in range(len(switches)):
            await switches[i].feedback(parsed_states)