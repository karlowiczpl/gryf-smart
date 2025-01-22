from ..const import CONF_ID, CONF_PIN , OUTPUT_STATES

from ..send import send_command

outputs = []

async def async_output_state_changed(parsed_states):
    for output in outputs:
        await output.feedback(parsed_states)

def added_new_output(instance):
    global outputs

    outputs.append(instance)

class _GryfOutput:
    _id : int
    _pin : int
    _state : int
    
    def __init__(self , conf_device):
        self._id = conf_device.get(CONF_ID)
        self._pin = conf_device.get(CONF_PIN)
        self._state = 0

        self._old_state = 0

        added_new_output(self)

    @property
    def get_state(self):
        return self._state

    def set_out(self , state):

        if self._pin > 6:
            states_list = ["0", "0", "0", "0", "0", "0" , "0" , "0"]
        else:
            states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = state
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        send_command(command)

    async def feedback(self , parsed_states):
        if int(parsed_states[0]) == self._id:
            self._state = int(parsed_states[self._pin])
            await self.async_update()

    async def async_update(self):
        pass
