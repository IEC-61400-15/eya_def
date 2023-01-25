"""Pydantic data models for wind farm and turbine configurations.

"""

import datetime as dt

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.enums import WindFarmRelevance
from eya_def_tools.data_models.fields import comments_field, description_field
from eya_def_tools.data_models.spatial import Location


# TODO expand definition of operational restriction
class OperationalRestriction(EyaDefBaseModel):
    """Specifications of an operational restriction."""

    label: str = pdt.Field(
        ...,
        description="Label of the operational restriction.",
        examples=["WSM curtailment", "MEC curtailment"],
    )
    description: str | None = description_field
    comments: str | None = comments_field


class TurbineConfiguration(EyaDefBaseModel):
    """Specification of all details for a turbine configuration."""

    turbine_id: str | None = pdt.Field(
        None,
        description="Unique identifier of the turbine specification.",
        examples=["b55caeac-f152-4b13-8217-3fddeab792cf", "T1-scen1"],
    )
    label: str = pdt.Field(
        ...,
        description="Label of the turbine.",
        examples=[
            "T1",
            "WTG02",
            "WEA_003",
        ],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    location: Location = pdt.Field(
        ..., description="Horizontal location of the turbine."
    )
    hub_height: float = pdt.Field(..., description="Turbine hub height.")
    turbine_model_id: str = pdt.Field(
        ..., description="Unique identifier of the turbine model."
    )

    # TODO consider moving restrictions to a separate model
    restrictions: list[OperationalRestriction] | None = pdt.Field(
        None, description="List of operational restrictions at the turbine level."
    )


class WindFarmConfiguration(EyaDefBaseModel):
    """A collection of wind turbines considered as one unit (plant)."""

    name: str = pdt.Field(
        ...,
        description="Name of the wind farm.",
        examples=["Barefoot Wind Farm", "Project Summit Phase III"],
    )
    label: str | None = pdt.Field(
        None,
        description="Abbreviated label of the wind farm.",
        examples=["BWF", "Summit PhIII"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    turbines: list[TurbineConfiguration] = pdt.Field(
        ..., description="List of specifications for constituent turbines."
    )
    relevance: WindFarmRelevance = pdt.Field(
        ..., description="The relevance of the wind farm for the assessment."
    )
    operational_lifetime_start_date: dt.date | None = pdt.Field(
        None,
        description="Operational lifetime start date (format YYYY-MM-DD).",
        examples=["2026-01-01", "2017-04-01"],
    )
    operational_lifetime_end_date: dt.date | None = pdt.Field(
        None,
        description="Operational lifetime end date (format YYYY-MM-DD).",
        examples=["2051-03-31", "2025-12-31"],
    )

    # TODO consider moving restrictions to a separate model
    wind_farm_restrictions: list[OperationalRestriction] | None = pdt.Field(
        None, description="List of operational restrictions at the wind farm level."
    )
