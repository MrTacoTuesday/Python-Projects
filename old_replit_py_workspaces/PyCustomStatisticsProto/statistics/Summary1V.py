from typing import final

from .Summary import Summary


@final
class Summary1V(Summary):

    def __init__(self, data: dict[float, float], title: str = "One Var Summary"):
        super().__init__(data, title)
