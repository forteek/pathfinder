import socket
from typing import Any
from app.env.EnvHandler import EnvHandler
from app.struct.Metrics import Metrics
from json import dumps
from time import sleep


class Server:
    def __init__(self, env_handler: EnvHandler, metrics: Metrics):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._recipient = env_handler.list('UDP_RECIPIENT_HOST', 'UDP_RECIPIENT_PORT')
        self._metrics = metrics
        self._shutdown = False

    def _send(self, message: Any) -> int:
        return self._socket.sendto(
            dumps(message.__dict__).encode('utf-8'),
            self._recipient
        )

    def run(self) -> None:
        while not self._shutdown:
            self._send(self._metrics)
            sleep(0.2)

    def shutdown(self) -> None:
        self._shutdown = True
