from app.http.Request import Request


class Controller:
    def __init__(self, request: Request):
        self._request = request
