from app.http.controller.Controller import Controller
from app.http.Response import Response


class MapController(Controller):
    def post(self) -> Response:
        return Response({'elo': 'moto', 'ciagnik': 'coto'}, 201)
