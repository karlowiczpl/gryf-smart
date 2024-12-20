import asyncio
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.const import CONF_HOST, CONF_PORT

from ..send import send_command

ENABLE = False

_LOGGER = logging.getLogger(__name__)

TCP_HOST = "0.0.0.0"
TCP_PORT = 8080

connected_clients = []

def setEnabled(en):
    global ENABLE
    ENABLE = en

def setup(hass: HomeAssistant):
    host = TCP_HOST
    port = TCP_PORT

    hass.loop.create_task(start_tcp_server(hass, host, port))

    return True

async def start_tcp_server(hass: HomeAssistant, host: str, port: int):
    """Startuje serwer TCP i obsługuje połączenia."""
    server = await asyncio.start_server(handle_client, host, port)
    _LOGGER.info(f"Started TCP server {host}:{port}")

    await server.serve_forever()

async def handle_client(reader, writer):
    """Obsługuje połączenie TCP, odbierając i wysyłając dane."""
    if ENABLE:
        connected_clients.append((reader, writer))
        try:
            message = "Connected to rti\n"
            writer.write(message.encode())
            await writer.drain()
            _LOGGER.info(f"Wysłano powitanie: {message}")

            while True:
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode()
                _LOGGER.info(f"Odebrano wiadomość: {message}")
                if message != "Hello" and message != "Hello\n":
                    send_command(f"{message}")

        except Exception as e:
            _LOGGER.error(f"Error while handling client: {e}")
        finally:
            # Usuwamy klienta z listy po zakończeniu połączenia
            connected_clients.remove((reader, writer))
            writer.close()  # Zamknięcie połączenia
            await writer.wait_closed()  # Czekaj na zakończenie zamknięcia połączenia

async def tcp_send(command):
    """Funkcja wysyłająca wiadomość do wszystkich połączonych klientów."""
    if ENABLE:
        await broadcast_message(command)

async def broadcast_message(message: str):
    """Funkcja wysyłająca wiadomość do wszystkich podłączonych klientów."""
    for reader, writer in connected_clients:
        try:
            _LOGGER.info(f"Wysyłam wiadomość do klienta: {message}")
            writer.write(message.encode())
            await writer.drain()  # Upewniamy się, że wiadomość jest wysłana
        except Exception as e:
            _LOGGER.error(f"Nie udało się wysłać wiadomości do klienta: {e}")
