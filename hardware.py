from .send import send_command

outputs = []
inputs = []

async def new_output_command(parsed_states):
    for output in outputs:
        await output.private_feedback(parsed_states)

async def new_input_command(parsed_states):
    for input in inputs:
        await input.private_feedback(parsed_states)
    
class _gryf_input:
    def __init__(self , id , pin):
        self._id = id
        self._pin = pin

        new_input_instance(self)

    async def private_feedback(self , parsed_states):
        if int(parsed_states[0]) == self._id:
            await self.output_state_changed(int(parsed_states[self._pin]))

    async def output_state_changed(self , state):
        pass
class _gryf_output:
    def __init__(self , id , pin):
        self._id = id
        self._pin = pin

        new_output_instance(self)

    def set_out(self , state):
        if state == 0:
            self.create_command("2")
        elif state == 1:
            self.create_command("1")
        else:
            self.create_command("3")
            
    def create_command(self , state):
        if self._pin > 6:
            states_list = ["0", "0", "0", "0", "0", "0" , "0" , "0"]
        else:
            states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = state
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        send_command(command)

    async def private_feedback(self , parsed_states):
        if int(parsed_states[0]) == self._id:
            await self.output_state_changed(int(parsed_states[self._pin]))

    async def output_state_changed(self , state):
        pass

def new_output_instance(instance: _gryf_output):
    global outputs

    outputs.append(instance)

def new_input_instance(instance: _gryf_input):
    global inputs

    inputs.append(instance)
