from .service import Service


class TimedService(Service):

    def __init__(self,
                 name: str,
                 price: int,
                 price_per_minute: float,
                 max_minutes: float | None = None):
        super().__init__(name, price, ["timed"])
        self.price_per_minute = price_per_minute
        self.max_minutes = max_minutes

    def calc(self, minutes: int) -> int:
        return int(self.price + self.price_per_minute *
                   min(minutes, self.max_minutes or minutes))

    def __str__(self) -> str:
        return f"{self.name}: {self.price} WD + {self.price_per_minute} WD/min"
