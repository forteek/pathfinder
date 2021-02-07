from app.http.controller.Controller import Controller
from app.http.Response import Response
from app.http.Request import Request
from app.struct.OrderQueue import OrderQueue
from app.container.Container import Container
from app.model.Order import Order
from app.model.OrderItem import OrderItem
from app.http.Client import Client
from json import loads
from app.struct.Map import Map


class OrderController(Controller):
    def __init__(self, request: Request, order_queue: OrderQueue, http_client: Client, map: Map):
        super().__init__(request)

        self._order_queue = order_queue
        self._http_client = http_client
        self._map = map

    def post(self) -> Response:
        items = [OrderItem(guid) for guid in self._request.body['items']]
        order = Order(items)

        query = '&guids='.join(self._request.body['items'])
        response = self._http_client.get('/api/products?guids=' + query)
        response = loads(response.read().decode())

        for item_data in response:
            if item_data['state'] != 'Stored':
                print('invalid state')
                continue

            if item_data['shelfGuid'] is None:
                print('no shelf guid')
                continue

            shelf = [s for s in self._map.shelves if s.guid == item_data['shelfGuid']]
            if len(shelf) == 0:
                print('no shelves')
                continue
            shelf = shelf[0]

            relevant_item = [i for i in items if i.item == item_data['guid']][0]
            relevant_item.shelf = shelf

        unavailable = [i for i in items if i.shelf is None]
        if len(unavailable) > 0:
            del order

            return Response({'error': 'Requested unavailable items.', 'items': unavailable}, 422)

        order.shelves = [item.shelf for item in order.items]
        self._order_queue.append(order)

        return Response(order, 201)
