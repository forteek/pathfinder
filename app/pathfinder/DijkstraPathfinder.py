from app.model.Point import Point
from app.struct.Map import Map
from app.model.Heap import Heap
from app.model.Order import Order


class DijkstraPathfinder:
    def __init__(self, map: Map):
        self._map = map

    def find_path(self, order: Order):
        points = [p for p in self._map.points if p.shelf and p.shelf in order.shelves]
        path = []

        starting_point = [p for p in self._map.points if p.home][0]
        while len(points) > 0:
            smallest_distance = None
            closest_point = None
            shortest_path = None

            for point in points:
                distance = 0
                point_path = self._run(starting_point, point)
                print(point_path)
                if (point_path is not None) and (smallest_distance is None or distance < smallest_distance):
                    print(point_path)
                    smallest_distance = distance
                    closest_point = point
                    shortest_path = point_path[1:-1]

            starting_point = closest_point
            path.append(shortest_path)
            points = [p for p in points if p.guid != closest_point.guid]

    def _run(self, start: Point, end: Point):
        weighted_graph = {}
        start = start.guid
        end = end.guid

        for node in self._map.points:
            node_distances = {}
            relevant_rails = [r for r in self._map.rails if r.point_from == node or r.point_to == node]

            for rail in relevant_rails:
                other_point = rail.point_from if rail.point_to == node else rail.point_to
                node_distances[other_point.guid] = rail.length

            weighted_graph[node.guid] = node_distances

        distances = {i: float('inf') for i in weighted_graph}
        best_parents = {i: None for i in weighted_graph}

        to_visit = Heap()
        to_visit.add((0, start))
        distances[start] = 0

        visited = set()

        while to_visit:
            src_distance, source = to_visit.pop()
            if src_distance > distances[source]:
                continue
            if source == end:
                break
            visited.add(source)
            for target, distance in weighted_graph[source].items():
                if target in visited:
                    continue
                new_dist = distances[source] + weighted_graph[source][target]
                if distances[target] > new_dist:
                    distances[target] = new_dist
                    best_parents[target] = source
                    to_visit.add((new_dist, target))

        return Heap.backtrack(best_parents, start, end)
