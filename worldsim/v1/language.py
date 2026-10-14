from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field, replace
from enum import StrEnum, auto
from typing import TypeAlias, overload
from uuid import UUID, uuid4, uuid5

from .ids import (
    ConceptID,
    ContentID,
    FrozenIDSet,
    IPAPronunciation,
    LanguageID,
    PhonemeID,
    SenseID,
    WordForm,
    WordID,
    content_id,
)
from .origins import Origin, OriginKind, Origins
from .registry import Registry
from .semantics import SpeechAct


LANGUAGE_ID_NAMESPACE = UUID("52fdc84f-61d0-5f18-9b93-64b14d8a4719")


class MorphemePosition(StrEnum):
    PREFIX = auto()
    INFIX = auto()
    ROOT = auto()
    SUFFIX = auto()


class TenseRelativity(StrEnum):
    IMMEDIATE = auto()
    DISTANT = auto()


class TenseTime(StrEnum):
    PAST = auto()
    PRESENT = auto()
    FUTURE = auto()


class WordFlag(StrEnum):
    LOAN_WORD = auto()


@dataclass(frozen=True, slots=True)
class WordFeatures:
    position: MorphemePosition = MorphemePosition.ROOT
    tense: TenseTime | None = None
    tense_relativity: TenseRelativity | None = None
    flags: frozenset[WordFlag] = field(default_factory=frozenset)

    def with_flag(self, flag: WordFlag) -> WordFeatures:
        return replace(self, flags=self.flags | {flag})

    def __bytes__(self) -> bytes:
        values = (
            self.position,
            self.tense or "no-tense",
            self.tense_relativity or "no-relativity",
            *sorted(self.flags),
        )
        return content_id("word-features", *values).to_bytes(8, "big")


@dataclass(frozen=True, slots=True)
class PhonemeUnit:
    language_id: LanguageID
    form: WordForm
    pronunciation: IPAPronunciation
    origins: Origins[PhonemeID] = field(default_factory=Origins[PhonemeID])
    id: PhonemeID = field(default_factory=uuid4)

    @property
    def content_id(self) -> ContentID:
        return content_id(
            "phoneme",
            self.language_id,
            self.form,
            self.pronunciation,
            bytes(self.origins),
        )

    def __bytes__(self) -> bytes:
        return self.id.bytes


@dataclass(frozen=True, slots=True, init=False)
class PhonemeSequence(Sequence[PhonemeUnit]):
    units: tuple[PhonemeUnit, ...]

    def __init__(self, units: Iterable[PhonemeUnit] = ()) -> None:
        object.__setattr__(self, "units", tuple(units))

    @overload
    def __getitem__(self, index: int) -> PhonemeUnit: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[PhonemeUnit, ...]: ...

    def __getitem__(
        self, index: int | slice
    ) -> PhonemeUnit | tuple[PhonemeUnit, ...]:
        return self.units[index]

    def __len__(self) -> int:
        return len(self.units)

    def __iter__(self) -> Iterator[PhonemeUnit]:
        return iter(self.units)

    @property
    def content_id(self) -> ContentID:
        return content_id(
            "phoneme-sequence", *(unit.content_id for unit in self.units)
        )

    @property
    def form(self) -> WordForm:
        return "".join(unit.form for unit in self.units)

    @property
    def pronunciation(self) -> IPAPronunciation:
        return "".join(unit.pronunciation for unit in self.units)

    def __bytes__(self) -> bytes:
        return self.content_id.to_bytes(8, "big")

    def __str__(self) -> str:
        return self.form


@dataclass(frozen=True, slots=True)
class LexicalSense:
    language_id: LanguageID
    word_id: WordID
    concept_id: ConceptID
    evidence_confidence: float = 1.0
    origins: Origins[SenseID] = field(default_factory=Origins[SenseID])
    id: SenseID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not 0.0 <= self.evidence_confidence <= 1.0:
            raise ValueError("evidence_confidence must be between 0.0 and 1.0")

    @property
    def content_id(self) -> ContentID:
        return content_id(
            "lexical-sense",
            self.language_id,
            self.word_id,
            self.concept_id,
            self.evidence_confidence.hex(),
            bytes(self.origins),
        )


@dataclass(frozen=True, slots=True)
class Word:
    language_id: LanguageID
    units: PhonemeSequence
    features: WordFeatures = field(default_factory=WordFeatures)
    relates_to: FrozenIDSet[WordID] = field(default_factory=FrozenIDSet[WordID])
    inspired_by: FrozenIDSet[WordID] = field(default_factory=FrozenIDSet[WordID])
    origins: Origins[WordID] = field(default_factory=Origins[WordID])
    id: WordID = field(default_factory=uuid4)

    @property
    def content_id(self) -> ContentID:
        return content_id(
            "word",
            self.language_id,
            self.units.content_id,
            bytes(self.features),
            bytes(self.relates_to),
            bytes(self.inspired_by),
            bytes(self.origins),
        )

    @property
    def form(self) -> WordForm:
        return self.units.form

    @property
    def pronunciation(self) -> IPAPronunciation:
        return self.units.pronunciation

    def __bytes__(self) -> bytes:
        return self.id.bytes

    def __str__(self) -> str:
        return self.form


LanguageItem: TypeAlias = PhonemeUnit | Word | LexicalSense


@dataclass(slots=True)
class Language:
    name: str
    source_key: str | None = None
    id: LanguageID = field(default_factory=uuid4)
    phonemes: Registry[PhonemeUnit] = field(default_factory=Registry[PhonemeUnit])
    words: Registry[Word] = field(default_factory=Registry[Word])
    senses: Registry[LexicalSense] = field(
        default_factory=Registry[LexicalSense]
    )

    @classmethod
    def from_source(cls, name: str, source_key: str) -> Language:
        """Create a canonical imported language with a repeatable UUID."""
        return cls(
            name=name,
            source_key=source_key,
            id=uuid5(LANGUAGE_ID_NAMESPACE, source_key),
        )

    def register[Item: LanguageItem](self, item: Item) -> Item:
        match item:
            case PhonemeUnit():
                self._register_phoneme(item)
            case Word():
                self._register_word(item)
            case LexicalSense():
                self._register_sense(item)
            case _:
                raise TypeError(
                    f"Language cannot register {type(item).__name__}"
                )
        return item

    def _register_phoneme(self, phoneme: PhonemeUnit) -> None:
        if phoneme.language_id != self.id:
            raise ValueError(
                f"Phoneme belongs to {phoneme.language_id!r}, not {self.id!r}"
            )
        self.phonemes.register(phoneme)

    def _register_word(self, word: Word) -> None:
        if word.language_id != self.id:
            raise ValueError(
                f"Word belongs to {word.language_id!r}, not {self.id!r}"
            )
        for phoneme in word.units:
            self.register(phoneme)
        self.words.register(word)

    def _register_sense(self, sense: LexicalSense) -> None:
        if sense.language_id != self.id:
            raise ValueError(
                f"Sense belongs to {sense.language_id!r}, not {self.id!r}"
            )
        if sense.word_id not in self.words:
            raise ValueError(f"Sense refers to an unregistered word: {sense.word_id}")
        self.senses.register(sense)

    def senses_for(self, word_id: WordID) -> Iterator[LexicalSense]:
        return (sense for sense in self.senses if sense.word_id == word_id)

    def borrow_word(
        self,
        source: Word,
        *,
        source_senses: Iterable[LexicalSense] = (),
        phoneme_map: Mapping[PhonemeID, PhonemeID] | None = None,
        tick: int | None = None,
    ) -> Word:
        """Borrow a word, optionally mapping source sounds to target sounds."""
        source_senses = tuple(source_senses)
        for sense in source_senses:
            if sense.language_id != source.language_id or sense.word_id != source.id:
                raise ValueError(
                    f"Sense {sense.id} does not belong to source word {source.id}"
                )

        existing = self._word_from_origin(source.language_id, source.id)
        if existing is not None:
            self._borrow_senses(source_senses, existing, tick)
            return existing

        units = PhonemeSequence(
            self._borrow_phoneme(unit, phoneme_map, tick) for unit in source.units
        )
        borrowed = Word(
            language_id=self.id,
            units=units,
            features=source.features.with_flag(WordFlag.LOAN_WORD),
            inspired_by=FrozenIDSet({source.id}),
            origins=Origins(
                (
                    Origin(
                        kind=OriginKind.BORROWED,
                        language_id=source.language_id,
                        source_id=source.id,
                        tick=tick,
                    ),
                )
            ),
        )
        self.register(borrowed)
        self._borrow_senses(source_senses, borrowed, tick)
        return borrowed

    def _borrow_senses(
        self,
        source_senses: Iterable[LexicalSense],
        borrowed_word: Word,
        tick: int | None,
    ) -> None:
        for source_sense in source_senses:
            if self._sense_from_origin(
                source_sense.language_id, source_sense.id
            ) is not None:
                continue

            self.register(
                LexicalSense(
                    language_id=self.id,
                    word_id=borrowed_word.id,
                    concept_id=source_sense.concept_id,
                    evidence_confidence=source_sense.evidence_confidence,
                    origins=Origins(
                        (
                            Origin(
                                kind=OriginKind.BORROWED,
                                language_id=source_sense.language_id,
                                source_id=source_sense.id,
                                tick=tick,
                            ),
                        )
                    ),
                )
            )

    def _borrow_phoneme(
        self,
        source: PhonemeUnit,
        phoneme_map: Mapping[PhonemeID, PhonemeID] | None,
        tick: int | None,
    ) -> PhonemeUnit:
        if phoneme_map is not None and source.id in phoneme_map:
            target_id = phoneme_map[source.id]
            try:
                return self.phonemes[target_id]
            except KeyError as error:
                raise ValueError(
                    f"Mapped target phoneme is not registered: {target_id}"
                ) from error

        inherited = self._phoneme_from_origin(source.language_id, source.id)
        if inherited is not None:
            return inherited

        for phoneme in self.phonemes:
            if (
                phoneme.form == source.form
                and phoneme.pronunciation == source.pronunciation
            ):
                return phoneme

        borrowed = PhonemeUnit(
            language_id=self.id,
            form=source.form,
            pronunciation=source.pronunciation,
            origins=Origins(
                (
                    Origin(
                        kind=OriginKind.BORROWED,
                        language_id=source.language_id,
                        source_id=source.id,
                        tick=tick,
                    ),
                )
            ),
        )
        return self.register(borrowed)

    def _phoneme_from_origin(
        self, source_language_id: LanguageID, source_id: PhonemeID
    ) -> PhonemeUnit | None:
        for phoneme in self.phonemes:
            if any(
                origin.language_id == source_language_id
                and origin.source_id == source_id
                for origin in phoneme.origins
            ):
                return phoneme
        return None

    def _word_from_origin(
        self, source_language_id: LanguageID, source_id: WordID
    ) -> Word | None:
        for word in self.words:
            if any(
                origin.language_id == source_language_id
                and origin.source_id == source_id
                for origin in word.origins
            ):
                return word
        return None

    def _sense_from_origin(
        self, source_language_id: LanguageID, source_id: SenseID
    ) -> LexicalSense | None:
        for sense in self.senses:
            if any(
                origin.language_id == source_language_id
                and origin.source_id == source_id
                for origin in sense.origins
            ):
                return sense
        return None


@dataclass(frozen=True, slots=True)
class Construction:
    language_id: LanguageID
    speech_act: SpeechAct
    pattern: tuple[str, ...]
