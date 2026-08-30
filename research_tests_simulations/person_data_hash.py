from dataclasses import dataclass, field
from datetime import date, datetime
from functools import reduce
import hashlib
from re import A
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, MethodDescriptorType, MethodType, MethodWrapperType, WrapperDescriptorType
from typing import Any, ClassVar, Optional
from collections.abc import Buffer, Collection, Mapping, MappingView, Sequence


def json(o: Any) -> dict[str, Any] | list[Any] | int | str | bool | float | None:
    if hasattr(o, "__json__"):
        return o.__json__()
    elif isinstance(o, int | str | bool | float | None):
        return o
    elif isinstance(o, Mapping):
        return {
            str(json(k)): json(v) for k,v in o.items()
        }
    elif isinstance(o, Sequence):
        return [json(v) for v in o]
    else:
        try:
            return json(o.__dict__)
        except:
            print(dir(o.__class__))
            raise
        raise TypeError(o)
    

def Hash(o: Any, seed: int = 0) -> bytes:
    hasher = hashlib.md5(seed.to_bytes(64, signed=True))
    if o is None or o is object:
        pass
    elif isinstance(o, Buffer):
        hasher.update(o)
    elif isinstance(o, int):
        hasher.update(o.to_bytes(o.bit_length(), signed=o<0))
    elif isinstance(o, float):
        hasher.update(Hash(o.as_integer_ratio(), seed=seed))
    elif isinstance(o, str):
        hasher.update(o.encode())
    elif isinstance(o, Sequence):
        for i in o:
            hasher.update(Hash(i, seed=seed))
    elif isinstance(o, Mapping):
        for k,v in o.items():
            hasher.update(Hash(k, seed=seed))
            hasher.update(Hash(v, seed=seed))
    elif isinstance(o, type):
        print("Type found::", o)
        hasher.update(Hash(o.__dict__, seed=seed))
    elif isinstance(o, object):
        print("Object found::", o)
        try:
            _dct = o.__dict__
        except:
            _dct = {k: o.__getattribute__(k) for k in o.__slots__} # pyright: ignore[reportAttributeAccessIssue]
        hasher.update(Hash(_dct, seed=seed))
    else:
        print("Unknown hash type::", o)
    return hasher.digest()

@dataclass
class Name:
    first: str
    middle: Optional[str] = None
    last: Optional[str] = None
    maiden: Optional[str] = None
    title: Optional[str] = None
    quantifier: Optional[str] = None
    reversed: bool = False
    
    def __json__(self) -> Any:
        return self.__dict__
    
    def __str__(self) -> str:
        if self.reversed:
            t = (self.last, self.maiden, self.middle, self.first, self.title, self.quantifier)
        else:
            t = (self.title, self.first, self.middle, self.maiden, self.last, self.quantifier)
        return " ".join(x for x in t if x is not None)
    
    

@dataclass
class Address:
    @dataclass
    class Street:
        number: int
        name: str
        def __str__(self) -> str:
            return f"{self.number} {self.name}"
    @dataclass
    class Unit:
        identifier: str
        number: int
        def __str__(self) -> str:
            return f"{self.identifier} {self.number}"
        
        @classmethod
        def Suite(cls, number: int):
            return cls("Ste", number)
        
        @classmethod
        def Unit(cls, number: int):
            return cls("Unit", number)
    @dataclass(kw_only=True)
    class Region:
        county: Optional[str] = None
        city: str
        state: str
        zipcode: str|int
        country: str
        
        def __str__(self) -> str:
            return "%s%s, %s  %s, %s" % (((self.county + " ") if self.county is not None else ""), self.city, self.state, self.zipcode, self.country)
        
        @classmethod
        def US(cls, *, 
            county: Optional[str] = None,
            city: str,
            state: str,
            zipcode: str|int
        ):
            return cls(county=county,city=city,state=state,zipcode=zipcode,country="United States")
        
        @classmethod
        def US_GA(cls, *, 
            county: Optional[str] = None,
            city: str,
            zipcode: str|int
        ):
            return cls(county=county,city=city,state="GA",zipcode=zipcode,country="United States")

    place: Optional[str]
    street: Street
    unit: Optional[Unit]
    region: Region
    
    def __str__(self) -> str:
        place = (self.place + ", ") if self.place is not None else ""
        unit = (str(self.unit) + ", ") if self.unit is not None else ""
        return "%s%s, %s%s" % (place, self.street, unit, self.region)

@dataclass(kw_only=True)
class Person:
    
    name: Name | str
    birthdate: Optional[datetime | date] = None
    addressbook: dict[str,Address] = field(default_factory=dict)
    
    def __json__(self) -> Any:
        return {
            "name": json(self.name),
            "birthdate": json(self.birthdate),
            "addressbook": {
                k:str(v) for k,v in self.addressbook.items()
            }
        }
    
    def __str__(self) -> str:
        return str(self.__json__())
    
    
    
    




person = Person(
    name=Name(first="Weston", middle="Hunter", last="Chaney"),
    birthdate=date(2005, 11, 28)
)
person.addressbook['home'] = Address(None, Address.Street(1703, "Chesil Dr"), None, Address.Region.US_GA(city="Martinez", zipcode=30907))
person.addressbook['work'] = Address("Jersey Mike's Subs", Address.Street(403, "Furys Ferry Rd"), Address.Unit.Suite(115), Address.Region.US_GA(city="Martinez", zipcode=30907))


print(person)
print(Hash(person))