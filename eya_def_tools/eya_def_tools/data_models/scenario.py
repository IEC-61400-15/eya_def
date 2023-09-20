"""Data models relating to EYA scenarios.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.energy_assessment import EnergyAssessment
from eya_def_tools.data_models.wind_resource import TurbineWindResourceAssessment


class Scenario(EyaDefBaseModel):
    """Single unique energy yield assessment scenario."""

    id: Optional[str] = pdt.Field(
        default=None,
        description="Optional unique identifier of the scenario.",
        examples=["3613a846-1e74-4535-ad40-7368f7ad452d"],
    )
    label: str = pdt.Field(
        default=...,
        description="Label of the scenario.",
        examples=["Sc1", "A", "B01"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the scenario.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the scenario.",
    )
    is_main_scenario: Optional[bool] = pdt.Field(
        default=None,
        description="Whether or not this is the main scenario in the report.",
    )
    operational_lifetime_length_years: float = pdt.Field(
        default=...,
        description="Number of years of project operational lifetime.",
        gt=1.0,
        lt=100.0,
        examples=[10.0, 20.0, 30.0],
    )
    wind_farm_ids: list[str] = pdt.Field(
        default=...,
        description="List of the IDs for all wind farms included in the scenario.",
    )
    turbine_wind_resource_assessment: TurbineWindResourceAssessment = pdt.Field(
        default=...,
        description="Wind resource assessment at the turbine locations.",
    )
    energy_assessment: EnergyAssessment = pdt.Field(
        default=...,
        description=(
            "Energy assessment details and results, including gross energy, plant "
            "performance, net energy and uncertainties."
        ),
    )
