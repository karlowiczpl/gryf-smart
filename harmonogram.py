from homeassistant.helpers.storage import Store

import uuid
from datetime import datetime

from .const import HELPER_DATETIME_OFF, HELPER_DATETIME_ON , HELPER_BOOLEAN_OFF , HELPER_BOOLEAN_ON , HELPER_BOOLEAN_OFF , CONF_ALL , CONF_ON , CONF_OFF

System_on = True
names = []
ptrs = []

async def setup_date_time(hass, name: str, ptr , mode):
    global names
    global ptrs
    if mode == CONF_ALL:
        await create_enable_button(hass , name + HELPER_BOOLEAN_ON)
        await create_enable_button(hass , name + HELPER_BOOLEAN_OFF)
        await create_time(hass , name , 2)
    elif mode == CONF_ON:
        await create_enable_button(hass , name + HELPER_BOOLEAN_ON)
        await create_time(hass , name , 0)
    elif mode == CONF_OFF:
        await create_enable_button(hass , name + HELPER_BOOLEAN_OFF)
        await create_time(hass , name , 1)

    names.append(name)
    ptrs.append(ptr)

def async_while(hass):
    now = datetime.now()
    for name, ptr in zip(names, ptrs):
        id = f"input_boolean.{name.replace(" ", "_").lower()}"
        en_on_state = hass.states.get(id + HELPER_BOOLEAN_ON)
        en_off_state = hass.states.get(id + HELPER_BOOLEAN_OFF)

        id = f"input_datetime.{name.replace(" ", "_").lower()}"
        on_state = hass.states.get(id + HELPER_DATETIME_ON)
        off_state = hass.states.get(id + HELPER_DATETIME_OFF)
        if on_state is not None and now.hour == on_state.attributes.get("hour", 0) and now.minute == on_state.attributes.get("minute", 0) and en_on_state.state == CONF_ON:
            ptr.turn_on()
        if off_state is not None and now.hour == off_state.attributes.get("hour", 0) and now.minute == off_state.attributes.get("minute", 0) and en_off_state.state == CONF_ON:
            ptr.turn_off()

        
def system_off():
    global system_on
    system_on = False

async def create_enable_button(hass, name: str):
    store = Store(hass, 1, "input_boolean")

    data = await store.async_load() or {"items": []}

    if any(item["name"] == name for item in data["items"]):
        return

    new_helper = {
        "id": str(uuid.uuid4()),
        "name": name,
    }

    data["items"].append(new_helper)

    await store.async_save(data)
    
async def create_time(hass, name: str , type):
    store = Store(hass, 1, "input_datetime")

    data = await store.async_load() or {"items": []}

    if any(item["name"] == (name + "_on") for item in data["items"]):
        return

    new_helper = {
        "id": str(uuid.uuid4()),
        "name": name + "_on",
        "has_time": True,
        "has_date": False,
    }
    new_helper1 = {
        "id": str(uuid.uuid4()),
        "name": name + "_off",
        "has_time": True,
        "has_date": False,
    }

    if type == 0 or type == 2:
        data["items"].append(new_helper)
    if type == 1 or type == 2:
        data["items"].append(new_helper1)

    await store.async_save(data)
