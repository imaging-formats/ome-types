from __future__ import annotations

import io
from pathlib import Path

import pytest
from pydantic import ValidationError

from ome_types import from_xml, model
from ome_types._conversion import OME_2016_06_URI, _get_root_ome_type

DATA = Path(__file__).parent / "data"
VALIDATE = [False]


@pytest.mark.parametrize("validate", VALIDATE)
def test_from_valid_xml(valid_xml: Path, validate: bool) -> None:
    ome = model.OME.from_xml(valid_xml, validate=validate)  # class method for coverage
    assert ome
    assert repr(ome)


@pytest.mark.parametrize("validate", VALIDATE)
def test_from_invalid_xml(invalid_xml: Path, validate: bool) -> None:
    if validate:
        with pytest.raises(ValidationError):
            from_xml(invalid_xml, validate=validate)
    else:
        with pytest.warns():
            from_xml(invalid_xml, validate=validate)


def test_with_ome_ns() -> None:
    assert from_xml(DATA / "ome_ns.ome.xml").experimenters


def test_get_root_ome_type() -> None:
    xml = io.BytesIO(f'<Image xmlns="{OME_2016_06_URI}" />'.encode())
    t = _get_root_ome_type(xml)
    assert t is model.Image

    xml = io.BytesIO(f'<ome:Image xmlns:ome="{OME_2016_06_URI}" />'.encode())
    t = _get_root_ome_type(xml)
    assert t is model.Image

    with pytest.raises(ValueError, match="Unknown root element"):
        _get_root_ome_type(io.BytesIO(b"<Imdgage />"))

    # this can be used to instantiate XML with a non OME root type:
    obj = from_xml(f'<Project xmlns="{OME_2016_06_URI}" />')
    assert isinstance(obj, model.Project)
    obj = from_xml(
        f'<XMLAnnotation xmlns="{OME_2016_06_URI}"><Value><Data>'
        "</Data></Value></XMLAnnotation>"
    )
    assert isinstance(obj, model.XMLAnnotation)


def test_unknown_ns() -> None:
    with pytest.raises(ValueError, match="Unsupported document namespace"):
        from_xml('<Image xmlns="http://unknown.org" />')


def test_uncapitalized_ns() -> None:
    xml = '<Detector xmlns="http://www.openmicroscopy.org/Schemas/ome/2016-06" />'
    ome = from_xml(xml)
    assert isinstance(ome, model.Detector)


def test_2013_06s_ns() -> None:
    # typo'd namespaces written by python-bioformats' omexml.py (e.g. imctools)
    pytest.importorskip("lxml", reason="lxml needed for old schema")
    xml = """
    <ome:OME xmlns:ns2="http://www.openmicroscopy.org/Schemas/BinaryFile/2013-06s"
      xmlns:ome="http://www.openmicroscopy.org/Schemas/ome/2013-06s"
      xmlns:sa="http://www.openmicroscopy.org/Schemas/sa/2013-06s">
      <ome:Image ID="Image:0" Name="test">
        <ome:Pixels DimensionOrder="XYCZT" ID="Pixels:0" SizeC="1" SizeT="1"
          SizeX="2" SizeY="2" SizeZ="1" Type="float">
          <ome:Channel ID="Channel:0:0" Name="ch0" SamplesPerPixel="1" />
          <ns2:BinData BigEndian="false" Length="0" />
        </ome:Pixels>
      </ome:Image>
      <sa:StructuredAnnotations>
        <sa:CommentAnnotation ID="Annotation:0"><sa:Value>hi</sa:Value>
        </sa:CommentAnnotation>
      </sa:StructuredAnnotations>
    </ome:OME>
    """
    ome = from_xml(xml)
    assert ome.images[0].pixels.channels[0].name == "ch0"
    assert ome.structured_annotations.comment_annotations[0].value == "hi"


def test_weird_input() -> None:
    with pytest.raises(ValueError, match="Could not parse XML"):
        from_xml("ImageJmetadata")


def test_must_be_binary(tmp_path: Path) -> None:
    xml = tmp_path / "test.xml"
    xml.write_text('<OME xmlns="http://www.openmicroscopy.org/Schemas/ome/2016-06" />')

    with open(xml, "rb") as fh:
        assert isinstance(from_xml(fh), model.OME)

    with open(xml) as fh, pytest.raises(TypeError, match="must be opened in binary"):
        from_xml(fh)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="Unsupported source type"):
        from_xml(8)  # type: ignore[arg-type]
