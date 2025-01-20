import logging
from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelEntityFeature, CodeFormat
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_DISARMED,
    STATE_ALARM_TRIGGERED,
)
from .hardware import _gryf_output

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the custom alarm control panel."""
    async_add_entities([CustomAlarmEntity()])

class CustomAlarmEntity(AlarmControlPanelEntity , _gryf_output):
    """Representation of a custom alarm control panel."""

    _attr_should_poll = False
    # _attr_code_arm_required = True
    # _attr_code_format = CodeFormat.NUMBER
    _state = STATE_ALARM_DISARMED
    _is_active = False
    _code = 1234 
    _changed_by = None

    def __init__(self):
        # self._id = config.get("id")
        # self._pin = config.get("pin")
        # self._name = config.get("name")
        _gryf_output.__init__(self , 3 , 1)

        self._supported_features = (
            AlarmControlPanelEntityFeature.ARM_HOME
        )

    @property
    def name(self):
        return "Custom Alarm"

    @property
    def state(self):
        """Return the state of the device."""
        return self._state
    async def output_state_changed(self , state):
        if state == 1:
            self._state = STATE_ALARM_ARMED_HOME  # Ustawiamy stan na 'rozbrojony'
            self.async_write_ha_state()
        else:
            self._state = STATE_ALARM_DISARMED  # Ustawiamy stan na 'rozbrojony'
            self.async_write_ha_state()

    @property
    def supported_features(self):
        """Return the supported features."""
        return self._supported_features

    @property
    def code_arm_required(self):
        """Indicate if code is required to arm the alarm."""
        return True  # Kod jest wymagany

    @property
    def code_format(self):
        """Format for the code (set to number)."""
        return CodeFormat.NUMBER  # Wymuszenie formatu jako liczba

    @property
    def changed_by(self):
        """Last change triggered by."""
        return self._changed_by

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            "is_active": self._is_active,
            "changed_by": self._changed_by,
        }

    async def async_update(self):
        """Fetch the latest data from the device (e.g., state or changes)."""
        # Tu dodaj logikę do pobrania stanu z urządzenia
        # np. z sieci lub innego źródła
        pass

    async def async_alarm_disarm(self, code=None):
        self.set_out(0)
        

    async def async_alarm_arm_home(self, code=None):
        self.set_out(1)

    async def async_alarm_trigger(self, code=None):
        """Trigger the alarm."""
        _LOGGER.info("Alarm triggered")
        self._state = STATE_ALARM_TRIGGERED  # Ustawiamy stan na 'wyzwolony'
        self._is_active = True
        self._changed_by = "System"  # Ustawiamy, kto zmienił stan
        self.async_write_ha_state()
