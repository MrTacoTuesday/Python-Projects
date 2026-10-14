class Type:

	LITERALS = {}

	def __init__(self, name: str):
		self.name = name
		self.__inherits__ = [self]
		self.__literals__ = []

	@property
	def Type(self) -> "Type":
		return self

	def inheritance(self, *type: "Type") -> "Type":
		types = map(lambda i: (None if self.__inherits__.count(i) else i), type)
		self.__inherits__.extend(list(types))
		return self

	def literals(self, *type: type) -> "Type":
		types = map(lambda i: (None if self.__literals__.count(i) else i), type)
		for t in types:
			Type.LITERALS.setdefault(t, []).append(self)
			self.__literals__.append(t)
		return self

	def isliteral(self, literal: type) -> bool:
		for typ in self.__inherits__:
			print(typ, typ.__literals__)
			if self.__literals__.count(type(literal)):
				return True
			if typ == self: continue
			if typ.isliteral(literal):
				return True
		return False

	def inherits(self, type: "Type") -> bool:
		if type.name == "Object": return True
		for typ in self.__inherits__:
			if typ.name == type.name:
				return True
			if typ == self: continue
			if typ.inherits(type):
				return True
		return False

	def isOf(instance: "Type" or type, type: "Type") -> bool:
		if isinstance(instance, Type):
			return instance.inherits(type)
		else:
			return type.isliteral(instance)

	def __and__(self, other: "Type") -> "Generic":
		return Generic("_TYPE")

	def __repr__(self) -> str:
		return self.name


from functools import reduce


class Generic(Type):

	def __init__(self, name: str, *constraints: "Type"):
		super().__init__(name)
		self.inheritance(*constraints, Object)

	def literals(self, *type: type) -> "Generic":
		return self

	def conforms(type: "Type", generic: "Generic") -> bool:
		return reduce(lambda a, b: a and type.inherits(b), generic.__inherits__,
		              True)

	def __repr__(self) -> str:
		_ftr = list(
		 filter(lambda a: a is not Object and a is not self, self.__inherits__))
		return (repr(_ftr).replace("[", "some ").replace("]", "").replace(",", " &")
		        if len(_ftr) else "some Object")


### Object: Everything inherits this
Object = Type("Object")

### Numeric: The Base Class of all number Types
# Note: Cannot compare literals
# Complex is Numeric
# Type.isOf(Complex, Numeric) == True
Numeric = Type("Numeric").inheritance(Object)

Int = Type("Int").inheritance(Numeric).literals(int)
Float = Type("Float").inheritance(Numeric).literals(float)
Complex = Type("Complex").inheritance(Numeric).literals(complex)

### AnyNumber: Used to check values of any number type
# Type.isOf(32, AnyNumber) == True
# Type.isOf(AnyNumber, Complex) == True
AnyNumber = Type("AnyNumber").inheritance(Int, Float, Complex)

### NoneType: Represents 'None'
# Type.isOf(None, NoneType) == True
NoneType = Type("None").inheritance(Object).literals(type(None))

### Boolean: Represents boolean values
Boolean = Type("Boolean").inheritance(Object).literals(bool)

print(Type.isOf(True, Boolean))
