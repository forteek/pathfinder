from app.container.Container import Container
from app.container import bindings
from http.server import HTTPServer
from threading import Thread
from app.pathfinder.Server import Server as PathfinderServer
from app.udp.Server import Server as UDPServer

if __name__ == '__main__':
    print('Initializing app')

    container = Container()
    bindings.apply(container)

    http_server: HTTPServer = container.get('http-server')
    pathfinder_server: PathfinderServer = container.get('app.pathfinder.Server.Server')
    udp_server: UDPServer = container.get('app.udp.Server.Server')

    threads = {
        'http': Thread(target=http_server.serve_forever),
        'pathfinder': Thread(target=pathfinder_server.run),
        'udp': Thread(target=udp_server.run),
    }

    for thread in threads.values():
        thread.start()

    print('Servers are up')
