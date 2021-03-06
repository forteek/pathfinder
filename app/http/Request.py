from typing import Optional


class Request:
    def __init__(self, method: str, path: str, headers: dict, body: Optional[dict]):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
