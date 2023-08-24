"""Data models for wind farm and turbine configurations.

"""

import datetime as dt
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import WindFarmRelevance
from eya_def_tools.data_models.spatial import Location


class OperationalRestriction(EyaDefBaseModel):
    """Specifications of a restriction that limits power output.

    In the current draft of the schema, 'label', 'description' and
    'comments' fields are available to describe the restriction with
    free text. This is intended to be expanded into a more comprehensive
    data model.
    """

    label: str = pdt.Field(
        default=...,
        description="Short label to indicate the type of operational restriction.",
        examples=["WSM curtailment", "MEC curtailment"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the operational restriction.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the operational restriction.",
    )


class TurbineConfiguration(EyaDefBaseModel):
    """Specification of all details for a turbine configuration."""

    id: str = pdt.Field(
        default=...,
        description="Unique identifier of the turbine.",
        examples=["b55caeac-f152-4b13-8217-3fddeab792cf", "T1-scen1"],
    )
    label: Optional[str] = pdt.Field(
        default=None,
        description="Label of the turbine, if different from the 'id'.",
        examples=[
            "T1",
            "WTG02",
            "WEA_003",
        ],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the turbine.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the turbine.",
    )
    location: Location = pdt.Field(
        default=...,
        description="The horizontal spatial location of the turbine.",
    )
    hub_height: float = pdt.Field(
        default=...,
        description="The hub height of the turbine.",
    )
    turbine_model_id: str = pdt.Field(
        default=...,
        description="Unique identifier of the turbine model.",
    )
    restrictions: Optional[list[OperationalRestriction]] = pdt.Field(
        default=None,
        description="List of operational restrictions at the turbine level.",
    )


class WindFarmConfiguration(EyaDefBaseModel):
    """A collection of wind turbines considered as one unit (plant)."""

    label: str = pdt.Field(
        default=...,
        description="Label or name of the wind farm.",
        examples=["Barefoot Wind Farm", "Project Summit Phase III"],
    )
    abbreviation: Optional[str] = pdt.Field(
        default=None,
        description="Optional abbreviated label of the wind farm.",
        examples=["BWF", "Summit PhIII"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the wind farm.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the wind farm.",
    )
    turbines: list[TurbineConfiguration] = pdt.Field(
        default=...,
        description="List of specifications for constituent turbines.",
    )
    relevance: WindFarmRelevance = pdt.Field(
        default=...,
        description="The relevance of the wind farm for the assessment.",
    )
    operational_lifetime_start_date: Optional[dt.date] = pdt.Field(
        default=None,
        description="Operational lifetime start date (format YYYY-MM-DD).",
        examples=["2026-01-01", "2017-04-01"],
    )
    operational_lifetime_end_date: Optional[dt.date] = pdt.Field(
        default=None,
        description="Operational lifetime end date (format YYYY-MM-DD).",
        examples=["2051-03-31", "2025-12-31"],
    )
    restrictions: Optional[list[OperationalRestriction]] = pdt.Field(
        default=None,
        description="List of operational restrictions at the wind farm level.",
    )
