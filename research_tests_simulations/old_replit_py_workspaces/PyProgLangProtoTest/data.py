from research_tests_simulations.old_replit_py_workspaces.PyProgLangProtoTest.tools import ifpresent, concat


class Element:

	def __init__(self, data: "Element" or "Data" = None):
		self.set(data)

	def set(self, value: "Element" or "Data") -> "Element":
		if not isinstance(value, (Element, Data)):
			raise TypeError("'value' must be an instance of Data or Element")
		self.value = value

	def get(self) -> "Element" or "Data":
		if not self.value:
			return self
		elif isinstance(self.value, Element):
			return self.value.get()
		elif isinstance(self.value, Data):
			return self.value.get()
		else:
			return self.value

	def __repr__(self) -> str:
		return f"{self.value}"


class Literal(Element):

	def set(self, value: "Element" or "Data") -> "Element":
		if isinstance(value, (Element, Data)):
			raise TypeError("'value' must not be an instance of Data or Element")
		self.value = value

	def get(self) -> object:
		return self.value


class TypeVar(Element):

	def set(self, value: "BaseType") -> "Element":
		if not isinstance(value, BaseType):
			raise TypeError("'value' must be an instance of BaseType")
		self.value = value

	def get(self) -> "BaseType":
		return self.value

	def __repr__(self) -> str:
		return f"{self.value.name}.self"


class Data:

	def __init__(self, name: str):
		self.name = name
		self.data = {}

	def set(self,
	        key: str,
	        value: "Element" or "Data" or dict = None) -> "Element":
		if key is None and type(value) is dict:
			self.data = value
		else:
			self.data[key] = value
		return self

	def get(self, key: str = None) -> "Element" or "Data" or None:
		if key is None:
			return self
		elif key in self.data:
			return self.data[key]

	def __repr__(self) -> str:
		return f"{ifpresent(self.name, self.data)}"


class BaseType(Data):

	def __init__(self, name: str, type: str):
		self.name = name
		self.type = type  # 'type', 'generic', 'protocol'
		## List[]
		self.conforms = []
		## List[Generic]
		self.parameters = []
		self.data = {"Type": self, "self": TypeVar(self)}

	def __repr__(self) -> str:
		if self.type == "type":
			return f"{self.name}.Type"
		elif self.type == "generic":
			return f"""{self.name}[{concat(*self.conforms, map=lambda i: i.name)}]"""
		elif self.type == "protocol":
			return f"{self.name}.Proto"

###### Experimental ######
class Type(BaseType):
	
	pass  ## Type(name), conforms Protocol or Class ~ generic -> list


class Struct(Type):
	pass  ## Struct(name), conforms Proto or


class Class(Type):
	pass ## Inherits one Class, and multiple Protocols (ProtoClass must be for same class)


class Generic(BaseType): 
	pass ## One Class, 


class Protocol(BaseType):
	pass ## Can inherit a class, can conform to Protocols


class Proto(Protocol):
	pass ## No class inheritance, 


class ProtoClass(Protocol):
	pass ## Inherits one Class, and multiple Protos



a = BaseType("Integer", "type")
a.set("Type", a)
a.set("self", TypeVar(a))
a.set("isSigned", Literal(False))
print(a, a.get("self"), a.get("isSigned"))
b = BaseType("Element", "generic")
