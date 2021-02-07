from typing import List
from app.model.OrderItem import OrderItem
from app.model.Shelf import Shelf


class Order:
    def __init__(self, items: List[OrderItem]):
        self.items = items

        self.shelves: List[Shelf] = []
        self.collected: bool = False
