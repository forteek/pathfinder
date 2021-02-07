from app.model.Point import Point
from app.model.Rail import Rail
from app.model.Shelf import Shelf
from typing import List


class Map:
    def __init__(self):
        self.points: List[Point] = []
        self.rails: List[Rail] = []
        self.shelves: List[Shelf] = []

    def fill(self, points: List[Point], rails: List[Rail], shelves: List[Shelf]) -> None:
        self.points = points
        self.rails = rails
        self.shelves = shelves

    def truncate(self) -> None:
        for point in self.points:
            del point

        for rail in self.rails:
            del rail

        for shelf in self.shelves:
            del shelf
