import asyncio

from .send import send_command

module_count = None
enable = True

async def setup_update_states(module , interval):
    global module_count

    module_count = module
    await asyncio.sleep(3)

    for i in range(1, int(module_count) + 1):
            command = f"AT+StanOUT={i}"
            send_command(command)
            await asyncio.sleep(0.1)

            command = f"AT+StanIN={i}"
            send_command(command)

            await asyncio.sleep(0.1)

    if interval:
        while True:
            for i in range(1, int(module_count) + 1):
                command = f"AT+StanOUT={i}"
                send_command(command)
                await asyncio.sleep(0.1)

                command = f"AT+StanIN={i}"
                send_command(command)

                await asyncio.sleep(3)


async def update_states():
    for i in range(1, int(module_count) + 1):
            command = f"AT+StanOUT={i}"
            send_command(command)
            await asyncio.sleep(0.1)

            command = f"AT+StanIN={i}"
            send_command(command)

            await asyncio.sleep(0.1)
