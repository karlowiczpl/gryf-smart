from .switch import Switch
from .related import LightEntity , LockEntity , GateEntity
from .reset import ResetEntity
from ..send import send_command
from ..update_states import update_states
from ..harmonogram import setup_date_time

import asyncio

switches = []

async def reset_switch():
    merged = {}

    for switch in switches[:-1]:
        switch_id = switch.get_id
        switch_pin = switch.get_pin

        if switch_id not in merged:
            merged[switch_id] = [None] * 8
        merged[switch_id][switch_pin - 1] = switch

    await asyncio.sleep(5)
    for switch_id, pins in merged.items():

        states = [0] * (8 if len(pins) > 6 else 6)
        for pin_index, switch in enumerate(pins):
            if switch:
                if switch.is_on:
                    states[pin_index] = 1 
                else:
                    states[pin_index] = 2

        if states[7] == 0 and states[6] == 0:
            states.pop()
            states.pop()

        command = f"AT+SetOut={switch_id},{','.join(map(str, states))}"
        send_command(command)

        await asyncio.sleep(0.1)
    
    await update_states()



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
        entity = LightEntity(name, switch_id, pin)
        if light.get("harmonogram") is not None:
            await setup_date_time(hass , name, entity , light.get("harmonogram"))
        switches.append(entity)

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

    async_add_entities([ResetEntity("GRYF RST" , 0 , 0)])
    async_add_entities(switches)

    # for item in light_config:
    #     if item.get("harmonogram") is not None:
    #         await setup_date_time(hass , item.get("name"))


async def new_switch_command(parsed_states):
    if switches:
        for i in range(len(switches)):
            await switches[i].feedback(parsed_states)
