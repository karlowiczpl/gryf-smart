from homeassistant.components.climate.const import HVACMode , HVACAction 

DOMAIN = "gryf_smart"

CONF_LIGHTS = "lights"
CONF_BUTTON = "buttons"
CONF_NAME = "name"
CONF_ID = "id"
CONF_PIN = "pin"
CONF_SERIAL = "port"
CONF_DOORS = "doors"
CONF_WINDOW = "windows"
CONF_TEMPERATURE = "temperature"
CONF_COVER = "covers"
CONF_TIME = "time"
CONF_LOCK = "lock"
CONF_PWM = "pwm"
CONF_CLIMATE = "climate"
CONF_HARMONOGRAM = "harmonogram"
CONF_T_ID = "t_id"
CONF_O_ID = "o_id"
CONF_T_PIN = "t_pin"
CONF_O_PIN = "o_pin"
CONF_ID_COUNT = "id"
CONF_GATE = "gate"
CONF_P_COVER = "p_covers"
CONF_IP = "ip"
CONF_STATES_UPDATE = "states_update"
CONF_HARMONOGRAM = "harmonogram"
CONF_ON = "on"
CONF_OFF = "off"
CONF_ALL = "all"

COVER_DEVICE_CLASS = "window"
DOOR_DEVICE_CLASS = "door"
WINDOW_DEVICE_CLASS = "window"

STATE_PAUSED = "zatrzymano"

CLIMATE_START_TEMPERATURE = 85
CLIMATE_START_TARGET_TEMPERATURE = 20
CLIMATE_MIN_TEMP = 5
CLIMATE_MAX_TEMP = 35

DEFAULT_HAVAC_MODE = HVACMode.OFF
DEFAULT_HAVAC_ACTION = HVACAction.IDLE

HELPER_BOOLEAN_ON = "_en_on"
HELPER_BOOLEAN_OFF = "_en_off"
HELPER_DATETIME_ON = "_on"
HELPER_DATETIME_OFF = "_off"
