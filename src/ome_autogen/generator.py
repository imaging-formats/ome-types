from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator

import ome_autogen.overrides as ovr
from ome_autogen import _util
from xsdata_pydantic_basemodel.generator import PydanticBaseFilters

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jinja2 import Environment, FileSystemLoader
    from xsdata.codegen.models import Attr, Class
    from xsdata.codegen.resolver import DependenciesResolver
    from xsdata.models.config import GeneratorConfig


class OmeGenerator(DataclassGenerator):
    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return OmeFilters(config)

    def render_module(
        self, resolver: DependenciesResolver, classes: list[Class]
    ) -> str:
        mod = super().render_module(resolver, classes)

        # xsdata renames classes like "FillRule" (which appears as a SimpleType
        # inside of the Shape ComplexType) as "Shape_FillRule".
        # We want to make them available as "FillRule" in the corresponding
        # module, (i.e. the "Shape" module in this case).
        # That is, we want "Shape = Shape_FillRule" included in the module.
        # this is for backwards compatibility.
        aliases = []
        for c in classes:
            for i in resolver.imports:
                if f"{c.name}_" in i.qname:
                    # import_name is something like 'Shape_FillRule'
                    import_name = i.qname.rsplit("}", 1)[-1]
                    # desired alias is just 'FillRule'
                    alias = import_name.split(f"{c.name}_")[-1]
                    aliases.append(f"{alias} = {import_name}")

            # we also want inner (nested) classes to be available at the top level
            # e.g. map.Map.M -> map.M
            for inner in c.inner:
                aliases.append(f"{inner.name} = {c.name}.{inner.name}")

        if aliases:
            mod += "\n\n" + "\n".join(aliases) + "\n"

        return mod


class OmeFilters(PydanticBaseFilters):
    def register(self, env: Environment) -> None:
        # add our own templates dir to the search path
        tpl_dir = Path(__file__).parent.joinpath("templates")
        cast("FileSystemLoader", env.loader).searchpath.insert(0, str(tpl_dir))
        super().register(env)
        env.filters.update({"methods": self.methods})

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)

        # TODO: it would be nice to know how to get the schema we're processing from
        # the config.  For now, we just assume it's the OME schema and that's the
        # hardcoded default in _util.get_appinfo
        self.appinfo = _util.get_appinfo()

    def class_params(self, obj: Class) -> Iterator[tuple[str, str, str]]:  # type: ignore[override]
        # This method override goes along with the docstring jinja template override
        # to fixup the numpy docstring format.
        # https://github.com/tefra/xsdata/issues/818
        # The type ignore is because xsdata returns an iterator of 2-tuples
        # but we want to return a 3-tuple.
        for attr in obj.attrs:
            # IMPORTANT:
            # self.field_type must be called before getting attr.name, since that
            # is currently where plural names are corrected.  (This is a hack.)
            type_ = self.field_type(obj, attr)

            name = (
                # use local_name for enums to preserve original XML value (e.g. "Å")
                # xsdata 24.4+ transforms attr.name to Unicode char names for non-ASCII
                self.constant_name(attr.local_name, obj.name)
                if obj.is_enumeration
                else self.field_name(attr.name, obj.name)
            )
            if not (help_ := attr.help):
                help_ = f"(The {obj.name} {attr.name})."
            yield name, type_, self.clean_docstring(help_)

    def class_bases(self, obj: Class, class_name: str) -> list[str]:
        # we don't need PydanticBaseFilters to add the Base class
        # because we add it in the config.extensions
        # This could go once PydanticBaseFilters is better about deduping
        return Filters.class_bases(self, obj, class_name)

    def _attr_is_optional(self, attr: Attr) -> bool:
        if attr.name in ovr.NEVER_OPTIONAL:
            return False
        return attr.is_nillable or (attr.default is None and attr.is_optional)

    def _format_type(self, attr: Attr, result: str) -> str:
        if self._attr_is_optional(attr):
            return f"None | {result}"
        return result

    def field_type(self, obj: Class, attr: Attr) -> str:
        if attr.is_list and not getattr(attr, "_plural_set", False):
            # HACK
            # It would be nicer to put this in the self.field_name method...but that
            # method only receives the attr name, not the attr object, and so we
            # don't know at that point whether it belongs to a list or not.
            # This hack works only because this method is called BEFORE self.field_name
            # in the class.jinja2 template, so we directly modify the attr object here.
            attr.name = self.appinfo.plurals.get(attr.name, f"{attr.name}s")
            attr._plural_set = True  # type: ignore

        if attr.name in ovr.OVERRIDE_ELEM_TO_CLASS:
            return self._format_type(attr, ovr.OVERRIDE_ELEM_TO_CLASS[attr.name])

        type_name = super().field_type(obj, attr)
        if attr.name == "Union":
            # xsdata >= 26.1 makes all elements in a <choice> optional,
            # but ROI.Union is required (minOccurs=1 in a single-element choice)
            type_name = type_name.removeprefix("None | ")
        # we want to use datetime.datetime instead of XmlDateTime
        return type_name.replace("XmlDateTime", "datetime")

    @classmethod
    def build_import_patterns(cls) -> dict[str, dict]:
        import_patterns = super().build_import_patterns()
        for mod, types in ovr.IMPORT_PATTERNS.items():
            mod_entry: dict[str, list[str]] = import_patterns.setdefault(mod, {})
            for name, patterns in types.items():
                name_entry: list[str] = mod_entry.setdefault(name, [])
                name_entry.extend(patterns)
        return {key: import_patterns[key] for key in sorted(import_patterns)}

    def field_default_value(self, attr: Attr, ns_map: dict | None = None) -> str:
        if override := ovr.get(attr.name):
            if override.default_factory:
                return override.default_factory
            if override.default:
                return override.default

        return super().field_default_value(attr, ns_map)

    def format_arguments(self, kwargs: dict, indent: int = 0) -> str:
        # keep default_factory at the front
        attr_name = kwargs.get("metadata", {}).get("name")
        if (override := ovr.get(attr_name)) and override.default_factory:
            kwargs.pop("default", None)
            kwargs["default_factory"] = override.default_factory

        # uncomment this to use new_uuid as the default_factory for all UUIDs
        # but then we have an equality checking problem in the tests
        # if kwargs.get("metadata", {}).get("pattern", "").startswith("(urn:uuid:"):
        #     kwargs.pop("default", None)
        #     kwargs = {"default_factory": "new_uuid", **kwargs}
        return super().format_arguments(kwargs, indent)

    def constant_name(self, name: str, class_name: str) -> str:
        if class_name in self.appinfo.enums:
            # use the enum names found in appinfo/xsdfu/enum
            enum_values = self.appinfo.enums[class_name]
            if name in enum_values:
                return enum_values[name].enum
        return super().constant_name(name, class_name)

    def methods(self, obj: Class) -> list[str]:
        if (override := ovr.get(obj.name)) and (lines := override.add_lines):
            return ["\n\n" + "\n".join(lines)]
        return []
