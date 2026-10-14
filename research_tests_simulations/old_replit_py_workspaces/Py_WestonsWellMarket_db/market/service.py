from typing import List, Literal

SvcCategory = Literal["shoulders", "hands", "feet", "timed", "other"]


class Service:

    def __init__(self, name: str, price: int, cat: List[SvcCategory]):
        self.name = name
        self.price = price
        self.category = cat

    def calc(self, minutes: int = 0) -> int:
        return self.price

    def __str__(self) -> str:
        return f"{self.name}: {self.price} WD"
