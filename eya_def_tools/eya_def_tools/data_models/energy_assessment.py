"""Pydantic data models relating to energy assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models import base_models, result
from eya_def_tools.data_models.assessment_process_description import (
    AssessmentProcessDescription,
)
from eya_def_tools.data_models.plant_performance import PlantPerformanceCategory
from eya_def_tools.data_models.uncertainty import UncertaintyAssessment


class EnergyAssessment(base_models.EyaDefBaseModel):
    """Energy assessment details and results."""

    gross_eya_process: AssessmentProcessDescription = pdt.Field(
        ...,
        description=(
            "Specification of the model used to calculate the gross EYA estimates."
        ),
    )
    gross_eya_results: list[result.Result] = pdt.Field(
        ...,
        description="Gross energy production predictions in GWh.",
    )
    plant_performance_loss_categories: list[PlantPerformanceCategory] = pdt.Field(
        ...,
        description="Plant performance loss assessment categories including results.",
    )
    net_energy_uncertainty_assessment: UncertaintyAssessment | None = pdt.Field(
        None,  # TODO remove optional
        description=(
            "Net energy production uncertainty assessment, including the "
            "conversion of the wind resource assessment uncertainty results "
            "from wind speed to energy quantities and results for all main "
            "energy uncertainty categories."
        ),
    )
    net_eya_results: list[result.Result] = pdt.Field(
        ...,
        description=(
            "Net energy production predictions in GWh, including overall "
            "uncertainties and results at different confidence levels."
        ),
    )
