from http.server import BaseHTTPRequestHandler
from json import dumps
from typing import Tuple, Optional
from socketserver import BaseServer
from app.http.Request import Request
from main import container
from app.http.routes import routes
from app.http.controller.Controller import Controller
from app.http.Response import Response


class Server(BaseHTTPRequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: BaseServer):
        for method in self.SUPPORTED_METHODS:
            setattr(self, 'do_' + method, self.do)
        self._container = container

        super().__init__(request, client_address, server)

    def do(self) -> None:
        self._prepare_request()

        controller = self._resolve_controller()
        if controller is None:
            return

        method = getattr(controller, self.command.lower(), None)
        if not callable(method):
            self._response(
                Response({'error': 'Method not allowed'}, 405)
            )
            return

        self._response(method())

    def _prepare_request(self) -> None:
        request = Request(
            self.command,
            self.path,
            self.headers.__dict__,
            self._get_body()
        )

        self._container.bind('app.http.Request.Request', request)

    def _get_body(self) -> Optional[str]:
        if 'Content-Length' not in self.headers:
            return None

        content_length = int(self.headers['Content-Length'])
        return self.rfile.read(content_length).decode()

    def _resolve_controller(self) -> Optional[Controller]:
        try:
            controller_name = routes[self.path]
        except KeyError:
            self._response(
                Response({'error': 'Route not found'}, 404)
            )
            return None

        module = '.'.join(self.__module__.split('.')[:-1])
        class_path = '%s.controller.%s.%s' % (module, controller_name, controller_name)

        return self._container.get(class_path)

    def _response(self, response: Response):
        self.send_response(response.status_code)
        self.end_headers()
        self.wfile.write(dumps(response.body).encode('utf-8'))
