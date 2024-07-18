"""Data models relating to energy assessments.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.plant_performance import PlantPerformanceAssessment
from eya_def_tools.data_models.wind_uncertainty import WindUncertaintyAssessment


class GrossEnergyAssessmentResults(EyaDefBaseModel):
    """Gross energy assessment results."""

    annual_energy_production: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Gross annual energy production (AEP) estimates in "
            "gigawatt hour per annum (GW h year-1). The first standard "
            "dataset should have no binning dimension (i.e. correspond "
            "to the overall value for the wind farm(s) under "
            "assessment). The dimension of the second standard result "
            "dataset should be 'turbine_id'. Only the P50 (median) "
            "statistics are required. Further results with other "
            "dimensions may be included optionally."
        ),
    )
    energy_production: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional gross energy production estimates over a "
            "specific period of time in gigawatt hour (GW h). This "
            "field should be used for energy production estimates that "
            "are not annualised. For all annual energy production "
            "(AEP) estimates, the field 'annual_energy_production' "
            "should be used. The time period that values correspond to "
            "should be made clear (e.g. in description and/or comments "
            "fields) if not obvious from the binning dimension(s)."
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
    results: GrossEnergyAssessmentResults = pdt.Field(
        default=...,
        description=(
            "Gross energy yield assessment (EYA) predictions, covering "
            "the central (P50) gross annual energy production (AEP) "
            "estimate at the wind farm and turbine levels."
        ),
    )


class NetEnergyAssessmentResults(EyaDefBaseModel):
    """Net energy assessment results."""

    annual_energy_production: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Net annual energy production (AEP) estimates in gigawatt "
            "hour per annum (GW h year-1). The first standard dataset "
            "should have no binning dimension (i.e. correspond to the "
            "overall value for the wind farm(s) under assessment) and "
            "should include as a minimum the P50 (median) value, the "
            "standard deviation value and the P90 value for the full "
            "assessment period, for any one year during the assessment "
            "period, for the first ten years and for any one year "
            "during the first ten years. The dimension of the second "
            "standard result dataset should be 'turbine_id' and should "
            "as a minimum include the assessment period P50 (median) "
            "value for each individual turbine. Further results with "
            "other dimensions may be included optionally."
        ),
    )
    energy_production: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Net energy production estimates over a specific period of "
            "time in gigawatt hour (GW h). This field should be used "
            "for energy production estimates that are not annualised. "
            "For all net annual energy production (AEP) estimates, the "
            "field 'annual_energy_production' should be used. The time "
            "period that values correspond to should be made clear "
            "(e.g. in description and/or comments fields) if not "
            "obvious from the binning dimension(s). The dimensions of "
            "the first standard result dataset should be 'month' and "
            "'hour' (in that order), providing the 12 x 24 matrix of "
            "seasonal and diurnal variation in overall energy "
            "production. If time variable elements are considered in "
            "the assessment, a second standard dataset resolving the "
            "time variability should be included. If statistics vary "
            "on an annual basis, it should have the dimension 'year'."
            "If statistics vary on a monthly basis (e.g. when "
            "considering expected commissioning and availability of "
            "turbines for each month), it should have the dimensions "
            "'year' and 'month' (in that order). Further results with "
            "other dimensions may be included optionally."
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
    results: NetEnergyAssessmentResults = pdt.Field(
        default=...,
        description=(
            "Net energy yield assessment (EYA) predictions, including "
            "central (P50) estimates, overall uncertainty standard "
            "deviation values, results at various confidence levels, "
            "and production profiles describing for example seasonal "
            "and diurnal variations."
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
