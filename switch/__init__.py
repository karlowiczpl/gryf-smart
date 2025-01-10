from .related import LightEntity , LockEntity , GateEntity
from .reset import ResetEntity

from ..send import send_command
from ..update_states import update_states
from ..harmonogram import setup_date_time
from ..const import CONF_NAME , CONF_PIN , CONF_ID , CONF_TIME

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

async def setup_entities(config , clas, hass):
    global switches

    for item in config:
        entity = clas(item.get("name") , item.get("id") , item.get("pin"))
        if item.get("harmonogram") is not None:
            await setup_date_time(hass , item.get("name") , entity , item.get("harmonogram"))
        switches.append(entity)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global switches

    light_config = discovery_info[0] or []
    lock_config = discovery_info[1] or []
    gate_config = discovery_info[2] or []

    await setup_entities(light_config , LightEntity , hass)
    await setup_entities(lock_config , LockEntity , hass)
    await setup_entities(gate_config , GateEntity , hass)

    async_add_entities([ResetEntity("GRYF RST" , 0 , 0)])
    async_add_entities(switches)

async def new_switch_command(parsed_states):
    if switches:
        for i in range(len(switches)):
            await switches[i].feedback(parsed_states)
