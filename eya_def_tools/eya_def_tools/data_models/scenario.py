"""Data models relating to EYA scenarios.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.energy_assessment import EnergyAssessment
from eya_def_tools.data_models.general import NonEmptyStr
from eya_def_tools.data_models.wind_resource import TurbineWindResourceAssessment


class Scenario(EyaDefBaseModel):
    """Single unique energy yield assessment scenario."""

    id: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional unique identifier of the scenario, which should "
            "not be empty if the field is included."
        ),
        examples=["3613a846-1e74-4535-ad40-7368f7ad452d"],
    )
    label: NonEmptyStr = pdt.Field(
        default=...,
        description="Label of the scenario.",
        examples=["Sc1", "A", "B01"],
    )
    description: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional description of the scenario, which should not be "
            "empty if the field is included."
        ),
    )
    comments: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional comments on the scenario, which should not be "
            "empty if the field is included."
        ),
    )
    is_main_scenario: Optional[bool] = pdt.Field(
        default=None,
        description=(
            "Optional flag to specify whether or not it is the main "
            "scenario in the report."
        ),
    )
    operational_lifetime_length_years: float = pdt.Field(
        default=...,
        description="Number of years of project operational lifetime.",
        gt=1.0,
        lt=100.0,
        allow_inf_nan=False,
        examples=[10.0, 20.0, 30.0],
    )
    wind_farm_ids: list[NonEmptyStr] = pdt.Field(
        default=...,
        description=(
            "List of the IDs for all wind farms included in the "
            "scenario. Each ID refers to a wind farm configuration "
            "data object within the 'wind_farms' section of the "
            "top-level of the EYA DEF document. Only wind farms for "
            "which turbine interaction effects are modelled shall be "
            "included."
        ),
    )
    turbine_wind_resource_assessment: TurbineWindResourceAssessment = pdt.Field(
        default=...,
        description="Wind resource assessment at the turbine locations.",
    )
    energy_assessment: EnergyAssessment = pdt.Field(
        default=...,
        description=(
            "Energy assessment details and results, including gross "
            "energy, plant performance, net energy and uncertainties."
        ),
    )
