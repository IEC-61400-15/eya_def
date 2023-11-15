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
from eya_def_tools.data_models.process_description import AssessmentProcessDescription
from eya_def_tools.data_models.wind_uncertainty import WindUncertaintyAssessment


class WindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at measurement locations."""

    wind_speed: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Final long-term wind speed estimate(s) at the measurement "
            "location(s) in metre per second. The dimensions of the "
            "first standard result dataset should be 'measurement_id' "
            "and 'height' (in that order). Further results with other "
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
            "the dimensions 'measurement_id', 'height', 'wind_speed' "
            "and 'wind_from_direction' (in that order). The wind speed "
            "coordinates should be 1.0 metre per second bins centered "
            "on whole numbers, with the first bin half the width (i.e. "
            "0.25, 1.0, 2.0, 3.0, ...). The wind direction coordinates "
            "should be twelve 30.0 degree bins, with the the first bin "
            "centered at 0.0. Further results with other dimensions "
            "may be included optionally."
        ),
    )
    turbulence_intensity: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term turbulence intensity estimates at the "
            "measurement location(s), as dimensionless values. This "
            "field is optional since some measurement devices may "
            "lack meaningful turbulence measurements, but it should "
            "always be included when relevant turbulence data are "
            "available. The first standard result dataset should "
            "comprise the ambient turbulence intensity as a function "
            "of wind speed, with the dimensions 'measurement_id', "
            "'height' and 'wind_speed' (in that order). The wind speed "
            "coordinates should be 1.0 metre per second bins centered "
            "on whole numbers, with the first bin half the width (i.e. "
            "0.25, 1.0, 2.0, 3.0, ...). Further results with other "
            "dimensions may also be included."
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
            "available. The dimension of the first standard result "
            "dataset should be 'measurement_id' only. Further results "
            "with other dimensions may also be included."
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
            "'measurement_id' and 'height' (in that order). Further "
            "results with other dimensions may also be included."
        ),
    )
    air_density: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term air density estimates at the measurement "
            "location(s) in kilogram per cubic metre. This field is "
            "optional since some wind measurement stations may lack "
            "measurements required to derive air density estimates, "
            "but it should always be included when relevant air "
            "density data are available. The dimensions of the first "
            "standard result dataset should be 'measurement_id' and "
            "'height' (in that order). Further results with other "
            "dimensions may also be included."
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


class TurbineWindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at turbine locations."""

    wind_speed: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Final long-term wind speed estimates at the turbine "
            "location(s) in metre per second."
        ),
    )
    probability: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term probability distribution estimates at the "
            "turbine location(s), such as wind speed probability "
            "distributions or joint wind speed and direction frequency "
            "distributions, as dimensionless values."
        ),
    )
    turbulence_intensity: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term turbulence intensity estimates at the "
            "turbine location(s) as dimensionless values."
        ),
    )
    wind_shear_exponent: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term power law wind shear exponent estimates "
            "at the turbine location(s)."
        ),
    )
    temperature: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term temperature estimates at the turbine "
            "location(s) in degree C."
        ),
    )
    air_density: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Final long-term air density estimates at the turbine "
            "location(s) in kilogram per cubic metre."
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
        examples=["WRA01", "BfWF_WRA_1", "A"],
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
    wind_spatial_modelling_processes: list[AssessmentProcessDescription] = pdt.Field(
        default=...,
        description="Wind spatial modelling processes used in the assessment.",
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
    # TODO consider including measurement station weighting
