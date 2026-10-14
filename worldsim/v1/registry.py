from collections.abc import (
    Collection,
    Iterable,
    ItemsView,
    Iterator,
    KeysView,
    ValuesView,
)
from typing import Protocol
from uuid import UUID

from .ids import PersistentID


class Identified(Protocol):
    @property
    def id(self) -> PersistentID: ...


class Registry[T: Identified](Collection[T]):
    """An ID-keyed collection that iterates over its registered values."""

    __slots__ = ("_items",)

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items: dict[PersistentID, T] = {}
        for item in items:
            self.register(item)

    def register(self, item: T) -> T:
        existing = self._items.get(item.id)
        if existing is not None and existing is not item:
            raise ValueError(f"ID already registered: {item.id}")
        self._items[item.id] = item
        return item

    def replace(self, item: T) -> T | None:
        previous = self._items.get(item.id)
        self._items[item.id] = item
        return previous

    def get(self, item_id: PersistentID) -> T | None:
        return self._items.get(item_id)

    def discard(self, item_or_id: T | PersistentID) -> None:
        item_id = item_or_id if isinstance(item_or_id, UUID) else item_or_id.id
        self._items.pop(item_id, None)

    def remove(self, item_or_id: T | PersistentID) -> T:
        item_id = item_or_id if isinstance(item_or_id, UUID) else item_or_id.id
        return self._items.pop(item_id)

    def __getitem__(self, item_id: PersistentID) -> T:
        return self._items[item_id]

    def __contains__(self, value: object) -> bool:
        if isinstance(value, UUID):
            return value in self._items
        item_id = getattr(value, "id", None)
        return isinstance(item_id, UUID) and item_id in self._items

    def __iter__(self) -> Iterator[T]:
        return iter(self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    def ids(self) -> KeysView[PersistentID]:
        return self._items.keys()

    def values(self) -> ValuesView[T]:
        return self._items.values()

    def items(self) -> ItemsView[PersistentID, T]:
        return self._items.items()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self._items.values())!r})"
