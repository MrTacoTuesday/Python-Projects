from uuid import UUID

from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attribute_map import AttributeMap
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.attributes import Attributes
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.ATTRIBUTE.modifier_map import ModifierMap
from research_tests_simulations.old_replit_py_workspaces.Py_TextRPG_Proto.RESOURCES.locale import Locale


class Gender:

    MODIFIER_ID: UUID = UUID(hex="454cef29-87b3-4732-9d5a-ef9dbf75f1d4")

    Male: "Gender"
    Female: "Gender"
    Androgynous: "Gender"

    def __init__(self, name: str, modifiers: ModifierMap):
        self.name = name
        self.modifiers = modifiers

    def get_name(self) -> str:
        return Locale.get_name(self.name)

    def apply_modifiers(self, attributes: AttributeMap):
        attributes.apply_modifiers(self.modifiers)

    def remove_modifiers(self, attributes: AttributeMap):
        attributes.remove_modifiers(self.modifiers)


Gender.Male = Gender("gender.male.name", ModifierMap()
    ._put(
        Attributes.Core.STRENGTH, 
        Gender.MODIFIER_ID, 
        "+*", 
        0.4
    )._put(
        Attributes.Core.VITALITY,
        Gender.MODIFIER_ID,
        "+*",
        0.2
    )._put(
        Attributes.Core.INTELLIGENCE,
        Gender.MODIFIER_ID,
        "+*",
        0.1
    )
)

Gender.Female = Gender("gender.female.name", ModifierMap()
    ._put(
        Attributes.Core.DEXTERITY,
        Gender.MODIFIER_ID,
        "+*",
        0.3
    )._put(
        Attributes.Core.WISDOM, 
        Gender.MODIFIER_ID, 
        "+*", 
        0.3
    )._put(
        Attributes.Core.LUCK,
        Gender.MODIFIER_ID,
        "+*",
        0.1
    )
)

Gender.Androgynous = Gender("gender.androgynous.name", ModifierMap()
    ._put(
        Attributes.Core.STRENGTH, 
        Gender.MODIFIER_ID, 
        "+*", 
        0.2
    )._put(
        Attributes.Core.VITALITY,
        Gender.MODIFIER_ID,
        "+*",
        0.1
    )._put(
        Attributes.Core.DEXTERITY,
        Gender.MODIFIER_ID,
        "+*",
        0.15
    )._put(
        Attributes.Core.INTELLIGENCE,
        Gender.MODIFIER_ID,
        "+*",
        0.05
    )._put(
        Attributes.Core.WISDOM, 
        Gender.MODIFIER_ID, 
        "+*", 
        0.15
    )._put(
        Attributes.Core.LUCK,
        Gender.MODIFIER_ID,
        "+*",
        0.05
    )
)