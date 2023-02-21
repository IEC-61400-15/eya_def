"""Pydantic data models relating to turbine wind resource assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.calculation_model_specification import (
    CalculationModelSpecification,
)
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.uncertainty_assessment import UncertaintyAssessment


# TODO this needs to be completed with more fields for relevant details
class TurbineWindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the turbine locations."""

    turbine_wind_resource_results: list[Result] = pdt.Field(
        ..., description="Assessment results at the turbine location(s)."
    )
    wind_spatial_models: list[CalculationModelSpecification] = pdt.Field(
        ..., description="Wind spatial models used in the assessment."
    )
    # TODO should not be optional
    uncertainty_assessment: UncertaintyAssessment | None = pdt.Field(
        None, description="Turbine wind resource uncertainty assessment."
    )
