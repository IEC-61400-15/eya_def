"""Pydantic data models relating to wind resource assessments.

Wind resource assessment is commonly abbreviated as WRA.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.uncertainty_assessment import UncertaintyAssessment


# TODO - temporary placeholder to be extended
class ReferenceWindFarmAssessment(EyaDefBaseModel):
    """Details of an assessment of reference wind farm data."""

    raw_data_availability: list[Result] = pdt.Field(
        ...,
        description="Raw data availability results.",
    )
    filtered_data_availability: list[Result] = pdt.Field(
        ...,
        description="Filtered (post quality-control) data availability results.",
    )
    assessment_description: str = pdt.Field(
        ...,
        description="Description of the assessment process undertaken.",
    )


# TODO - temporary placeholder to be extended
class WindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the measurement locations."""

    # measurement_station_basis: MeasurementStationBasis
    # reference_wind_farm_basis: ReferenceWindFarmBasis
    # data_filtering
    # sensor_data_availability_results
    # sensor_results
    # gap_filling
    # primary_data_availability_results
    # primary_measurement_period_results
    # long_term_correction
    # long_term_results
    # vertical_extrapolation
    # hub_height_results
    results: list[Result] = pdt.Field(
        ..., description="Assessment results at the measurement location(s)."
    )
    uncertainty_assessment: UncertaintyAssessment = pdt.Field(
        ..., description="Measurement wind resource uncertainty assessment."
    )


class WindResourceAssessmentBasis(EyaDefBaseModel):
    """Measurement wind resource assessment basis in a scenario."""

    # TODO - placeholder to be implemented
    pass
