from collections.abc import Sequence
from dataclasses import dataclass, replace
from enum import StrEnum, auto
from typing import overload
from uuid import UUID

from .ids import ContentID, LanguageID, content_id


class OriginKind(StrEnum):
    BORROWED = auto()
    INHERITED = auto()
    CALQUED = auto()
    BLENDED = auto()
    COINED = auto()


@dataclass(frozen=True, slots=True)
class Origin[IDType: UUID]:
    kind: OriginKind
    language_id: LanguageID
    source_id: IDType
    tick: int | None = None

    @property
    def content_id(self) -> ContentID:
        return content_id(
            "origin",
            self.kind,
            self.language_id,
            self.source_id,
            self.tick if self.tick is not None else "no-tick",
        )

    def __bytes__(self) -> bytes:
        return self.content_id.to_bytes(8, "big")


@dataclass(frozen=True, slots=True)
class Origins[IDType: UUID](Sequence[Origin[IDType]]):
    items: tuple[Origin[IDType], ...] = ()

    def with_item(self, item: Origin[IDType]) -> Origins[IDType]:
        return replace(self, items=self.items + (item,))

    def __len__(self) -> int:
        return len(self.items)

    @overload
    def __getitem__(self, index: int) -> Origin[IDType]: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[Origin[IDType], ...]: ...

    def __getitem__(
        self, index: int | slice
    ) -> Origin[IDType] | tuple[Origin[IDType], ...]:
        return self.items[index]

    def __bytes__(self) -> bytes:
        return b"".join(bytes(origin) for origin in self.items)
