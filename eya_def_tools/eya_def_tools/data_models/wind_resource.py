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
from eya_def_tools.data_models.process_description import AssessmentProcessDescription
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.wind_uncertainty import WindUncertaintyAssessment


class WindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at measurement locations."""

    wind_speed: list[Result] = pdt.Field(
        default=...,
        description=(
            "Final long-term wind speed estimates at the measurement location(s)"
            "in metre per second."
        ),
    )
    probability: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term probability distribution estimates at the measurement "
            "location(s), such as wind speed probability distributions or joint wind "
            "speed and direction frequency distributions, as dimensionless values."
        ),
    )
    turbulence_intensity: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term turbulence intensity estimates at the measurement "
            "location(s) as dimensionless values."
        ),
    )
    wind_shear_exponent: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term power law wind shear exponent estimates at the "
            "measurement location(s)."
        ),
    )
    temperature: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term temperature estimates at the measurement location(s) "
            "in degree C."
        ),
    )
    air_density: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term air density estimates at the measurement location(s) "
            "in kilogram per cubic metre."
        ),
    )


class WindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the measurement location(s)."""

    wind_resource_assessment_id: str = pdt.Field(
        default=...,
        description=(
            "Unique ID of the wind resource assessment within the EYA DEF document."
        ),
        examples=["WRA01", "BfWF_WRA_1", "A"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the wind resource assessment.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the wind resource assessment.",
    )
    results: WindResourceResults = pdt.Field(
        default=...,
        description=(
            "Results of the wind resource assessment at the measurement location(s)."
        ),
    )


class TurbineWindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at turbine locations."""

    wind_speed: list[Result] = pdt.Field(
        default=...,
        description=(
            "Final long-term wind speed estimates at the turbine location(s) "
            "in metre per second."
        ),
    )
    probability: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term probability distribution estimates at the turbine "
            "location(s), such as wind speed probability distributions or joint wind "
            "speed and direction frequency distributions, as dimensionless values."
        ),
    )
    turbulence_intensity: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term turbulence intensity estimates at the turbine "
            "location(s) as dimensionless values."
        ),
    )
    wind_shear_exponent: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term power law wind shear exponent estimates at the "
            "turbine location(s)."
        ),
    )
    temperature: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term temperature estimates at the turbine location(s) "
            "in degree C."
        ),
    )
    air_density: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Final long-term air density estimates at the turbine location(s) "
            "in kilogram per cubic metre."
        ),
    )


class TurbineWindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the turbine locations."""

    wind_resource_assessment_id_reference: str = pdt.Field(
        default=...,
        description=(
            "The ID of the wind resource assessment on which the turbine wind resource "
            "assessment is based. This must refer to an ID of a wind resource "
            "assessment included at the top level of the EYA DEF. The schema requires "
            "that a turbine wind resource assessment is based on only one wind "
            "resource assessment."
        ),
        examples=["WRA01", "BfWF_WRA_1", "A"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the turbine wind resource assessment.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the turbine wind resource assessment.",
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
