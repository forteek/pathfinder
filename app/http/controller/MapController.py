from app.http.controller.Controller import Controller
from app.http.Response import Response
from app.http.Request import Request
from app.struct.Map import Map
from app.model.Shelf import Shelf
from app.model.Point import Point
from app.model.Rail import Rail


class MapController(Controller):
    def __init__(self, request: Request, map: Map):
        super().__init__(request)

        self._map = map

    def put(self) -> Response:
        starting_point = self._request.body['startPoint']['guid']

        points = []
        shelves = []
        for point_data in self._request.body['points']:
            shelf = None
            if point_data['shelfGuid'] is not None:
                shelf = Shelf(point_data['shelfGuid'])
                shelves.append(shelf)

            point = Point(
                guid=point_data['guid'],
                shelf=shelf,
                home=point_data['guid'] == starting_point,
            )
            points.append(point)

        rails = []
        for rail_data in self._request.body['rails']:
            rail = Rail(
                point_from=[p for p in points if p.guid == rail_data['fromPointGuid']][0],
                point_to=[p for p in points if p.guid == rail_data['toPointGuid']][0],
                length=rail_data['length'],
                direction=rail_data['direction']['value'],
            )
            rails.append(rail)

        self._map.truncate()
        self._map.fill(points, rails, shelves)

        return Response(self._map, 201)
