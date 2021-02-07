from app.model.GuidedModel import GuidedModel
from app.model.Shelf import Shelf
from typing import Optional


class Point(GuidedModel):
    def __init__(self, guid: str, shelf: Optional[Shelf] = None, home: bool = False):
        super().__init__(guid)

        self.shelf: Optional[Shelf] = shelf
        self.home: bool = home
