from app.container.Container import Container
from app.env.EnvHandler import EnvHandler
from app.http.Server import Server
from http.server import HTTPServer


def apply(container: Container) -> None:
    env_handler: EnvHandler = container.get('app.env.EnvHandler.EnvHandler')

    httpd = HTTPServer(env_handler.list('HTTP_HOST', 'HTTP_PORT'), Server)
    Server.CONTAINER = container

    container.bind('app.container.Container.Container', container)
    container.bind('http-server', httpd)
