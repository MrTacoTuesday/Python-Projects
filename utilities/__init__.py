from abc import abstractmethod
from copy import copy
from types import EllipsisType, GenericAlias, UnionType, get_original_bases
from typing import Any, Callable, Generic, Mapping, Type, TypeAlias, ParamSpec, Protocol, Self, TypeGuard, TypeVar, TypeVarTuple, TypedDict, final, get_args, get_origin, overload

from . import extensions, epsilon, numeric

__all__ = [
    "extensions",
    "epsilon",
    "numeric",
    "SupportsWrite",
    "SupportsFlush",
    "SupportsWriteAndFlush",
    "debug",
]


class SupportsWrite[T](Protocol):

    @abstractmethod
    def write(self, o: T) -> None:
        raise NotImplementedError


class SupportsFlush(Protocol):

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError


class SupportsWriteAndFlush[T](SupportsWrite[T], SupportsFlush, Protocol): ...

class ReadOnlyError(PermissionError): ...
class NotInitializedError(AttributeError): ...
class Field[Type = Any]:
    __slots__ = (
        'name', 'type', '_default', '_factory', 'requires_init', 'readonly'
    )
    def __new__(cls, name: str, type: type[Type], *, default: Type|EllipsisType = ..., factory: Callable[[], Type]|EllipsisType = ..., readonly: bool = False) -> Self:
        self = super().__new__(cls)
        self.name = name
        self.type = type
        if default is ... and factory is ...:
            self.requires_init = True
        elif default is not ... and factory is not ...:
            raise ValueError('Cannot provide both default and factory')
        else:
            self.requires_init = False
        self.readonly = readonly
        # self.annotations = ... # Final if Final[Type]; ClassVar if ClassVar[Type]; etc...
        self._default = default
        self._factory = factory
        return self

    def acquire_default(self) -> Type | None:
        if self._default is not ...:
            return copy(self._default)
        elif self._factory is not ...:
            return self._factory()

    @property
    def private_name(self) -> str:
        return '_field_'+self.name

    @overload
    def __get__[T](self, instance: None, owner: type[T], /) -> Self: ...
    @overload
    def __get__[T](self, instance: T, owner: type[T] | None = None, /) -> Type: ...
    def __get__[T](self, instance: T|None, owner: type[T] | None = None, /) -> Type | Self: 
        if instance is None:
            return self
        if getattr(owner, self.name, None) != self:
            raise ValueError(f'Expected field `{self.name}` to exist in instance owner {object.__repr__(owner)}') from None
        try: 
            value = object.__getattribute__(instance, self.private_name)
        except AttributeError:
            if self.requires_init:
                raise NotInitializedError() from None
            object.__setattr__(instance, self.private_name, value := self.acquire_default())
        if not is_instance(value, self.type):
            raise TypeError(f'{value} of type {type(value)} was found at {self.type} attribute `{self.name}` of {object.__repr__(instance)}') from None
        return value # type: ignore

    def __set__(self, instance: Any, value: Type, /) -> None: 
        if self.readonly:
            try:
                if self.requires_init:
                    object.__getattribute__(instance, self.private_name)
            except:
                pass
            else:
                raise ReadOnlyError(f'Attribute `{self.name}` of {object.__repr__(instance)} is marked read-only') from None
        if not is_instance(value, self.type):
            raise TypeError(f'{value} of type {type(value)} cannot be assigned to {self.type} attribute `{self.name}` of {object.__repr__(instance)}') from None
        object.__setattr__(instance, self.private_name, value)
    def __delete__(self, instance: Any, /) -> None: 
        try:
            object.__delattr__(instance, self.private_name)
        except:
            pass


def get_original_class[T](obj: T) -> type[T]:
    """
    Returns the object's original class, ex:
        ```python
        >>> a = list[int]([3,5,8])
        >>> a.__class__
        list
        >>> get_original_class(a)
        list[int]
        ```
    """
    return getattr(obj, '__orig_class__', None) or obj.__class__

ClassInfo: TypeAlias = "type | UnionType | tuple[ClassInfo, ...]"
def is_instance(obj: object, class_info: ClassInfo) -> TypeGuard[ClassInfo]:
    return is_subclass(get_original_class(obj), class_info)

def iter_class_info(t: ClassInfo):
    if isinstance(t, tuple):
        for i in t:
            yield from iter_class_info(i)
    elif isinstance(t, UnionType):
        yield from iter_class_info(t.__args__)
    else:
        yield t

def is_subclass(subclass: type, class_info: ClassInfo) -> TypeGuard[ClassInfo]:
    if isinstance(class_info, UnionType):
        class_info = class_info.__args__
    elif not isinstance(class_info, tuple):
        class_info = (class_info,)
    sub_origin = get_origin(subclass) or subclass
    for superclass in iter_class_info(class_info):
        if issubclass(sub_origin, get_origin(superclass) or superclass) and _typecheck_args(subclass, superclass):
            return True
    return False

def _typecheck_args[T](subclass: type[Any], superclass: type[T]) -> TypeGuard[type[T]]: # pyright: ignore[reportInvalidTypeForm]
    sub_args = get_reduced_args_map(subclass)
    sup_args = get_reduced_args_map(superclass)
    if set(sup_args)-set(sub_args)==set():
        for key in sup_args:
            sup_arg = sup_args[key]
            if not (sup_arg is Any or is_subclass(sub_args[key], sup_arg)):
                return False
        return True
    return False

TypeParam: TypeAlias = TypeVar | ParamSpec | TypeVarTuple
def get_args_map(tp: type) -> dict[TypeParam, type[Any]]:
    if tp is object:
        return {}
    map = {}
    origin = get_origin(tp) or tp
    if origin is Generic:
        return {arg: Any for arg in get_args(tp)} # type: ignore
    for base in get_original_bases(origin):
        map.update(get_args_map(base))
    map.update(zip(origin.__type_params__, get_args(tp), strict=False))
    #print(origin.__type_params__, get_args(tp))
    return map

def get_reduced_args_map(tp: type) -> dict[TypeParam, type[Any]]:
    map = get_args_map(tp)
    for k in tuple(map):
        key = k
        while isinstance(value := map.get(key), TypeParam) and value in map:
            map[k] = map[key] = map[value]
            key = value
    return map

def debug(
    *values: object,
    indent_level: int = 0,
    indent_with: str | None = '\t',
    sep: str | None = ' ',
    end: str | None = '\n',
    file: SupportsWrite[str] | SupportsWriteAndFlush[str] | None = None,
    flush: bool = False,
    printif: bool = True,
) -> None:
    if not printif:
        return
    if sep is None:
        sep = ""
    if indent_with is None:
        indent_with = ""
    return print(indent_level.__index__() * indent_with, sep.join(map(str, values)), sep='', end=end, file=file, flush=flush)  # type: ignore

