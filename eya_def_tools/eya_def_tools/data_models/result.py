"""Data models for results.

"""

from typing import TypeAlias

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    AssessmentPeriod,
    ResultsDimension,
    StatisticType,
)
from eya_def_tools.data_models.generic_fields import comments_field, description_field

ResultCoordinate: TypeAlias = tuple[float | int | str, ...]


ResultValue: TypeAlias = float


ResultValueAtCoordinate: TypeAlias = tuple[ResultCoordinate, ResultValue]


class ResultStatistic(EyaDefBaseModel):
    """Result values for one specific statistic type."""

    description: str | None = description_field
    comments: str | None = comments_field
    statistic_type: StatisticType = pdt.Field(
        ...,
        description="Type of statistic in the results component.",
    )
    values: ResultValue | list[ResultValueAtCoordinate] = pdt.Field(
        ...,
        description="Result as a single number or values at coordinates.",
    )


class Result(EyaDefBaseModel):
    """Collection of results a quantity along specific dimensions."""

    label: str | None = pdt.Field(
        None,
        description="Label of the results.",
        examples=["Seasonal distribution of net energy."],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    assessment_period: AssessmentPeriod | None = pdt.Field(
        None,
        description=(
            "Period of or in time that has been assessed and for which "
            "the results are applicable."
        ),
    )
    dimensions: tuple[ResultsDimension, ...] | None = pdt.Field(
        None,
        description=(
            "Dimensions along which the results are binned (all result values "
            "in the same results object must have the same dimensions)."
        ),
        examples=[
            (ResultsDimension.TURBINE, ResultsDimension.YEAR),
            (ResultsDimension.MEASUREMENT, ResultsDimension.HEIGHT),
        ],
    )
    statistics: list[ResultStatistic] = pdt.Field(
        ...,
        description=(
            "List of result statistic objects that each include result "
            "values for a specific statistic type."
        ),
    )
