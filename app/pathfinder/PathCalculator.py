from app.model.Shelf import Shelf
from typing import List
from app.struct.Map import Map
from app.model.Point import Point


class PathCalculator:
    def __init__(self, map: Map):
        self._map = map
        self._required = None

    def find(self, shelves: List[Shelf]) -> None:
        dock = [p for p in self._map.points if p.home][0]
        self._required = [p for p in self._map.points if p.shelf and p.shelf in shelves]

        self._traverse(dock, [], [])

    def _traverse(self, source_point: Point, path: List[Point], found: List[Point]):
        own_found = found
        if source_point in self._required:
            own_found.append(source_point)

        path.append(source_point)

        if len(own_found) == len(self._required):
            return path

        connections = [r for r in self._map.rails if r.point_from == source_point or r.point_to == source_point]
        unvisited_connections = [r for r in connections if r not in path]
