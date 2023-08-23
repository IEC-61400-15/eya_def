"""Data models for results.

"""

from typing import Optional, TypeAlias

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    AssessmentPeriod,
    ResultsDimension,
    StatisticType,
)

ResultValue: TypeAlias = float
ResultCoordinates: TypeAlias = list[float | int | str]


class ResultStatistic(EyaDefBaseModel):
    """Result values for one specific statistic type."""

    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the result statistic.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the result statistic.",
    )
    statistic_type: StatisticType = pdt.Field(
        default=...,
        description="Type of statistic in the results component.",
    )
    values: ResultValue | list[tuple[ResultCoordinates, ResultValue]] = pdt.Field(
        default=...,
        description="Result as a single number or values at coordinates.",
    )


class Result(EyaDefBaseModel):
    """Collection of results a quantity along specific dimensions."""

    label: Optional[str] = pdt.Field(
        default=None,
        description="Label of the results.",
        examples=["Seasonal distribution of net energy."],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the result.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the result.",
    )
    assessment_period: Optional[AssessmentPeriod] = pdt.Field(
        default=None,
        description=(
            "Period of or in time that has been assessed and for which "
            "the results are applicable."
        ),
    )
    dimensions: Optional[list[ResultsDimension]] = pdt.Field(
        default=None,
        description=(
            "Dimensions along which the results are binned (all result values "
            "in the same results object must have the same dimensions)."
        ),
        examples=[
            [ResultsDimension.TURBINE, ResultsDimension.YEAR],
            [ResultsDimension.MEASUREMENT, ResultsDimension.HEIGHT],
        ],
    )
    statistics: list[ResultStatistic] = pdt.Field(
        default=...,
        description=(
            "List of result statistic objects that each include result "
            "values for a specific statistic type."
        ),
    )
