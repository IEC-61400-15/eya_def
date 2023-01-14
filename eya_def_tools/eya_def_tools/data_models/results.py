"""EYA DEF pydantic data model for results.

"""

from typing import Literal

import pydantic as pdt

from eya_def_tools.data_models import enums, fields, types


class ResultsComponent(pdt.BaseModel):
    """Component of a set of results."""

    component_type: enums.StatisticType = pdt.Field(
        ...,
        description="Type of statistic in the results component.",
    )
    description: str | None = fields.description_field
    comments: str | None = fields.comments_field
    values: float | types.NestedAnnotatedFloatDict = pdt.Field(
        ...,
        description="Result value(s) as simple float or labeled map.",
        examples=[123.4, {"WTG01": 123.4, "WTG02": 143.2}],
    )


class Results(pdt.BaseModel):
    """Single set of results for an element of an energy assessment."""

    label: str = pdt.Field(
        ..., description="Label of the results.", examples=["10-year P50"]
    )
    description: str | None = fields.description_field
    comments: str | None = fields.comments_field
    unit: str = pdt.Field(
        ..., description="Unit of result values (TO REPLACE BY LITERAL)."
    )
    applicability_type: enums.ResultsApplicabilityType = pdt.Field(
        ..., description="Applicability type of energy assessment results."
    )
    results_dimensions: list[
        Literal["none", "location", "hub_height", "year", "month", "month_of_year"]
    ] = pdt.Field(..., description="Type of energy assessment results.")
    result_components: list[ResultsComponent] = pdt.Field(
        ..., description="List of result components."
    )
