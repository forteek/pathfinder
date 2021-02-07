from app.model.Point import Point


class Rail:
    def __init__(
        self,
        point_from: Point,
        point_to: Point,
        length: int,
        direction: int
    ):
        self.point_from = point_from
        self.point_to = point_to
        self.length = length
        self.direction = direction
