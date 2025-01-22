from homeassistant.helpers.event import async_track_state_change_event 

import re
import asyncio
import logging

from .output import async_output_state_changed

_LOGGER = logging.getLogger(__name__)

async def setup_devices(hass):
    async_track_state_change_event(hass, 'sensor.gryf_in', wrapped_state_changed)

async def sensor_state_changed(event):
    global first

    data = event.data.get('new_state')
    data = str(data)

    parts = data.split('=')
    parsed_states = parts[2].split(',')
    last_state = parsed_states[-1].split(';')
    parsed_states[-1] = last_state[0]
    
    parsed_states = filtr_parsed_states(parsed_states)

    if str(parts[0] == "O"):
        await async_output_state_changed(parsed_states)



def filtr_parsed_states(parsed_states):
    result = [re.sub(r'\D', '', item) for item in parsed_states]
    return result

async def wrapped_state_changed(event):
    task = asyncio.create_task(sensor_state_changed(event))
    try:
        await asyncio.wait_for(task, timeout=1)
    except TimeoutError:
        _LOGGER.warning("Task timed out while handling event: %s", event)
    except Exception as e:
        _LOGGER.error("Unexpected error in wrapped_state_changed: %s", e)
