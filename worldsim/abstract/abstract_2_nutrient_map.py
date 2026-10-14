
from dataclasses import dataclass, field
from enum import Enum, auto
from math import inf
from typing import Iterable


class Nutrient:
    ...

class NutrientMap(dict[Nutrient, float]):

    def empiric_units(self, other: NutrientMap) -> float:
        eu = inf
        for nutrient in self:
            eu = min(eu, other.get(nutrient,0) / self[nutrient])
            if eu == 0:
                return 0
        return eu
    def reduce(self) -> NutrientMap:
        total = sum(self.values())
        return NutrientMap({k : v/total for k,v in self.items()})
    def transfer(self, nutrient: Nutrient, other: NutrientMap, weight: float = 1):
        assert 0 <= weight <= 1, "Weight out of acceptable range [0,1]."
        other.setdefault(nutrient, 0)
        quantity = self[nutrient] * weight
        other[nutrient] += quantity
        self[nutrient] -= quantity
    def transfer_all(self, other: NutrientMap):
        for nutrient in self:
            self.transfer(nutrient, other)
    def __mul__(self, other: int|float) -> NutrientMap:
        return NutrientMap((k, v*other) for k,v in self.items())
    def __truediv__(self, other: int|float) -> NutrientMap:
            return NutrientMap((k, v/other) for k,v in self.items())
    def __sub__(self, other: NutrientMap) -> NutrientMap:
        return NutrientMap((k, self[k]-other[k]) for k in self)
    def __add__(self, other: NutrientMap) -> NutrientMap:
        return NutrientMap((k, self[k]+other[k]) for k in self)
    def __iadd__(self, other: NutrientMap):
        for k in other:
            self.setdefault(k,0)
            self[k] += other[k]
        return self
    def __isub__(self, other: NutrientMap):
        for k in other:
            self.setdefault(k,0)
            self[k] -= other[k]
        return self
    def __imul__(self, other: int | float):
        for k in self:
            self[k] *= other
        return self
    def __itruediv__(self, other: int | float):
        for k in self:
            self[k] /= other
        return self
            
@dataclass
class NutrientFormula:
    reactant: NutrientMap
    product: NutrientMap
    rate: float = 1
    @property
    def weighted_reactant(self) -> NutrientMap:
        return self.reactant * self.rate

    @property
    def weighted_product(self) -> NutrientMap:
        return self.product * self.rate

@dataclass
class NutrientProcess:
    formula: NutrientFormula
    available_reactant: NutrientMap = field(default_factory=NutrientMap)
    available_product: NutrientMap = field(default_factory=NutrientMap)
    def step(self):
        units = self.formula.reactant.empiric_units(self.available_reactant)
        units = min(self.formula.rate, units)
        if units == 0:
            return
        self.available_reactant -= self.formula.reactant * units
        self.available_product += self.formula.product * units


class Nutrients(Nutrient, Enum):
    Carbohydrate = auto()
    Protein = auto()
    AminoAcid = auto()
    Fat = auto()

    Water = auto()
    Oxygen = auto()

    Energy = auto()


class DefaultFormulas:
    Glycolysis = NutrientFormula(
        reactant=NutrientMap({ Nutrients.Carbohydrate : 1, Nutrients.Oxygen : 6 }),
        product=NutrientMap({ Nutrients.Water : 6, Nutrients.Energy : 6}) # ignoring unused molecule CO2
    )
    Lipolysis = NutrientFormula(
        reactant=NutrientMap({ Nutrients.Fat : 1, Nutrients.Oxygen : 22 }),
        product=NutrientMap({ Nutrients.Water : 2, Nutrients.Energy : 22})
    )

@dataclass
class WeightedItem[Item]:
    item: Item
    weight: float

class WeightPool[Item](list[WeightedItem[Item]]):
    def reduce(self):
        total = sum(wi.weight for wi in self)
        if total == 1: 
            return
        for wi in self:
            wi.weight /= total

class NutrientProcesses(set[NutrientProcess]):
    def __init__(self, iterable: Iterable[NutrientProcess]) -> None:
        super().__init__(iterable)
        self._nutrient_map: dict[Nutrient, WeightPool[NutrientProcess]] = {}
        self.available_product: NutrientMap = NutrientMap()
        for p in self:
            r = p.formula.weighted_reactant
            for n in r:
                self._nutrient_map.setdefault(n, WeightPool())
                self._nutrient_map[n].append(WeightedItem(p, r[n]))
    def send(self, nutrients: NutrientMap):
        for nutrient in nutrients:
            if nutrient in self._nutrient_map:
                pool = self._nutrient_map[nutrient]
                pool.reduce()
                for wi in pool:
                    nutrients.transfer(nutrient, wi.item.available_product, wi.weight)
    def collect(self):
        for p in self:
            p.available_product.transfer_all(self.available_product)


class Organ:
    failure: float = 0

    processes: NutrientProcesses

    