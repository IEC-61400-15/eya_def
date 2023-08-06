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

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.process_description import AssessmentProcessDescription
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.wind_uncertainty import WindUncertaintyAssessment


class WindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at measurement locations."""

    wind_speed: list[Result] = pdt.Field(
        ...,
        description=(
            "Final long-term wind speed estimates at the measurement location(s)"
            "in metre per second."
        ),
    )
    probability: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term probability distribution estimates at the measurement "
            "location(s), such as wind speed probability distributions or joint wind "
            "speed and direction frequency distributions, as dimensionless values."
        ),
    )
    turbulence_intensity: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term turbulence intensity estimates at the measurement "
            "location(s) as dimensionless values."
        ),
    )
    wind_shear_exponent: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term power law wind shear exponent estimates at the "
            "measurement location(s)."
        ),
    )
    temperature: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term temperature estimates at the measurement location(s) "
            "in degree C."
        ),
    )
    air_density: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term air density estimates at the measurement location(s) "
            "in kilogram per cubic metre."
        ),
    )


class WindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the measurement location(s)."""

    wind_resource_assessment_id: str = pdt.Field(
        ...,
        description=(
            "Unique ID of the wind resource assessment within the EYA DEF document."
        ),
        examples=["WRA01", "BfWF_WRA_1", "A"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    results: WindResourceResults = pdt.Field(
        ...,
        description=(
            "Results of the wind resource assessment at the measurement location(s)."
        ),
    )


class TurbineWindResourceResults(EyaDefBaseModel):
    """Wind resource assessment results at turbine locations."""

    wind_speed: list[Result] = pdt.Field(
        ...,
        description=(
            "Final long-term wind speed estimates at the turbine location(s) "
            "in metre per second."
        ),
    )
    probability: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term probability distribution estimates at the turbine "
            "location(s), such as wind speed probability distributions or joint wind "
            "speed and direction frequency distributions, as dimensionless values."
        ),
    )
    turbulence_intensity: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term turbulence intensity estimates at the turbine "
            "location(s) as dimensionless values."
        ),
    )
    wind_shear_exponent: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term power law wind shear exponent estimates at the "
            "turbine location(s)."
        ),
    )
    temperature: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term temperature estimates at the turbine location(s) "
            "in degree C."
        ),
    )
    air_density: list[Result] | None = pdt.Field(
        None,
        description=(
            "Final long-term air density estimates at the turbine location(s) "
            "in kilogram per cubic metre."
        ),
    )


class TurbineWindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the turbine locations."""

    wind_resource_assessment_id_reference: str = pdt.Field(
        ...,
        description=(
            "The ID of the wind resource assessment on which the turbine wind resource "
            "assessment is based. This must refer to an ID of a wind resource "
            "assessment included at the top level of the EYA DEF. The schema requires "
            "that a turbine wind resource assessment is based on only one wind "
            "resource assessment."
        ),
        examples=["WRA01", "BfWF_WRA_1", "A"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    wind_spatial_modelling_processes: list[AssessmentProcessDescription] = pdt.Field(
        ...,
        description="Wind spatial modelling processes used in the assessment.",
    )
    results: TurbineWindResourceResults = pdt.Field(
        ...,
        description=(
            "Results of the wind resource assessment at the turbine location(s)."
        ),
    )
    wind_uncertainty_assessment: WindUncertaintyAssessment = pdt.Field(
        ...,
        description=(
            "Wind related uncertainty assessment categories including results."
        ),
    )
    # TODO consider including measurement station weighting
