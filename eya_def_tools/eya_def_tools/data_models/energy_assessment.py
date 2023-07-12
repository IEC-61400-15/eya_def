"""Pydantic data models relating to energy assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.energy_uncertainty import EnergyUncertaintyCategory
from eya_def_tools.data_models.plant_performance import PlantPerformanceCategory
from eya_def_tools.data_models.process_description import AssessmentProcessDescription
from eya_def_tools.data_models.result import Result


class EnergyAssessment(EyaDefBaseModel):
    """Energy assessment details and results."""

    gross_eya_process: AssessmentProcessDescription = pdt.Field(
        ...,
        description=(
            "Specification of the model used to calculate the gross EYA estimates."
        ),
    )
    gross_eya_results: list[Result] = pdt.Field(
        ...,
        description="Gross energy production predictions in GWh.",
    )
    plant_performance_loss_categories: list[PlantPerformanceCategory] = pdt.Field(
        ...,
        description="Plant performance loss assessment categories including results.",
    )
    energy_uncertainty_categories: list[EnergyUncertaintyCategory] = pdt.Field(
        ...,
        description=(
            "Energy related uncertainty assessment categories including results."
        ),
    )
    net_eya_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Net energy production predictions in GWh, including overall "
            "uncertainties and results at different confidence levels."
        ),
    )
