from app.struct.OrderQueue import OrderQueue
from app.model.Order import Order
from typing import Optional, List
from app.pathfinder.RobotStates import RobotStates
from app.model.Point import Point
from app.pathfinder.DijkstraPathfinder import DijkstraPathfinder
from app.pathfinder.Collector import Collector
from app.struct.Metrics import Metrics
from time import sleep


class Server:
    def __init__(self, order_queue: OrderQueue, pathfinder: DijkstraPathfinder, collector: Collector, metrics: Metrics):
        self._order_queue = order_queue
        self._pathfinder = pathfinder
        self._collector = collector
        self._metrics = metrics

        self._shutdown: bool = False
        self._current_order: Optional[Order] = None
        self._path: List[Point] = []
        self._state: str = RobotStates.AWAITING_ORDER

    def run(self) -> None:
        while not self._shutdown:
            if self._state == RobotStates.AWAITING_ORDER:
                order = self._find_order()
                self._accept_order(order)
                self._update_metrics()
                continue

            elif self._state == RobotStates.CALCULATING_ROUTE:
                path = self._pathfinder.find_path(self._current_order)
                self._set_path(path)
                self._update_metrics()
                continue

            elif self._state == RobotStates.COLLECTING_ORDER:
                if not self._current_order.collected:
                    self._collector.collect(self._current_order, self._path)
                else:
                    self._state = RobotStates.ISSUING

                self._update_metrics()
                continue

            elif self._state == RobotStates.ISSUING:
                # todo zlozyc zamowienie
                self._state = RobotStates.AWAITING_ORDER
                self._update_metrics()
                continue

    def _find_order(self) -> Optional[Order]:
        if self._order_queue.count() > 0:
            return self._order_queue.shift()

        return None

    def _accept_order(self, order: Optional[Order]) -> None:
        if order is None:
            return

        self._current_order = order
        self._state = RobotStates.CALCULATING_ROUTE

    def _set_path(self, path: List[Point]):
        if len(path) == 0:
            return

        self._path = path
        self._state = RobotStates.COLLECTING_ORDER

    def _update_metrics(self):
        self._metrics.state = self._state
