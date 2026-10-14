from uuid import uuid4
from typing import TypeVar, AnyStr as String
from utils import Supplier
from enum import Enum


class AttributeModifier:
	Self = TypeVar("AttributeModifier.Self", bound="AttributeModifier")

	#LOGGER: Logger = LogUtils.getLogger();

	class Operation(Enum):
		Self = TypeVar("Operation.Self", bound="AttributeModifier.Operation")

		ADDITION = 0
		MULTIPLY_BASE = 1
		MULTIPLY_TOTAL = 2

		def toValue(self: Self) -> int:
			return self.value

		@staticmethod
		def fromValue(value: int) -> Self:
			if value >= 0 and value < 3:
				return AttributeModifier.Operation(value)
			else:
				raise ValueError(f"No operation with value {value}")

	def init1(name: String, amount: float, operation: Operation) -> Self:
		return AttributeModifier(uuid4(), lambda: name, amount, operation)

	def init2(uuid: uuid4, name: String, amount: float,
	          operation: Operation) -> Self:
		return AttributeModifier(uuid, lambda: name, amount, operation)

	def __init__(self: Self, uuid: uuid4, nameGetter: Supplier[String],
	             amount: float, operation: Operation):
		self.id = uuid
		self.nameGetter = nameGetter
		self.amount = amount
		self.operation = operation

	def getId(self: Self) -> uuid4:
		return self.id

	def getName(self: Self) -> String:
		return self.nameGetter()

	def getOperation(self: Self) -> Operation:
		return self.operation

	def getAmount(self: Self) -> float:
		return self.amount

	def __eq__(self: Self, other: object) -> bool:
		if self is other:
			return True
		elif other is not None and isinstance(other, self.__class__):
			return self.id is other.id
		else:
			return False

	equals = __eq__

	def hashCode(self: Self) -> int:
		return hash(self.id)

	__hash__ = hashCode

	def __repr__(self: Self) -> String:
		return f"""AttributeModifier{'{'}amount={self.amount}, operation={self.operation}, name='{self.getName()}', id={self.id}{'}'}"""

	toString = __repr__


Operation = AttributeModifier.Operation
"""
import com.mojang.logging.LogUtils;
import javax.annotation.Nullable;
import net.minecraft.nbt.CompoundTag;
import org.slf4j.Logger;

public class AttributeModifier {

public CompoundTag save() {
	CompoundTag compoundtag = new CompoundTag();
	compoundtag.putString("Name", this.getName());
	compoundtag.putDouble("Amount", this.amount);
	compoundtag.putInt("Operation", this.operation.toValue());
	compoundtag.putUUID("UUID", this.id);
	return compoundtag;
}

@Nullable
public static AttributeModifier load(CompoundTag tag) {
	try {
		UUID uuid = tag.getUUID("UUID");
		AttributeModifier.Operation attributemodifier$operation = AttributeModifier.Operation.fromValue(tag.getInt("Operation"));
		return new AttributeModifier(uuid, tag.getString("Name"), tag.getDouble("Amount"), attributemodifier$operation);
	} catch (Exception exception) {
		LOGGER.warn("Unable to create attribute: {}", (Object)exception.getMessage());
		return null;
	}
}
}
"""
