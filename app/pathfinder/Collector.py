from app.model.Rail import Rail
from app.model.Shelf import Shelf
from typing import List, Optional
from app.struct.Map import Map
from app.model.Point import Point
from app.model.Order import Order
from app.struct.Metrics import Metrics
from app.pathfinder.CollectorStates import CollectorStates
from datetime import datetime
from time import sleep
from math import pi


class Collector:
    WHEEL_DIAMETER = 20

    def __init__(self, map: Map, metrics: Metrics):
        self._map = map
        self._metrics = metrics

        self._state: str = CollectorStates.AWAITING_PATH
        self._path: List[Point] = []
        self._order: Optional[Order] = None
        self._collected: List[Shelf] = []

        self._current_point: Optional[Point] = None
        self._next_point: Optional[Point] = None
        self._rail: Optional[Rail] = None

        self._direction = 90
        self._travelled_distance: float = 0
        self._travelling_since: Optional[datetime] = None

    def collect(self, order: Order, path: List[Point]):
        if self._state == CollectorStates.AWAITING_PATH:
            self._path = path
            self._order = order

            self._initialize_point_travel()
            self._state = CollectorStates.AT_POINT

        elif self._state == CollectorStates.GOING:
            self._travel()

        elif self._state == CollectorStates.AT_POINT:
            if self._current_point.shelf in self._order.shelves and self._current_point.shelf not in self._collected:
                self._state = CollectorStates.COLLECTING
            else:
                if self._rail.direction != self._direction:
                    self._state = CollectorStates.ROTATING
                    self._correct_direction()
                else:
                    self._initialize_point_travel()
                    self._state = CollectorStates.GOING

        elif self._state == CollectorStates.COLLECTING:
            self._collect(self._next_point.shelf)

        self._update_metrics()

    def _initialize_point_travel(self) -> None:
        if len(self._path) >= 0:
            self._get_points()
            self._travelled_distance = 0
            self._travelling_since = datetime.now()
        else:
            self._finish()

    def _get_points(self) -> None:
        if self._current_point is None:
            self._current_point = self._path.pop(0)
        else:
            self._current_point = self._next_point

        if len(self._path) > 0:
            self._next_point = self._path.pop(0)
        else:
            self._next_point = None

        if self._current_point and self._next_point:
            relevant_points = [self._current_point, self._next_point]
            filtered_rails = [r for r in self._map.rails if r.point_from in relevant_points and r.point_to in relevant_points]

            if len(filtered_rails) > 0:
                self._rail = filtered_rails[0]
            else:
                self._rail = None
        else:
            self._rail = None

    def _travel(self) -> None:
        previously_travelled = self._travelled_distance
        delta_time = datetime.now().timestamp() - self._travelling_since.timestamp()
        now_travelled = Collector.WHEEL_DIAMETER * pi * 1 * (delta_time ** 2)

        self._travelled_distance = previously_travelled + now_travelled

        if self._travelled_distance >= self._rail.length:
            self._state = CollectorStates.AT_POINT

    def _collect(self, shelf: Shelf) -> None:
        # simulates having to actually pick up the item from shelf
        sleep(3)
        self._collected.append(shelf)
        self._state = CollectorStates.AT_POINT

    def _correct_direction(self) -> None:
        if self._rail.direction > self._direction:
            self._direction += 5
        elif self._rail.direction < self._direction:
            self._direction -= 5

    def _finish(self):
        self._order.collected = True
        self._order = None
        self._path = []
        self._collected = []

        self._current_point = None
        self._next_point = None
        self._rail = None

        self._travelled_distance = 0
        self._travelling_since = None

        self._state = CollectorStates.AWAITING_PATH

    def _update_metrics(self):
        self._metrics.direction = self._direction
        self._metrics.path = ', '.join(p.guid for p in self._path)
        self._metrics.collected = ', '.join(s.guid for s in self._collected)
        self._metrics.collector_state = self._state
        self._metrics.route_length = self._rail.length
        self._metrics.route_traveled = self._travelled_distance
