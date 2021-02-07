from typing import Optional, Union
from json import dumps
from app.http.ObjectEncoder import ObjectEncoder


class Response:
    def __init__(self, body: Optional[Union[dict, object]] = None, status_code: int = 200):
        self.body = dumps(obj=body, cls=ObjectEncoder)
        self.status_code = status_code
