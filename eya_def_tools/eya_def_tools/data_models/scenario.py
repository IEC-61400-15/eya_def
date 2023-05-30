"""Pydantic data models relating to EYA scenarios.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.energy_assessment import EnergyAssessment
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration
from eya_def_tools.data_models.wind_resource import TurbineWindResourceAssessment


class Scenario(EyaDefBaseModel):
    """Single unique energy yield assessment scenario."""

    scenario_id: str | None = pdt.Field(
        None,
        description="Unique identifier of the scenario.",
        examples=["3613a846-1e74-4535-ad40-7368f7ad452d"],
    )
    label: str = pdt.Field(
        ...,
        description="Label of the scenario.",
        examples=["Sc1", "A", "B01"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    is_main_scenario: bool | None = pdt.Field(
        None,
        description="Whether or not this is the main scenario in the report.",
    )
    operational_lifetime_length_years: float = pdt.Field(
        ...,
        description="Number of years of project operational lifetime.",
        gt=1.0,
        lt=100.0,
        examples=[10.0, 20.0, 30.0],
    )
    wind_farms: list[WindFarmConfiguration] = pdt.Field(
        ...,
        description="List of all wind farms included in the scenario.",
    )
    turbine_wind_resource_assessment: TurbineWindResourceAssessment = pdt.Field(
        ...,
        description="Wind resource assessment at the turbine locations.",
    )
    energy_assessment: EnergyAssessment = pdt.Field(
        ...,
        description=(
            "Energy assessment details and results, including gross energy, plant "
            "performance, net energy and uncertainties."
        ),
    )
