from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias, TypedDict

if TYPE_CHECKING:
    from datetime import datetime

    import ome_types.model as ome


class RefDict(TypedDict):
    id: str


class AffineTransformDict(TypedDict, total=False):
    a00: float
    a01: float
    a02: float
    a10: float
    a11: float
    a12: float


class AnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str


AnnotationRefDict: TypeAlias = RefDict


class ArcDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    power: None | float
    power_unit: ome.UnitsPower | str
    serial_number: None | str
    type: None | (ome.Arc_Type | str)


class BinDataDict(TypedDict, total=False):
    big_endian: bool
    compression: ome.BinData_Compression | str
    length: int
    value: bytes


class BinaryFileDict(TypedDict, total=False):
    bin_data: None | BinDataDict
    external: None | ExternalDict
    file_name: str
    mime_type: None | str
    size: int


class BooleanAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: bool


class ChannelDict(TypedDict, total=False):
    acquisition_mode: None | (ome.Channel_AcquisitionMode | str)
    annotation_refs: list[AnnotationRefDict]
    color: ome.Color | str
    contrast_method: None | (ome.Channel_ContrastMethod | str)
    detector_settings: None | DetectorSettingsDict
    emission_wavelength: None | float
    emission_wavelength_unit: ome.UnitsLength | str
    excitation_wavelength: None | float
    excitation_wavelength_unit: ome.UnitsLength | str
    filter_set_ref: None | FilterSetRefDict
    fluor: None | str
    id: str
    illumination_type: None | (ome.Channel_IlluminationType | str)
    light_path: None | LightPathDict
    light_source_settings: None | LightSourceSettingsDict
    name: None | str
    nd_filter: None | float
    pinhole_size: None | float
    pinhole_size_unit: ome.UnitsLength | str
    pockel_cell_setting: None | int
    samples_per_pixel: None | int


ChannelRefDict: TypeAlias = RefDict


class CommentAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: str


class DatasetDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    experimenter_group_ref: None | ExperimenterGroupRefDict
    experimenter_ref: None | ExperimenterRefDict
    id: str
    image_refs: list[ImageRefDict]
    name: None | str


DatasetRefDict: TypeAlias = RefDict


class DetectorDict(TypedDict, total=False):
    amplification_gain: None | float
    annotation_refs: list[AnnotationRefDict]
    gain: None | float
    id: str
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    offset: None | float
    serial_number: None | str
    type: None | (ome.Detector_Type | str)
    voltage: None | float
    voltage_unit: ome.UnitsElectricPotential | str
    zoom: None | float


class DetectorSettingsDict(TypedDict, total=False):
    binning: None | (ome.Binning | str)
    gain: None | float
    id: str
    integration: None | int
    offset: None | float
    read_out_rate: None | float
    read_out_rate_unit: ome.UnitsFrequency | str
    voltage: None | float
    voltage_unit: ome.UnitsElectricPotential | str
    zoom: None | float


class DichroicDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    serial_number: None | str


DichroicRefDict: TypeAlias = RefDict


class DoubleAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: float


class EllipseDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    id: str
    locked: None | bool
    radius_x: float
    radius_y: float
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict
    x: float
    y: float


class ExperimentDict(TypedDict, total=False):
    description: None | str
    experimenter_ref: None | ExperimenterRefDict
    id: str
    microbeam_manipulations: list[MicrobeamManipulationDict]
    type: list[ome.Experiment_value | str]


ExperimentRefDict: TypeAlias = RefDict


class ExperimenterDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    email: None | str
    first_name: None | str
    id: str
    institution: None | str
    last_name: None | str
    middle_name: None | str
    user_name: None | str


class ExperimenterGroupDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    experimenter_refs: list[ExperimenterRefDict]
    id: str
    leaders: list[LeaderDict]
    name: None | str


ExperimenterGroupRefDict: TypeAlias = RefDict
ExperimenterRefDict: TypeAlias = RefDict


class ExternalDict(TypedDict, total=False):
    compression: ome.External_Compression | str
    href: str
    sha1: bytes


class FilamentDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    power: None | float
    power_unit: ome.UnitsPower | str
    serial_number: None | str
    type: None | (ome.Filament_Type | str)


class FileAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    binary_file: BinaryFileDict
    description: None | str
    id: str
    namespace: None | str


class FilterDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    filter_wheel: None | str
    id: str
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    serial_number: None | str
    transmittance_range: None | TransmittanceRangeDict
    type: None | (ome.Filter_Type | str)


FilterRefDict: TypeAlias = RefDict


class FilterSetDict(TypedDict, total=False):
    dichroic_ref: None | DichroicRefDict
    emission_filters: list[FilterRefDict]
    excitation_filters: list[FilterRefDict]
    id: str
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    serial_number: None | str


FilterSetRefDict: TypeAlias = RefDict


class FolderDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    folder_refs: list[FolderRefDict]
    id: str
    image_refs: list[ImageRefDict]
    name: None | str
    roi_refs: list[ROIRefDict]


FolderRefDict: TypeAlias = RefDict


class GenericExcitationSourceDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: None | str
    manufacturer: None | str
    map: None | MapDict
    model: None | str
    power: None | float
    power_unit: ome.UnitsPower | str
    serial_number: None | str


class ImageDict(TypedDict, total=False):
    acquisition_date: None | datetime
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    experiment_ref: None | ExperimentRefDict
    experimenter_group_ref: None | ExperimenterGroupRefDict
    experimenter_ref: None | ExperimenterRefDict
    id: str
    imaging_environment: None | ImagingEnvironmentDict
    instrument_ref: None | InstrumentRefDict
    microbeam_manipulation_refs: list[MicrobeamManipulationRefDict]
    name: None | str
    objective_settings: None | ObjectiveSettingsDict
    pixels: PixelsDict
    roi_refs: list[ROIRefDict]
    stage_label: None | StageLabelDict


ImageRefDict: TypeAlias = RefDict


class ImagingEnvironmentDict(TypedDict, total=False):
    air_pressure: None | float
    air_pressure_unit: ome.UnitsPressure | str
    co2_percent: None | float
    humidity: None | float
    map: None | MapDict
    temperature: None | float
    temperature_unit: ome.UnitsTemperature | str


class InstrumentDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    arcs: list[ArcDict]
    detectors: list[DetectorDict]
    dichroics: list[DichroicDict]
    filaments: list[FilamentDict]
    filter_sets: list[FilterSetDict]
    filters: list[FilterDict]
    generic_excitation_sources: list[GenericExcitationSourceDict]
    id: str
    lasers: list[LaserDict]
    light_emitting_diodes: list[ome.LightEmittingDiode | str]
    microscope: None | MicroscopeDict
    objectives: list[ObjectiveDict]


InstrumentRefDict: TypeAlias = RefDict


class LabelDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    id: str
    locked: None | bool
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict
    x: float
    y: float


class LaserDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    frequency_multiplication: None | int
    id: str
    laser_medium: None | (ome.Laser_LaserMedium | str)
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    pockel_cell: None | bool
    power: None | float
    power_unit: ome.UnitsPower | str
    pulse: None | (ome.Laser_Pulse | str)
    pump: None | PumpDict
    repetition_rate: None | float
    repetition_rate_unit: ome.UnitsFrequency | str
    serial_number: None | str
    tuneable: None | bool
    type: None | (ome.Laser_Type | str)
    wavelength: None | float
    wavelength_unit: ome.UnitsLength | str


class LeaderDict(TypedDict, total=False):
    id: str


class LightPathDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    dichroic_ref: None | DichroicRefDict
    emission_filters: list[FilterRefDict]
    excitation_filters: list[FilterRefDict]


class LightSourceDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    id: str
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    power: None | float
    power_unit: ome.UnitsPower | str
    serial_number: None | str


class LightSourceSettingsDict(TypedDict, total=False):
    attenuation: None | float
    id: str
    wavelength: None | float
    wavelength_unit: ome.UnitsLength | str


class LineDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    id: str
    locked: None | bool
    marker_end: None | (ome.Marker | str)
    marker_start: None | (ome.Marker | str)
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict
    x1: float
    x2: float
    y1: float
    y2: float


class LongAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: int


class ManufacturerSpecDict(TypedDict, total=False):
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    serial_number: None | str


class MapDict(TypedDict, total=False):
    ms: list[ome.Map.M | str]


class MapAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: MapDict


class MaskDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    bin_data: BinDataDict
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    height: float
    id: str
    locked: None | bool
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict
    width: float
    x: float
    y: float


class MicrobeamManipulationDict(TypedDict, total=False):
    description: None | str
    experimenter_ref: ExperimenterRefDict
    id: str
    light_source_settings_combinations: list[LightSourceSettingsDict]
    roi_refs: list[ROIRefDict]
    type: list[ome.MicrobeamManipulation_value | str]


MicrobeamManipulationRefDict: TypeAlias = RefDict


class MicroscopeDict(TypedDict, total=False):
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    serial_number: None | str
    type: None | (ome.Microscope_Type | str)


class OMEDict(TypedDict, total=False):
    binary_only: None | (ome.OME.BinaryOnly | str)
    creator: None | str
    datasets: list[DatasetDict]
    experimenter_groups: list[ExperimenterGroupDict]
    experimenters: list[ExperimenterDict]
    experiments: list[ExperimentDict]
    folders: list[FolderDict]
    images: list[ImageDict]
    instruments: list[InstrumentDict]
    plates: list[PlateDict]
    projects: list[ProjectDict]
    rights: None | RightsDict
    rois: list[ROIDict]
    screens: list[ScreenDict]
    structured_annotations: None | StructuredAnnotationsDict
    uuid: None | str


class ObjectiveDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    calibrated_magnification: None | float
    correction: None | (ome.Objective_Correction | str)
    id: str
    immersion: None | (ome.Objective_Immersion | str)
    iris: None | bool
    lens_na: None | float
    lot_number: None | str
    manufacturer: None | str
    model: None | str
    nominal_magnification: None | float
    serial_number: None | str
    working_distance: None | float
    working_distance_unit: ome.UnitsLength | str


class ObjectiveSettingsDict(TypedDict, total=False):
    correction_collar: None | float
    id: str
    medium: None | (ome.ObjectiveSettings_Medium | str)
    refractive_index: None | float


class PixelsDict(TypedDict, total=False):
    big_endian: None | bool
    bin_data_blocks: list[BinDataDict]
    channels: list[ChannelDict]
    dimension_order: ome.Pixels_DimensionOrder | str
    id: str
    interleaved: None | bool
    metadata_only: None | (ome.MetadataOnly | str)
    physical_size_x: None | float
    physical_size_x_unit: ome.UnitsLength | str
    physical_size_y: None | float
    physical_size_y_unit: ome.UnitsLength | str
    physical_size_z: None | float
    physical_size_z_unit: ome.UnitsLength | str
    planes: list[PlaneDict]
    significant_bits: None | int
    size_c: int
    size_t: int
    size_x: int
    size_y: int
    size_z: int
    tiff_data_blocks: list[TiffDataDict]
    time_increment: None | float
    time_increment_unit: ome.UnitsTime | str
    type: ome.PixelType | str


class PlaneDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    delta_t: None | float
    delta_t_unit: ome.UnitsTime | str
    exposure_time: None | float
    exposure_time_unit: ome.UnitsTime | str
    hash_sha1: None | bytes
    position_x: None | float
    position_x_unit: ome.UnitsLength | str
    position_y: None | float
    position_y_unit: ome.UnitsLength | str
    position_z: None | float
    position_z_unit: ome.UnitsLength | str
    the_c: int
    the_t: int
    the_z: int


class PlateDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    column_naming_convention: None | (ome.NamingConvention | str)
    columns: None | int
    description: None | str
    external_identifier: None | str
    field_index: None | int
    id: str
    name: None | str
    plate_acquisitions: list[PlateAcquisitionDict]
    row_naming_convention: None | (ome.NamingConvention | str)
    rows: None | int
    status: None | str
    well_origin_x: None | float
    well_origin_x_unit: ome.UnitsLength | str
    well_origin_y: None | float
    well_origin_y_unit: ome.UnitsLength | str
    wells: list[WellDict]


class PlateAcquisitionDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    end_time: None | datetime
    id: str
    maximum_field_count: None | int
    name: None | str
    start_time: None | datetime
    well_sample_refs: list[WellSampleRefDict]


class PointDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    id: str
    locked: None | bool
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict
    x: float
    y: float


class PolygonDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    id: str
    locked: None | bool
    points: str
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict


class PolylineDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    id: str
    locked: None | bool
    marker_end: None | (ome.Marker | str)
    marker_start: None | (ome.Marker | str)
    points: str
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict


class ProjectDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    dataset_refs: list[DatasetRefDict]
    description: None | str
    experimenter_group_ref: None | ExperimenterGroupRefDict
    experimenter_ref: None | ExperimenterRefDict
    id: str
    name: None | str


ProjectRefDict: TypeAlias = RefDict


class PumpDict(TypedDict, total=False):
    id: str


class ROIDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    id: str
    name: None | str
    union: ome.ROI.Union | str


ROIRefDict: TypeAlias = RefDict


class ReagentDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    id: str
    name: None | str
    reagent_identifier: None | str


ReagentRefDict: TypeAlias = RefDict


class RectangleDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    height: float
    id: str
    locked: None | bool
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict
    width: float
    x: float
    y: float


class RightsDict(TypedDict, total=False):
    rights_held: None | str
    rights_holder: None | str


class ScreenDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    description: None | str
    id: str
    name: None | str
    plate_refs: list[ome.Screen.PlateRef | str]
    protocol_description: None | str
    protocol_identifier: None | str
    reagent_set_description: None | str
    reagent_set_identifier: None | str
    reagents: list[ReagentDict]
    type: None | str


class ShapeDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    fill_color: None | (ome.Color | str)
    fill_rule: None | (ome.Shape_FillRule | str)
    font_family: None | (ome.Shape_FontFamily | str)
    font_size: None | int
    font_size_unit: ome.UnitsLength | str
    font_style: None | (ome.Shape_FontStyle | str)
    id: str
    locked: None | bool
    stroke_color: None | (ome.Color | str)
    stroke_dash_array: None | str
    stroke_width: None | float
    stroke_width_unit: ome.UnitsLength | str
    text: None | str
    the_c: None | int
    the_t: None | int
    the_z: None | int
    transform: None | AffineTransformDict


class StageLabelDict(TypedDict, total=False):
    name: str
    x: None | float
    x_unit: ome.UnitsLength | str
    y: None | float
    y_unit: ome.UnitsLength | str
    z: None | float
    z_unit: ome.UnitsLength | str


class StructuredAnnotationsDict(TypedDict, total=False):
    boolean_annotations: list[BooleanAnnotationDict]
    comment_annotations: list[CommentAnnotationDict]
    double_annotations: list[DoubleAnnotationDict]
    file_annotations: list[FileAnnotationDict]
    list_annotations: list[ome.ListAnnotation | str]
    long_annotations: list[LongAnnotationDict]
    map_annotations: list[MapAnnotationDict]
    tag_annotations: list[TagAnnotationDict]
    term_annotations: list[TermAnnotationDict]
    timestamp_annotations: list[TimestampAnnotationDict]
    xml_annotations: list[XMLAnnotationDict]


class TagAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: str


class TermAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: str


class TiffDataDict(TypedDict, total=False):
    first_c: int
    first_t: int
    first_z: int
    ifd: int
    plane_count: None | int
    uuid: None | (ome.TiffData.UUID | str)


class TimestampAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: datetime


class TransmittanceRangeDict(TypedDict, total=False):
    cut_in: None | float
    cut_in_tolerance: None | float
    cut_in_tolerance_unit: ome.UnitsLength | str
    cut_in_unit: ome.UnitsLength | str
    cut_out: None | float
    cut_out_tolerance: None | float
    cut_out_tolerance_unit: ome.UnitsLength | str
    cut_out_unit: ome.UnitsLength | str
    transmittance: None | float


class WellDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    color: ome.Color | str
    column: int
    external_description: None | str
    external_identifier: None | str
    id: str
    reagent_ref: None | ReagentRefDict
    row: int
    type: None | str
    well_samples: list[WellSampleDict]


class WellSampleDict(TypedDict, total=False):
    id: str
    image_ref: None | ImageRefDict
    index: int
    position_x: None | float
    position_x_unit: ome.UnitsLength | str
    position_y: None | float
    position_y_unit: ome.UnitsLength | str
    timepoint: None | datetime


WellSampleRefDict: TypeAlias = RefDict


class XMLAnnotationDict(TypedDict, total=False):
    annotation_refs: list[AnnotationRefDict]
    annotator: None | str
    description: None | str
    id: str
    namespace: None | str
    value: ome.XMLAnnotation.Value | str
