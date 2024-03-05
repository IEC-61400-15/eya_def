"""Data models relating to energy assessments.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.plant_performance import PlantPerformanceAssessment


class EnergyAssessmentResults(EyaDefBaseModel):
    """Energy assessment results."""

    annual_energy_production: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Annual energy production (AEP) estimates at the turbine "
            "location(s) in gigawatt hour (GW h). The dimension of the "
            "first standard result dataset should be 'wind_farm_id'. "
            "The dimension of the second standard result dataset "
            "should be 'turbine_id'. Further results with other "
            "dimensions may be included optionally."
        ),
    )


class GrossEnergyAssessment(EyaDefBaseModel):
    """Gross energy assessment details and results."""

    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the gross energy assessment, "
            "which should not be empty if the field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the gross energy assessment, which "
            "should not be empty if the field is included."
        ),
    )
    results: EnergyAssessmentResults = pdt.Field(
        default=...,
        description="Gross EYA estimates.",
    )


class NetEnergyAssessment(EyaDefBaseModel):
    """Net energy assessment details and results."""

    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the net energy assessment, which "
            "should not be empty if the field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the net energy assessment, which "
            "should not be empty if the field is included."
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
