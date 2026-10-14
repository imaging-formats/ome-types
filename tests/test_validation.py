from __future__ import annotations

import contextlib
from contextlib import AbstractContextManager, nullcontext
from typing import TYPE_CHECKING

import pytest

from ome_types import _conversion, validate_xml

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

VALIDATORS: dict[str, Callable] = {}
with contextlib.suppress(ImportError):
    import lxml  # noqa: F401

    VALIDATORS["lxml"] = _conversion.validate_xml_with_lxml

with contextlib.suppress(ImportError):
    import xmlschema  # noqa: F401

    VALIDATORS["xmlschema"] = _conversion.validate_xml_with_xmlschema


REQUIRES_TRANSFORM = {"seq0000xy01c1.ome.xml", "2008_instrument.ome.xml"}


@pytest.mark.filterwarnings("ignore:unclosed file")
@pytest.mark.parametrize("backend", VALIDATORS)
def test_validation_good(valid_xml: Path, backend: str) -> None:
    if valid_xml.name in REQUIRES_TRANSFORM:
        ctx: AbstractContextManager = pytest.warns(match="Transformed source from")
    else:
        ctx = nullcontext()
    with ctx:
        VALIDATORS[backend](valid_xml)


def test_validation_anybackend(single_xml: Path) -> None:
    if VALIDATORS:
        validate_xml(single_xml)
    else:
        with pytest.raises(ImportError):
            validate_xml(single_xml)


@pytest.mark.parametrize("backend", VALIDATORS)
def test_validation_raises(invalid_xml: Path, backend: str) -> None:
    with pytest.raises(_conversion.ValidationError):
        VALIDATORS[backend](invalid_xml)
