from homeassistant.helpers.storage import Store
import uuid
import asyncio
import logging
from datetime import datetime


System_on = True
names = []
ptrs = []

async def setup_date_time(hass, name: str, ptr , mode):
    global names
    global ptrs
    if mode == "all":
        await create_enable_button(hass , name + "_en_on")
        await create_enable_button(hass , name + "_en_off")
        await create_time(hass , name , 2)
    elif mode == "on":
        await create_enable_button(hass , name + "_en_on")
        await create_time(hass , name , 0)
    elif mode == "off":
        await create_enable_button(hass , name + "_en_off")
        await create_time(hass , name , 1)

    names.append(name)
    ptrs.append(ptr)

def async_while(hass):
    now = datetime.now()
    for name, ptr in zip(names, ptrs):
        id = f"input_boolean.{name.replace(" ", "_").lower()}"
        en_on_state = hass.states.get(id + "_en_on")
        en_off_state = hass.states.get(id + "_en_off")

        id = f"input_datetime.{name.replace(" ", "_").lower()}"
        on_state = hass.states.get(id + "_on")
        off_state = hass.states.get(id + "_off")
        # _LOGGER.debug("Logger: %s and %s == %s and %s and %s", en_on_state.state , now.hour , on_state.attributes.get("hour", 0) , now.minute , on_state.attributes.get("minute", 0))
        if on_state is not None and now.hour == on_state.attributes.get("hour", 0) and now.minute == on_state.attributes.get("minute", 0) and en_on_state.state == "on":
            ptr.turn_on()
        if off_state is not None and now.hour == off_state.attributes.get("hour", 0) and now.minute == off_state.attributes.get("minute", 0) and en_off_state.state == "on":
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
