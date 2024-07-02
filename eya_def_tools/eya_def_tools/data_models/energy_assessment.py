"""Data models relating to energy assessments.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.plant_performance import PlantPerformanceAssessment
from eya_def_tools.data_models.wind_uncertainty import WindUncertaintyAssessment


class EnergyAssessmentResults(EyaDefBaseModel):
    """Energy assessment results."""

    annual_energy_production: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Annual energy production (AEP) estimates at the turbine "
            "location(s) in gigawatt hour per annum (GW h year-1). The "
            "dimension of the first standard result dataset should be "
            "'wind_farm_id'. The dimension of the second standard "
            "result dataset should be 'turbine_id'. Further results "
            "with other dimensions may be included optionally."
        ),
    )
    energy_production: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Energy production estimates at the turbine location(s) "
            "over a specific period of time in gigawatt hour (GW h). "
            "This field should be used for energy production estimates "
            "that are not annualised. For all annual energy production "
            "(AEP) estimate, the field 'annual_energy_production' "
            "should be used."
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
        description=(
            "Gross energy yield assessment (EYA) predictions, covering "
            "the central (P50) gross annual energy production (AEP) "
            "estimate at the wind farm and turbine levels."
        ),
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
            "Net energy yield assessment (EYA) predictions, including "
            "central (P50) estimates, overall uncertainty standard "
            "deviation values and results at various confidence levels."
        ),
    )


class EnergyAssessment(EyaDefBaseModel):
    """Energy assessment details and results."""

    gross_energy_assessment: GrossEnergyAssessment = pdt.Field(
        default=...,
        description="Details and results for the assessment of gross energy yield.",
    )
    wind_uncertainty_assessment: WindUncertaintyAssessment = pdt.Field(
        default=...,
        description="Details of the wind related uncertainty assessment.",
    )
    plant_performance_assessment: PlantPerformanceAssessment = pdt.Field(
        default=...,
        description="Plant performance loss assessment categories including results.",
    )
    net_energy_assessment: NetEnergyAssessment = pdt.Field(
        default=...,
        description="Details and results for the assessment of net energy yield.",
    )
