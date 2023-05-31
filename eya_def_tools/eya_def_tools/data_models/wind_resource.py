"""Pydantic data models relating to wind resource assessments (WRAs).

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
from eya_def_tools.data_models.enums import WindResourceAssessmentStepType
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.process_description import AssessmentProcessDescription
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.uncertainty import UncertaintyAssessment


class WindResourceAssessmentStep(EyaDefBaseModel):
    """A step in a wind resource assessment at measurement location(s).

    A step can be a data processing procedure (e.g. filtering for
    spurious data) or a model extrapolation procedure (e.g. temporal
    extrapolation using long-term reference data).
    """

    # TODO - this is an initial placeholder that needs to be developed
    #        it will not be included in the fist version of the schema

    label: WindResourceAssessmentStepType = pdt.Field(
        ...,
        description="Label of the plant performance loss subcategory.",
    )
    description: str | None = description_field
    comments: str | None = comments_field
    results: list[Result] = pdt.Field(
        ...,
        description="Results of the wind resource assessment step.",
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
    wind_speed_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Final long-term wind speed estimates from the wind resource "
            "assessment at the measurement location(s)."
        ),
    )

    # TODO - Placeholder for assessment steps to be considered at a later stage
    # steps: list[WindResourceAssessmentStep]


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
        ..., description="Wind spatial modelling processes used in the assessment."
    )
    wind_speed_results: list[Result] = pdt.Field(
        ...,
        description="Final long-term wind speed estimates at the turbine location(s).",
    )
    wind_resource_uncertainty_assessment: UncertaintyAssessment | None = pdt.Field(
        None,
        description="Turbine wind resource uncertainty assessment.",
    )  # TODO should not be optional

    # TODO consider including measurement station weighting
