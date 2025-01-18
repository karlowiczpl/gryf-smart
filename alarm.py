import logging
from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelEntityFeature
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_DISARMED,
    STATE_ALARM_TRIGGERED,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the custom alarm control panel."""
    async_add_entities([CustomAlarmEntity()])

class CustomAlarmEntity(AlarmControlPanelEntity):
    """Representation of a custom alarm control panel."""

    _attr_should_poll = False
    _attr_code_arm_required = False

    def __init__(self):
        """Initialize the alarm panel."""
        self._state = STATE_ALARM_DISARMED
        self._is_active = False
        self._code = "1234"  # Default PIN code, change it as needed
        self._supported_features = (
            AlarmControlPanelEntityFeature.ARM_HOME
            | AlarmControlPanelEntityFeature.ARM_AWAY
            | AlarmControlPanelEntityFeature.ARM_NIGHT
        )

    @property
    def name(self):
        """Return the name of the alarm."""
        return "Custom Alarm"

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def supported_features(self):
        """Return the supported features."""
        return self._supported_features

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            "is_active": self._is_active,
        }

    async def async_alarm_disarm(self, code=None):
        """Send disarm command."""
        if code == self._code:
            _LOGGER.info("Disarming alarm with correct code")
            self._state = STATE_ALARM_DISARMED
            self._is_active = False
            self.async_write_ha_state()
        else:
            _LOGGER.warning("Failed disarming attempt with incorrect code")

    async def async_alarm_arm_home(self, code=None):
        """Send arm home command."""
        if code == self._code:
            _LOGGER.info("Arming alarm in home mode with correct code")
            self._state = STATE_ALARM_ARMED_HOME
            self._is_active = True
            self.async_write_ha_state()
        else:
            _LOGGER.warning("Failed arming attempt with incorrect code")

    async def async_alarm_arm_away(self, code=None):
        """Send arm away command."""
        if code == self._code:
            _LOGGER.info("Arming alarm in away mode with correct code")
            self._state = STATE_ALARM_ARMED_AWAY
            self._is_active = True
            self.async_write_ha_state()
        else:
            _LOGGER.warning("Failed arming attempt with incorrect code")

    async def async_alarm_trigger(self, code=None):
        """Trigger the alarm."""
        _LOGGER.info("Alarm triggered")
        self._state = STATE_ALARM_TRIGGERED
        self._is_active = True
        self.async_write_ha_state()
