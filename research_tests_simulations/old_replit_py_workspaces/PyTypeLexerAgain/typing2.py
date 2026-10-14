from research_tests_simulations.old_replit_py_workspaces.PyTypeLexerAgain.Type import Type, Generic


Element = Generic("Element", Int, Float)
print(Element)

class Container(Type):

	def __init__(self, name: str, *generics: Generic):
		self.constraints = tuple(generics)
		for i in generics:
			i.fullname = name + "." + i.name
			setattr(self, i.name, i)
		super().__init__(name)

	def __getitem__(self, *item: Type) -> "Container":
		items = item[0]
		if type(items) is not tuple:
			items = tuple([items])
		if len(self.constraints) != len(items):
			error = IndexError(
			 f"""Expected {len(self.constraints)} type input{"s" if len(self.constraints) != 1 else ""} but got {len(items)} instead"""
			)
			raise error
		for i in range(len(items)):
			_type = items[i]
			constraint = self.constraints[i]
			if not Generic.conforms(_type, constraint):
				error = TypeError(
				 f"""Expected type {_type} to conform to constraining type {self.name}.{constraint}""")
				raise error
		return (Container(self.name, Generic(*items)).inheritance(*self.__inherits__).literals(
		 *self.__literals__))

	def inheritance(self, *type: "Type") -> "Type":
		
		types = map(lambda i: (None if self.__inherits__.count(i) else i), type)
		self.__inherits__.extend(list(types))
		return self

	def __repr__(self) -> str:
		return (self.name +
		        repr(list(self.constraints)) if len(self.constraints) else "")


print(Type.isOf(AnyNumber, Object))

### The Base Collection Type
Collection = Container("Collection", Generic("Element")).inheritance(Object)
"""String = Container("String", Generic("Element")).literals(str)
String.inheritance(Collection[String])
String.Element.inheritance(String)"""
List = Container("List", Generic("Element")).inheritance().literals(list)

print(Collection.Element)
print(Collection[Int].__inherits__)
print(Collection[Float])
