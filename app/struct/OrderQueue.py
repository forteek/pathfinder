from typing import List, Optional
from app.model.Order import Order


class OrderQueue:
    def __init__(self):
        self.orders: List[Order] = []

    def append(self, item: Order) -> None:
        self.orders.append(item)

    def count(self) -> int:
        return len(self.orders)

    def shift(self) -> Optional[Order]:
        return self.orders.pop(0)
