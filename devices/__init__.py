import logging
import asyncio
import re

from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.core import HomeAssistant

from .output import new_output_command

_LOGGER = logging.getLogger(__name__)

async def wrapped_state_changed(event):
    task = asyncio.create_task(sensor_state_changed(event))
    try:
        await asyncio.wait_for(task, timeout=1)
    except TimeoutError:
        _LOGGER.warning("Task timed out while handling event: %s", event)
    except Exception as e:
        _LOGGER.error("Unexpected error in wrapped_state_changed: %s", e)
async def async_device_init(hass: HomeAssistant):
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

    # if first:
    #     first = False
    #     await setup_update_states(conf[DOMAIN].get(CONF_ID_COUNT, 0) , conf[DOMAIN].get(CONF_STATES_UPDATE, True))

    if str(parts[1]) == "O":
        new_output_command(parsed_states)

    # if str(parts[1]) == "I":
    #
    # if str(parts[1]) == "PL":
    #
    # if str(parts[1]) == "PS":
    #
    # if str(parts[1]) == "T":
    #
    # if str(parts[1]) == "R":
def filtr_parsed_states(parsed_states):
    result = [re.sub(r'\D', '', item) for item in parsed_states]
    return result
