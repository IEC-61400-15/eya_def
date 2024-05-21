"""Data models relating to wind resource assessments (WRAs).

The description of wind resource assessments is divided into the model
class ``WindResourceAssessment`` covering the measurement location(s)
and ``TurbineWindResourceAssessment`` covering the turbine locations.
The reason for this split is that the assessment of wind resource at the
measurement location(s) does not depend on the scenario and is therefore
contained at the top level of the EYA DEF schema, whereas the turbine
wind resource assessment depends on the turbine layout (and potentially
other aspects of a scenario) and is therefore contained at the scenario
level.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.wind_uncertainty import WindUncertaintyAssessment


class WindResourceDatasetStatistics(EyaDefBaseModel):
    """Statistics related to the wind resource assessment datasets.

    This schema includes statistics items that describe the raw input
    datasets, which are not covered under the metadata schemas for the
    measurement stations, reference meteorological datasets and
    reference operational wind farms.
    """

    data_availability: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Dimensionless raw data availability (also known as data "
            "recovery rate and data coverage) for the primary inputs "
            "to the wind resource assessment. The standard required "
            "dataset(s) should report data availability on a monthly "
            "basis, with dimensions 'wind_dataset_id', 'location_id' "
            "(where the wind dataset has more than one location, "
            "otherwise omitted), 'point_id', 'year' and 'month' (in "
            "that order) for datasets from wind measurement stations "
            "and meteorological reference sources; and dimensions "
            "'reference_wind_farm_id', 'operational_dataset_id', "
            "'variable_id' (where data availability is not identical "
            "across all relevant variables within the operational "
            "dataset, otherwise omitted), 'turbine_id' (for variables "
            "at the turbine level and where data availability is not "
            "identical across all turbines, otherwise omitted), "
            "'year' and 'month' (in that order) for operational "
            "reference wind farm datasets. Additional datasets with "
            "other dimensions may be included optionally. The raw data "
            "availability is defined as the proportion of samples "
            "available in the raw dataset relative to the possible "
            "maximum amount of samples within a certain time frame "
            "(i.e. if no data were missing), before the author of the "
            "EYA has undertaken any data filtering. The raw dataset "
            "may include filtering inherent in the process of creating "
            "it, such as quality filtering implemented in the firmware "
            "of remote sensing devices (RSDs), and the raw data "
            "availability then describes the state of the dataset "
            "after such filtering has been applied."
        ),
    )


class WindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at measurement locations."""

    wind_speed: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Final long-term wind speed estimate(s) at the measurement "
            "location(s) in metre per second (m s-1). The dimensions "
            "of the first standard result dataset should be "
            "'wind_dataset_id', 'location_id' (where the wind dataset "
            "has more than one location, otherwise omitted), and "
            "'height' (in that order). Further results with other "
            "dimensions may be included optionally."
        ),
    )
    probability: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Final long-term probability distribution estimates at the "
            "measurement location(s), as dimensionless values. The "
            "first standard result dataset should comprise the joint "
            "wind speed and direction probability distributions, with "
            "dimensions 'wind_dataset_id', 'location_id' (where the "
            "wind dataset has multiple locations, otherwise omitted), "
            "'height', 'wind_speed' and 'wind_from_direction' (in that "
            "order). The wind speed coordinates should be 1.0 metre "
            "per second bins centered on whole numbers, with the first "
            "bin half the width (i.e. 0.25, 1.0, 2.0, 3.0, ...). The "
            "wind direction coordinates should be twelve 30.0 degree "
            "bins, with the the first bin centered at 0.0. Further "
            "results with other dimensions may be included optionally."
        ),
    )
    ambient_turbulence_intensity: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final ambient turbulence intensity estimates at the "
            "measurement location(s), as dimensionless values. This "
            "field is optional since some measurement devices may "
            "lack meaningful turbulence measurements, but it should "
            "always be included when relevant turbulence data are "
            "available. The first standard result dataset should "
            "comprise the ambient turbulence intensity as a function "
            "of wind speed, with the dimensions 'wind_dataset_id', "
            "'location_id' (where the wind dataset has more than one "
            "location, otherwise omitted), 'height' and 'wind_speed' "
            "(in that order). The wind speed coordinates should be 1.0 "
            "metre per second bins centered on whole numbers, with the "
            "first bin half the width (i.e. 0.25, 1.0, 2.0, 3.0, ...). "
            "Further results with other dimensions may also be "
            "included."
        ),
    )
    wind_shear_exponent: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term power law wind shear exponent estimates "
            "at the measurement location(s). This field is optional "
            "since some wind measurement stations may only include a "
            "single measurement height, but it should always be "
            "included when relevant wind shear exponent data are "
            "available. The dimension(s) of the first standard result "
            "dataset should be 'wind_dataset_id' and 'location_id' "
            "(where the wind dataset has more than one location, "
            "otherwise omitted). Further results with other dimensions "
            "may also be included."
        ),
    )
    temperature: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term temperature estimates at the measurement "
            "location(s) in degree C. This field is optional since "
            "some wind measurement stations may lack measurements of "
            "temperature, but it should always be included when "
            "relevant temperature data are available. The dimensions "
            "of the first standard result dataset should be "
            "'wind_dataset_id', 'location_id' (where the wind dataset "
            "has more than one location, otherwise omitted), and "
            "'height' (in that order). Further results with other "
            "dimensions may also be included."
        ),
    )
    air_density: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term air density estimates at the measurement "
            "location(s) in kilogram per cubic metre (kg m-3). This "
            "field is optional since some wind measurement stations "
            "may lack measurements required to derive air density "
            "estimates, but it should always be included when relevant "
            "data are available. The dimensions of the first standard "
            "result dataset should be 'wind_dataset_id', 'location_id' "
            "(where the wind dataset has more than one location, "
            "otherwise omitted), and 'height' (in that order). Further "
            "results with other dimensions may also be included."
        ),
    )
    displacement_height: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Estimated effective displacement of the boundary layer at "
            "the measurement location(s) due to vegetation (forestry) "
            "in metre. The displacement height is measured as positive "
            "upwards from the ground level. This field is optional as "
            "it is only relevant at forested sites. The dimensions of "
            "the first standard result dataset should be "
            "'wind_dataset_id' and 'location_id' (where the wind "
            "dataset has more than one location, otherwise omitted). "
            "Further results with other dimensions, such as "
            "displacement height binned by wind direction, may also be "
            "included."
        ),
    )


class WindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the measurement location(s)."""

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Unique ID of the wind resource assessment within the EYA "
            "DEF document, used to reference it from other parts of "
            "the document."
        ),
        examples=["WRA01", "BfWF_WRA_1", "A"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind resource assessment, "
            "which should not be empty if the field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind resource assessment, which "
            "should not be empty if the field is included."
        ),
    )
    dataset_statistics: WindResourceDatasetStatistics = pdt.Field(
        default=...,
        description=(
            "Statistics relating to the wind resource assessment "
            "datasets, such as data availability."
        ),
    )
    results: WindResourceResults = pdt.Field(
        default=...,
        description=(
            "Final results of the wind resource assessment at the "
            "measurement location(s). Results should generally be "
            "included at the primary measurement height and "
            "extrapolated to all assessed turbine hub heights at each "
            "measurement location, as relevant."
        ),
    )


class TurbineWindResourceWeighting(EyaDefBaseModel):
    """Details of weighting applied to estimate turbine wind resource."""

    source_wind_data: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional specification of the weight applied to the "
            "prediction based on each source of wind data when making "
            "the final wind resource estimate at each target turbine "
            "location. The dimensions of the first standard weighting "
            "specification dataset should be 'turbine_id' (the target "
            "turbine of the estimate for which the weight is applied), "
            "'wind_dataset_id' (the source wind dataset whose "
            "prediction the weight is applied to), 'location_id' "
            "(where the wind dataset has more than one location, "
            "otherwise omitted), and 'variable_id' (if different "
            "weights were applied to different variables, such as wind "
            "speed and wind direction weighted differently, otherwise "
            "omitted). Further results with additional dimensions may "
            "optionally be included, in which case the initial set of "
            "dimensions must be the same as those for the first "
            "standard dataset. For example, if weights are applied by "
            "wind direction bin, an additional dataset with dimensions "
            "'turbine_id', 'wind_dataset_id', 'location_id', "
            "'variable_id' and 'wind_from_direction' (bin) may be "
            "included."
        ),
    )


class TurbineWindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at turbine locations."""

    wind_speed: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Final long-term wind speed estimates at the turbine "
            "location(s) at hub height in metre per second (m s-1). "
            "The dimension of the first standard result dataset should "
            "be 'turbine_id'. Further results with other dimensions "
            "may be included optionally."
        ),
    )
    probability: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term probability distribution estimates at the "
            "turbine location(s) at hub height, as dimensionless "
            "values. The first standard result dataset should comprise "
            "the joint wind speed and direction probability "
            "distributions, with dimensions 'turbine_id', 'wind_speed' "
            "and 'wind_from_direction' (in that order). The wind speed "
            "coordinates should be 1.0 metre per second bins centered "
            "on whole numbers, with the first bin half the width "
            "(i.e. 0.25, 1.0, 2.0, 3.0, ...). The wind direction "
            "coordinates should be twelve 30.0 degree bins, with the "
            "the first bin centered at 0.0. Further results with other "
            "dimensions may also be included."
        ),
    )
    ambient_turbulence_intensity: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final ambient turbulence intensity estimates at the "
            "turbine location(s) at hub height, as dimensionless "
            "values. The first standard result dataset should comprise "
            "the ambient turbulence intensity as a function of wind "
            "speed, with the dimensions 'turbine_id' and 'wind_speed' "
            "(in that order). The wind speed coordinates should be 1.0 "
            "metre per second bins centered on whole numbers, with the "
            "first bin half the width (i.e. 0.25, 1.0, 2.0, 3.0, ...). "
            "Further results with other dimensions may also be "
            "included."
        ),
    )
    wind_shear_exponent: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final power law wind shear exponent estimates at the "
            "turbine location(s). The dimension of the first standard "
            "result dataset should be 'turbine_id'. Further results "
            "with other dimensions may also be included."
        ),
    )
    temperature: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term temperature estimates at the turbine "
            "location(s) at hub height in degree C. The dimension of "
            "the first standard result dataset should be 'turbine_id'. "
            "Further results with other dimensions may also be "
            "included."
        ),
    )
    air_density: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term air density estimates at the turbine "
            "location(s) at hub height in kilogram per cubic metre "
            "(kg m-3). The dimension of the first standard result "
            "dataset should be 'turbine_id'. Further results with "
            "other dimensions may also be included."
        ),
    )
    displacement_height: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Estimated effective displacement of the boundary layer at "
            "the turbine location(s) due to vegetation (forestry) in "
            "metre. The displacement height is measured as positive "
            "upwards from the ground level. This field is optional as "
            "it is only relevant at forested sites. The dimension of "
            "the first standard result dataset should be 'turbine_id'. "
            "Further results with other dimensions, such as "
            "displacement height binned by wind direction, may also be "
            "included."
        ),
    )


class TurbineWindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the turbine locations."""

    wind_resource_assessment_id_reference: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "The ID of the wind resource assessment on which the "
            "turbine wind resource assessment is based. This must "
            "refer to an ID of a wind resource assessment included at "
            "the top level of the EYA DEF. The schema requires that a "
            "turbine wind resource assessment is based on only one "
            "wind resource assessment."
        ),
        examples=["WRA01", "BfWF_WRA_1"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the turbine wind resource "
            "assessment, which should not be empty if the field is "
            "included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the turbine wind resource "
            "assessment, which should not be empty if the field is "
            "included."
        ),
    )
    weighting: Optional[TurbineWindResourceWeighting] = pdt.Field(
        default=None,
        description=(
            "Optional specification of the weighting applied to "
            "estimate the wind resource at the turbine location(s),"
            "relevant for example when predictions from different "
            "measurement stations were weighted individually at each "
            "turbine based on representativeness."
        ),
    )
    results: TurbineWindResourceResults = pdt.Field(
        default=...,
        description=(
            "Results of the wind resource assessment at the turbine location(s)."
        ),
    )
    wind_uncertainty_assessment: WindUncertaintyAssessment = pdt.Field(
        default=...,
        description=(
            "Wind related uncertainty assessment categories including results."
        ),
    )
