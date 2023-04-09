"""Pydantic data models relating to wind resource assessments.

Wind resource assessment is commonly abbreviated as WRA.

"""

import pydantic as pdt

from eya_def_tools.data_models import assessment_process_description as eya_prcs_desc
from eya_def_tools.data_models import (
    assessment_results,
    base_models,
    measurement_station,
    reference_wind_farm,
    uncertainty,
)


# TODO - temporary placeholder to be extended
class ReferenceWindFarmAssessment(base_models.EyaDefBaseModel):
    """Details of an assessment of reference wind farm data."""

    raw_data_availability: list[assessment_results.Result] = pdt.Field(
        ...,
        description="Raw data availability results.",
    )
    filtered_data_availability: list[assessment_results.Result] = pdt.Field(
        ...,
        description="Filtered (post quality-control) data availability results.",
    )
    assessment_description: str = pdt.Field(
        ...,
        description="Description of the assessment process undertaken.",
    )


# TODO - temporary placeholder to be extended
class WindResourceAssessment(base_models.EyaDefBaseModel):
    """Wind resource assessment at the measurement locations."""

    measurement_station_reference: (
        measurement_station.MeasurementStationReference | None
    ) = pdt.Field(
        None, description="Assessment results at the measurement location(s)."
    )
    reference_wind_farm_reference: (
        reference_wind_farm.ReferenceWindFarmReference | None
    ) = pdt.Field(
        None, description="Assessment results at the measurement location(s)."
    )
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
    subcategory_results: list[assessment_results.Result] = pdt.Field(
        ..., description="Assessment results at the measurement location(s)."
    )
    uncertainty_assessment: uncertainty.UncertaintyAssessment = pdt.Field(
        ..., description="Measurement wind resource uncertainty assessment."
    )


class WindResourceAssessmentReference(base_models.EyaDefBaseModel):
    """Measurement wind resource assessment basis in a scenario."""

    # TODO - placeholder to be implemented
    pass


# TODO this needs to be completed with more fields for relevant details
class TurbineWindResourceAssessment(base_models.EyaDefBaseModel):
    """Wind resource assessment at the turbine locations."""

    turbine_wind_resource_results: list[assessment_results.Result] = pdt.Field(
        ..., description="Assessment results at the turbine location(s)."
    )
    wind_spatial_modelling_processes: list[
        eya_prcs_desc.AssessmentProcessDescription
    ] = pdt.Field(
        ..., description="Wind spatial modelling processes used in the assessment."
    )
    # TODO should not be optional
    uncertainty_assessment: uncertainty.UncertaintyAssessment | None = pdt.Field(
        None, description="Turbine wind resource uncertainty assessment."
    )
