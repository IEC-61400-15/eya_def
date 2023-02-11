"""Pydantic data models for results.

"""

from typing import TypeAlias

import pydantic as pdt

from eya_def_tools.data_models import enums, fields
from eya_def_tools.data_models.base_models import EyaDefBaseModel

ResultCoordinate: TypeAlias = tuple[float | int | str, ...]


ResultValue: TypeAlias = float


ResultValueAtCoordinate: TypeAlias = tuple[ResultCoordinate, ResultValue]


class ResultStatistic(EyaDefBaseModel):
    """Result values for one specific statistic type."""

    description: str | None = fields.description_field
    comments: str | None = fields.comments_field
    statistic_type: enums.StatisticType = pdt.Field(
        ...,
        description="Type of statistic in the results component.",
        examples=[enums.StatisticType.MEDIAN, enums.StatisticType.P90],
    )
    values: ResultValue | list[ResultValueAtCoordinate] = pdt.Field(
        ...,
        description="Result as a single number or values at coordinates.",
    )


class Result(EyaDefBaseModel):
    """Set of results for an element of an energy assessment."""

    label: str | None = pdt.Field(
        ...,
        description="Label of the results.",
        examples=["Seasonal distribution of net energy."],
    )
    description: str | None = fields.description_field
    comments: str | None = fields.comments_field
    assessment_period: enums.AssessmentPeriod = pdt.Field(
        enums.AssessmentPeriod.LIFETIME,
        description=(
            "Period of or in time that has been assessed and for which "
            "the results are applicable."
        ),
        examples=[
            enums.AssessmentPeriod.LIFETIME,
            enums.AssessmentPeriod.ANY_ONE_YEAR,
        ],
    )
    dimensions: tuple[enums.ResultsDimension, ...] | None = pdt.Field(
        None,
        description=(
            "Dimensions along which the results are binned (all result values "
            "in the same results object must have the same dimensions)."
        ),
        examples=[
            (
                enums.ResultsDimension.TURBINE,
                enums.ResultsDimension.YEAR,
            ),
            (enums.ResultsDimension.MEASUREMENT, enums.ResultsDimension.HEIGHT),
        ],
    )
    statistics: list[ResultStatistic] = pdt.Field(
        ...,
        description=(
            "List of result statistic objects that each include result "
            "values for a specific statistic type."
        ),
    )
