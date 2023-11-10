"""Data models relating to energy assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.plant_performance import PlantPerformanceAssessment
from eya_def_tools.data_models.process_description import AssessmentProcessDescription


class EnergyAssessmentResults(EyaDefBaseModel):
    """Energy assessment results."""

    annual_energy_production: list[Dataset] = pdt.Field(
        default=...,
        min_items=1,
        description="Annual energy production estimates in GWh.",
    )


class GrossEnergyAssessment(EyaDefBaseModel):
    """Gross energy assessment details and results."""

    process_description: AssessmentProcessDescription = pdt.Field(
        default=...,
        description=(
            "Specification of the process used to calculate the gross EYA estimates."
        ),
    )
    results: EnergyAssessmentResults = pdt.Field(
        default=...,
        description="Gross EYA estimates.",
    )


class NetEnergyAssessment(EyaDefBaseModel):
    """Net energy assessment details and results."""

    process_description: AssessmentProcessDescription = pdt.Field(
        default=...,
        description=(
            "Specification of the process used to calculate the net EYA estimates."
        ),
    )
    results: EnergyAssessmentResults = pdt.Field(
        default=...,
        description=(
            "Net EYA predictions, including central estimates, overall "
            "uncertainties and results at different confidence levels."
        ),
    )


class EnergyAssessment(EyaDefBaseModel):
    """Energy assessment details and results."""

    gross_energy_assessment: GrossEnergyAssessment = pdt.Field(
        default=...,
        description="Details and results for the assessment of gross energy yield.",
    )
    plant_performance_assessment: PlantPerformanceAssessment = pdt.Field(
        default=...,
        description="Plant performance loss assessment categories including results.",
    )
    net_energy_assessment: NetEnergyAssessment = pdt.Field(
        default=...,
        description="Details and results for the assessment of net energy yield.",
    )
