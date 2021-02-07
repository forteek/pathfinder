from app.model.Shelf import Shelf
from typing import Optional


class OrderItem:
    def __init__(self, item: str, shelf: Optional[Shelf] = None, collected: bool = False):
        self.item = item
        self.shelf = shelf
        self.collected = False
