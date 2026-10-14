from typing import TypeVar, Optional, Set, Dict
from uuid import UUID
from .attribute import Attribute
from .attributemodifier import AttributeModifier, Operation
from research_tests_simulations.old_replit_py_workspaces.PyMinecraftJavaAttributePortProto.utils import Consumer


class AttributeInstance:
	Self = TypeVar("AttributeInstance.Self", bound="AttributeInstance")

	def __init__(self: Self, attribute: Attribute, onDirty: Consumer[Self]):
		self.attribute: Attribute = attribute
		self.modifiersByOperation: Dict[Operation, Set[AttributeModifier]] = {}
		self.modifierById: Dict[UUID, AttributeModifier] = {}
		self.permanentModifiers: Set[AttributeModifier] = set()
		self.baseValue: float = attribute.getDefaultValue()
		self.dirty: bool = True
		self.cachedValue: float = None
		self.onDirty: Consumer[AttributeInstance] = onDirty

	def getAttribute(self: Self) -> Attribute:
		return self.attribute

	def getBaseValue(self: Self) -> float:
		return self.baseValue

	def setBaseValue(self: Self, value: float):
		if value != self.baseValue:
			self.baseValue = value
			self.setDirty()

	def getModifiers(self: Self,
	                 operation: Optional[Operation] = ...
	                 ) -> Set[AttributeModifier]:
		if operation is not None and operation is not ...:
			return self.modifiersByOperation.setdefault(operation, set())
		else:
			return set(self.modifierById.values())

	def getModifier(self: Self, uuid: UUID) -> AttributeModifier:
		return self.modifierById.get(uuid)

	def hasModifier(self: Self, modifier: AttributeModifier) -> bool:
		return self.modifierById.get(modifier.getId()) is not None

	def addModifier(self: Self, modifier: AttributeModifier):
		if modifier.getId() in self.modifierById:
			raise ValueError("Modifier is already applied on this attribute!")
		else:
			self.modifierById.setdefault(modifier.getId(), modifier)
			self.getModifiers(modifier.getOperation()).add(modifier)
			self.setDirty()

	def addTransientModifier(self: Self, modifier: AttributeModifier):
		self.addModifier(modifier)

	def addPermanentModifier(self: Self, modifier: AttributeModifier):
		self.addModifier(modifier)
		self.permanentModifiers.add(modifier)

	def setDirty(self: Self):
		self.dirty = True
		self.onDirty(self)

	def removeModifier(self: Self, item: AttributeModifier | UUID):
		if isinstance(item, AttributeModifier):
			self.getModifiers(item.getOperation()).remove(item)
			self.modifierById.pop(item.getId())
			if item in self.permanentModifiers:
				self.permanentModifiers.remove(item)
			self.setDirty()
		else:
			attributemodifier = self.getModifier(item)
			if (attributemodifier is not None):
				self.removeModifier(attributemodifier)

	def removePermanentModifier(self: Self, uuid: UUID) -> bool:
		attributemodifier = self.getModifier(uuid)
		if attributemodifier in self.permanentModifiers:
			self.removeModifier(attributemodifier)
			return True
		else:
			return False

	def removeModifiers(self: Self):
		for modifier in self.getModifiers():
			self.removeModifier(modifier)

	def getValue(self: Self) -> float:
		if self.dirty:
			self.cachedValue = self.calculateValue()
			self.dirty = False
		return self.cachedValue

	def calculateValue(self: Self) -> float:
		d0 = self.getBaseValue()
		for modifier in self.getModifiers(Operation.ADDITION):
			d0 += modifier.getAmount()
		d1 = d0
		for modifier in self.getModifiers(Operation.MULTIPLY_BASE):
			d1 += d0 * modifier.getAmount()
		for modifier in self.getModifiers(Operation.MULTIPLY_TOTAL):
			d1 *= 1.0 + modifier.getAmount()
		return self.attribute.sanitizeValue(d1)

	def replaceFrom(self: Self, other: Self):
		self.baseValue = other.baseValue
		self.modifierById.clear()
		self.modifierById.update(other.modifierById)
		self.permanentModifiers.clear()
		self.permanentModifiers.update(other.permanentModifiers)
		self.modifiersByOperation.clear()
		for (operation, modifiers) in other.modifiersByOperation.items():
			self.getModifiers(operation).update(modifiers)
		self.setDirty()


"""
import com.google.common.collect.ImmutableSet;
import net.minecraft.core.Registry;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;


public CompoundTag save() {
	CompoundTag compoundtag = new CompoundTag();
	compoundtag.putString("Name", Registry.ATTRIBUTE.getKey(this.attribute).toString());
	compoundtag.putDouble("Base", this.baseValue);
	if (!this.permanentModifiers.isEmpty()) {
		ListTag listtag = new ListTag();
		
		for(AttributeModifier attributemodifier : this.permanentModifiers) {
			listtag.add(attributemodifier.save());
		}
		
		compoundtag.put("Modifiers", listtag);
	}
	
	return compoundtag;
}

public void load(CompoundTag p_22114_) {
	this.baseValue = p_22114_.getDouble("Base");
	if (p_22114_.contains("Modifiers", 9)) {
		ListTag listtag = p_22114_.getList("Modifiers", 10);
		
		for(int i = 0; i < listtag.size(); ++i) {
			AttributeModifier attributemodifier = AttributeModifier.load(listtag.getCompound(i));
			if (attributemodifier != null) {
				this.modifierById.put(attributemodifier.getId(), attributemodifier);
				this.getModifiers(attributemodifier.getOperation()).add(attributemodifier);
				this.permanentModifiers.add(attributemodifier);
			}
		}
	}
	
	this.setDirty();
}
"""
