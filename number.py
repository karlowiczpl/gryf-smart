from homeassistant.components.number import NumberEntity

from .send import send_command
from .const import CONF_NAME , CONF_HARMONOGRAM , CONF_ID , CONF_PIN

from .harmonogram import setup_date_time

pwms = []

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global pwms

    pwm_config = discovery_info or []

    for pwm_conf in pwm_config:
        entity = Pwm(pwm_conf.get(CONF_NAME), pwm_conf.get(CONF_ID), pwm_conf.get(CONF_PIN))
        if pwm_conf.get(CONF_HARMONOGRAM) is not None:
            await setup_date_time(hass , pwm_conf.get(CONF_NAME) , entity , pwm_conf.get(CONF_HARMONOGRAM))
        pwms.append(entity)

    async_add_entities(pwms)

class Pwm(NumberEntity):
    def __init__(self, name, pwm_id , pin):
        self._attr_name = name
        self._attr_min_value = 0
        self._attr_max_value = 100
        self._attr_value = 0
        self._pin = pin
        self._id = pwm_id

    async def async_set_native_value(self, value: float) -> None:
        command = f"SetLED={self._id},{self._pin},{int(value)}"
        send_command(command)

        self._attr_value = value
        self.schedule_update_ha_state()

    def turn_on(self):
        command = f"SetLED={self._id},{self._pin},100"
        send_command(command)

    def turn_off(self):
        command = f"SetLED={self._id},{self._pin},0"
        send_command(command)

    @property
    def native_value(self) -> float:
        return self._attr_value
