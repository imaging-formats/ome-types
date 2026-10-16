from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

# from ome_types._mixins._base_type import AUTO_SEQUENCE
# avoiding import to avoid build-time dependency on the ome-types package
AUTO_SEQUENCE = "__auto_sequence__"

MIXIN_MODULE = "ome_types._mixins"
# class_name, import_string, whether-to-prepend or append to the existing Bases
MIXINS: list[tuple[str, str, bool]] = [
    (".*", f"{MIXIN_MODULE}._base_type.OMEType", False),  # base type on every class
    ("OME", f"{MIXIN_MODULE}._ome.OMEMixin", True),
    ("Instrument", f"{MIXIN_MODULE}._instrument.InstrumentMixin", False),
    ("Reference", f"{MIXIN_MODULE}._reference.ReferenceMixin", True),
    ("Map", f"{MIXIN_MODULE}._map_mixin.MapMixin", False),
    ("Union", f"{MIXIN_MODULE}._collections.ShapeUnionMixin", True),
    (
        "StructuredAnnotations",
        f"{MIXIN_MODULE}._collections.StructuredAnnotationsMixin",
        True,
    ),
    ("(Shape|ManufacturerSpec|Annotation)", f"{MIXIN_MODULE}._kinded.KindMixin", True),
]


@dataclass
class Ovr:
    """Override settings for a given name in the XSD."""

    # Name of an attribute or element in the XSD
    # (this is autopopulated by the key in the OVERRIDES dict, so as to ensure
    # that we don't have more than one override for a given name in the XSD.)
    name: str = ""
    # additional lines to add to generated classes
    # Note: imports for these methods must be added to the IMPORT_PATTERNS elsewhere.
    add_lines: Sequence[str] = ()
    # when name is found as a type in the XSD, the type will be overridden with this
    # e.g. "Color" -> ("ome_types.model._color", "Color")
    type_override: tuple[str, str] | None = None
    # When name is used as a type hint, it should never be Optional[]
    never_optional: bool = False
    # default value for a field with this type
    default: str | None = None
    # default factory for a field with this type
    default_factory: str = ""


OVERRIDES: dict[str, Ovr] = {
    "ID": Ovr(default=repr(AUTO_SEQUENCE)),
    "Union": Ovr(never_optional=True, default_factory="lambda: ROI.Union()"),
    "StructuredAnnotations": Ovr(
        never_optional=True, default_factory="StructuredAnnotations"
    ),
    "FillColor": Ovr(type_override=("ome_types.model._color", "Color")),
    "StrokeColor": Ovr(
        type_override=("ome_types.model._color", "Color"),
    ),
    "Color": Ovr(
        type_override=("ome_types.model._color", "Color"),
        default_factory="Color",
    ),
    "BinData": Ovr(
        add_lines=[
            "_vbindata = model_validator(mode='before')(bin_data_root_validator)"
        ],
    ),
    "Value": Ovr(
        add_lines=["_vany = field_validator('any_elements')(any_elements_validator)"],
    ),
    "Pixels": Ovr(
        add_lines=["_vpix = model_validator(mode='before')(pixels_root_validator)"],
    ),
    "XMLAnnotation": Ovr(
        add_lines=[
            "_vval = field_validator('value', mode='before')(xml_value_validator)"
        ],
    ),
    "PixelType": Ovr(add_lines=["numpy_dtype = property(pixel_type_to_numpy_dtype)"]),
    "OME": Ovr(
        add_lines=[
            "_v_structured_annotations = field_validator('structured_annotations', mode='before')(validate_structured_annotations)"
        ],
    ),
    "ROI": Ovr(
        add_lines=[
            "_v_shape_union = field_validator('union', mode='before')(validate_shape_union)"
        ],
    ),
    "Map": Ovr(
        add_lines=[
            "_v_map = model_validator(mode='before')(validate_map_annotation)",
            "dict: ClassVar = MapMixin._pydict",
            "__iter__: ClassVar = MapMixin.__iter__  # type: ignore[assignment]",
        ],
    ),
}

# autopopulate the name attribute
for k, v in OVERRIDES.items():
    v.name = k
    if v.never_optional and not (v.default or v.default_factory):
        raise ValueError(
            f"never_optional overrides must have a default or default_factory: {k}"
        )

# Quick lookup mapping XSD name to overridden type name
# e.g. {'FillColor': 'Color', 'StrokeColor': 'Color', 'Color': 'Color'}
OVERRIDE_ELEM_TO_CLASS: dict[str, str] = {}

# set of element names that should never be optional
# (but always have default_factories)
NEVER_OPTIONAL = {x for x in OVERRIDES if OVERRIDES[x].never_optional}

# import patterns
# key is a module path.  Value is a map of type names to a list of patterns to match
# in the generated code.  If a pattern is found, the type will be imported from the
# module specified, in the file where the pattern was found.
IMPORT_PATTERNS: dict[str, dict[str, list[str]]] = {
    "typing": {"ClassVar": [": ClassVar"]},
    "ome_types._mixins._util": {"new_uuid": ["default_factory=new_uuid"]},
    "datetime": {"datetime": ["datetime"]},
    "pydantic": {
        "validator": ["validator("],
        "model_validator": ["model_validator("],
        "field_validator": ["field_validator("],
    },
    "ome_types._mixins._validators": {
        "any_elements_validator": ["any_elements_validator"],
        "bin_data_root_validator": ["bin_data_root_validator"],
        "pixel_type_to_numpy_dtype": ["pixel_type_to_numpy_dtype"],
        "pixels_root_validator": ["pixels_root_validator"],
        "validate_map_annotation": ["validate_map_annotation"],
        "validate_shape_union": ["validate_shape_union"],
        "validate_structured_annotations": ["validate_structured_annotations"],
        "xml_value_validator": ["xml_value_validator"],
    },
}


for override in OVERRIDES.values():
    if override.type_override:
        module, type_name = override.type_override
        mod_entry = IMPORT_PATTERNS.setdefault(module, {})
        mod_entry[type_name] = [
            f": {type_name} =",
            f": Optional[{type_name}] =",
            f": None | {type_name} =",
        ]
        OVERRIDE_ELEM_TO_CLASS[override.name] = type_name


def get(name: str, default: Ovr | None = None) -> Ovr | None:
    """Get an override by name.  If not found, return default."""
    return OVERRIDES.get(name, default)
