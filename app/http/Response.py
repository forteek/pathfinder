from typing import Optional


class Response:
    def __init__(self, body: Optional[dict] = None, status_code: int = 200):
        self.body = body
        self.status_code = status_code
