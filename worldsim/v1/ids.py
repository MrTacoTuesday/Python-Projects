from hashlib import blake2b
from typing import TypeAlias
from uuid import UUID


PersistentID: TypeAlias = UUID
ContentID: TypeAlias = int
LanguageID: TypeAlias = PersistentID
PhonemeID: TypeAlias = PersistentID
WordID: TypeAlias = PersistentID
SenseID: TypeAlias = PersistentID
ConceptID: TypeAlias = PersistentID
RealmID: TypeAlias = PersistentID
ObjectID: TypeAlias = PersistentID
IPAPronunciation: TypeAlias = str
WordForm: TypeAlias = str
IDPart: TypeAlias = str | bytes | int | UUID


def content_id(namespace: str, *parts: IDPart) -> ContentID:
    """Return a deterministic 64-bit fingerprint for a value's contents."""
    digest = blake2b(digest_size=8, person=b"worldsim-id-v1")

    for part in (namespace, *parts):
        if isinstance(part, bytes):
            encoded = b"b" + part
        elif isinstance(part, str):
            encoded = b"s" + part.encode("utf-8")
        elif isinstance(part, int):
            encoded = b"i" + str(part).encode("ascii")
        elif isinstance(part, UUID):
            encoded = b"u" + part.bytes
        else:
            raise TypeError(f"Unsupported ID component: {type(part).__name__}")

        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)

    return int.from_bytes(digest.digest(), "big")


class FrozenIDSet[T: PersistentID](frozenset[T]):
    def __bytes__(self) -> bytes:
        return b"".join(sorted(item_id.bytes for item_id in self))


class IDSet[T: PersistentID](set[T]):
    def __bytes__(self) -> bytes:
        return b"".join(sorted(item_id.bytes for item_id in self))
