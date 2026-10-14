# Usage

`ome_types` is useful for parsing the [OME-XML
format](https://docs.openmicroscopy.org/ome-model/latest/ome-xml/) into
Python objects for interactive or programmatic access in python. It can
also take these Python objects and turn them back into OME-XML.

For example, you can parse an ome.xml, and then explore it with pythonic
`camel_case` syntax and readable object representations:

## Reading

``` python
In [1]: from ome_types import from_xml

In [2]: ome = from_xml('tests/data/hcs.ome.xml')  # or ome_types.OME.from_xml()
```

[ome_types.from_xml][] returns an instance of [ome_types.OME][].
This object is a container for all information objects accessible by OME.

``` python
In [3]: ome
Out[3]: 
OME(
    images=[<1 Images>],
    plates=[<1 Plates>],
)

In [4]: ome.plates[0]
Out[4]: 
Plate(
    id='Plate:1',
    name='Control Plate',
    column_naming_convention='letter',
    columns=12,
    row_naming_convention='number',
    rows=8,
    wells=[<1 Wells>],
)

In [5]: ome.plates[0].wells[0]
Out[5]: 
Well(
    id='Well:1',
    column=0,
    row=0,
    well_samples=[<1 Well_Samples>],
)

In [6]: ome.images[0]
Out[6]: 
Image(
    id='Image:0',
    name='Series 1',
    pixels=Pixels(
        id='Pixels:0',
        dimension_order='XYCZT',
        size_c=3,
        size_t=16,
        size_x=1024,
        size_y=1024,
        size_z=1,
        type='uint16',
        bin_data=[<1 Bin_Data>],
        channels=[<3 Channels>],
        physical_size_x=0.207,
        physical_size_y=0.207,
        time_increment=120.1302,
    ),
    acquisition_date=datetime.fromisoformat('2008-02-06T13:43:19'),
    description='An example OME compliant file, based on Olympus.oib',
)

In [7]: ome.images[0].pixels.channels[0]
Out[7]: 
Channel(
    id='Channel:0:0',
    name='CH1',
    acquisition_mode='LaserScanningConfocalMicroscopy',
    emission_wavelength=523.0,
    excitation_wavelength=488.0,
    illumination_type='Epifluorescence',
    pinhole_size=103.5,
    samples_per_pixel=1,
)

In [8]: ome.images[0].pixels.channels[0].emission_wavelength                                                                               
Out[8]: 523.0
```

## Modifying or Creating

The `OME` object is mutable, and you may make changes:

``` python
In [9]: from ome_types.model import UnitsLength

In [10]: from ome_types.model.channel import AcquisitionMode

In [11]: ome.images[0].description = "This is the new description."

In [12]: ome.images[0].pixels.physical_size_x = 350.0

In [13]: ome.images[0].pixels.physical_size_x_unit = UnitsLength.NANOMETER

In [14]: for c in ome.images[0].pixels.channels:
             c.acquisition_mode = AcquisitionMode.SPINNING_DISK_CONFOCAL
```

And add elements by constructing new `OME` model objects:

``` python
In [15]: from ome_types.model import Instrument, Microscope, Objective, InstrumentRef

In [16]: microscope_mk4 = Microscope(
             manufacturer='OME Instruments',
             model='Lab Mk4',
             serial_number='L4-5678',
         )

In [17]: objective_40x = Objective(
             manufacturer='OME Objectives',
             model='40xAir',
             nominal_magnification=40.0,
         )

In [18]: instrument = Instrument(
             microscope=microscope_mk4,
             objectives=[objective_40x],
         )

In [19]: ome.instruments.append(instrument)

In [20]: ome.images[0].instrument_ref = InstrumentRef(instrument.id)

In [21]: ome.instruments
Out[21]:
[Instrument(
    id='Instrument:1',
    microscope=Microscope(
       manufacturer='OME Instruments',
       model='Lab Mk4',
       serial_number='L4-5678',
    ),
    objectives=[<1 Objectives>],
 )]
```

## Serialization

You can generate the OME-XML representation of the OME model
object, for writing to a standalone `.ome.xml` file or inserting into the
header of an OME-TIFF file:

``` python
In [22]: from ome_types import to_xml

In [23]: print(to_xml(ome))  # or ome.to_xml()
<OME ...>
    <Plate ColumnNamingConvention="letter" Columns="12" ID="Plate:1" ...>
        ...
    </Plate>
    <Instrument ID="Instrument:1">
        <Microscope Manufacturer="OME Instruments" Model="Lab Mk4" SerialNumber="L4-5678" />
        <Objective Manufacturer="OME Objectives" Model="40xAir" ID="Objective:1" NominalMagnification="40.0" />
    </Instrument>
    <Image ID="Image:0" Name="Series 1">
        <AcquisitionDate>2008-02-06T13:43:19</AcquisitionDate>
        <Description>This is the new description.</Description>
        <InstrumentRef ID="Instrument:1" />
        <Pixels ... PhysicalSizeX="350.0" PhysicalSizeXUnit="nm" ...>
            <Channel AcquisitionMode="SpinningDiskConfocal" ...>
             ...
        </Pixels>
    </Image>
</OME>
```

## Writing companion OME files

The writing capability can be used to generate OME-TIFF filesets as
described in the [OME-TIFF](https://ome-model.readthedocs.io/en/stable/ome-tiff/specification.html)
by storing the metadata as OME-XML into a companion file.

The following code demonstrates how to write  companion files for the
multi-channel fluorescent images published in
[IDR](https://idr.openmicroscopy.org/) under the accession idr0052 and
available at [10.17867/10000123a](https://doi.org/10.17867/10000123a).

The associated raw TIFF files can be downloaded from
[here](https://ftp.ebi.ac.uk/pub/databases/IDR/idr0052-walther-condensinmap/20181113-ftp/MitoSys/160719_NCAPD2gfpc272c78_MitoSys2/cell0005_R0001/rawtif/)

```python
from ome_types.model import Channel
from ome_types.model import Image
from ome_types.model import OME
from ome_types.model import Pixels
from ome_types.model import TiffData
import uuid

ome = OME(uuid=f"urn:uuid:{uuid.uuid4()}")
pixels = Pixels(
    dimension_order="XYZCT",
    physical_size_x="0.2516",
    physical_size_y="0.2516",
    physical_size_z="0.75",
    size_x=256,
    size_y=256,
    size_z=31,
    size_c=3,
    size_t=40,
    type="uint16",
)
pixels.channels.extend(
    [
        Channel(color="16711935", name="NCAPD2", samples_per_pixel=1),
        Channel(color="65535", name="DNA", samples_per_pixel=1),
        Channel(color="-1", name="NEG_Dextran", samples_per_pixel=1),
    ]
)
ome.images.append(Image(name="cell0005_R0001", pixels=pixels))

for t in range(40):
    filename = "TR1_2_W0001_P0001_T%04g.tif" % (t + 1)
    tiff_uuid = f"urn:uuid:{uuid.uuid4()}"
    tiff = TiffData(
        first_c=0,
        first_t=t,
        first_z=0,
        plane_count=93,
        uuid=TiffData.UUID(value=tiff_uuid, file_name=filename),
    )
    pixels.tiff_data_blocks.append(tiff)

with open("cell0005_R0001.companion.ome", "w") as f:
    f.write(ome.to_xml())
```
