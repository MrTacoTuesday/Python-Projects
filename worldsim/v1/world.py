from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TypeAlias
from uuid import uuid4

from .ids import IDSet, LanguageID, PhonemeID, RealmID, WordID
from .language import Language, Word
from .registry import Registry
from .semantics import Concept
from .tiles import TileMap


@dataclass(slots=True)
class Realm:
    name: str
    id: RealmID = field(default_factory=uuid4)
    languages: IDSet[LanguageID] = field(default_factory=IDSet[LanguageID])
    # units
    # cultures
    # claimed tile regions


AtlasItem: TypeAlias = Language | Realm | Concept


@dataclass(slots=True)
class Atlas:
    languages: Registry[Language] = field(default_factory=Registry[Language])
    realms: Registry[Realm] = field(default_factory=Registry[Realm])
    concepts: Registry[Concept] = field(default_factory=Registry[Concept])

    def register[Item: AtlasItem](self, item: Item) -> Item:
        match item:
            case Language():
                self.languages.register(item)
            case Realm():
                self.realms.register(item)
            case Concept():
                self.concepts.register(item)
            case _:
                raise TypeError(f"Atlas cannot register {type(item).__name__}")
        return item

    def borrow_word(
        self,
        target_language_id: LanguageID,
        source_language_id: LanguageID,
        source_word_id: WordID,
        *,
        phoneme_map: Mapping[PhonemeID, PhonemeID] | None = None,
        tick: int | None = None,
    ) -> Word:
        target = self.languages[target_language_id]
        source = self.languages[source_language_id]
        source_word = source.words[source_word_id]
        return target.borrow_word(
            source_word,
            source_senses=source.senses_for(source_word.id),
            phoneme_map=phoneme_map,
            tick=tick,
        )


@dataclass(slots=True)
class World:
    atlas: Atlas = field(default_factory=Atlas)
    tile_map: TileMap = field(default_factory=TileMap)
    tick: int = 0

    def advance(self, hours: int = 1) -> None:
        if hours < 0:
            raise ValueError("Cannot advance the world by a negative duration")
        self.tick += hours
