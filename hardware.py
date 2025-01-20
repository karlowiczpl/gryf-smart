from .send import send_command

outputs = []

async def new_output_command(parsed_states):
    for output in outputs:
        output.private_feedback(parsed_states)
    
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
        if parsed_states[0] == str(self._id):
            if parsed_states[self._pin] == 1:
                await self.output_state_changed(1)
            elif parsed_states[self._pin] == 2:
                await self.output_state_changed(0)

    async def output_state_changed(self , state):
        pass

def new_output_instance(instance: _gryf_output):
    global outputs

    outputs.append(instance)
