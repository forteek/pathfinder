class Server:
    def __init__(self):
        self._shutdown = False

    def run(self) -> None:
        while not self._shutdown:
            pass
