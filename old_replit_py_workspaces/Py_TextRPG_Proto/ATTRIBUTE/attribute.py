class Attribute:

    def __init__(self, name: str, value: float | int, investable: bool = True):
        self.name: str = name
        self.baseValue: float = float(value)
        self.investable = investable

    def is_same_attribute(self, name: str) -> bool:
        return self.name == name

    def __eq__(self, other):
        return self.is_same_attribute(other.name)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"{self.name} ({self.baseValue})"
