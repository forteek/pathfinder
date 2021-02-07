from http.client import HTTPConnection, HTTPResponse
from app.env.EnvHandler import EnvHandler
from json import dumps
from app.http.ObjectEncoder import ObjectEncoder


class Client:
    def __init__(self, env_handler: EnvHandler):
        host, port = env_handler.list('WAREHOUSE_API_HOST', 'WAREHOUSE_API_PORT')

        self._connection = HTTPConnection(host, port)

    def get(self, route: str) -> HTTPResponse:
        self._connection.request('GET', route)

        return self._connection.getresponse()

    def post(self, route: str, body: dict) -> HTTPResponse:
        body = dumps(obj=body, cls=ObjectEncoder)
        self._connection.request('POST', route, body)

        return self._connection.getresponse()
