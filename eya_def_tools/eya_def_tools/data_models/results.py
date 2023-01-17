"""Pydantic data models for results.

"""

from __future__ import annotations

from typing import TypeAlias

import pydantic as pdt

from eya_def_tools.data_models import enums, fields
from eya_def_tools.data_models.base_models import EyaDefBaseModel

ResultCoordinate: TypeAlias = tuple[float | int | str, ...]


ResultValue: TypeAlias = float


ResultValueAtCoordinate: TypeAlias = tuple[ResultCoordinate, ResultValue]


class ResultsComponent(EyaDefBaseModel):
    """Component of a set of results."""

    description: str | None = fields.description_field
    comments: str | None = fields.comments_field
    component_type: enums.StatisticType = pdt.Field(
        ...,
        description="Type of statistic in the results component.",
        examples=[enums.StatisticType.MEDIAN, enums.StatisticType.P90],
    )
    unit: enums.MeasurementUnit = pdt.Field(
        ...,
        description="Unit in which the result values are measured.",
        examples=[
            enums.MeasurementUnit.METRE_PER_SECOND,
            enums.MeasurementUnit.MEGAWATT_HOUR,
        ],
    )
    values: ResultValue | list[ResultValueAtCoordinate] = pdt.Field(
        ...,
        description="Result as a single number or values at coordinates.",
    )


class Results(EyaDefBaseModel):
    """Set of results for an element of an energy assessment."""

    label: str | None = pdt.Field(
        ...,
        description="Label of the results.",
        examples=["Seasonal distribution of net energy."],
    )
    description: str | None = fields.description_field
    comments: str | None = fields.comments_field
    applicability_type: enums.ResultsApplicabilityType = pdt.Field(
        enums.ResultsApplicabilityType.LIFETIME,
        description="Applicability type of the results.",
        examples=[
            enums.ResultsApplicabilityType.LIFETIME,
            enums.ResultsApplicabilityType.ANY_ONE_YEAR,
        ],
    )
    results_dimensions: tuple[enums.ResultsDimension, ...] | None = pdt.Field(
        None,
        description="Dimensions along which the results are binned.",
        examples=[
            (
                enums.ResultsDimension.TURBINE,
                enums.ResultsDimension.YEAR,
            ),
            (enums.ResultsDimension.MEASUREMENT, enums.ResultsDimension.HEIGHT),
        ],
    )
    result_components: list[ResultsComponent] = pdt.Field(
        ...,
        description="List of result components.",
    )
