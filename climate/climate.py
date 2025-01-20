from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, HVACAction, ClimateEntityFeature
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.helpers.restore_state import RestoreEntity

from ..send import send_command
from ..const import (
    CLIMATE_START_TEMPERATURE,
    CLIMATE_START_TARGET_TEMPERATURE,
    CLIMATE_MIN_TEMP,
    CLIMATE_MAX_TEMP,
    DEFAULT_HAVAC_MODE,
    DEFAULT_HAVAC_ACTION
)

class Climate(ClimateEntity, RestoreEntity):
    def __init__(self, name, t_id, t_pin, o_id, o_pin , tilt):
        self._name = name
        self._temperature = CLIMATE_START_TEMPERATURE
        self._target_temperature = CLIMATE_START_TARGET_TEMPERATURE
        self._hvac_mode = DEFAULT_HAVAC_MODE
        self._min_temp = CLIMATE_MIN_TEMP
        self._max_temp = CLIMATE_MAX_TEMP
        self._t_pin = t_pin
        self._t_id = t_id
        self._o_pin = o_pin
        self._o_id = o_id
        self._hvac_action = DEFAULT_HAVAC_ACTION

        if tilt != None:
            self.tilt = tilt
        else:
            self.tilt = 0

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            
            self._target_temperature = last_state.attributes.get(ATTR_TEMPERATURE, CLIMATE_START_TARGET_TEMPERATURE)
            self._hvac_mode = last_state.state if last_state.state in self.hvac_modes else DEFAULT_HAVAC_MODE
            self._hvac_action = last_state.attributes.get("hvac_action", DEFAULT_HAVAC_ACTION)

        self.async_write_ha_state()

    async def set_new_state(self, state):
        self._temperature = float(state)
        self.update()

    async def update_out(self, parsed_states):
        if parsed_states[self._o_pin] == "1":
            self._hvac_action = HVACAction.HEATING
        else:
            self._hvac_action = HVACAction.IDLE
        self.update()
        self.async_write_ha_state()

    @property
    def hvac_action(self):
        return self._hvac_action

    @property
    def name(self):
        return self._name

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        return self._temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def hvac_mode(self):
        return self._hvac_mode

    @property
    def get_id(self):
        return self._t_id

    @property
    def get_pin(self):
        return self._t_pin

    @property
    def get_o_id(self):
        return self._o_id

    @property
    def hvac_modes(self):
        return [HVACMode.HEAT, HVACMode.OFF]

    @property
    def supported_features(self):
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF

    @property
    def min_temp(self):
        return self._min_temp

    @property
    def max_temp(self):
        return self._max_temp

    def turn_on(self):
        self._hvac_action = HVACMode.HEAT

    def turn_off(self):
        self._hvac_action = HVACMode.OFF

    async def async_set_temperature(self, **kwargs):
        if ATTR_TEMPERATURE in kwargs:
            self._target_temperature = kwargs[ATTR_TEMPERATURE]
            self.async_write_ha_state()
        self.update()

    async def async_set_hvac_mode(self, hvac_mode):
        if hvac_mode in self.hvac_modes:
            self._hvac_mode = hvac_mode
            self.async_write_ha_state()
        self.update()

    def update(self):
        if self._hvac_mode == HVACMode.HEAT:
            states = ["0"] * (6 if self._o_pin < 7 else 8)
            if self._tilt == 0:
                states[self._o_pin - 1] = "1" if self._temperature < self._target_temperature else "2"
            else:
                if self._target_temperature > self._temperature + self._tilt:
                    states[self._o_pin - 1] = "2"
                elif self._target_temperature < self._temperature - self._tilt:
                    states[self._o_pin - 1] = "1"
            command = f"AT+SetOut={self._o_id},{','.join(states)}"
            send_command(command)
        elif self._hvac_mode == HVACMode.OFF:
            states = ["0"] * (6 if self._o_pin < 7 else 8)
            states[self._o_pin - 1] = "2"
            command = f"AT+SetOut={self._o_id},{','.join(states)}"
            send_command(command)
        self.schedule_update_ha_state()
